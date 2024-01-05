import cplex
from icecream import ic
import display
import sys


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
        if values[i] > 0.5:
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


def solve_kittsp(node_names, edge_list, K = 1):
    """
    node_names: list of node names (strings)
    edge_list: list of edges represented as touples in format (node1, node2, cost),
    where node1 and node2 must be strings present in node_names
    K: number of independent tours to be found

    This function returns a cplex.Cplex() object after solving the kittsp
    """
    N = len(node_names)
    M = len(edge_list)

    cpx_object = cplex.Cplex()
    cpx_object.parameters.threads.set(1)
    cpx_object.objective.set_sense(cpx_object.objective.sense.minimize)

    for edge in edge_list:
        node1, node2, cost = edge


        variable_names = [
                variable_name(node1, node2, tour_index) for tour_index in range(K)
                ]
        cpx_object.variables.add(
                obj = [float(cost) for tour_index in range(K)],  
                types = [cpx_object.variables.type.binary for tour_index in range(K)], 
                names = variable_names
                )
        
        
        # adding constraints that none of the edges can be in more that one tour
        lin_expr = cplex.SparsePair(
                ind = variable_names,
                val = [1 for variable in variable_names]
        )
        cpx_object.linear_constraints.add(
                lin_expr = [lin_expr],
                senses=["L"], 
                rhs = [1],
                names = [f"{node1}-{node2}"]
                )
        
        # adding simple constraints
            # that in each tour in each node exactly two edges must be selected
    for node in node_names:
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
                
    class MyLazyConsCallback(cplex.callbacks.LazyConstraintCallback):
        def __call__(self):
            """
            This function is used to add a constraint eliminating subtours using bfs algorithm
            """

            try:
                visited_nodes = tour(self.possible_edges, self.get_values(), self.K)

                for k in range(self.K):
                    if len(visited_nodes[k]) < len(self.nodes):
                        # if the tour turned out to be just a subtour
                        node_group1 = visited_nodes[k]
                        node_group2 = set(self.nodes) - set(visited_nodes[k])

                        variable_names = []
                        for node1 in node_group1: 
                            for node2 in node_group2:
                                v = variable_name(node1, node2, k)
                                if v in self.possible_edges:
                                    variable_names.append(v)

                        lin_expr = cplex.SparsePair(
                            ind = variable_names,
                            val = [1] * len(variable_names))
                        self.add(
                            constraint = lin_expr,
                            sense = "G",
                            rhs = 1
                            )
            except:
                print(sys.exc_info()[0])
                raise
                    
        def read_graph(self, nodes, K, variable_names):
            """
            This function is used to provide nodes and possible edges to 
            the LazyCallback object
            """
            self.nodes = nodes
            self.possible_edges = variable_names
            self.K = K

    lazyCB = cpx_object.register_callback(MyLazyConsCallback)
    
    lazyCB.read_graph(node_names, K, cpx_object.variables.get_names())
    
    cpx_object.parameters.preprocessing.presolve.set(cpx_object.parameters.preprocessing.presolve.values.off)
    cpx_object.parameters.mip.strategy.search.set(cpx_object.parameters.mip.strategy.search.values.traditional)
    cpx_object.solve()

    return cpx_object

def read_input(filename):
    """
    This function reads the input file
    and then returns the list of nodes, list of edges and K
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
        nodes = []
        for i in range(N):
            nodes.append(file.readline().strip())
        M = int(file.readline().strip())

        edges = []
        for i in range(M):
            line = file.readline().split()
            node1, node2, cost = line
            edges.append((node1, node2, cost))
    return nodes, edges, K


if __name__ == "__main__":
    nodes, edges, K = read_input("./preprocessed/data1_for_kittsp.txt")
    cpx = solve_kittsp(nodes, edges, K)
    if cpx.solution.get_status()!=103 and cpx.solution.get_status()!=108:
        display.console_write_result(cpx, K)
    else:
        print(cpx.solution.get_status())