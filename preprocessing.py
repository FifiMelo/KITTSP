"""
Purpose of this module is to change format of data collected from the website:
https://www.math.uwaterloo.ca/tsp/world/countries.html
convert it to data format readable by our solver and add edges.
"""

import math
from icecream import ic
import random

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
    print("Please enter file name to be preprocessed: (from folder raw_data)")
    name = input()
    print("Please enter number of independent tours to be found:")
    output_file_tours_number = int(input())
    print("Please enter number of nodes to be taken: (-1 if all the nodes)")
    number_of_incoming_nodes = int(input())
    read_in_file_name = f"./raw_data/{name}.tsp"
    if number_of_incoming_nodes == -1:
        output_file_name = f"./preprocessed/{name}.txt"
    else:
        output_file_name = f"./preprocessed/{name[:2]}{number_of_incoming_nodes}.txt"
    
    random.seed(212)

    with open(read_in_file_name, "r") as in_file:
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
                read_in = in_file.readline()
                #ic(read_in)
                if read_in[:3] == "EOF":
                    break
                index, x, y = read_in.split()
                node_name = f"{index}_{x}_{y}"
                nodes.append((float(x), float(y), node_name))

            if number_of_incoming_nodes == -1:
                nodes = list(set(nodes))
            else:
                nodes = list(set(random.sample(nodes, number_of_incoming_nodes)))
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