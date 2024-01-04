import cplex
import display
import utils
import sys
from icecream import ic



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

        # adding variables
        for i in range(M):
            node1, node2, cost = file.readline().split()

            variable_names = [
                utils.variable_name(node1, node2, tour_index) for tour_index in range(K)
                ]


            cpx_object.variables.add(
                obj = [float(cost) for tour_index in range(K)],  
                types = [cpx_object.variables.type.binary for tour_index in range(K)], 
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
                variables = utils.get_variables_of_node(node, tour_index, cpx_object)
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


        visited_nodes = utils.tour(self.possible_edges, self.get_values(), self.K)

        for k in range(self.K):
            if len(visited_nodes[k]) < len(self.nodes):
                # if the tour turned out to be just a subtour
                node_group1 = visited_nodes[k]
                node_group2 = set(self.nodes) - set(visited_nodes[k])
                variable_names = [
                    utils.variable_name(node1, node2, k) for node1 in node_group1 for node2 in node_group2
                    ]
                lin_expr = cplex.SparsePair(
                    ind = variable_names,
                    val = [1] * len(variable_names))
                self.add(
                    constraint = lin_expr,
                    sense = "E",
                    rhs = 2.0
                    )
                
    def read_graph(self, nodes, K, variable_names):
        """
        This function is used to provide nodes and possible edges to 
        the LazyCallback object
        """
        self.nodes = nodes
        self.possible_edges = variable_names
        self.K = K
        

def main():
    print("Please enter problem instance name: (from folder preprocessed)")
    input_file_name = f"./preprocessed/{input()}.txt"
    print("Do you want to display graph? (Y/N) (only for instances with nodes names in format title_x_y)")
    if input() in ["Y", "y", "T", "t"]:
        display_graph = True
    else:
        display_graph = False
    cpx = cplex.Cplex()
    cpx.parameters.threads.set(1)
    cpx.objective.set_sense(cpx.objective.sense.minimize)
    nodes, K = get_input(input_file_name, cpx)

    #lazyCB = cpx.register_callback(MyLazyConsCallback)
    #lazyCB.read_graph(nodes, K, cpx.variables.get_names())
    cpx.parameters.preprocessing.presolve.set(cpx.parameters.preprocessing.presolve.values.off)
    cpx.parameters.mip.strategy.search.set(cpx.parameters.mip.strategy.search.values.traditional)
    cpx.solve()

    if cpx.solution.get_status()!=103 and cpx.solution.get_status()!=108:
        display.console_write_result(cpx, K)
        if display_graph:
            display.display(cpx, nodes, K, f"instance: {input_file_name}, K: {K}")
    else:
        print(cpx.solution.get_status())


if __name__ == '__main__':
    main()

