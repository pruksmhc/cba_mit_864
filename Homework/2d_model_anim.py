
import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import numpy as np
# N is num iterations
def explicit_diff(D, N, iter_time, dx, dt):
    F = dt/math.pow(dx,2)
    u_n = ([0]*249) + [1] + ([0]*250)  # mesh points in space
    u = [0]*500
    final = []
    final.append(u)
    # Compute u at inner mesh points
    for j in range(iter_time):
        for i in range(1, (N-1)):
            u[i] = u_n[i] + F*(u_n[i-1] - 2*u_n[i] + u_n[i+1])
        print("At t=")
        print(j)
        print(u)
        final.append(u)
        u[0] = 0;  u[N-1] = 0
        u_n = u
        u = [0]*500
    return final

# Init only required for blitting to give a clean slate.

dt = [1 , 0.5, 0.1]
for i in dt:
    final = explicit_diff(1, 500, 150, 1, i)
    print(len(final))
    print(len(final[0]))
    fig, ax = plt.subplots()
    x = np.arange(-250, 250, 1)
    line, = ax.plot(x, np.sin(x))
    def animate(i):
        line.set_ydata(final[i])  # update the data
        return line,

    def init():
        line.set_ydata(np.ma.array(x, mask=True))
        return line,
    ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), init_func=init,
                                  interval=1,  blit=True)
    plt.show()