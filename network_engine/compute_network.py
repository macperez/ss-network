

STEP = 2
HISTORIAL_NUMBER_OF_ROWS = 14
import pandas as pd
import numpy as np
def build (dt_close):
    todas=[]
    for n in range(1,10,STEP):
        R.append(np.corrcoef([dt_close.ix[n:n+HISTORIAL_NUMBER_OF_ROWS][col] for col in dt_close.columns]))


    meanH=np.mean(triu(H))
    stdH=np.std(triu(H))
    return todas
