
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
    return visited_nodes 