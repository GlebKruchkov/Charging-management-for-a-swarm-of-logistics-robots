import enum
import logging
import simpy
import typing

from structures import Position, Direction, Mail, RobotType, Charger
from exceptions import RobotWithoutMailException, RobotWithMailException, IncorrectOutputException

if typing.TYPE_CHECKING:
    from brains import Brain, OnlineBrain
    import simpy.core
    from structures import Map
    from cell import Cell, SafeCell
    from modelling import Model

CellT = typing.TypeVar("CellT", bound="Cell", covariant=True)


class Robot(typing.Generic[CellT]):
    class Action(enum.Enum):
        idle = 0
        move = 1
        take = 2
        put = 3
        charge = 1007
        nothing = 77
        turn_to_up = 10
        turn_to_left = 11
        turn_to_down = 12
        turn_to_right = 13

        @staticmethod
        def turn_to(direction: Direction):
            return Robot.Action(10 + direction.value)

    _last_robot_id: int = 0

    @property
    def position(self):
        return self._position

    @property
    def direction(self):
        return self._direction

    @property
    def mail(self):
        return self._mail

    @property
    def charger(self):
        return self._charger

    @property
    def get_time_to_charge(self):
        return self.type.time_to_charge

    @property
    def get_bat_capacity(self):
        return self._battery_capacity

    @property
    def get_charge_to_start(self):
        return self.type.charge_to_start

    def change_charge(self, consumption: int):
        self._current_charge -= consumption

    @property
    def charger_id(self):
        return self._charger_id

    def set_charger_id(self, new_id: int):
        self._charger_id = new_id

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def max_idle(self):
        return self._max_idle

    def __init__(self, model: "Model[Map[CellT], Brain[Map[CellT], Robot[Cell]], Robot[Cell]]",
                 type_: RobotType,
                 position: Position,
                 direction: Direction,
                 battery_capacity: int,
                 current_charge: int,
                 charging_threshold: int,
                 robot_is_standing: bool,
                 charger_id: int = -1
                 ):
        self.counter_of_mails = 0
        self.first_charge = True
        self.charge_vec = []
        self.charge_vec_first = []
        self.is_going_to_charger_ = False
        self.robot_is_standing_ = robot_is_standing
        self.changing_threshold_ = True
        self._battery_capacity = battery_capacity
        self._current_charge = current_charge
        self._max_idle = 0
        self._cur_idle = 0
        self._charging_threshold = charging_threshold
        self._charger_id = charger_id
        self._if_set_id = True

        self._id = Robot._last_robot_id
        Robot._last_robot_id += 1

        self._model = model
        self._type = type_
        self._position = position
        self._direction = direction

        self._cell_request = model.map[position].reserve()
        self._action = model.process(self._run())

        self._mail: Mail | None = None
        self._charger: Charger | None = None
        self._start_charge_time: simpy.core.SimTime | None = None
        self._event: simpy.Event = model.event()
        self._aborted = False
        self.timeout = False

    def _new_abortable_event(self, event: simpy.Event | None = None):
        def cancel_event(evt: simpy.Event):
            if not self._event.triggered:
                self._event.succeed(evt.value)
                self._aborted = False

        self._event = self._model.event()
        if event is not None:
            event.callbacks.append(cancel_event)  # pyright: ignore[reportUnknownMemberType]
        return self._event

    def abort(self):
        if self._event.triggered:
            logging.warn(f"Tried to abort {self}'s event.")
            return False
        logging.info(f"{self}'s event aborted.")
        self._event.succeed()
        self._aborted = True
        return True

    def _idle(self):
        self._cur_idle += 1
        self.charge_vec_first.append(f"iddle {self._current_charge}\n")
        if not self.robot_is_standing_:
            self._current_charge -= self.type.charge_to_stop
            self.robot_is_standing_ = True
        logging.info(f"{self} is idle.")
        yield self._new_abortable_event()

    def _move(self) -> typing.Generator[simpy.Event, bool, None]:
        self.charge_vec_first.append(f"move {self._current_charge}\n")
        #print("SUKAAA")
        self.charge_vec.append(self.get_curr_charge() / 100000)
        next_position = self._position.get_next_on(self._direction)
        request = self._model.map[next_position].reserve()
        yield request
        logging.info(f"{self} is moving to {next_position}.")
        yield self._model.timeout(self._type.time_to_move)
        self._model.map[self._position].unreserve(self._cell_request)
        self._position = next_position
        if self.robot_is_standing_:
            self._current_charge -= self.type.charge_to_start
            self.robot_is_standing_ = False
        self._current_charge -= self.type.charge_to_go
        self._cell_request = request

    def _put(self):
        self._max_idle = max(self._max_idle, self._cur_idle)
        self.charge_vec_first.append(f"put {self._current_charge}\n")
        self.charge_vec.append(self.get_curr_charge() / 100000)
        if self._mail is None:
            raise RobotWithoutMailException(self)
        if self._model.map[self.position].output_id != self._mail.destination:
            raise IncorrectOutputException(self._mail, self._model.map[self.position])
        logging.info(f"{self} is putting {self._mail}.")
        yield self._model.timeout(self._type.time_to_put)
        self._current_charge -= self.type.charge_to_put
        self._mail = None

    def _take(self) -> typing.Generator[simpy.Event, Mail, None]:
        self._cur_idle = 0
        self.charge_vec_first.append(f"take {self._current_charge}\n")
        self.charge_vec.append(self.get_curr_charge() / 100000)
        if self._mail is not None:
            raise RobotWithMailException(self)
        logging.info(f"{self} is waiting for mail.")
        mail = yield self._new_abortable_event(
            self._model.map[self._position].get_input())
        if self._aborted:
            return
        logging.info(f"{self} is taking {self._mail}.")
        yield self._model.timeout(self._type.time_to_take)
        self._current_charge -= self.type.charge_to_take
        self._mail = mail

    def _nothing(self):
        yield self._model.timeout(0)

    def _charge(self):
        self.charge_vec_first.append(f"charge {self._current_charge}\n")
        #print(1)
        part = (self.get_bat_capacity - self.get_curr_charge()) / self.get_bat_capacity
        temp = self.get_curr_charge()
        adder = (self.get_bat_capacity - temp) / (self.type.time_to_charge * part)
        while temp < self.get_bat_capacity:
            self.charge_vec.append(temp / 100000)
            temp += adder
        self.charge_vec.append(temp / 100000)
        yield self._model.timeout(self.type.time_to_charge)
        self.set_curr_charge()
        if self.first_charge:
            self.first_charge = False
            self._charging_threshold = 5850
        if not self.robot_is_standing_:
            self._current_charge -= self.type.charge_to_stop
            self.robot_is_standing_ = True
        # self._model.map.get_free_chargers[self.charger_id] = True
        # self._charger_id = -1

    def _turn(self, new_direction: Direction):
        self.charge_vec_first.append(f"turn {self._current_charge}\n")
        self.charge_vec.append(self.get_curr_charge() / 100000)
        logging.info(f"{self} is turning to {new_direction}.")
        yield self._model.timeout(Direction.turn_count(self._direction, new_direction) \
                                  * self._type.time_to_turn)
        self._current_charge -= self.type.charge_to_turn
        self._direction = new_direction

    def _run(self):
        yield self._cell_request
        while True:
            match self._model.brain.get_next_action(self):
                case Robot.Action.idle:
                    yield self._model.process(self._idle())
                case Robot.Action.move:
                    yield self._model.process(self._move())
                case Robot.Action.take:
                    yield self._model.process(self._take())
                case Robot.Action.put:
                    yield self._model.process(self._put())
                case Robot.Action.nothing:
                    yield self._model.process(self._nothing())
                case Robot.Action.charge:
                    yield self._model.process(self._charge())
                case Robot.Action.turn_to_up | Robot.Action.turn_to_left \
                     | Robot.Action.turn_to_down | Robot.Action.turn_to_right as turn:
                    yield self._model.process(self._turn(Direction(turn.value - 10)))

    @typing.override
    def __repr__(self):
        return f"Robot#{self._id}"

    def get_curr_charge(self):
        return self._current_charge

    def set_curr_charge(self):
        self._current_charge = self._battery_capacity

    def set_curr_threshold_(self):
        self._charging_threshold = 5850

    def get_threshold(self):
        return self._charging_threshold

    def get_change_threshold(self):
        return self.changing_threshold_

    def set_change_threshold(self):
        self.changing_threshold_ = False

    def if_set_id(self):
        return self._if_set_id

    def set_id(self, temp: bool):
        self._if_set_id = temp

    def get_charger_id(self):
        return self.charger_id


class SafeRobot(Robot["SafeCell"]):
    def __init__(self, model: "Model[Map[SafeCell], OnlineBrain[Map[SafeCell]], SafeRobot]",
                 type_: RobotType,
                 position: Position,
                 direction: Direction,
                 battery_capacity: int,
                 current_charge: int,
                 charging_threshold: int,
                 robot_is_standing: bool,
                 charger_id: int = -1,
                 wait_time: float = -1
                 ):
        super().__init__(model, type_, position, direction, battery_capacity, current_charge, charging_threshold,
                         robot_is_standing, charger_id)  # type: ignore
        self.is_going_to_charger_ = False
        self.temp = 0
        self.wait_time = wait_time

    @typing.override
    def _move(self) -> typing.Generator[simpy.Event, bool, None]:
        self.charge_vec_first.append(f"move {self._current_charge}\n")
        next_position = self._position.get_next_on(self._direction)
        request = self._model.map[next_position].reserve()
        logging.info(f"{self} is waiting for {next_position} to free.")
        if self.wait_time > 0:
            start_time = self._model.now
            yield self._new_abortable_event(request) | self._model.timeout(self.wait_time)
            self.timeout = (self._model.now - start_time) >= self.wait_time
        else:
            yield self._new_abortable_event(request)
            self.timeout = False
        if self.timeout:
            logging.info(f"{self} waited too much ({self.wait_time}).")
        if self.timeout or self._aborted:
            self._model.map[next_position].unreserve(request)
            return
        logging.info(f"{self} is moving to {next_position}.")
        yield self._model.timeout(self._type.time_to_move)
        self._model.map[self._position].unreserve(self._cell_request)
        self._position = next_position
        self._current_charge -= self.type.charge_to_go
        self._cell_request = request

    @typing.override
    def _run(self):
        yield self._cell_request
        while True:
            match act := self._model.brain.get_next_action(self):
                case Robot.Action.idle:
                    yield self._model.process(self._idle())
                case Robot.Action.move:
                    yield self._model.process(self._move())
                case Robot.Action.take:
                    yield self._model.process(self._take())
                case Robot.Action.put:
                    yield self._model.process(self._put())
                case Robot.Action.charge:
                    yield self._model.process(self._charge())
                case Robot.Action.nothing:
                    yield self._model.process(self._nothing())
                case Robot.Action.turn_to_up | Robot.Action.turn_to_left \
                     | Robot.Action.turn_to_down | Robot.Action.turn_to_right:
                    yield self._model.process(self._turn(Direction(act.value - 10)))
            if act is not Robot.Action.move:
                self.timeout = False
