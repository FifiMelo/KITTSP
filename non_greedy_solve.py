import utils
import display
import kittsp

if __name__ == '__main__':
    """
    This function solves kittsp using classical formulation.
    """
    print("Please enter problem instance name: (from folder preprocessed)")
    input_file_name = f"./preprocessed/{input()}.txt"
    print("Do you want to display graph? (Y/N) (only for instances with nodes names in format title_x_y)")
    if input() in ["Y", "y", "T", "t"]:
        display_graph = True
    else:
        display_graph = False

    nodes, edges, K = utils.read_input(input_file_name)
    cpx = kittsp.solve_kittsp(nodes, edges, K)

    objective = cpx.solution.get_objective_value()
    solution = cpx.solution.get_values()
    variable_names = cpx.variables.get_names()

    tours = utils.tour(variable_names, solution, K)

    if cpx.solution.get_status()!=103 and cpx.solution.get_status()!=108:
        display.console_write_result(tours, objective, K)
        if display_graph:
            display.display(nodes, tours, K, f"instance: {input_file_name}, K: {K}, non-greedy")
    else:
        print(cpx.solution.get_status())