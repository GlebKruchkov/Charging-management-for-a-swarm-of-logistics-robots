from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter

# angles = []
# around_charger = []
# center = []
# around_walls_and_center = []
times = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/9robots_on_the_angle.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         angles.append(int(elem))
#
# with open("/Users/glebkruckov/robotic-sorting/results/9robots_pos_f0_3_s0_5_th_0_7.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         around_charger.append(int(elem))
#
# with open("/Users/glebkruckov/robotic-sorting/results/9robots_pos_f3_7_s4_4_th_6_2.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         center.append(int(elem))
#
# with open("/Users/glebkruckov/robotic-sorting/results/9robots_f2_0_s2_8_th6_3.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         around_walls_and_center.append(int(elem))
#
# for i in range(30):
#     times.append(i * 666)
#
# plt.plot(times, around_charger, label='Возле пунктов, куда роботы везут письма')
#
# plt.plot(times, angles, label='В углах склада')
#
#
# plt.plot(times, center, label='В центре склада')
#
# plt.plot(times, around_walls_and_center, label='В центре и возле стен')
#
# plt.xlabel("Момент времени (в секундах)")
# plt.ylabel("Количество развезенных писем")
#
# plt.legend(loc='best')
# plt.show()


# rob7 = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/7robots1charger4_8.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         rob7.append(int(elem))
#
# rob8 = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/8robots1charger4_8.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         rob8.append(int(elem))
#
# rob9 = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/9robots1charger4_8.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         rob9.append(int(elem))
#
# rob10 = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/10robots1charger4_8.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         rob10.append(int(elem))
#
# rob11 = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/11robots1charger4_8.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         rob11.append(int(elem))
#
# for i in range(30):
#     times.append(i * 666)
#
# plt.plot(times, rob7, label='7 роботов 1 зарядка')
#
# plt.plot(times, rob8, label='8 роботов 1 зарядка')
#
#
# plt.plot(times, rob9, label='9 роботов 1 зарядка')
#
# plt.plot(times, rob10, label='10 роботов 1 зарядка')
# plt.plot(times, rob11, label='11 роботов 1 зарядка')
#
# plt.xlabel("Момент времени (в секундах)")
# plt.ylabel("Количество развезенных писем")
#
# plt.legend(loc='best')
# plt.show()

# rob9 = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/9robots2charger5_4_4_8.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         rob9.append(int(elem))
#
# rob10 = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/10robots2charger5_4_4_8.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         rob10.append(int(elem))
#
# rob11 = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/11robots2charger5_4_4_8.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         rob11.append(int(elem))
#
# rob12 = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/12robots2charger5_4_4_8.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         rob12.append(int(elem))
#
# rob13 = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/13robots2charger5_4_4_8.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         rob13.append(int(elem))
#
# rob14 = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/14robots2charger5_4_4_8.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         rob14.append(int(elem))
#
# rob15 = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/15robots2charger5_4_4_8.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         rob15.append(int(elem))
#
# for i in range(30):
#     times.append(i * 666)
#
# plt.plot(times, rob9, label='9 роботов 2 зарядки')
#
# plt.plot(times, rob10, label='10 роботов 2 зарядки')
#
# plt.plot(times, rob11, label='11 роботов 2 зарядки')
#
# plt.plot(times, rob12, label='12 роботов 2 зарядки')
#
# plt.plot(times, rob13, label='13 роботов 2 зарядки')
#
# plt.plot(times, rob14, label='14 роботов 2 зарядки')
#
# plt.plot(times, rob15, label='15 роботов 2 зарядки')
#
# plt.xlabel("Момент времени (в секундах)")
# plt.ylabel("Количество развезенных писем")
#
# plt.legend(loc='best')
# plt.show()



#
# rob14 = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/14robots3charger0_0_8_0_8_8.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         rob14.append(int(elem))
#
# rob15 = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/15robots3charger0_0_8_0_8_8.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         rob15.append(int(elem))
#
# rob16 = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/16robots3charger0_0_8_0_8_8.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         rob16.append(int(elem))
#
# for i in range(30):
#     times.append(i * 666)
#
# plt.plot(times, rob14, label='14 роботов 3 зарядки')
#
# plt.plot(times, rob15, label='15 роботов 3 зарядки')
#
# plt.plot(times, rob16, label='16 роботов 3 зарядки')
#
# plt.xlabel("Момент времени (в секундах)")
# plt.ylabel("Количество развезенных писем")
#
# plt.legend(loc='best')
# plt.show()


# rob15 = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/15robots4charger0_0_8_0_8_8_0_8.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         rob15.append(int(elem))
#
# rob16 = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/16robots4charger0_0_8_0_8_8_0_8.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         rob16.append(int(elem))
#
# rob17 = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/17robots4charger0_0_8_0_8_8_0_8.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         rob17.append(int(elem))
#
# for i in range(30):
#     times.append(i * 666)
#
# plt.plot(times, rob15, label='15 роботов 4 зарядки')
#
# plt.plot(times, rob16, label='16 роботов 4 зарядки')
#
# plt.plot(times, rob17, label='17 роботов 4 зарядки')
#
# plt.xlabel("Момент времени (в секундах)")
# plt.ylabel("Количество развезенных писем")
#
# plt.legend(loc='best')
# plt.show()




# center = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/15robots3charger3_7_4_4_6_2.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         center.append(int(elem))
#
# angles = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/15robots3charger0_0_8_0_8_8.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         angles.append(int(elem))
#
# center_and_lines = []
#
# with open("/Users/glebkruckov/robotic-sorting/results/15robots3charger2_0_2_8_6_3.txt", "r") as file:
#     temp = file.read().splitlines()[0].split()
#     for elem in temp:
#         center_and_lines.append(int(elem))
#
# for i in range(30):
#     times.append(i * 666)
#
# plt.plot(times, center, label='все зарядки по центру')
#
# plt.plot(times, angles, label='все зарядки по углам')
#
# plt.plot(times, center_and_lines, label='по бокам и одна в середине')
#
# plt.xlabel("Момент времени (в секундах)")
# plt.ylabel("Количество развезенных писем 15 роботов")
#
# plt.legend(loc='best')
# plt.show()



chargers = []

with open("/Users/glebkruckov/robotic-sorting/results/9robots2charger5_4_4_8.txt", "r") as file:
    temp = file.read().splitlines()[0].split()
    for elem in temp:
        chargers.append(int(elem))

without = []

with open("/Users/glebkruckov/robotic-sorting/results/9robots_without_charger.txt", "r") as file:
    temp = file.read().splitlines()[0].split()
    for elem in temp:
        without.append(int(elem))

for i in range(30):
    times.append(i * 666)

plt.plot(times, chargers, label='2 зарядки 9 роботов')

plt.plot(times, without, label='без траты заряда 9 роботов')

plt.xlabel("Момент времени (в секундах)")
plt.ylabel("Количество развезенных писем 15 роботов")

plt.legend(loc='best')
plt.show()