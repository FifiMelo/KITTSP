import cplex

def get_pairs(list):
    """
    This function yields a list of all possible pairs of elements from the given list
    """
    for i in range(len(list)):
        for j in range(i + 1, len(list)):
            yield [list[i], list[j]]


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
            cpx_object.variables.add(
                obj = [float(cost)] * K,  
                types = [cpx_object.variables.type.binary] * K, 
                names = [f"{node1}-{node2}-{j}" for j in range(K)]
                )
        
        

        




def main():
    cpx = cplex.Cplex()
    cpx.parameters.threads.set(1)
    cpx.objective.set_sense(cpx.objective.sense.minimize)
    get_input("./data_for_kittsp.txt", cpx)



    




if __name__ == '__main__':
    main()

