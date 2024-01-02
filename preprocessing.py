"""
Purpose of this module is to change format of data collected from the website:
https://www.math.uwaterloo.ca/tsp/world/countries.html
convert it to data format readable by our solver and add edges.
"""

import math
from icecream import ic

def distance(x1, y1, x2, y2):
    """
    We will be able to watch changes in the path after changing type of metrics we use
    """
    assert type(x1) is float
    assert type(y1) is float
    assert type(x2) is float
    assert type(y2) is float
    return int(math.sqrt((x1 - x2)**2 + (y1 - y2)**2))

def main():
    name = "dj38"
    input_file_name = f"./raw_data/{name}.tsp"
    output_file_name = f"./preprocessed/{name}.txt"
    output_file_tours_number = 1


    with open(input_file_name, "r") as in_file:
        with open(output_file_name, "w") as out_file:

            # first 7 lines contains some information we don't need
            for i in range(7):
                in_file.readline()

            # adding numbers K and N
            out_file.write(str(output_file_tours_number))
            out_file.write("\n")
            

            nodes = []

            # reading nodes
            while True:
                input = in_file.readline()
                #ic(input)
                if input[:3] == "EOF":
                    break
                index, x, y = input.split()
                node_name = f"{index}_{x}_{y}"
                nodes.append((float(x), float(y), node_name))


            nodes = list(set(nodes))
            number_of_incoming_nodes = len(nodes)
            out_file.write(str(number_of_incoming_nodes))
            out_file.write("\n")

            #adding nodes to the output file
            for i in range(number_of_incoming_nodes):
                out_file.write(f"{nodes[i][2]}\n")

            out_file.write(str((number_of_incoming_nodes * (number_of_incoming_nodes - 1)) // 2))
            out_file.write("\n")

            for i in range(number_of_incoming_nodes):
                for j in range(i + 1, number_of_incoming_nodes):
                    x1, y1, node_name1 = nodes[i]
                    x2, y2, node_name2 = nodes[j]
                    x1 = float(x1)
                    y1 = float(y1)
                    x2 = float(x2)
                    y2 = float(y2)
                    out_file.write(f"{node_name1} {node_name2} {str(distance(x1, y1, x2, y2))}\n")
                    


            

        


if __name__ == '__main__':
    main()