import matplotlib.pyplot as plt
import utils
from matplotlib import cm
import numpy as np





def console_write_result(cpx_object, K):
    objective = cpx_object.solution.get_objective_value()
    solution = cpx_object.solution.get_values()
    variable_names = cpx_object.variables.get_names()
    tours = utils.tour(variable_names, solution, K)
    for k in range(K):
        print(f"\nTour number {k}:")
        print(tours[k][-1])
        for i in range(len(tours[k])):
            print(tours[k][i])
    print(f"\n total distance is: {objective}")



def display(cpx_object, nodes, K, title):
    objective = cpx_object.solution.get_objective_value()
    solution = cpx_object.solution.get_values()
    variable_names = cpx_object.variables.get_names()
    tours = utils.tour(variable_names, solution, K)
    X, Y = [], []
    for node in nodes:
        _, x, y = node.split("_")

        X.append(float(x))
        Y.append(float(y))
    
    colours = cm.rainbow(np.linspace(0, 1, K))

    for k in range(K):
        for i in range(len(tours[k]) - 1):
            _, x1, y1 = tours[k][i].split("_")
            _, x2, y2 = tours[k][i + 1].split("_")
            plt.plot([float(x1), float(x2)], [float(y1), float(y2)], color = colours[k][:-1])
        _, x1, y1 = tours[k][0].split("_")
        _, x2, y2 = tours[k][-1].split("_")
        plt.plot([float(x1), float(x2)], [float(y1), float(y2)], color = colours[k][:-1])
    plt.scatter(X, Y)
    plt.title(title)
    plt.show()


