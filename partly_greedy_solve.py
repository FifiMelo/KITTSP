import utils
import display
from icecream import ic

if __name__ == '__main__':
    print("Please enter problem instance name: (from folder preprocessed)")
    input_file_name = f"./preprocessed/{input()}.txt"
    print("Do you want to display graph? (Y/N) (only for instances with nodes names in format title_x_y)")
    if input() in ["Y", "y", "T", "t"]:
        display_graph = True
    else:
        display_graph = False

    nodes, edges, K = utils.read_input(input_file_name)
    solution = []

    for k in range(K):
        cpx = utils.solve_kittsp(nodes, edges, 1)

        new_edges = []

        names = cpx.variables.get_names()
        values = cpx.solution.get_values()

        solution.append(utils.tour(names, values, 1)[0])

        for i in range(len(values)):
            if values[i] < 0.5:
                new_edges.append(edges[i])
        edges = new_edges
    print(solution)



