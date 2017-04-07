import pandas as pd
import numpy as np
impor   t networkx as nx

STEP = 1
HISTORIAL_NUMBER_OF_ROWS = 15


def build(df_close):
    if STEP > HISTORIAL_NUMBER_OF_ROWS:
        raise ValueError('The STEP parameter must be greater \
                          than HISTORIAL_NUMBER_OF_ROWS')
    correlations = []
    correlation_means = []
    correlation_std = []

    end_index = df_close.shape[0] - HISTORIAL_NUMBER_OF_ROWS

    if STEP > end_index:
        raise ValueError('The STEP parameter must be less than {0} days'
                         .format(end_index))

    # We consider the STEP but you should think the remainder until end_index
    for i in range(0, df_close.shape[0] - HISTORIAL_NUMBER_OF_ROWS, STEP):
        subdf = df_close.ix[i:i+HISTORIAL_NUMBER_OF_ROWS, :]
        graph = pd.DataFrame(np.diff(np.log(subdf.dropna(1)), axis=0))
        graph1 = np.corrcoef([graph[col] for col in graph.columns])

        correlations.append(graph1)
        correlation_means.append(np.mean(graph1))
        correlation_std.append(np.std(graph1))
    #
    # # With the remainder we build another grp
    # remainder = end_index % STEP
    # if remainder > 0:
    #     subdf = df_close.ix[end_index-remainder:end_index, :]
    #     graph=pd.DataFrame(np.diff(np.log(subdf.dropna(1)),axis=0))
    #     graph1=np.corrcoef([graph[col] for col in graph.columns])
    #
    #     correlations.append(graph1)
    #     correlation_means.append(np.mean(graph1))
    #     correlation_std.append(np.std(graph1))

    return correlation_means, correlation_std
