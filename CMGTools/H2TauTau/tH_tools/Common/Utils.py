import os
import math
import array

import ROOT

def take_sample(folder, method, sample, region, tree_name = 'Tree') :
  '''
  Returns the tree for the given sample in the given (fake) region
  
  folder : /afs/cern.ch/work/m/manzoni/public/tH_ntuple/antiIsolatedTau
  method : f12, f13
  sample : tt2l, tt1l, tH_YtMinus1, data, ZZ, WZ, TTZ, TTW, TTH
  region : signal, antiE, antiMu, antiEMu
  tree_name : Tree (Default)
  '''
  file_name = folder+'_'.join([method, region ,sample])+'.root'
  file = ROOT.TFile.Open(file_name)
  file.cd()
  tree = ROOT.gDirectory.FindObjectAny(tree_name)
    
  return tree

