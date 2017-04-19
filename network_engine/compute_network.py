import pandas as pd
import numpy as np
import networkx as nx
from networkx import *
STEP = 1
HISTORIAL_NUMBER_OF_ROWS = 15


def build (df_close):

    if STEP > HISTORIAL_NUMBER_OF_ROWS:
        raise ValueError('The STEP parameter must be greater than HISTORIAL_NUMBER_OF_ROWS')

    correlations = []
    correlation_means = []
    correlation_std = []

    end_index = df_close.shape[0] - HISTORIAL_NUMBER_OF_ROWS

#    import ipdb; ipdb.set_trace()
    if STEP > end_index:
        raise ValueError('The STEP parameter must be less than {0} days'\
            .format(end_index))

    # We consider the STEP but you should think the remainder until end_index
    for i in range(0, df_close.shape[0] - HISTORIAL_NUMBER_OF_ROWS, STEP):
        subdf = df_close.ix[i:i+HISTORIAL_NUMBER_OF_ROWS, :]
        graph=pd.DataFrame(np.diff(np.log(subdf.dropna(1)), axis=0))
        graph1=np.corrcoef([graph[col] for col in graph.columns])
        inversegraph1=(1-np.absolute(graph1))*np.sign(graph1)
        inversegraph2=nx.from_numpy_matrix(inversegraph1)
        tree = nx.minimum_spanning_tree(inversegraph2)
        tree1 = nx.to_numpy_matrix(tree)
        tree2 = np.squeeze(np.asarray(tree1))
        tree3 = (1-np.absolute(tree2))*np.sign(tree2)
        np.fill_diagonal(tree3, 1)
        correlations.append(tree3)
        correlation_means.append(np.mean(tree3))
        correlation_std.append(np.std(tree3))
    #    import ipdb; ipdb.set_trace()


    #print (correlations)
    #print (type(correlations))




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


    return correlation_means, correlation_std, tree
