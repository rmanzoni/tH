from ROOT import TFile, gDirectory, TH1F, TLegend, TCanvas, gStyle, TPad, TLine, gROOT, TTree, THStack
import math, copy, sys
from array import array
from CMGTools.RootTools.DataMC.DataMCPlot import DataMCPlot
from CMGTools.H2TauTau.proto.plotter.officialStyle import officialStyle
from CMGTools.RootTools.Style import *
from CMGTools.H2TauTau.proto.plotter.rootutils import *
import config as tool
import optparse

#pname = {'WZ':0, 'ZZ':1, 'tt1l':2, 'tt2l':3, 'tH_YtMinus1':4,'data':5};
pname = {'WZ':0, 'ZZ':1, 'tt1l':2, 'tt2l':3, 'tH_YtMinus1':4, 'TTH':5, 'TTW':6, 'TTZ':7, 'data':8};
#pname = {'WZ':0, 'ZZ':1, 'data':2}

region  = {'signal':0, 'antiE':1, 'antiMu':2, 'antiEMu':3};


gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0);


def createStackHistogram(hist, hist_kNN, name):
    h = DataMCPlot(name)

    flag_ttbar = False
    tot = 0
    
    for iprocess, pval in sorted(pname.items()):

        if iprocess!='data':
            h.AddHistogram(iprocess,
                           hist[region['signal']][pval], pval)

            if iprocess=='tt1l' or iprocess=='tt2l':
                flag_ttbar = True
                tot += hist[region['signal']][pval].GetSumOfWeights()
                
#    print 'ttbar=', tot
    h.Group('WZ+ZZ', ['WZ','ZZ'])

    print flag_ttbar
    if flag_ttbar:
        h.Group('ttbar', ['tt1l','tt2l'])


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
        print Ndata, 'out of ', Nmc, 'has passed. SF = ', sf, ikey
        hist_kNN[ival][pname['data']].Scale(sf)

    h_rbkg = hist_kNN[region['antiE']][pname['data']]
    h_rbkg.Add(hist_kNN[region['antiMu']][pname['data']])
    h_rbkg.Add(hist_kNN[region['antiEMu']][pname['data']],-1)


#    h_rbkg.SetMaximum(15.7)
#    hist[region['signal']][pname['data']].SetMaximum(15.7)
#    print 'antiE =  ', hist_kNN[region['antiE']][pname['data']].GetSumOfWeights()
#    print 'antiMu = ', hist_kNN[region['antiMu']][pname['data']].GetSumOfWeights()
#    print 'antiE + antiMu = ', hist_kNN[region['antiEMu']][pname['data']].GetSumOfWeights()


    print 'Reducible bkg estimation = ', h_rbkg.GetSumOfWeights()
    print 'ttbar estimation = ', tot
    
    tool.DecoHist('Reducible', h_rbkg, '','')
    h.AddHistogram('Reducible', h_rbkg, 3)
    h.AddHistogram('data', hist[region['signal']][pname['data']], 2999)
    

#    if flag_ttbar:
#        h.Hist('ttbar').NormalizeToBinWidth()

#    h.Hist('data').NormalizeToBinWidth()
#    h.Hist('WZ+ZZ').NormalizeToBinWidth()
#    h.Hist('Reducible').NormalizeToBinWidth()
#    print h.Hist('ttbar').Print()
    h.Hist('data').stack = False
    print name, 'has been registered'
    return h


def draw(h1, h2, name):
    can = TCanvas('c'+name)
    hstack = createStackHistogram(h1, h2, name)
#    hstack.DrawStack('HIST',None, None, None, 15.7)
    hstack.DrawStack('HIST')
    can.SaveAs('figure/' + options.cr + '_'+name+'.png')


### For options
parser = optparse.OptionParser()
parser.add_option('--cr', action="store", dest="cr", default='f12')
options, args = parser.parse_args()


print 'control region = ', options.cr


file = TFile('Plot_' + options.cr + '_kNN50.root')

h_M     = [[0 for ii in range(len(pname))] for i in range(len(region))]
h_kNN_M = [[0 for ii in range(len(pname))] for i in range(len(region))]


for rkey, rval in sorted(region.items()):
    for key, val in sorted(pname.items()):

        hname = 'h_M_' + rkey + '_' + key
        h_M[rval][val] = file.Get(hname)
#        h_M[rval][val].SetMaximum(15.7)
        tool.DecoHist(key, h_M[rval][val], tool.ldict['submass_x'], tool.ldict['submass_y'])
    
        hname = 'h_kNN_M_' + rkey + '_' + key
        h_kNN_M[rval][val] = file.Get(hname)
#        h_kNN_M[rval][val].SetMaximum(15.7)

### Draw
draw(h_M, h_kNN_M, 'h_mass')


