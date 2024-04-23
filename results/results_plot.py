from matplotlib import pyplot as plt

with_ch = []

with open("/Users/glebkruckov/Robots/Charging-management-in-a-robotic-warehouse/results/9robots_without_chargers.txt",
          "r") as file:
    temp = file.read().splitlines()[0].split()
    for elem in temp:
        with_ch.append(int(elem))

without_ch = []

with open("/Users/glebkruckov/Robots/Charging-management-in-a-robotic-warehouse/results/9robots0_0_8_0_8_8.txt",
          "r") as file:
    temp = file.read().splitlines()[0].split()
    for elem in temp:
        without_ch.append(int(elem))

times = []

for i in range(31):
    times.append(i * 2067)

plt.plot(times, with_ch, label='9 роботов с зарядными устройствами')
plt.plot(times, without_ch, label='9 роботов без зарядных устройств')

plt.grid(True, linewidth=0.5)

plt.xlim(0, 65000)
plt.ylim(0, 8000)

plt.xticks(fontsize=15, fontstyle='normal')
plt.yticks(fontsize=15, fontstyle='normal')
plt.legend(loc='best')
plt.show()
