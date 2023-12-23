import cplex


def get_variables_of_node(node_name, tour_index, cpx_object):
    """
    This function returns a list of variables corresponding to the given node, and given tour index
    """
    all_variables = cpx_object.variables.get_names()
    selected_variables = []
    for variable in all_variables:
        node1, node2, tour = variable.split("-")
        if (node1 == node_name or node2 == node_name) and int(tour) == tour_index:
            selected_variables.append(variable)
    return selected_variables


def get_input(filename, cpx_object):
    """
    This function returns set of cplex variables as well as cplex constrains
    read from the file. The file must be in specific format, i.e.:
    3 <- K, the number of independent tours to be found
    5 <- N, the number of nodes in the graph
    A
    B
    C 
    D 
    E <- names of the nodes (N lines)
    9 <- M, the number of edges, M <= N! / (2! * (N - 2)!)
    A B 5
    A C 9
    A D 3
    A E 2
    B C 3
    B D 10
    B E 8
    C E 5
    D E 1 <- the edges in format: node1 node2 cost
    """
    with open(filename) as file:
        K = int(file.readline().strip())
        N = int(file.readline().strip())
        Nodes = []
        for i in range(N):
            Nodes.append(file.readline().strip())
        M = int(file.readline().strip())

        # adding varaibles
        for i in range(M):
            node1, node2, cost = file.readline().split()
            variable_names = [f"{node1}-{node2}-{tour_index}" for tour_index in range(K)]
            cpx_object.variables.add(
                obj = [float(cost)] * K,  
                types = [cpx_object.variables.type.binary] * K, 
                names = [f"{node1}-{node2}-{tour_index}" for tour_index in range(K)]
                )
            
            # adding constraints that none of the edges can be in more that one tour
            lin_expr = cplex.SparsePair(
                ind = variable_names,
                val = [1] * len(variable_names))
            cpx_object.linear_constraints.add(
                lin_expr = [lin_expr],
                senses=["L"], 
                rhs = [2],
                names = [f"{node1}-{node2}"]
                )
            
            
        # adding simple constraints
        # that in each tour in each node exactly two edges must be selected
        for node in Nodes:
            for tour_index in range(K):
                variables = get_variables_of_node(node, tour_index, cpx_object)
                lin_expr = cplex.SparsePair(
                    ind = variables,
                    val = [1] * len(variables)
                    )
                cpx_object.linear_constraints.add(
                    lin_expr = [lin_expr],
                    senses=["E"], 
                    rhs = [2],
                    names = [f"{node}-{tour_index}"]
                    )
        
        
        
        

        




def main():
    cpx = cplex.Cplex()
    cpx.parameters.threads.set(1)
    cpx.objective.set_sense(cpx.objective.sense.minimize)
    get_input("./data_for_kittsp.txt", cpx)

    # print(cpx.linear_constraints.get_names())
    cpx.solve()

    if cpx.solution.get_status()!=103 and cpx.solution.get_status()!=108:
        myObj=cpx.solution.get_objective_value()
        mySol=cpx.solution.get_values()
        print(myObj)
        print(mySol)
    else:
        print("ERROR")



    




if __name__ == '__main__':
    main()

