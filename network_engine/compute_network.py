

STEP = 1
HISTORIAL_NUMBER_OF_ROWS = 14

import pandas as pd
import numpy as np

def build (df_close):
    correlations = []
    correlation_means=[]
    correlation_std=[]
#    dates = pd.date_range('20130101', periods=30)
#    df_close = pd.DataFrame(np.random.randn(30,4), index=dates, columns=list('ABCD'))
    import ipdb; ipdb.set_trace()

    for i in range(0, df_close.shape[0] - HISTORIAL_NUMBER_OF_ROWS):
        subdf = df_close.ix[i:i+HISTORIAL_NUMBER_OF_ROWS, :]
        graph = np.corrcoef(subdf.fillna(0))
        correlations.append(graph)
        correlation_means.append(np.mean(graph))
        correlation_std.append(np.std(graph))

    #for n in range(1,10,STEP):

        #R.append(np.corrcoef([dt_close.ix[n:n+HISTORIAL_NUMBER_OF_ROWS][col] for col in dt_close.columns]))
#        meanR.append(np.mean(R))
#        stdR.append(np.std(R))
    import ipdb; ipdb.set_trace()
    return correlation_means, correlation_std



if __name__ == '__main__':
    pass
