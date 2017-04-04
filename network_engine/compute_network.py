

STEP = 1
HISTORIAL_NUMBER_OF_ROWS = 14

import pandas as pd
import numpy as np

def build (df_close):
    correlations = []
    correlation_means=[]
    correlation_std=[]

    import ipdb; ipdb.set_trace()

    for i in range(0, df_close.shape[0] - HISTORIAL_NUMBER_OF_ROWS):
        subdf = df_close.ix[i:i+HISTORIAL_NUMBER_OF_ROWS, :]
        graph = np.corrcoef(subdf.fillna(0))
        correlations.append(graph)
        correlation_means.append(np.mean(graph))
        correlation_std.append(np.std(graph))


    import ipdb; ipdb.set_trace()
    return correlation_means, correlation_std



if __name__ == '__main__':
    pass
