
def tour(possible_edges, values, K):
    """
    This function gets objects provided by solving a cplex problem
    and gives the answer as a list of consecutive nodes.

    possible_edges: a list of all posible edges (access it with cpx_object.variables.get_names())

    values: a list of 0s and 1s where 1 in j-th position means that j-th edge is taken
    (access it with cpx_object.solution.get_values())

    K: number of tours

    """
    adjacency_list = [dict() for i in range(K)]
    for i in range(len(possible_edges)):
        if values[i] == 1:
            node1, node2, tour = possible_edges[i].split("-")
            tour = int(tour)

            if node1 in adjacency_list[tour]:
                adjacency_list[tour][node1].append(node2)
            else:
                adjacency_list[tour][node1] = [node2]

            if node2 in adjacency_list[tour]:
                adjacency_list[tour][node2].append(node1)
            else:
                adjacency_list[tour][node2] = [node1]
    
    all_nodes = []
    for k in range(K):
        # we will check if the k-th tour is really a tour (and not few sub-tours)
        first_node = list(adjacency_list[k].keys())[0]
        visited_nodes = []
        previous_node = first_node
        new_node = adjacency_list[k][previous_node][0]
        visited_nodes.append(previous_node)
        while not new_node == first_node:
            visited_nodes.append(new_node)
            if adjacency_list[k][new_node][0] == previous_node:
                previous_node = new_node
                new_node = adjacency_list[k][new_node][1]
            else:
                previous_node = new_node
                new_node = adjacency_list[k][new_node][0]
        all_nodes.append(visited_nodes)
    return all_nodes 


def variable_name(node1, node2, k):
    """
    This function returns variable name responsible for connecting two nodes in k-th tour.
    Purpose of this function is to always keep nodes in alphabetical order.
    """
    if node1 < node2:
        return f"{node1}-{node2}-{k}"
    return f"{node2}-{node1}-{k}"

def get_variables_of_node(node_name, tour_index, cpx_object):
    """
    This function returns a list of variables corresponding to the given node and given tour index
    """
    all_variables = cpx_object.variables.get_names()
    selected_variables = []
    for variable in all_variables:
        node1, node2, tour = variable.split("-")
        if (node1 == node_name or node2 == node_name) and int(tour) == tour_index:
            selected_variables.append(variable)
    return selected_variables