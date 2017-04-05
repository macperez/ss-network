

STEP = 1
HISTORIAL_NUMBER_OF_ROWS = 15

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def build (df_close, close_data_frame_IBEX ):
    correlations = []
    correlation_means=[]
    correlation_std=[]

    #import ipdb; ipdb.set_trace()

    for i in range(0, df_close.shape[0] - HISTORIAL_NUMBER_OF_ROWS):
        subdf = df_close.ix[i:i+HISTORIAL_NUMBER_OF_ROWS, :]
        graph=pd.DataFrame(np.diff(np.log(subdf.dropna(1)),axis=0))
        graph1=np.corrcoef([graph[col] for col in graph.columns])
    #    graph1 = np.corrcoef(np.triu(subdf.fillna(0)))
        #graph = np.corrcoef(np.triu(np.diff(np.log(subdf.fillna(0)))))
        correlations.append(graph1)
        correlation_means.append(np.mean(graph1))
        correlation_std.append(np.std(graph1))

    #for n in range(1,10,STEP):
    #print(correlation_means)
    #plt.plot(close_data_frame_IBEX)
    plt.subplot(3,1,1)
    plt.title('Ibex35',fontsize = 28, color = '0.75', verticalalignment = 'baseline', horizontalalignment = 'center')
    plt.plot(close_data_frame_IBEX)
    plt.legend( ('Valor del Índice', 'Etiqueta2', 'Etiqueta3'), loc = 'upper left')
    plt.subplot(3,1,2)
    plt.plot(correlation_means)
    plt.legend( ('Correlación media', 'Etiqueta2', 'Etiqueta3'), loc = 'upper left')
    plt.subplot(3,1,3)
    plt.plot(correlation_std)
    plt.legend( ('Desviación de la correlación', 'Etiqueta2', 'Etiqueta3'), loc = 'upper left')
    plt.show()
#    import ipdb; ipdb.set_trace()
    return correlation_means, correlation_std



if __name__ == '__main__':
    pass
