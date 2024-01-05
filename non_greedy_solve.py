import utils
import display

if __name__ == '__main__':
    print("Please enter problem instance name: (from folder preprocessed)")
    input_file_name = f"./preprocessed/{input()}.txt"
    print("Do you want to display graph? (Y/N) (only for instances with nodes names in format title_x_y)")
    if input() in ["Y", "y", "T", "t"]:
        display_graph = True
    else:
        display_graph = False

    nodes, edges, K = utils.read_input(input_file_name)
    cpx = utils.solve_kittsp(nodes, edges, K)
    if cpx.solution.get_status()!=103 and cpx.solution.get_status()!=108:
        display.console_write_result(cpx, K)
        if display_graph:
            display.display(cpx, nodes, K, f"instance: {input_file_name}, K: {K}")
    else:
        print(cpx.solution.get_status())