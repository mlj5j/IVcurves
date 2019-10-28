import numpy as np
import ROOT

def findT(fileT):

    lnR = np.zeros(1,dtype=float)
    T = np.zeros(1,dtype=float)
    T_data = [0.0,0.0]
    
    tempMap = ROOT.TF1('tempMap','468.64-83.7475*x+4.95671*x^2-0.119079*x^3',5,14)

    print "Now processing " + fileT
    fT = open(fileT,'r')
    hT = ROOT.TH1F('hT','Temperature (C)',500, -35, 25)

    for lineT in fT:
        thingT = lineT
        dataT = thingT.strip().split(',')
        lnR[0] = ROOT.TMath.Log(float(dataT[1]))
        T[0] = tempMap(lnR[0])
        hT.Fill(T[0])

#    c2 = ROOT.TCanvas('c2', 'c2', 500,500)
#    hT.Draw()
    T_data[0] = hT.GetMean(1)
    T_data[1] = hT.GetMeanError(1)
    return T_data

