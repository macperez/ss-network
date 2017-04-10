"""
This module is built with Matplotlib in order to present historial-data
It is fairly enough for this purpose.

@author: Manuel Castro
@email: desarrollo@institutoibt.come

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from networkx import *

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
    pass


def paint_network(G, component_names):

    components_labels = {i:component_names[i] for i in range(len(component_names))}
    nx.draw_spectral(G)

    #nx.draw_networkx(G,labels=components_labels,with_labels=True)      #nx.draw_networkx(G, with_labels=True)
    plt.draw()  # pyplot draw()
    plt.show()

    pass
