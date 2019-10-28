from FindVb import findVb
from FindT import findT
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
        self.graph.Fit('pol1')
    
#make sipm objects
s5 = sipm('HPK_2940','1E13', 'HPK_2940_IVfilelist.txt', 'HPK_2940_Tfilelist.txt')
s3 = sipm('HPK_2938','1E12','HPK_2938_IVfilelist.txt', 'HPK_2938_Tfilelist.txt')
s1 = sipm('HPK_2898','0.0', 'HPK_2898_IVfilelist.txt', 'HPK_2898_Tfilelist.txt')

#s6 = sipm('HPK_2941', '1E13', 'HPK_2941_IVfilelist.txt', 'HPK_2941_Tfilelist.txt')
#s4 = sipm('HPK_2939','1E12', 'HPK_2939_IVfilelist.txt', 'HPK_2939_Tfilelist.txt')
#s2 = sipm('HPK_2914', '0.0', 'HPK_2914_IVfilelist.txt', 'HPK_2914_Tfilelist.txt')

ROOT.gStyle.SetOptFit()

s5.makeGraph()
s3.makeGraph()
s1.makeGraph()

#s2.makeGraph()
#s4.makeGraph()
#s6.makeGraph()

#findT returns T[0]=mean temp and T[1]=error on mean


#Make canvas and draw
#c6 = ROOT.TCanvas('c6', 'c6', 500, 500)
#s6.graph.Draw('Aep')

c5 = ROOT.TCanvas('c5', 'c5', 500,500)
s5.graph.Draw('Aep')

#c4 = ROOT.TCanvas('c4', 'c4', 500, 500)
#s4.graph.Draw('Aep')

c3 = ROOT.TCanvas('c3', 'c3', 500, 500)
s3.graph.Draw('Aep')

#c2 = ROOT.TCanvas('c2', 'c2', 500, 500)
#s2.graph.Draw('Aep')

c1 = ROOT.TCanvas('c1', 'c1', 500, 500)
s1.graph.Draw('Aep')

sys.stdin.readline()
