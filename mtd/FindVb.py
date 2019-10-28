import numpy as np
import ROOT
import sys
import argparse
import array

def findVb(IVfile):
    xpos = np.zeros(1,dtype=float)
    voltage = np.zeros(1,dtype=float)
    current = np.zeros(1,dtype=float)

    print "Now processing " + IVfile
    f1 = open(IVfile,'r')
    gr = ROOT.TGraph()


    gr.SetLineColor(2)

    grs = ROOT.TGraph()
    grlog = ROOT.TGraph()

    i=0
    for line in f1:
        thing = line
        data = thing.strip().split(',')
        voltage[0] = float(data[0])
        current[0] = float(data[1])
        gr.SetPoint(i,voltage[0],ROOT.TMath.Abs(current[0]))
        i = i+1


    gs = ROOT.TGraphSmooth("normal")
    grs = gs.SmoothSuper(gr,"",0,0)
    N = grs.GetN()
    gd = ROOT.TGraph() 
    #hprof = ROOT.TProfile("hprof", "hprof", 1460, 0, 73, -10, 10)
    hprof = ROOT.TProfile("hprof", 'hprof', 1400, 0, 70, -10, 10)
    peaks = ROOT.TSpectrum(1)

    ax = ROOT.Double()
    ay = ROOT.Double()

    x=[]
    y=[]
    dydx = []
    for j in range(N):
        grs.GetPoint(j,ax,ay)
        x.append(float(ax))
        y.append(ROOT.TMath.Log(ROOT.TMath.Abs(ay)))

    for j in range(1,N):
    
        dydx.append((y[j]-y[j-1])/(x[j]-x[j-1]))
        gd.SetPoint(j-1,x[j],dydx[j-1])
        hprof.Fill(x[j], dydx[j-1])

    Npeaks = peaks.Search(hprof, 2, "", 0.05)
        
    xpos = peaks.GetPositionX()
    s1 = "Breakdown = {}".format(xpos[0])
    print s1
    hprof.SetTitle(s1)
#    c1 = ROOT.TCanvas('c1', 'c1',500,500)
#    ROOT.gPad.SetLogy()
#    gr.Draw("Al")
#    grs.Draw("lsame")

    
#    c3 = ROOT.TCanvas('c3', 'c3', 500,500)
#    hprof.Draw("l")

    return xpos[0]
    
