import os
import math
import array

import ROOT

class fake_bkg_estimation( object ) :
  '''
  bla bla
  
  folder     : /afs/cern.ch/work/m/manzoni/public/tH_ntuple/antiIsolatedTau/
  method     : f12, f3
  lepton     : electron, muon
  knnfolder  : /afs/cern.ch/work/m/manzoni/public/tH_ntuple/antiIsolatedTau/weights
  MVA_method : KNN (Default)
  '''

  def __init__(self, folder, method, knnfolder, MVA_method = 'KNN') :    

    self.folder_     = folder
    self.method_     = method
    self.knnfolder_  = knnfolder
    self.MVA_method_ = MVA_method
    self.histo_      = ROOT.TH1F('muon_pt','muon_pt',10,0,100)

  
  def take_sample(self, sample, region, tree_name = 'Tree') :
    '''
    Returns the tree for the given sample in the given (fake) region
    
    sample : tt2l, tt1l, tH_YtMinus1, data, ZZ, WZ, TTZ, TTW, TTH
    region : signal, antiE, antiMu, antiEMu
    tree_name : Tree (Default)
    '''
    file_name = self.folder_+'_'.join([self.method_, region ,sample])+'.root'
    file = ROOT.TFile.Open(file_name)
    file.cd()
    tree = ROOT.gDirectory.FindObjectAny(tree_name)
    
    return tree
    
  def book_mva_readers(self, sample) :
    '''
    Books a reader for an already trained MVA regression (weights should be present)
        
    sample : tt2l, tt1l, data, ZZ, WZ
    '''
    file_name_mu  = self.knnfolder_+'_'.join([self.MVA_method_, sample, 'muon'    ,'50'])+'.xml'
    file_name_ele = self.knnfolder_+'_'.join([self.MVA_method_, sample, 'electron','50'])+'.xml'

    self.reader_ = ROOT.TMVA.Reader()

    self.lepton_pt_        = array.array('f',[0]) ; self.reader_.AddVariable('lepton_pt'       , self.lepton_pt_        )
    self.lepton_kNN_jetpt_ = array.array('f',[0]) ; self.reader_.AddVariable('lepton_kNN_jetpt', self.lepton_kNN_jetpt_ )
    self.evt_njet_         = array.array('f',[0]) ; self.reader_.AddVariable('evt_njet'        , self.evt_njet_         )
    
    self.reader_.BookMVA(self.MVA_method_+'_muon'    ,file_name_mu )
    self.reader_.BookMVA(self.MVA_method_+'_electron',file_name_ele)

  def evaluate_mva_weigh(self, lepton_pt, lepton_kNN_jetpt, evt_njet, lepton) :

    self.lepton_pt_        [0] = lepton_pt      
    self.lepton_kNN_jetpt_ [0] = lepton_kNN_jetpt
    self.evt_njet_         [0] = evt_njet        
    
    return self.reader_.EvaluateMVA(self.MVA_method_+'_'+lepton) 

  def loop_over_tree(self, sample, region, tree_name = 'Tree') :
    
    tree = self.take_sample(sample, region, tree_name)
        
    for evt in tree :
      if region == 'antiMu' :
        weight_mu = self.evaluate_mva_weigh(evt.muon_pt    , evt.muon_kNN_jetpt    , evt.evt_njet, 'muon'    )
        weight = weight_mu / (1. - weight_mu)      
      if region == 'antiE' :
        weight_el = self.evaluate_mva_weigh(evt.electron_pt, evt.electron_kNN_jetpt, evt.evt_njet, 'electron')
        weight = weight_el / (1. - weight_el)
      if region == 'antiEMu' :
        weight_mu = self.evaluate_mva_weigh(evt.muon_pt    , evt.muon_kNN_jetpt    , evt.evt_njet, 'muon'    )
        weight_el = self.evaluate_mva_weigh(evt.electron_pt, evt.electron_kNN_jetpt, evt.evt_njet, 'electron')
        weight    = -1. * (weight_mu / (1. - weight_mu)) * (weight_el / (1. - weight_el))

      #self.histo_.Fill( evt.muon_pt, weight )
      self.histo_.Fill( evt.evt_Mmt, weight )
      
      
      
      
      
      
      
      
      
      
      
      