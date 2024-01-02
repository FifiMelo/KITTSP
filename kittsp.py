import cplex
import display


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


def variable_name(node1, node2, k):
    """
    This function returns variable name responsible for connecting two nodes in k-th tour.
    Purpose of this function is to always keep nodes in alphabetical order.
    """
    if node1 < node2:
        return f"{node1}-{node2}-{k}"
    return f"{node2}-{node1}-{k}"

def get_input(filename, cpx_object):
    """
    This function reads the input file, adds variables and constraints to the cpx object, 
    and then returns the list of nodes of the graph as well as K - number of tours
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

            variable_names = [variable_name(node1, node2, tour_index) for tour_index in range(K)]


            cpx_object.variables.add(
                obj = [float(cost)] * K,  
                types = [cpx_object.variables.type.binary] * K, 
                names = variable_names
                )

            
            # adding constraints that none of the edges can be in more that one tour
            lin_expr = cplex.SparsePair(
                ind = variable_names,
                val = [1] * len(variable_names))
            cpx_object.linear_constraints.add(
                lin_expr = [lin_expr],
                senses=["L"], 
                rhs = [1],
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
        return Nodes, K
        
        
class MyLazyConsCallback(cplex.callbacks.LazyConstraintCallback):

    def __call__(self):
        """
        This function is used to add a constraint eliminating subtours using bfs algorithm
        """
        values = self.get_values()


        # we need to create adjacency lists to be able to do bfs algorithm efficiently
        adjacency_list = [dict() for i in range(self.K)]
        for i in range(len(self.possible_edges)):
            if values[i] == 1:
                node1, node2, tour = self.possible_edges[i].split("-")
                tour = int(tour)

                if node1 in adjacency_list[tour]:
                    adjacency_list[tour][node1].append(node2)
                else:
                    adjacency_list[tour][node1] = [node2]

                if node2 in adjacency_list[tour]:
                    adjacency_list[tour][node2].append(node1)
                else:
                    adjacency_list[tour][node2] = [node1]
        
        for k in range(self.K):
            # we will check if the k-th tour is really a tour (and not few sub-tours)
            visited_nodes = set()
            previous_node = self.nodes[0]
            new_node = adjacency_list[k][previous_node][0]
            visited_nodes.add(previous_node)
            while not new_node == self.nodes[0]:
                visited_nodes.add(new_node)
                if adjacency_list[k][new_node][0] == previous_node:
                    previous_node = new_node
                    new_node = adjacency_list[k][new_node][1]
                else:
                    previous_node = new_node
                    new_node = adjacency_list[k][new_node][0]


            if len(visited_nodes) < len(self.nodes):
                # if the tour turned out to be just a subtour
                node_group1 = visited_nodes
                node_group2 = set(self.nodes) - visited_nodes
                variable_names = [variable_name(node1, node2, k) for node1 in node_group1 for node2 in node_group2]
                lin_expr = cplex.SparsePair(
                    ind = variable_names,
                    val = [1] * len(variable_names))
                self.add(
                    constraint = lin_expr,
                    sense = "E",
                    rhs = 2.0
                    )
                
    def read_graph(self, nodes, K, cpx_object):
        """
        This function is used to provide nodes and possible edges to 
        the LazyCallback object
        """
        self.nodes = nodes
        self.possible_edges = cpx_object.variables.get_names()
        self.K = K
        self.cpx_object = cpx_object
        

def display_result(cpx_object, K):
    objective = cpx_object.solution.get_objective_value()
    solution = cpx_object.solution.get_values()
    taken_edges = [set() for tour_index in range(K)]
    variable_names = cpx_object.variables.get_names()
    for edge_index in range(len(variable_names)):
        if solution[edge_index] == 1:
            taken_edges[int(variable_names[edge_index][-1])].add(variable_names[edge_index])
    for tour_index in range(K):
        print(f"Edges taken to the tour number {tour_index}:")
        for edge in taken_edges[tour_index]:
            print(edge[:-2])
    print(f"Full distance is {objective}")

            




def main():
    input_file_name = "./preprocessed/data1_for_kittsp.txt"
    cpx = cplex.Cplex()
    cpx.parameters.threads.set(1)
    cpx.objective.set_sense(cpx.objective.sense.minimize)
    nodes, K = get_input(input_file_name, cpx)

    lazyCB = cpx.register_callback(MyLazyConsCallback)
    lazyCB.read_graph(nodes, K, cpx)
    cpx.parameters.preprocessing.presolve.set(cpx.parameters.preprocessing.presolve.values.off)
    cpx.parameters.mip.strategy.search.set(cpx.parameters.mip.strategy.search.values.traditional)
    cpx.solve()

    if cpx.solution.get_status()!=103 and cpx.solution.get_status()!=108:
        display.get_lists(cpx, K)
    else:
        print("ERROR")
        print(cpx.solution.get_status())


if __name__ == '__main__':
    main()

