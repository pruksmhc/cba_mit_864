from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

def line_min(points):
    print("line min")
def plot_data(n,S,title,simplex_flag):
    S = np.array(S)
    print(np.shape(S))
    t1 = title
    font = {'family': 'monospace',
        'color':  '#39393d',
        'weight': 'light',
        'size': 14,
        }
    fig = plt.figure(figsize=(10,6), facecolor="white")
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(t1, fontdict=font)
    ax.set_xlabel('x',fontdict=font)
    ax.set_ylabel('y',fontdict=font)
    X = []
    Y = []
    Z = []
    g = 2.0
    for i in range(int(-n/2),int(n/2)):
        X.append(np.ones(n)*(i+1)*(g/n))
        Y.append(np.linspace(-g/2, g/2, n))
    for i in range(len(X)):
        x = X[i]
        y = Y[i]
        Z.append((1-x)**2 + 100*(y-x**2)**2)
    ax.plot_surface(X,Y,Z,color="red")

    # rotate the view shown in the plot
    ax.view_init(elev=50., azim=60)
    plt.show() 


def create_simplex(init_point, step):
    x = np.zeros((len(init_point)+1,len(init_point))) 
    x[0] = init_point
    for i in range(1,len(init_point)+1): # has one more vertex than dimensions
        x[i] = init_point
        x[i,i-1] = init_point[i-1] + step # this has x and y coordinate
    # This has an x and y
    new_x = []
    for i in range(len(x)):
         new_x.append([x[i], f(x[i][0], x[i][1])])
    print(new_x)
    return new_x


def shrink_all(x, f):
    # srhink all towards the best vertex
    for i in range(len(x)):
        x[i][0] = (1/2)*(x[i][0] + x[len(x) -1][0])
        x[i][1] = f(x[i][0][0], x[i][0][1])
    return x
        
def rank_vertices(x):
    x.sort(key=lambda x: x[1])
    x.reverse()
    return x

        
def downhill_simplex(f, init_point, step):
    first_point = init_point
    x = create_simplex(first_point, step)
    prev_best = f(init_point[0], init_point[0]) 
    state = []
    for i in range(100):  # think about stopping condition
        x = rank_vertices(x)
        prev = x
        best = x[-1][1]
        worst = x[0][1]
        second = x[1][1]
        if ((prev_best - best) < 0.000000001):
            print("done")
            #return best
        x_mean = [0.] * 2
        for tup in x[1:]:
            for i, c in enumerate(tup[0]):
                x_mean[i] += c / (len(x)-1)
        p1 = x_mean + 1*(x_mean- x[0][0])
        f_p1 = f(p1[0], p1[1])
        prev_best = best
        if (f_p1 <= best): # clearly best, try seeing if doubling helps
            p2 = x_mean + 2*(x_mean  - x[0][0])
            f_p2 = f(p2[0], p2[1])
            if (f_p2 < f_p1):#update x. 
                x = x[1:]
                x.append([p2, f_p2])
            else:
                x = x[1:]
                x.append([p1, f_p1])
        elif (f_p1 <= second):
            temp = x[1]
            x[1] = [p1, f_p1]
            x[0] = temp
        else:
            p3 = x_mean + ((1/2)*(x_mean- x[0][0]))
            f_p3 = f(p3[0], p3[1])
            if (f_p3 > second):
                p4 =  x_mean - ((1/2)*(x_mean- x[0][0]))
                f_p4 = f(p4[0], p4[1])
                if (f_p4 > second):
                    x = shrink_all(x,f)
                else:
                    temp = x[1]
                    x[1] = [p4, f_p4]
                    x[0] = temp   
            else:
                temp = x[1]
                x[1] = [p3, f_p3]
                x[0] = temp   
        state.append(x)
    new_s = []
    for i in state:
    	new = []
    	for j in i:
    		new.append(j[0])
    	new_s.append(new)
    plot_data(50, new_s, "Nelder", True)
    return x[-1] # gives the best value of 
    

init_point = np.array([-1, -1])
def f(x, y): 
    r = pow((1-x), 2) + (100*pow((y-pow(x, 2)), 2))
    return r
print(downhill_simplex(f, init_point, 0.3))
