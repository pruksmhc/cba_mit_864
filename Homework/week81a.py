import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x = y = np.linspace(0, 100, 100)
X, Y = np.meshgrid(x, y)
f = lambda x, y :  ((1-x) ** 2) + 100*((y-pow(x, 2))**2)
# CLEAN UP 
z = []
for i in range(len(x)):
	z.append(f(x, y))
print(z)
Z = np.array(z)
ax.plot_surface(X, Y, Z)
ax.set_title("Rosenbrock function")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('F(X,Y)')
plt.show()
