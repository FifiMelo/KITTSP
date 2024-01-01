"""
Purpose of this module is to change format of data collected from the website:
https://www.math.uwaterloo.ca/tsp/world/countries.html
convert it to data format readable by our solver and add edges.
"""

import math


def distance(x1, y1, x2, y2):
    """
    We will be able to watch changes in the path after changing type of metrics we use
    """
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def main():
    input_file_name = "./data/uy734.tsp"
    output_file_name = "./data/data.txt"
    output_file_tours_number = 3
    number_of_incoming_nodes = 734


    with open(input_file_name, "r") as in_file:
        with open(output_file_name, "w") as out_file:

            # first 7 lines contains some information we don't need
            for i in range(7):
                in_file.readline()

            # adding numbers K and N
            out_file.write(str(output_file_tours_number))
            out_file.write("\n")
            out_file.write(str(number_of_incoming_nodes))
            out_file.write("\n")

            nodes = []

            # adding nodes
            for node in range(number_of_incoming_nodes):
                index, x, y = in_file.readline().split()
                out_file.write(f"{index}_{x}_{y}\n")
                nodes.append((int(index), float(x), float(y)))

            out_file.write(str((number_of_incoming_nodes * (number_of_incoming_nodes - 1)) // 2))
            out_file.write("\n")

            for i in range(number_of_incoming_nodes):
                for j in range(i + 1, number_of_incoming_nodes):
                    pass
                    


            

        


if __name__ == '__main__':
    main()