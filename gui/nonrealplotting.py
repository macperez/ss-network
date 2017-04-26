"""
This module is built with Matplotlib in order to present historial-data
It is fairly enough for this purpose.

@author: Manuel Castro
@email: desarrollo@institutoibt.come

"""

import pandas as pd
import numpy as np
import networkx as nx

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt


def paint (close_data_frame_IBEX, correlation_means, correlation_std):
    plt.figure(figsize=(20,10))
    plt.subplot(3,1,1)
    plt.title('Ibex35',fontsize = 28, color = '0', verticalalignment = 'baseline', horizontalalignment = 'center')
    plt.plot(close_data_frame_IBEX)
    plt.ylabel('Index value')
    plt.subplot(3,1,2)
    plt.plot(correlation_means)
    plt.ylabel('Mean correlation')
    plt.subplot(3,1,3)
    plt.plot(correlation_std)
    plt.ylabel('Correlation deviation')
    plt.show()


# def paint_network(G, component_names):
#
#     agraph = nx.nx_agraph.to_agraph(G)
#     agraph.node_attr['shape'] = 'ellipse'
#     agraph.node_attr['fontsize'] = 8
#     component_index = 0
#     for node in agraph.nodes():
#         node.attr['label'] = component_names[component_index]
#         component_index += 1
#
#     #graphviz_layout
#     agraph.draw('file.png',prog='neato')
