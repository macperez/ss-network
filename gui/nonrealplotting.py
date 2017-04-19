"""
This module is built with Matplotlib in order to present historial-data
It is fairly enough for this purpose.

@author: Manuel Castro
@email: desarrollo@institutoibt.come

"""

import pandas as pd
import numpy as np
import matplotlib as plt
plt.use('TkAgg')


class Picture:
    # def __init__(self):
    #     self.data =

    def paint(self, close_data_frame_IBEX, correlation_means, correlation_std):
        plt.subplot(3, 1, 1)
        plt.title('Ibex35', fontsize=28, color='0.75',
                  verticalalignment='baseline', horizontalalignment='center')
        plt.plot(close_data_frame_IBEX)
        plt.legend(('Valor del Índice', 'Label2', 'Label3'), loc='upper left')
        plt.subplot(3, 1, 2)
        plt.plot(correlation_means)
        plt.legend(('Correlación media', 'Etiqueta2', 'Etiqueta3'),
                   loc='upper left')
        plt.subplot(3, 1, 3)
        plt.plot(correlation_std)
        plt.legend(('Desviación de la correlación', 'Etiqueta2', 'Etiqueta3'),
                   loc='upper left')
        plt.show()

    def paint_network(self, data):
        pass


def paint_network(G, component_names):

    components_labels = {i: component_names[i]
                         for i in range(len(component_names))}
    #nx.draw_spectral(G)
    nx.draw_random(G)
    #nx.draw_networkx(G,labels=components_labels,with_labels=True)      #nx.draw_networkx(G, with_labels=True)
    plt.draw()  # pyplot draw()
    plt.show()

    pass
