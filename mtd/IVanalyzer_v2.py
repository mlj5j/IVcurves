from FindVb import findVb
from FindT import findT
from FindIdark import findIdark
import sys
import numpy as np
import ROOT

class sipm:
    def __init__(self, SN, dose, IVfilelist, Tfilelist):
        self.SN = SN #SiPM serial number from HPK
        self.dose = dose
        self.IVfilelist = IVfilelist  #Text file that contains list of IV curve data filenames
        self.Tfilelist = Tfilelist  #Text file that contains list of thermistor data filenames
        self.graph = ROOT.TGraphErrors()
        self.Vb_T = ROOT.TF1('Vb_T','pol1')
        self.DCRgraph = ROOT.TGraphErrors()
        self.DCRmgraph = ROOT.TMultiGraph()
        
    def makeGraph(self):
        Vb = []
        T = [1.0,1.0]
        self.graph.SetTitle(self.SN)
        self.graph.GetXaxis().SetTitle('Temperature (C)')
        self.graph.GetYaxis().SetTitle('Breakdown Voltage (V)')
        f = open(self.IVfilelist,'r')
        i=0
        for line in f:
            Vb.append(findVb(line.strip()))
        fT = open(self.Tfilelist,'r')
        for line in fT:
            T = findT(line.strip())
            self.graph.SetPoint(i, T[0], Vb[i])
            self.graph.SetPointError(i, T[1], 0.05)
            i+=1
        self.graph.Fit(self.Vb_T)

    def getDCR(self, OV):
        testgraph = ROOT.TGraphErrors()
        testgraph.SetTitle(self.SN)
        testgraph.GetXaxis().SetTitle('Temperature (C)')
        testgraph.GetYaxis().SetTitle('Dark current (A)')
        self.DCRgraph.SetTitle(self.SN)
        self.DCRgraph.GetXaxis().SetTitle('Temperature (C)')
        self.DCRgraph.GetYaxis().SetTitle('Dark current (A)')
        Idark = []
        V = []
        T = []
        T_sigma = []
        Tdata = [1.0,1.0]
        i = 0
        fT = open(self.Tfilelist,'r')
        for line in fT:
            Tdata = findT(line.strip())
            T.append(Tdata[0])
            T_sigma.append(Tdata[1])
            V.append((round(2*(OV + self.Vb_T.Eval(Tdata[0],0,0,0))))/2)
        f = open(self.IVfilelist,'r')
        for line in f:
#            self.DCRgraph.append(ROOT.TGraphErrors())
            Idark.append(findIdark(line.strip(),V[i]))
            self.DCRgraph.SetPoint(i,T[i], Idark[i])
            testgraph.SetPoint(i,T[i], Idark[i])
            testgraph.SetPointError(i, T_sigma[i], 0.1*Idark[i])
            self.DCRgraph.SetPointError(i, T_sigma[i], 0.1*Idark[i])
            i += 1
        return testgraph
            
def darkplot(sipm,OVa):
    glist = []
    mg = ROOT.TMultiGraph()
    mg.SetTitle('Temperature vs Dark Current; Temperature (C); Dark Current (A)') 
    for v in OVa:
        glist.append(sipm.getDCR(v))

    for i in range(len(glist)):
        glist[i].SetMarkerColor(i+1)
        glist[i].SetLineColor(i+1)
        mg.Add(glist[i])
    return mg
        

    
quiet = 1


#make sipm objects
s5 = sipm('HPK_2940','1E13', 'HPK_2940_IVfilelist.txt', 'HPK_2940_Tfilelist.txt')
s3 = sipm('HPK_2938','1E12','HPK_2938_IVfilelist.txt', 'HPK_2938_Tfilelist.txt')
s1 = sipm('HPK_2898','0.0', 'HPK_2898_IVfilelist.txt', 'HPK_2898_Tfilelist.txt')

s6 = sipm('HPK_2941', '1E13', 'HPK_2941_IVfilelist.txt', 'HPK_2941_Tfilelist.txt')
s4 = sipm('HPK_2939','1E12', 'HPK_2939_IVfilelist.txt', 'HPK_2939_Tfilelist.txt')
s2 = sipm('HPK_2914', '0.0', 'HPK_2914_IVfilelist.txt', 'HPK_2914_Tfilelist.txt')

s7 = sipm('HPK_2890', '0.0', 'HPK_2890_IVfilelist.txt', 'HPK_2890_Tfilelist.txt')
s8 = sipm('HPK_2915', '0.0', 'HPK_2915_IVfilelist.txt', 'HPK_2915_Tfilelist.txt')
s9 = sipm('HPK_2917', '0.0', 'HPK_2917_IVfilelist.txt', 'HPK_2917_Tfilelist.txt')

ROOT.gStyle.SetOptFit()

s5.makeGraph()
s3.makeGraph()
s1.makeGraph()

s2.makeGraph()
s4.makeGraph()
s6.makeGraph()

s7.makeGraph()
s8.makeGraph()
s9.makeGraph()


OV = [1.0, 2.0, 3.0, 4.0]
g6 = []
g6.append(s6.getDCR(1.0))
g6.append(s6.getDCR(2.0))
g6.append(s6.getDCR(3.0))

for i in range(len(g6)):
    g6[i].SetMarkerColor(i+1)
    g6[i-1].SetLineColor(i+1)
    s6.DCRmgraph.Add(g6[i])
    
ctest = ROOT.TCanvas('ctest', 'ctest', 500, 500)
s6.DCRmgraph.Draw('Aep')

mg6 = darkplot(s4,OV)
c12 = ROOT.TCanvas('c12','c12', 500, 500)
mg6.Draw('Aep')
#findT returns T[0]=mean temp and T[1]=error on mean


#Make canvas and draw
if quiet==0:
    c9 = ROOT.TCanvas('c9', 'c9', 500, 500)
    s9.graph.Draw('Aep')

    c8 = ROOT.TCanvas('c8', 'c8', 500,500)
    s8.graph.Draw('Aep')

    c7 = ROOT.TCanvas('c7', 'c7', 500, 500)
    s7.graph.Draw('Aep')

    c6 = ROOT.TCanvas('c6', 'c6', 500, 500)
    s6.graph.Draw('Aep')

    c5 = ROOT.TCanvas('c5', 'c5', 500,500)
    s5.graph.Draw('Aep')

    c4 = ROOT.TCanvas('c4', 'c4', 500, 500)
    s4.graph.Draw('Aep')

    c3 = ROOT.TCanvas('c3', 'c3', 500, 500)
    s3.graph.Draw('Aep')

    c2 = ROOT.TCanvas('c2', 'c2', 500, 500)
    s2.graph.Draw('Aep')

    c1 = ROOT.TCanvas('c1', 'c1', 500, 500)
    s1.graph.Draw('Aep')


sys.stdin.readline()
