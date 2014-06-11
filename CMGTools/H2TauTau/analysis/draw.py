from ROOT import TFile, gDirectory, TH1F, TLegend, TCanvas, gStyle, TPad, TLine, gROOT, TTree, THStack
import math, copy, sys
from array import array
from CMGTools.RootTools.DataMC.DataMCPlot import DataMCPlot
from CMGTools.H2TauTau.proto.plotter.officialStyle import officialStyle
from CMGTools.RootTools.Style import *
from CMGTools.H2TauTau.proto.plotter.rootutils import *
import config as tool
import optparse

#pname = {'WZ':0, 'ZZ':1, 'tt1l':2, 'tt2l':3, 'tH_YtMinus1':4, 'data':5};
pname = {'WZ':0, 'ZZ':1, 'tt1l':2, 'tt2l':3, 'TTW':4, 'TTZ':5, 'tH_YtMinus1':6, 'TTH':7,  'data':8};
region  = {'signal':0, 'antiE':1, 'antiMu':2, 'antiEMu':3};

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)

def returnMax(h):
    max = 0

    for ibin in range(1, h.GetNbinsX()+1):
        if max < h.GetBinContent(ibin) + h.GetBinError(ibin):
            max = h.GetBinContent(ibin) + h.GetBinError(ibin)

    return max
        
def createStackHistogram(hist, hist_kNN, name):
    h = DataMCPlot(name)

    flag_ttbar = False
   
    for iprocess, pval in sorted(pname.items()):

        if iprocess!='data':
            h.AddHistogram(iprocess,
                           hist[region['signal']][pval], pval)

            if iprocess=='tt1l' or iprocess=='tt2l':
                flag_ttbar = True
                
    h.Group('WZ+ZZ', ['WZ','ZZ'])
    h.Group('t#bar{t}Z, t#bar{t}W', ['TTW','TTZ'])

    if flag_ttbar:
        h.Group('t#bar{t}', ['tt1l','tt2l'])

    for ikey, ival in sorted(region.items()):
        if ikey=='signal':
            continue

        Nmc = 0
        Ndata = 0
        for iprocess, pval in sorted(pname.items()):

            if iprocess=='data':
                Ndata = hist[ival][pval].GetSumOfWeights()
            else:
                Nmc += hist[ival][pval].GetSumOfWeights()

        sf = (Ndata-Nmc)/Ndata
        print ikey, '(Data, MC) = ', Ndata, Nmc, ' SF = ', sf
        hist_kNN[ival][pname['data']].Scale(sf)

    print '---------', name, '----------------'
    print 'antiE   =  ', hist_kNN[region['antiE']][pname['data']].GetSumOfWeights(), hist_kNN[region['antiE']][pname['data']].GetEntries()
    print 'antiMu  = ', hist_kNN[region['antiMu']][pname['data']].GetSumOfWeights(), hist_kNN[region['antiMu']][pname['data']].GetEntries()
    print 'antiEMu = ', hist_kNN[region['antiEMu']][pname['data']].GetSumOfWeights(), hist_kNN[region['antiEMu']][pname['data']].GetEntries()

    h_rbkg = copy.deepcopy(hist_kNN[region['antiE']][pname['data']])
    h_rbkg.Add(hist_kNN[region['antiMu']][pname['data']],1.)
    h_rbkg.Add(hist_kNN[region['antiEMu']][pname['data']],-1.)

    print '--> after'
    print 'antiE   =  ', hist_kNN[region['antiE']][pname['data']].GetSumOfWeights()
    print 'antiMu  = ', hist_kNN[region['antiMu']][pname['data']].GetSumOfWeights()
    print 'antiEMu = ', hist_kNN[region['antiEMu']][pname['data']].GetSumOfWeights()
    print 'Red. = ', h_rbkg.GetSumOfWeights()
    
    print 'Reducible bkg estimation = ', h_rbkg.GetSumOfWeights()
#    print 'ttbar estimation = ', tot
    
    tool.DecoHist('Reducible', h_rbkg, '','')
    h.AddHistogram('Reducible', h_rbkg, 3)
    h.AddHistogram('data', hist[region['signal']][pname['data']], 2999)

    print h

#    h.Hist('data').NormalizeToBinWidth()
#    h.Hist('WZ+ZZ').NormalizeToBinWidth()
#    h.Hist('Reducible').NormalizeToBinWidth()
#    print h.Hist('ttbar').Print()
    h.Hist('data').stack = False

    return h


def createHistogram(hist, hist_kNN, name):
    h_total_bkg = copy.deepcopy(hist[region['signal']][pname['data']])
    
    print 'check1', h_total_bkg.GetSumOfWeights()

    for iprocess, pval in sorted(pname.items()):

        if iprocess!='data' and iprocess!='tH_YtMinus1':
            h_total_bkg.Add(hist[region['signal']][pval], 1.)
            print 'check2', iprocess, h_total_bkg.GetSumOfWeights()

    h_total_bkg.Add(hist[region['signal']][pname['data']],-1.)
    print 'check3', h_total_bkg.GetSumOfWeights()
    
    for ikey, ival in sorted(region.items()):
        if ikey=='signal':
            continue

        Nmc = 0
        Ndata = 0
        for iprocess, pval in sorted(pname.items()):

            if iprocess=='data':
                Ndata = hist[ival][pval].GetSumOfWeights()
            else:
                Nmc += hist[ival][pval].GetSumOfWeights()

        sf = (Ndata-Nmc)/Ndata
        print Nmc, 'is MC out of Ndata = ', Ndata, ' SF = ', sf, ikey, '(', ival, ')'
        hist_kNN[ival][pname['data']].Scale(sf)

    print '---------', name, '----------------'
    print 'antiE   =  ', hist_kNN[region['antiE']][pname['data']].GetSumOfWeights(), hist_kNN[region['antiE']][pname['data']].GetEntries()
    print 'antiMu  = ', hist_kNN[region['antiMu']][pname['data']].GetSumOfWeights(), hist_kNN[region['antiMu']][pname['data']].GetEntries()
    print 'antiEMu = ', hist_kNN[region['antiEMu']][pname['data']].GetSumOfWeights(), hist_kNN[region['antiEMu']][pname['data']].GetEntries()

    h_total_bkg.Add(hist_kNN[region['antiE']][pname['data']],1.)
    print 'check4', h_total_bkg.GetSumOfWeights()
    h_total_bkg.Add(hist_kNN[region['antiMu']][pname['data']],1.)
    print 'check5', h_total_bkg.GetSumOfWeights()
    h_total_bkg.Add(hist_kNN[region['antiEMu']][pname['data']],-1.)
    print 'check6', h_total_bkg.GetSumOfWeights()
    
    h_signal = hist[region['signal']][pname['tH_YtMinus1']]
    
    return h_signal, h_total_bkg



def draw(h1, h2, name):
    can = TCanvas('c'+name)
    hstack = createStackHistogram(h1, h2, name)
    hstack.DrawStack('HIST')
    can.SaveAs('figure/' + options.cr + '_'+name+'.png')


def compare(h1, h2, name):
    can = TCanvas('c_compare_'+name)
    h_sig, h_bkg = createHistogram(h1, h2, name)

    h_sig.SetLineColor(kRed)
    h_sig.SetMarkerColor(kRed)
    h_sig.SetLineWidth(3)
    h_bkg.SetLineWidth(2)
    h_sig.Scale(1./h_sig.GetSumOfWeights())
    h_bkg.Scale(1./h_bkg.GetSumOfWeights())

    e_sig = returnMax(h_sig)
    e_bkg = returnMax(h_bkg)
    if e_sig > e_bkg:
        h_sig.SetMaximum(e_sig*1.2)
        h_bkg.SetMaximum(e_sig*1.2)

    if e_sig < e_bkg:
        h_sig.SetMaximum(e_bkg*1.2)
        h_bkg.SetMaximum(e_bkg*1.2)

    h_sig.SetMinimum(0.)
    h_sig.Draw()
    h_bkg.Draw('same')
#    h_sig.DrawNormalized()
#    h_bkg.DrawNormalized('elsame')

    legend = TLegend(0.63,0.65,0.9,0.9)
    tool.LegendSettings(legend)
    legend.AddEntry(h_sig, 'signal', 'lep')
    legend.AddEntry(h_bkg, 'background', 'lep')
    legend.Draw()
    can.SaveAs('figure/' + options.cr + '_'+name+'_normalized.png')
#pname = {'WZ':0, 'ZZ':1, 'tt1l':2, 'tt2l':3, 'tH_YtMinus1':4, 'data':5};
#region  = {'signal':0, 'antiE':1, 'antiMu':2, 'antiEMu':3};





### For options
parser = optparse.OptionParser()
parser.add_option('--cr', action="store", dest="cr", default='f12')
options, args = parser.parse_args()


print 'control region = ', options.cr


file = TFile('Plot_' + options.cr + '_kNN50.root')

h_M     = [[0 for ii in range(len(pname))] for i in range(len(region))]
h_kNN_M = [[0 for ii in range(len(pname))] for i in range(len(region))]

h_nbjet     = [[0 for ii in range(len(pname))] for i in range(len(region))]
h_kNN_nbjet = [[0 for ii in range(len(pname))] for i in range(len(region))]

h_njet     = [[0 for ii in range(len(pname))] for i in range(len(region))]
h_kNN_njet = [[0 for ii in range(len(pname))] for i in range(len(region))]

h_njet30     = [[0 for ii in range(len(pname))] for i in range(len(region))]
h_kNN_njet30 = [[0 for ii in range(len(pname))] for i in range(len(region))]

h_jet_eta     = [[0 for ii in range(len(pname))] for i in range(len(region))]
h_kNN_jet_eta = [[0 for ii in range(len(pname))] for i in range(len(region))]

h_jet_eta30     = [[0 for ii in range(len(pname))] for i in range(len(region))]
h_kNN_jet_eta30 = [[0 for ii in range(len(pname))] for i in range(len(region))]

# Muon-related variables :

h_muon_eta     = [[0 for ii in range(len(pname))] for i in range(len(region))]
h_kNN_muon_eta = [[0 for ii in range(len(pname))] for i in range(len(region))]

h_muon_phi     = [[0 for ii in range(len(pname))] for i in range(len(region))]
h_kNN_muon_phi = [[0 for ii in range(len(pname))] for i in range(len(region))]

h_muon_pt     = [[0 for ii in range(len(pname))] for i in range(len(region))]
h_kNN_muon_pt = [[0 for ii in range(len(pname))] for i in range(len(region))]

h_muon_MT     = [[0 for ii in range(len(pname))] for i in range(len(region))]
h_kNN_muon_MT = [[0 for ii in range(len(pname))] for i in range(len(region))]


# electron-related variables :

h_electron_eta     = [[0 for ii in range(len(pname))] for i in range(len(region))]
h_kNN_electron_eta = [[0 for ii in range(len(pname))] for i in range(len(region))]

h_electron_phi     = [[0 for ii in range(len(pname))] for i in range(len(region))]
h_kNN_electron_phi = [[0 for ii in range(len(pname))] for i in range(len(region))]

h_electron_pt     = [[0 for ii in range(len(pname))] for i in range(len(region))]
h_kNN_electron_pt = [[0 for ii in range(len(pname))] for i in range(len(region))]

h_electron_MT     = [[0 for ii in range(len(pname))] for i in range(len(region))]
h_kNN_electron_MT = [[0 for ii in range(len(pname))] for i in range(len(region))]


# tau-related variables :

h_tau_eta     = [[0 for ii in range(len(pname))] for i in range(len(region))]
h_kNN_tau_eta = [[0 for ii in range(len(pname))] for i in range(len(region))]

h_tau_phi     = [[0 for ii in range(len(pname))] for i in range(len(region))]
h_kNN_tau_phi = [[0 for ii in range(len(pname))] for i in range(len(region))]

h_tau_pt     = [[0 for ii in range(len(pname))] for i in range(len(region))]
h_kNN_tau_pt = [[0 for ii in range(len(pname))] for i in range(len(region))]

h_tau_MT     = [[0 for ii in range(len(pname))] for i in range(len(region))]
h_kNN_tau_MT = [[0 for ii in range(len(pname))] for i in range(len(region))]


for rkey, rval in sorted(region.items()):
    for key, val in sorted(pname.items()):

        hname = 'h_M_' + rkey + '_' + key
        h_M[rval][val] = file.Get(hname)

        print h_M[rval][val]

#        tool.DecoHist(key, h_M[rval][val], 'M(l2,tau)', 'Events')
        tool.DecoHist(key, h_M[rval][val], tool.ldict['submass_x'], tool.ldict['submass_y'])
   
        hname = 'h_kNN_M_' + rkey + '_' + key
        h_kNN_M[rval][val] = file.Get(hname)

        hname = 'h_nbjet_' + rkey + '_' + key
        h_nbjet[rval][val] = file.Get(hname)
        tool.DecoHist(key, h_nbjet[rval][val], 'nbjet', 'Events')
   
        hname = 'h_kNN_nbjet_' + rkey + '_' + key
        h_kNN_nbjet[rval][val] = file.Get(hname)

        hname = 'h_njet_' + rkey + '_' + key
        h_njet[rval][val] = file.Get(hname)
        tool.DecoHist(key, h_njet[rval][val], 'njet', 'Events')
           
        hname = 'h_kNN_njet_' + rkey + '_' + key
        h_kNN_njet[rval][val] = file.Get(hname)

        hname = 'h_njet30_' + rkey + '_' + key
        h_njet30[rval][val] = file.Get(hname)
        tool.DecoHist(key, h_njet30[rval][val], 'njet (pT 30)', 'Events')
           
        hname = 'h_kNN_njet30_' + rkey + '_' + key
        h_kNN_njet30[rval][val] = file.Get(hname)


        hname = 'h_jet_eta_' + rkey + '_' + key
        h_jet_eta[rval][val] = file.Get(hname)
        tool.DecoHist(key, h_jet_eta[rval][val], 'jet eta of max. #eta jet', 'Events')
           
        hname = 'h_kNN_jet_eta_' + rkey + '_' + key
        h_kNN_jet_eta[rval][val] = file.Get(hname)

        hname = 'h_jet_eta30_' + rkey + '_' + key
        h_jet_eta30[rval][val] = file.Get(hname)
        tool.DecoHist(key, h_jet_eta30[rval][val], 'jet eta of max. #eta jet (pT 30)', 'Events')
           
        hname = 'h_kNN_jet_eta30_' + rkey + '_' + key
        h_kNN_jet_eta30[rval][val] = file.Get(hname)


        hname = 'h_muon_eta_' + rkey + '_' + key
        h_muon_eta[rval][val] = file.Get(hname)
        tool.DecoHist(key, h_muon_eta[rval][val], 'muon eta', 'Events')
           
        hname = 'h_kNN_muon_eta_' + rkey + '_' + key
        h_kNN_muon_eta[rval][val] = file.Get(hname)

        hname = 'h_muon_phi_' + rkey + '_' + key
        h_muon_phi[rval][val] = file.Get(hname)
        tool.DecoHist(key, h_muon_phi[rval][val], 'muon phi', 'Events')
           
        hname = 'h_kNN_muon_phi_' + rkey + '_' + key
        h_kNN_muon_phi[rval][val] = file.Get(hname)

        hname = 'h_muon_pt_' + rkey + '_' + key
        h_muon_pt[rval][val] = file.Get(hname)
        tool.DecoHist(key, h_muon_pt[rval][val], 'muon pt', 'Events')
           
        hname = 'h_kNN_muon_pt_' + rkey + '_' + key
        h_kNN_muon_pt[rval][val] = file.Get(hname)

        hname = 'h_muon_MT_' + rkey + '_' + key
        h_muon_MT[rval][val] = file.Get(hname)
        tool.DecoHist(key, h_muon_MT[rval][val], 'muon MT', 'Events')
           
        hname = 'h_kNN_muon_MT_' + rkey + '_' + key
        h_kNN_muon_MT[rval][val] = file.Get(hname)



        hname = 'h_electron_eta_' + rkey + '_' + key
        h_electron_eta[rval][val] = file.Get(hname)
        tool.DecoHist(key, h_electron_eta[rval][val], 'electron eta', 'Events')
           
        hname = 'h_kNN_electron_eta_' + rkey + '_' + key
        h_kNN_electron_eta[rval][val] = file.Get(hname)
        
        hname = 'h_electron_phi_' + rkey + '_' + key
        h_electron_phi[rval][val] = file.Get(hname)
        tool.DecoHist(key, h_electron_phi[rval][val], 'electron phi', 'Events')
           
        hname = 'h_kNN_electron_phi_' + rkey + '_' + key
        h_kNN_electron_phi[rval][val] = file.Get(hname)

        hname = 'h_electron_pt_' + rkey + '_' + key
        h_electron_pt[rval][val] = file.Get(hname)
        tool.DecoHist(key, h_electron_pt[rval][val], 'electron pt', 'Events')
           
        hname = 'h_kNN_electron_pt_' + rkey + '_' + key
        h_kNN_electron_pt[rval][val] = file.Get(hname)

        hname = 'h_electron_MT_' + rkey + '_' + key
        h_electron_MT[rval][val] = file.Get(hname)
        tool.DecoHist(key, h_electron_MT[rval][val], 'electron MT', 'Events')
        
        hname = 'h_kNN_electron_MT_' + rkey + '_' + key
        h_kNN_electron_MT[rval][val] = file.Get(hname)


        hname = 'h_tau_eta_' + rkey + '_' + key
        h_tau_eta[rval][val] = file.Get(hname)
        tool.DecoHist(key, h_tau_eta[rval][val], 'tau eta', 'Events')
           
        hname = 'h_kNN_tau_eta_' + rkey + '_' + key
        h_kNN_tau_eta[rval][val] = file.Get(hname)
        
        hname = 'h_tau_phi_' + rkey + '_' + key
        h_tau_phi[rval][val] = file.Get(hname)
        tool.DecoHist(key, h_tau_phi[rval][val], 'tau phi', 'Events')
           
        hname = 'h_kNN_tau_phi_' + rkey + '_' + key
        h_kNN_tau_phi[rval][val] = file.Get(hname)

        hname = 'h_tau_pt_' + rkey + '_' + key
        h_tau_pt[rval][val] = file.Get(hname)
        tool.DecoHist(key, h_tau_pt[rval][val], 'tau pt', 'Events')
           
        hname = 'h_kNN_tau_pt_' + rkey + '_' + key
        h_kNN_tau_pt[rval][val] = file.Get(hname)

        hname = 'h_tau_MT_' + rkey + '_' + key
        h_tau_MT[rval][val] = file.Get(hname)
        tool.DecoHist(key, h_tau_MT[rval][val], 'tau MT', 'Events')
           
        hname = 'h_kNN_tau_MT_' + rkey + '_' + key
        h_kNN_tau_MT[rval][val] = file.Get(hname)



### First, draw purely using MC

draw(h_M, h_kNN_M, 'h_mass')
draw(h_nbjet, h_kNN_nbjet, 'h_nbjet')
draw(h_njet, h_kNN_njet, 'h_njet')
draw(h_njet30, h_kNN_njet30, 'h_njet30')
draw(h_jet_eta, h_kNN_jet_eta, 'h_jet_eta')
draw(h_jet_eta30, h_kNN_jet_eta30, 'h_jet_eta30')

draw(h_muon_eta, h_kNN_muon_eta, 'h_muon_eta')
draw(h_muon_phi, h_kNN_muon_phi, 'h_muon_phi')
draw(h_muon_pt, h_kNN_muon_pt, 'h_muon_pt')
draw(h_muon_MT, h_kNN_muon_MT, 'h_muon_MT')

draw(h_electron_eta, h_kNN_electron_eta, 'h_electron_eta')
draw(h_electron_phi, h_kNN_electron_phi, 'h_electron_phi')
draw(h_electron_pt, h_kNN_electron_pt, 'h_electron_pt')
draw(h_electron_MT, h_kNN_electron_MT, 'h_electron_MT')

draw(h_tau_eta, h_kNN_tau_eta, 'h_tau_eta')
draw(h_tau_phi, h_kNN_tau_phi, 'h_tau_phi')
draw(h_tau_pt, h_kNN_tau_pt, 'h_tau_pt')
draw(h_tau_MT, h_kNN_tau_MT, 'h_tau_MT')
#
#
#
#### Draw
compare(h_M, h_kNN_M, 'h_mass')
compare(h_nbjet, h_kNN_nbjet, 'h_nbjet')
compare(h_njet, h_kNN_njet, 'h_njet')
compare(h_njet30, h_kNN_njet30, 'h_njet30')
compare(h_jet_eta, h_kNN_jet_eta, 'h_jet_eta')
compare(h_jet_eta30, h_kNN_jet_eta30, 'h_jet_eta30')
#
compare(h_muon_eta, h_kNN_muon_eta, 'h_muon_eta')
compare(h_muon_phi, h_kNN_muon_phi, 'h_muon_phi')
compare(h_muon_pt, h_kNN_muon_pt, 'h_muon_pt')
compare(h_muon_MT, h_kNN_muon_MT, 'h_muon_MT')

compare(h_electron_eta, h_kNN_electron_eta, 'h_electron_eta')
compare(h_electron_phi, h_kNN_electron_phi, 'h_electron_phi')
compare(h_electron_pt, h_kNN_electron_pt, 'h_electron_pt')
compare(h_electron_MT, h_kNN_electron_MT, 'h_electron_MT')

compare(h_tau_eta, h_kNN_tau_eta, 'h_tau_eta')
compare(h_tau_phi, h_kNN_tau_phi, 'h_tau_phi')
compare(h_tau_pt, h_kNN_tau_pt, 'h_tau_pt')
compare(h_tau_MT, h_kNN_tau_MT, 'h_tau_MT')
