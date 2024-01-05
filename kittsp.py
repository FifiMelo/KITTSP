import utils
import cplex


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

                    variable_names = []
                    for node1 in node_group1: 
                        for node2 in node_group2:
                            v = utils.variable_name(node1, node2, k)
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