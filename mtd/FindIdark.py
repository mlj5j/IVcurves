import numpy as np
import ROOT
import sys


def findIdark(IVfile, V):

    voltage = np.zeros(1,dtype=float)
    current = np.zeros(1,dtype=float)

    f1 = open(IVfile,'r')

    for line in f1:
        thing = line
        data = thing.strip().split(',')
        voltage[0] = float(data[0])
        current[0] = float(data[1])
        if voltage[0] == V:
            break

    return current[0]
