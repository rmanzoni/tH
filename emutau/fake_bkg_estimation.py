import os
import math
import array

import ROOT

class fake_bkg_estimation( object ) :
  '''
  bla bla
  
  folder     : /afs/cern.ch/work/m/manzoni/public/tH_ntuple/antiIsolatedTau/
  method     : f12, f3
  knnfolder  : /afs/cern.ch/work/m/manzoni/public/tH_ntuple/antiIsolatedTau/weights
  MVA_method : KNN (Default)
  '''

  def __init__(self, folder, method, knnfolder, MVA_method = 'KNN') :    

    self.folder_     = folder
    self.method_     = method
    self.knnfolder_  = knnfolder
    self.MVA_method_ = MVA_method
    self.histo_      = ROOT.TH1F('Mmt','Mmt',10,0,150)
    self.weights_    = {}
    
    ROOT.TH1.SetDefaultSumw2()
  
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
    
    weights = self.get_weights()
        
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
      
      weight *= self.weights_[region]      
      self.histo_.Fill( evt.evt_Mmt, weight )
      

  def get_weights(self, tree_name = 'Tree') :
    
    yields = { 
               'antiE'  :{'data':1.,'WZ':1.,'ZZ':1.,'TTW':1.,'TTZ':1.,'tt1l':1.,'tt2l':1.,},
               'antiMu' :{'data':1.,'WZ':1.,'ZZ':1.,'TTW':1.,'TTZ':1.,'tt1l':1.,'tt2l':1.,},
               'antiEMu':{'data':1.,'WZ':1.,'ZZ':1.,'TTW':1.,'TTZ':1.,'tt1l':1.,'tt2l':1.,},
             }
    for region in yields.keys() :         
      for sample in yields[region] :
        tree = self.take_sample(sample, region, tree_name)
        h1 = ROOT.TH1F('h1','h1',1,0,10000000)
        tree.Draw('evt_Mmt>>h1','evt_weight')      
        yields[region][sample] = h1.Integral()  
    
    self.weights_['antiE']   = 1. - (yields['antiE']  ['WZ'] + yields['antiE']  ['ZZ'] + yields['antiE']  ['TTW'] + yields['antiE']  ['TTZ'] + yields['antiE']  ['tt1l'] + yields['antiE']  ['tt2l']) / yields['antiE']  ['data']
    self.weights_['antiMu']  = 1. - (yields['antiMu'] ['WZ'] + yields['antiMu'] ['ZZ'] + yields['antiMu'] ['TTW'] + yields['antiMu'] ['TTZ'] + yields['antiMu'] ['tt1l'] + yields['antiMu'] ['tt2l']) / yields['antiMu'] ['data']
    self.weights_['antiEMu'] = 1. - (yields['antiEMu']['WZ'] + yields['antiEMu']['ZZ'] + yields['antiEMu']['TTW'] + yields['antiEMu']['TTZ'] + yields['antiEMu']['tt1l'] + yields['antiEMu']['tt2l']) / yields['antiEMu']['data']
          

#   def evaluate_mva_weigh12(self, muon_pt, muon_kNN_jetpt, evt_njet, electron_pt, electron_kNN_jetpt, evt_njet) :
#     
#          
      
      
      