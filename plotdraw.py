import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot

# plot drawing & update
def draw_plot(data):

    print(type(data))
    for r in data:
        for k in r:
            print(k)

    plt.style.use('dark_background')

    host = host_subplot(111)

    par = host.twinx()

    host.set_ylabel("Temp.", c="red")
    par.set_ylabel("Pulse", c="blue")
    host.spines['left'].set_color("red")
    par.spines['right'].set_color("blue")

    y_temp = []
    y_pulse = []
    x = []
    x_ticks = []
    i = 0

    for r in data:
        print(r[5])
        y_temp.append(r[5])
        print(r[6])
        y_pulse.append(r[6])
        x.append(i)
        i += 1
        record = "day " + str(r[3]) + ", " + str(r[2])
        x_ticks.append(record)

    plt.xticks(x, x_ticks, rotation=10)

    print(y_temp)
    print(y_pulse)
    p1 = host.scatter(x, y_temp, c="red", label="Temp.")
    p2 = par.scatter(x, y_pulse, c="blue", label="Pulse")

    return x_ticks

