import random
import math
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt


def sample_spherical(npoints, radius=1 , origin = [0,0,0]) :

    vec = np.random.randn(3, npoints)

    vec /= np.linalg.norm(vec, axis=0)

    vec *= radius

    return np.array(vec[0])+origin[0], np.array(vec[1])+origin[1] , np.array(vec[2])+origin[2]


def instance_in_circle(num_task,origin , radius) :

    if origin[0]**2 + origin[1]**2+origin[2]**2 > radius**2 :

        a , d ,q = sample_spherical(num_task , radius , origin)

        a = a.astype(int)
        d = d.astype(int)
        q = q.astype(int)

        return list(range(len(a))),list(a),list(d),list(q)
    else : 
        print("impossible")
        return None




if __name__ == "__main__":

    N,a,d,q = instance_in_circle(700 , radius = 15 , origin = [100,100,100])

    fig = plt.figure(figsize = (10, 7))
    ax = plt.axes(projection ="3d")
    
    # Creating plot
    ax.scatter3D(a, d, q, color = "green")
    plt.title("Task simulated")
    
    # show plot
    plt.show()
