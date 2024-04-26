from matplotlib import pyplot as plt

from cell import Cell
from mail_factories import RandomAlwaysReadyMail
from import_data import import_map, import_json
from structures import Direction, Position, Map
from robot import Robot, RobotType
from brains.path_brain import PathBrain
from modelling import Model

model = Model[Map[Cell], PathBrain, Robot[Cell]]()

mail_factory = RandomAlwaysReadyMail(model, range(1, 10))
map_ = import_map(model, import_json(
    "data/map1-simple.json"), mail_factory)[0]
model.set_map(map_)

robot_type = RobotType(2, 2, 2, 2, 800, 0, 0, 0, 0, 0, 0)

model.set_brain(PathBrain(model, robot_type))
starts = [
    Position(1, 0),
    Position(1, 1),
    Position(1, 2),
    Position(1, 3),
    Position(1, 4),
    Position(1, 5),
    Position(1, 6),
    Position(1, 7),
]
robots = [Robot(model, robot_type, pos, Direction.down, 100000, 100000, 8000 + int(pos.y) * 5000, True) for pos in
          starts]

for i, robot in enumerate(robots):
    model.brain.robots_rests[robot] = starts[i]
    model.add_robot(robot)

robo9 = Robot(model, robot_type, Position(8, 3), Direction.up, 100000, 100000, 8000 + 5000 * 8, True)
model.brain.robots_rests[robo9] = Position(8, 3)
model.add_robot(robo9)

robo10 = Robot(model, robot_type, Position(8, 1), Direction.up, 100000, 100000, 8000 + 5000 * 9, True)
model.brain.robots_rests[robo10] = Position(8, 1)
model.add_robot(robo10)

robo11 = Robot(model, robot_type, Position(6, 0), Direction.right, 100000, 100000, 8000 + 5000 * 10, True)
model.brain.robots_rests[robo11] = Position(6, 0)
model.add_robot(robo11)

robo12 = Robot(model, robot_type, Position(6, 8), Direction.down, 100000, 100000, 8000 + 5000 * 11, True)
model.brain.robots_rests[robo12] = Position(6, 8)
model.add_robot(robo12)

robo13 = Robot(model, robot_type, Position(4, 1), Direction.down, 100000, 100000, 8000 + 5000 * 12, True)
model.brain.robots_rests[robo13] = Position(4, 1)
model.add_robot(robo13)

robo14 = Robot(model, robot_type, Position(8, 7), Direction.up, 100000, 100000, 8000 + 5000 * 13, True)
model.brain.robots_rests[robo14] = Position(8, 7)
model.add_robot(robo14)

robo15 = Robot(model, robot_type, Position(6, 7), Direction.up, 100000, 100000, 8000 + 5000 * 14, True)
model.brain.robots_rests[robo15] = Position(6, 7)
model.add_robot(robo15)

last_cnt = 0

results = []

time = []
charge = [[]]
for i in range(14):
    charge.append([])

with open("results/15robots.txt",
          "w") as file:
    for i in range(1, 31):
        if i == 1:
            file.write(str(0))
            file.write(" ")
        # for j in range(15):
        #     if model.robots[j].get_is_on_charge():
        #         charge[j].append(model.robots[j].get_last_charge() / 1000)
        #         model.robots[j].set_last_charge()
        #     else:
        #         charge[j].append(model.robots[j].get_curr_charge() / 1000)

        # time.append(model.now)
        model.run(model.now + 2000)
        if i % 1 == 0:
            print(f"время: {model.now}; количество развезенных писем: {str(model.brain.count)}")
            file.write(str(model.brain.count))
            file.write(" ")

# plt.plot(time, charge[6])
# plt.grid(True, linewidth=0.5)
# plt.xlim(0, max(time))
# plt.xticks(fontsize=15, fontstyle='normal')
# plt.yticks(fontsize=15, fontstyle='normal')
# plt.ylim(0, 100)
# plt.show()
