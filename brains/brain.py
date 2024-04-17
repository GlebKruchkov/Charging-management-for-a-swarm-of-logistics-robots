import abc
import typing

from robot import Robot, SafeRobot

if typing.TYPE_CHECKING:
    from modelling import Model
    from structures import Map
    from cell import Cell

RobotT = typing.TypeVar("RobotT", bound = "Robot[Cell]")
MapT = typing.TypeVar("MapT", bound = "Map[Cell]", covariant=True)


class Brain(abc.ABC, typing.Generic[MapT, RobotT]):
    """Abstract class for brain"""
    @property
    def count(self):
        """count of delivered mails"""
        return self._count

    def __init__(self, model: "Model[MapT, typing.Self, RobotT]"):
        self._model = model
        self._count = 0

    @abc.abstractmethod
    def get_next_action(self, robot: RobotT) -> Robot.Action:
        """Called by robot"""

    @abc.abstractmethod
    def new_robot(self, robot: RobotT) -> None:
        """Called by model when adding new robot"""


class OnlineBrain(Brain[MapT, SafeRobot]):
    """Abstract class for brain which for every robot position knowns action"""
    def __init__(self, model: "Model[MapT, typing.Self, SafeRobot]"):
        super().__init__(model)
        self._idle_robots: list[SafeRobot] = []
        self._input_destinations: dict[SafeRobot, int] = {}

    @typing.override
    def get_next_action(self, robot: SafeRobot) -> Robot.Action:
        if robot.mail is not None:
            if robot.position == self._model.map.outputs[robot.mail.destination]:
                self._mail_put(robot)
                self._count += 1
                return Robot.Action.put
            return self._go_with_mail(robot, robot.mail.destination)
        else:
            if robot.get_charger_id() != -1 and robot.position == self._model.map.chargers[robot.get_charger_id()]:
                self._come_to_charger(robot)
                return Robot.Action.charge

            if robot.get_curr_charge() < robot.get_threshold():
                if robot.get_charger_id() != -1:
                    return self._go_to_charger(robot, robot.get_charger_id())
                else:
                    where_to_go = -1
                    for key, value in self._model.map.get_free_chargers.items():
                        if value:
                            where_to_go = key
                            self._model.map.get_free_chargers[key] = False
                            break
                    if where_to_go != -1:
                        self._model.map.set_cur_charger_id(where_to_go)
                        robot.set_charger_id(where_to_go)
                        robot.set_id(False)
                        return self._go_to_charger(robot, robot.charger_id)

            if robot.position == self._model.map.inputs[self._input_destinations[robot]]:
                self._mail_taken(robot)
                return Robot.Action.take
            return self._go_without_mail(robot, self._input_destinations[robot])

    @abc.abstractmethod
    def _go_with_mail(self, robot: SafeRobot, destination: int) -> Robot.Action:
        """Called if robot has mail"""

    @abc.abstractmethod
    def _go_without_mail(self, robot: SafeRobot, destination: int) -> Robot.Action:
        """Called if robot does not have mail"""

    @abc.abstractmethod
    def _go_to_charger(self, robot: SafeRobot, destination: int) -> Robot.Action:
        """Called if robot charge level is too low"""

    def _mail_taken(self, robot: SafeRobot):
        """Called before sending `Action.take`"""

    def _mail_put(self, robot: SafeRobot):
        """Called before sending `Action.put`"""

    def _come_to_charger(self, robot: SafeRobot):
        """Called before sending `Action.put`"""
