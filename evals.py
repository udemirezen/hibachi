#!/usr/bin/env python
#==============================================================================
#
#          FILE:  evals.py
# 
#         USAGE:  import evals (from hib.py)
# 
#   DESCRIPTION:  evaluation routines
# 
#       UPDATES:  170339: removed shuffle from getfolds()
#                 170410: added reclass()
#        AUTHOR:  Pete Schmitt (hershey), pschmitt@upenn.edu
#       COMPANY:  University of Pennsylvania
#       VERSION:  0.1.2
#       CREATED:  Sun Mar 19 11:34:09 EDT 2017
#      REVISION:  Mon Apr 10 16:17:29 CDT 2017
#==============================================================================
import numpy as np
import pandas as pd
###############################################################################
def subsets(x,percent):
    """ take a subset of "percent" of x """
    p = percent / 100
    xa = np.array(x)
    subsample_indices = np.random.choice(xa.shape[1], int(xa.shape[1] * p), 
                                         replace=False)
    return (xa[:, subsample_indices]).tolist()
###############################################################################
def getfolds(x, num):
    """ return num folds of size 1/num'th of x """
    folds = []
    fsize = end = int(len(x[0]) / num)
    xa = np.array(x)
    start = 0
    for i in range(num):
        folds.append(xa[:,start:end])
        start += fsize
        end += fsize  
    return folds
###############################################################################
def addnoise(x,pcnt):
    """ add some percentage of noise to data """
    xa = np.array(x)
    val = pcnt/100
    rep = {}
    rep[0] = [1,2]
    rep[1] = [0,2]
    rep[2] = [0,1]

    for i in range(len(xa)):
        indices = np.random.choice(xa.shape[1], int(xa.shape[1] * val), 
                                   replace=False)
        for j in list(indices):
            xa[i][j] = np.random.choice(rep[xa[i][j]])

    return xa.tolist()
###############################################################################
def addnoise1(x,pcnt):
    """ add some percentage of noise to data (for +1 data) """
    xa = np.array(x)
    val = pcnt/100
    rep = {}
    rep[1] = [2,3]
    rep[2] = [1,3]
    rep[3] = [1,2]

    for i in range(len(xa)):
        indices = np.random.choice(xa.shape[1], int(xa.shape[1] * val), 
                                   replace=False)
        for j in list(indices):
            xa[i][j] = np.random.choice(rep[xa[i][j]])

    return xa.tolist()
###############################################################################
def reclass(x, result, pct):
    """ reclassify data """
    d = np.array(x).transpose()
    df = pd.DataFrame(d, columns=['X0','X1','X2'])
    df['Class'] = result
    df.sort_values('Class', ascending=True, inplace=True)
    
    dflen = len(df)
    cntl_cnt = dflen - int(dflen * (pct/100.0))
    df.loc[:cntl_cnt, 'Class'] = 0
    df.loc[cntl_cnt:, 'Class'] = 1
    
    df.sort_index(inplace=True)  # put data back in index order
    return df['Class'].tolist()
