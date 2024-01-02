import matplotlib.pyplot as plt
from icecream import ic

def get_lists(cpx_object, K):

    adjacency_lists = [dict() for k in range(K)]
    objective = cpx_object.solution.get_objective_value()
    solution = cpx_object.solution.get_values()
    variable_names = cpx_object.variables.get_names()
    for edge_index in range(len(variable_names)):
        if solution[edge_index] == 1:
            node1, node2, index = variable_names[edge_index].split('-')
            index = int(index)
            if node1 in adjacency_lists[index]:
                adjacency_lists[index][node1].append(node2)
            else:
                adjacency_lists[index][node1] = [node2]

            if node2 in adjacency_lists[index]:
                adjacency_lists[index][node2].append(node1)
            else:
                adjacency_lists[index][node2] = [node1]
    ic(adjacency_lists)
    """
    for k in range(K):
        previous_node = adjacency_lists[k].keys()[0]
        new_node = adjacency_lists[k][previous_node][0]
    """




def display_results(cpx_object, K):
    objective = cpx_object.solution.get_objective_value()
    solution = cpx_object.solution.get_values()
    variable_names = cpx_object.variables.get_names()