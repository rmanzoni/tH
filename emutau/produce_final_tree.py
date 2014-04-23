import sys
sys.path.append("../Common")

import ROOT 
import numpy as n
from Utils import *
from fake_bkg_estimation import fake_bkg_estimation as fb

class final_tree( object ) : 
  '''
  Merges the trees for different components, including fakes, into a single one.
  It saves into evt_component branch the different component ID
  Fake estimation works with f12 technique only at the moment.
  Example usage
  from produce_final_tree import final_tree as ft
  myft = ft()
  myft.produce_final_ntuple()
  '''
  def __init__(self      , 
               folder    = '/afs/cern.ch/work/m/manzoni/public/tH_ntuple/antiIsolatedTau/', 
               method    = 'f12', 
               knnfolder = '/afs/cern.ch/work/m/manzoni/public/tH_ntuple/antiIsolatedTau/weights/'
               ) :

    self.folder_     = folder
    self.method_     = method
    self.knnfolder_  = knnfolder
    self.trees_      = ROOT.TList()
    self.components_ = {'data'        : 0,
                        'fakes'       : 1,
                        'WZ'          : 2,
                        'ZZ'          : 3,
                        'TTH'         : 4,
                        'TTW'         : 5,
                        'TTZ'         : 6,
                        'tH_YtMinus1' : 7,
                        'tt1l'        : 8,
                        'tt2l'        : 9}

  def initialize_out_tree(self, sample, region) :
    '''
    Clones the tree structure from any f12 or f3 tree.
    Adds three branches for f12 and f3 weights and for the component ID.
    '''

    self.initialize_in_tree_(sample,region)
    self.tree_out = self.tree_in.CloneTree(0)

    self.evt_f12_weight = n.zeros(1, dtype=float) ; self.evt_f12_weight [0] = 1.
    self.evt_f3_weight  = n.zeros(1, dtype=float) ; self.evt_f3_weight  [0] = 1.
    self.evt_component  = n.zeros(1, dtype=int  ) ; self.evt_component  [0] = 0.

    self.tree_out.Branch('evt_f12_weight', self.evt_f12_weight,'evt_f12_weight/D')
    self.tree_out.Branch('evt_f3_weight' , self.evt_f3_weight ,'evt_f3_weight/D' )  
    self.tree_out.Branch('evt_component' , self.evt_component ,'evt_component/I' )  

  def initialize_in_tree_(self, sample, region) :
    '''
    Grabs one tree.
    sample : tt2l, tt1l, tH_YtMinus1, data, ZZ, WZ, TTZ, TTW, TTH
    region : signal, antiE, antiMu, antiEMu
    '''
    self.region_  = region
    self.sample_  = sample
    self.tree_in  = take_sample(self.folder_, self.method_, sample, region )
        
  def fill_out_tree(self, set_fakes_weights = False) :
    '''
    Loops over the self.tree_in, clones the event into self.tree_out and 
    possibly fills the f12 and f3 weights
    '''
    if set_fakes_weights :
      myfake = fb(self.folder_, self.method_, self.knnfolder_)
      myfake.book_mva_readers('data')
      myfake.get_weights()
      self.evt_component[0] = self.components_['fakes']
    else :   
      self.evt_component[0] = self.components_[self.sample_]
    for i, evt in enumerate(self.tree_in) :
      if set_fakes_weights and self.skim(self.tree_in) :
        self.evt_f12_weight[0], self.evt_f3_weight[0] = self.get_weights(evt, myfake)
      if self.skim(self.tree_in) : self.tree_out.Fill()
  
  def skim(self, tree) :
    '''
    Defines a skim function to select events.
    '''
    passed = tree.muon_pt > 0. and tree.muon_iso > -10.
    if passed : return True

  def get_weights(self, evt, fakes) :
    '''
    Runs the fake evaluation.
    Given the region, the lepton kinematics and the number of jets it returns
    a knn weight previously evaluated 
    '''  
    
    weight = 1.
    
    if 'antiMu' in self.region_ :
      weight_mu = fakes.evaluate_mva_weigh(evt.muon_pt    , evt.muon_kNN_jetpt    , evt.evt_njet, 'muon'    )
      weight = weight_mu / (1. - weight_mu)    
    if 'antiE' in self.region_ :
      weight_el = fakes.evaluate_mva_weigh(evt.electron_pt, evt.electron_kNN_jetpt, evt.evt_njet, 'electron')
      weight = weight_el / (1. - weight_el)
    if 'antiEMu' in self.region_ :
      weight_mu = fakes.evaluate_mva_weigh(evt.muon_pt    , evt.muon_kNN_jetpt    , evt.evt_njet, 'muon'    )
      weight_el = fakes.evaluate_mva_weigh(evt.electron_pt, evt.electron_kNN_jetpt, evt.evt_njet, 'electron')
      weight    = -1. * (weight_mu / (1. - weight_mu)) * (weight_el / (1. - weight_el))
   
    weight_f12 = weight * fakes.weights_[self.region_]
    weight_f3  = 1.
    
    return weight_f12, weight_f3

  def save_out_tree(self, tree_to_write, file_name = 'out_tree.root', options = 'recreate') :
    file = ROOT.TFile.Open(file_name, options)
    file.cd()
    tree_to_write.Write()
    file.Close()

  def produce_fakes(self) :       
    for region in ['antiEMu','antiMu','antiE'] :  
      self.initialize_out_tree('data',region)
      self.fill_out_tree(True)
      self.trees_.append(self.tree_out)

  def produce_final_ntuple(self, samples = ['tt2l', 'tt1l', 'tH_YtMinus1', 'data', 'ZZ', 'WZ', 'TTZ', 'TTW', 'TTH'], fakes = True, region = 'signal') :
    for sample in samples :
      self.initialize_out_tree(sample,region)
      self.fill_out_tree() 
      self.trees_.append(self.tree_out)
    if fakes :
      self.produce_fakes()
    final_tree = ROOT.TTree.MergeTrees(self.trees_)        
    self.save_out_tree(final_tree)

