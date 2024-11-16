from sklearn.metrics import f1_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import re
import ast
def r4(value):
    if isinstance(value, float):
        # If the input is a single float, round it and format it to 4 decimal places
        return f"{round(value, 3):.3f}"
    else:
        value = list(value)
        return [f"{round(v, 3):.3f}" for v in value]

def evaluate(y_test,y_pred, roundd = False, arrayed = False):    
    [pp, pn] = list(precision_recall_fscore_support(y_test, y_pred)[0])
    [rp, rn] = list(precision_recall_fscore_support(y_test, y_pred)[1])
    [fp, fn] = list(precision_recall_fscore_support(y_test, y_pred)[2])
    wf1 = f1_score(y_test, y_pred, average = 'weighted')
    acc = accuracy_score(y_test, y_pred)
    mcc = matthews_corrcoef(y_test, y_pred)
    if roundd:
        [pp, pn] = [r4(pp), r4(pn)]
        [rp, rn] = [r4(rp), r4(rn)]
        [fp, fn] = [r4(fp), r4(fn)]
        wf1 = r4(wf1)
        acc = r4(acc)
        mcc = r4(mcc)
    if arrayed:
        return [pp, pn, rp, rn, fp, fn, wf1, acc, mcc]
    
    return {'P+-': [pp, pn],\
            'R+-': [rp, rn],\
            'f1s': [fp, fn],\
            'wf1': wf1,\
            'ACC': acc,\
            'MCC': mcc}