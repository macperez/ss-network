

STEP = 1
HISTORIAL_NUMBER_OF_ROWS = 15

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def build (df_close):
    correlations = []
    correlation_means=[]
    correlation_std=[]
#    dates = pd.date_range('20130101', periods=30)
#    df_close = pd.DataFrame(np.random.randn(30,4), index=dates, columns=list('ABCD'))
#    import ipdb; ipdb.set_trace()

    for i in range(0, df_close.shape[0] - HISTORIAL_NUMBER_OF_ROWS):
        subdf = df_close.ix[i:i+HISTORIAL_NUMBER_OF_ROWS, :]
        graph = np.corrcoef(np.triu(subdf.fillna(0)))
        #graph = np.corrcoef(np.triu(np.diff(np.log(subdf.fillna(0)))))
        correlations.append(graph)
        correlation_means.append(np.mean(graph))
        correlation_std.append(np.std(graph))

    #for n in range(1,10,STEP):
    print(correlation_means)
    plt.plot(correlation_means)
    plt.plot(correlation_std)
    plt.show()
#    import ipdb; ipdb.set_trace()
    return #correlation_means, correlation_std



if __name__ == '__main__':
    pass
