import utils
import display
import random
from icecream import ic


def get_adjacency_list(nodes, edges, eps = 0.01):
    adjacency_list = dict()
    for edge in edges:
        node1, node2, cost = edge
        cost = int(cost)
        if not node1 in adjacency_list:
            adjacency_list[node1] = dict()  

        if not node2 in adjacency_list:
            adjacency_list[node2] = dict() 

        adjacency_list[node2][node1] = cost
        adjacency_list[node1][node2] = cost
    return adjacency_list

def find_tour(nodes, adjacency_list):
    path = []
    
    actual_node = random.choice(nodes)
    while actual_node is not None:
        path.append(actual_node)
        best_distance = float("Inf")
        new_node  = None
        for neighbour in adjacency_list[actual_node]:
            if (not neighbour in path) and adjacency_list[actual_node][neighbour] < best_distance:
                new_node = neighbour
                best_distance = adjacency_list[actual_node][neighbour]
        if new_node is None:
            break
        
        actual_node = new_node
    
    if not path[-1] in adjacency_list[path[0]]:
        path = find_tour(nodes, adjacency_list)
    return path
        

        

def main():
    print("Please enter problem instance name: (from folder preprocessed)")
    input_file_name = f"./preprocessed/{input()}.txt"
    print("Do you want to display graph? (Y/N) (only for instances with nodes names in format title_x_y)")
    if input() in ["Y", "y", "T", "t"]:
        display_graph = True
    else:
        display_graph = False
    nodes, edges, K = utils.read_input(input_file_name)
    adjacency_list = get_adjacency_list(nodes, edges)
    tours = []
    objective = 0
    for k in range(K - 1):
        path = find_tour(nodes, adjacency_list)
        tours.append(path)
        #now we need to remove from adjacency list edges already used
        for i in range(len(path) - 1):

            del adjacency_list[path[i]][path[i + 1]]
            del adjacency_list[path[i + 1]][path[i]]

        del adjacency_list[path[0]][path[-1]]
        del adjacency_list[path[-1]][path[0]]

    
    path = find_tour(nodes, adjacency_list)
    tours.append(path)

    display.console_write_result(tours, objective, K)
    if display_graph:
        display.display(nodes, tours, K, f"instance: {input_file_name}, K: {K}, greedy")
    
    
        
    
    



if __name__ == '__main__':
    main()