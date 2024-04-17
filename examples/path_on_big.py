from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter

from cell import Cell
from mail_factories import RandomAlwaysReadyMail
from import_data import import_map, import_json
from structures import Direction, Position, Map
from robot import Robot, RobotType
from brains.path_brain import PathBrain
from modelling import Model

model = Model[Map[Cell], PathBrain, Robot[Cell]]()

mail_factory = RandomAlwaysReadyMail(model, range(1, 10))
map_ = import_map(model, import_json("/Users/glebkruckov/robotic-sorting/data/map1-simple.json"), mail_factory)[0]
model.set_map(map_)

robot_type = RobotType(1, 1, 1, 1, 400, 10, 10, 100, 100, 325, 300)

model.set_brain(PathBrain(model, robot_type))
starts = [
    Position(1, 0),
    Position(1, 1),
    Position(1, 2),
    Position(1, 3),
    Position(1, 4),
    Position(1, 5),
    Position(1, 6),
    # Position(1, 7),
]
robots = [Robot(model, robot_type, pos, Direction.down, 100000, 100000, 5850 + 6000 * pos.y, True) for pos in starts]

for i, robot in enumerate(robots):
    model.brain.robots_rests[robot] = starts[i]
    model.add_robot(robot)

# robo9 = Robot(model, robot_type, Position(8, 3), Direction.up, 100000, 100000, 5850 + 10 * 6000, True)
# robo10 = Robot(model, robot_type, Position(8, 1), Direction.up, 100000, 100000, 5850 + 9 * 6000, True)
# model.brain.robots_rests[robo9] = Position(8, 3)
# model.add_robot(robo9)
# model.brain.robots_rests[robo10] = Position(8, 1)
# model.add_robot(robo10)
#
# robo11 = Robot(model, robot_type, Position(6, 0), Direction.right, 100000, 100000, 5850 + 10 * 6000, True)
# model.brain.robots_rests[robo11] = Position(6, 0)
# model.add_robot(robo11)
#
# robo12 = Robot(model, robot_type, Position(6, 8), Direction.down, 100000, 100000, 5850 + 11 * 6000, True)
# model.brain.robots_rests[robo12] = Position(6, 8)
# model.add_robot(robo12)
#
# robo13 = Robot(model, robot_type, Position(4, 1), Direction.down, 100000, 100000, 5850 + 12 * 6000, True)
# model.brain.robots_rests[robo13] = Position(4, 1)
# model.add_robot(robo13)
#
# robo14 = Robot(model, robot_type, Position(8, 7), Direction.up, 100000, 100000, 5850 + 13 * 6000, True)
# model.brain.robots_rests[robo14] = Position(8, 7)
# model.add_robot(robo14)
#
# robo15 = Robot(model, robot_type, Position(6, 7), Direction.up, 100000, 100000, 5850 + 14 * 6000, True)
# model.brain.robots_rests[robo15] = Position(6, 7)
# model.add_robot(robo15)

# robo16 = Robot(model, robot_type, Position(7, 5), Direction.up, 100000, 100000, 5850 + 14 * 3420, True)
# model.brain.robots_rests[robo16] = Position(7, 5)
# model.add_robot(robo16)
#
# robo17 = Robot(model, robot_type, Position(7, 4), Direction.up, 100000, 100000, 5850 + 16 * 3420, True)
# model.brain.robots_rests[robo17] = Position(7, 4)
# model.add_robot(robo17)


last_cnt = 0

results = []

# print(model.robots[0].max_idle)

with open("/Users/glebkruckov/robotic-sorting/results/7robots1charger4_8.txt", "w") as file:
    for i in range(1, 31):
        model.run(model.now + 1000)
        if i % 1 == 0:
            file.write(str(model.brain.count))
            file.write(" ")
#
# plt.plot(model.robots[0].charge_vec)
#
# plt.xlabel("Момент времени (в секундах)")
# plt.ylabel("Заряд робота (в процетах)")
#
# plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
# plt.show()

# model.record(1000)
# print(f"mails:{model.brain.count}")
# model.test(1000, 10)

#30 748 743 740 745 743 743 2434

# 749 748 749 742 744 744


# 5.5%, 1 зарядка 55720, 300 итераций
# 8%, 1 зарядка 55514 5420
# 9.5%, 1 зарядка 5490
# 11.5%, 1 зарядка
