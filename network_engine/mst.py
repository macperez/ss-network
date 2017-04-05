"""
A collection of Minimal spawn tree algorithms implemented in Python

@author: Manuel Castro
@email: desarrollo@institutoibt.come

"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def main():
    array = np.ones((4,4))
    matrix = np.matrix([[1,1],[2,1]])
    graph = nx.from_numpy_matrix(array)

    tree = nx.minimum_spanning_tree(graph)
    print (tree.edges())
    nx.draw(graph)
    plt.show()


if __name__ == '__main__':
    main()
