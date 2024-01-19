import numpy as np
import matplotlib.pyplot as plt
import os

import bezier

def gen_airfoil_coords(upper,lower,n_vals,nodes):
    x_points = np.array([0, 0, 0.33, 0.66, 0.9, 1.0])
    upper_surface = np.zeros(nodes+2)
    lower_surface = np.zeros(nodes+2)

    upper_surface[1:-1] = upper
    lower_surface[1:-1] = lower

    upper_nodes = np.asfortranarray([x_points, upper_surface])
    lower_nodes = np.asfortranarray([x_points, lower_surface])
    upper_curve = bezier.Curve(upper_nodes, degree=nodes+1)
    lower_curve = bezier.Curve(lower_nodes, degree=nodes+1)

    s_vals = np.linspace(0, 1, n_vals)
    upper_points = upper_curve.evaluate_multi(s_vals)
    lower_points = lower_curve.evaluate_multi(s_vals)
    return (upper_points, lower_points)

def save_dat(airfoil_name, upper_points, lower_points, n_vals):
    file_name = airfoil_name + '.dat'
    try:
        f = open(file_name, 'x')
    except:
        os.remove(file_name)
        f = open(file_name, 'x')

    f.write(airfoil_name + '\n')

    for i in range(n_vals):
        f.write(str("{0:.4f}".format(upper_points[0][n_vals-i-1])) + '\t' + str("{0:.4f}".format(upper_points[1][n_vals-i-1])) + '\n')
    for i in range(1, n_vals):
        f.write(str("{0:.4f}".format(lower_points[0][i])) + '\t' + str("{0:.4f}".format(lower_points[1][i])) + '\n')
    f.close()


if __name__ == '__main__':
    upper = np.array([0.1, 0.3, 0.2, 0.08])
    lower = np.array([-0.08, -0.05, 0.09, 0.075])
    n_vals = 50
    nodes = 4
    upper_points, lower_points = gen_airfoil_coords(upper,lower,n_vals, nodes)
    airfoil_name = 'NACA XXYY'
    save_dat(airfoil_name, upper_points, lower_points, n_vals)