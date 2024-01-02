import matplotlib.pyplot as plt
from icecream import ic
import utils




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
