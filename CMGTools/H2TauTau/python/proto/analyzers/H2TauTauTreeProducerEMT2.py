import math
from CMGTools.RootTools.analyzers.TreeAnalyzerNumpyEMT import TreeAnalyzerNumpyEMT
from CMGTools.H2TauTau.proto.analyzers.ntuple import *
from CMGTools.H2TauTau.proto.analyzers.ScaleFactorsMuEG201253X import *
from CMGTools.RootTools.fwlite.AutoHandle import AutoHandle
from CMGTools.RootTools.utils.DeltaR import cleanObjectCollection, matchObjectCollection, bestMatch
from CMGTools.RootTools.physicsobjects.PhysicsObjects import GenParticle

def isFinal(p):
    return not (p.numberOfDaughters() == 1 and p.daughter(0).pdgId() == p.pdgId())

class H2TauTauTreeProducerEMT2( TreeAnalyzerNumpyEMT ):
    '''Tree producer for the H->tau tau analysis.

    Some of the functions in this class should be made available to everybody.'''

    def declareVariables(self):

       tr = self.tree

       var( tr, 'run', int)
       var( tr, 'lumi', int)
       var( tr, 'evt', int)
       var( tr, 'rho')
       var( tr, 'pfmet')
       var( tr, 'pfmetphi')
       var( tr, 'weight')
       var( tr, 'nmuon')
       var( tr, 'nelectron')
       var( tr, 'ntau')
       var( tr, 'nvmuon')
       var( tr, 'nvelectron')
       var( tr, 'nvtau')
       var( tr, 'nBJets')
       var( tr, 'nJets')
       var( tr, 'nGen')
       var( tr, 'trig_type_M8E17')
       var( tr, 'trig_type_M17E8')
#       var( tr, 'NUP')
#       bookJet(tr, 'jet1')
#       bookJet(tr, 'jet2')

       mtr = self.mtree
       bookParticle(mtr, 'muon')
       var(mtr, 'muon_id')
       var(mtr, 'muon_iso')
       var(mtr, 'muon_MT')
       var(mtr, 'muon_trig_weight')
       var(mtr, 'muon_id_weight')
       var(mtr, 'muon_jetpt')
       var(mtr, 'muon_njet')
       var(mtr, 'muon_mass')
       var(mtr, 'muon_reliso')
       var(mtr, 'muon_trigmatch')

       etr = self.etree
       bookParticle(etr, 'electron')
       var(etr, 'electron_id')
       var(etr, 'electron_iso')
       var(etr, 'electron_MT')
       var(etr, 'electron_trig_weight')
       var(etr, 'electron_id_weight')
       var(etr, 'electron_jetpt')
       var(etr, 'electron_njet')
       var(etr, 'electron_mass')
       var(etr, 'electron_reliso')
       var(etr, 'electron_trigmatch')

       ttr = self.ttree
       bookParticle(ttr, 'tau')
       var(ttr, 'tau_id')
       var(ttr, 'tau_iso')
       var(ttr, 'tau_MT')
       var(ttr, 'tau_mass')
       var(ttr, 'tau_decaymode')
       var(ttr, 'tau_ep')
#       var(ttr, 'tau_trig_match')
       var(ttr, 'tau_againstELoose')
       var(ttr, 'tau_againstETight')
       var(ttr, 'tau_againstELooseArmin')
       var(ttr, 'tau_againstEMedium')
       var(ttr, 'tau_againstE2Loose')
       var(ttr, 'tau_againstE2Medium')
#       var(ttr, 'tau_againstE0Loose')
#       var(ttr, 'tau_againstE0Medium')
       var(ttr, 'tau_againstMuLoose')
       var(ttr, 'tau_againstMuTight')
       var(ttr, 'tau_mvaisolation')
       var(ttr, 'tau_mvaisolation_loose')
       var(ttr, 'tau_againstERaw')
       var(ttr, 'tau_againstECat')
       var(ttr, 'tau_againstE2Raw')
       var(ttr, 'tau_againstE2Cat')
       var(ttr, 'tau_againstE0Raw')
#       var(ttr, 'tau_againstE0Cat')
       var(ttr, 'dBisolation')

       ## RM new TauIDs
       var(ttr, 'byIsolationMVA3oldDMwoLTraw'    )
       var(ttr, 'byLooseIsolationMVA3oldDMwoLT'  )
       var(ttr, 'byMediumIsolationMVA3oldDMwoLT' )
       var(ttr, 'byTightIsolationMVA3oldDMwoLT'  )
       var(ttr, 'byVTightIsolationMVA3oldDMwoLT' )
       var(ttr, 'byVVTightIsolationMVA3oldDMwoLT')

       var(ttr, 'byIsolationMVA3oldDMwLTraw'     )
       var(ttr, 'byLooseIsolationMVA3oldDMwLT'   )
       var(ttr, 'byMediumIsolationMVA3oldDMwLT'  )
       var(ttr, 'byTightIsolationMVA3oldDMwLT'   )
       var(ttr, 'byVTightIsolationMVA3oldDMwLT'  )
       var(ttr, 'byVVTightIsolationMVA3oldDMwLT' )

       var(ttr, 'byIsolationMVA3newDMwoLTraw'    )
       var(ttr, 'byLooseIsolationMVA3newDMwoLT'  )
       var(ttr, 'byMediumIsolationMVA3newDMwoLT' )
       var(ttr, 'byTightIsolationMVA3newDMwoLT'  )
       var(ttr, 'byVTightIsolationMVA3newDMwoLT' )
       var(ttr, 'byVVTightIsolationMVA3newDMwoLT')

       var(ttr, 'byIsolationMVA3newDMwLTraw'     )
       var(ttr, 'byLooseIsolationMVA3newDMwLT'   )
       var(ttr, 'byMediumIsolationMVA3newDMwLT'  )
       var(ttr, 'byTightIsolationMVA3newDMwLT'   )
       var(ttr, 'byVTightIsolationMVA3newDMwLT'  )
       var(ttr, 'byVVTightIsolationMVA3newDMwLT' )

       var(ttr, 'againstMuonLoose3'   )
       var(ttr, 'againstMuonTight3'   )
       var(ttr, 'againstMuonMVALoose' )
       var(ttr, 'againstMuonMVAMedium')
       var(ttr, 'againstMuonMVATight' )

       var(ttr, 'againstElectronLoose'     )
       var(ttr, 'againstElectronMedium'    )
       var(ttr, 'againstElectronTight'     )
       var(ttr, 'againstElectronLooseMVA5' )
       var(ttr, 'againstElectronMediumMVA5')
       var(ttr, 'againstElectronTightMVA5' )
       var(ttr, 'againstElectronVTightMVA5')



       vmtr = self.vmtree
       bookParticle(vmtr, 'veto_muon')

       vetr = self.vetree
       bookParticle(vetr, 'veto_electron')

       vttr = self.vttree
       bookParticle(vttr, 'veto_tau')


       btr = self.btree
       var(btr, 'bjet_pt')
       var(btr, 'bjet_eta')
       var(btr, 'bjet_phi')
       var(btr, 'bjet_mass')
       var(btr, 'bjet_mva')
       var(btr, 'bjet_flav')

       jtr = self.jtree
       bookJet(jtr, 'jet')
       var(jtr, 'jet_flav')
       var(jtr, 'jet_mass')

       gtr = self.gentree
       var(gtr, 'gen_pt')
       var(gtr, 'gen_eta')
       var(gtr, 'gen_phi')
       var(gtr, 'gen_pdgid')

#       var(jtr, 'jet_pt')
#       var(jtr, 'jet_eta')
#       var(jtr, 'jet_phi')


    def declareHandles(self):
        super(H2TauTauTreeProducerEMT2, self).declareHandles()

        self.handles['pfmetraw'] = AutoHandle(
            'cmgPFMETRaw',
            'std::vector<cmg::BaseMET>'
            )

        self.handles['jets'] = AutoHandle( 'cmgPFJetSel',
                                           'std::vector<cmg::PFJet>' )

        self.mchandles['genParticles'] = AutoHandle('genParticlesPruned',
                                                    'std::vector<reco::GenParticle>'
            )

#        self.mchandles['source'] =  AutoHandle(
#            'source',
#            'LHEEventProduct'
#            )

    def process(self, iEvent, event):
       self.readCollections( iEvent )
       pfmet = self.handles['pfmetraw'].product()[0]
#       genParticles = [GenParticle(l) for l in self.mchandles['genParticles'].product() if l.status()==3 and l.pdgId()<100 and l.numberOfDaughters()==1 and l.daughter(0).pdgId() == l.pdgId() and abs(l.pdgId()) not in [12,14,16,23,24]]
#       genParticles = [GenParticle(l) for l in self.mchandles['genParticles'].product() if l.status()==3 and l.pdgId()<100 and l.numberOfDaughters()==1 and l.daughter(0).pdgId() == l.pdgId() and abs(l.pdgId()) not in [12,14,16,23,24]]
       genParticles = [GenParticle(l) for l in self.mchandles['genParticles'].product() if l.status()==3 and abs(l.pdgId()) in [11,13,15,5]]

       tr = self.tree
       tr.reset()

       fill( tr, 'run', event.run)
       fill( tr, 'lumi',event.lumi)
       fill( tr, 'evt', event.eventId)
       fill( tr, 'rho', event.rho)
       fill( tr, 'nmuon', len(event.muoncand))
       fill( tr, 'nelectron', len(event.electroncand))
       fill( tr, 'ntau', len(event.taucand))
       fill( tr, 'nvmuon', len(event.vetomuoncand))
       fill( tr, 'nvelectron', len(event.vetoelectroncand))
       fill( tr, 'nvtau', len(event.vetotaucand))
       fill( tr, 'pfmet', pfmet.pt())
       fill( tr, 'pfmetphi', pfmet.phi())
       fill( tr, 'nBJets', len(event.cleanBJets))
       fill( tr, 'nJets', len(event.cleanJets))
       fill( tr, 'weight', event.eventWeight)
       fill( tr, 'nGen', len(genParticles))

#       if self.cfg_comp.isMC:
#           nparton = self.mchandles['source'].product().hepeup().NUP
#           fill( tr, 'NUP', nparton)

#       nJets = len(event.cleanJets)
#       if nJets>=1:
#           fillJet(tr, 'jet1', event.cleanJets[0] )
#       if nJets>=2:
#           fillJet(tr, 'jet2', event.cleanJets[1] )

       trig_M8E17 = False
       trig_M17E8 = False

#       for itrig in event.hltPaths:
#
#           if itrig.find('Mu8_Ele17')!=-1:
#               trig_M8E17 = True
#           if itrig.find('Mu17_Ele8')!=-1:
#               trig_M17E8 = True

       fill( tr, 'trig_type_M8E17', trig_M8E17)
       fill( tr, 'trig_type_M17E8', trig_M17E8)

       self.tree.tree.Fill()


       allJets = self.handles['jets'].product()
       maxJets = []

       for ijet in allJets:
           if ijet.pt() > 12. and abs(ijet.eta()) < 5:
               maxJets.append(ijet)

       mtr = self.mtree
       mtr.reset()

       for im in event.muoncand:
           fillParticle(mtr, 'muon', im)
           fill(mtr, 'muon_id', im.flag_id)
           fill(mtr, 'muon_iso', im.flag_iso)
           fill(mtr, 'muon_trigmatch', im.trig_match)
           fill(mtr, 'muon_MT', self.returnMT(pfmet, im))
           fill(mtr, 'muon_trig_weight', muTrigScale_MuEG_2012_53X(im.pt(), im.eta()))
           fill(mtr, 'muon_id_weight', muIDscale_MuEG_2012_53X(im.pt(), im.eta()))
           fill(mtr, 'muon_mass', im.mass())
           fill(mtr, 'muon_reliso', im.relIso(0.5,1))


           bm, dr2min = bestMatch(im, maxJets)
           if dr2min < 0.25:
               fill( mtr, 'muon_jetpt', bm.pt())
               fill( mtr, 'muon_njet', len(event.cleanJets))
           else:
               fill( mtr, 'muon_jetpt', -999)
               fill( mtr, 'muon_njet', -999)



           self.mtree.tree.Fill()

       etr = self.etree
       etr.reset()

       for ie in event.electroncand:
           fillParticle(etr, 'electron', ie)
           fill(etr, 'electron_id', ie.flag_id)
           fill(etr, 'electron_iso', ie.flag_iso)
           fill(etr, 'electron_trigmatch', ie.trig_match)
           fill(etr, 'electron_MT', self.returnMT(pfmet, ie))
           fill(etr, 'electron_trig_weight', eleTrigScale_MuEG_2012_53X(ie.pt(), ie.eta()))
           fill(etr, 'electron_id_weight', eleIDscale_MuEG_2012_53X(ie.pt(), ie.eta()))
           fill(etr, 'electron_mass', ie.mass())
           fill(etr, 'electron_reliso', ie.relIso(0.5,1))

           bm, dr2min = bestMatch(ie, maxJets)
           if dr2min < 0.25:
               fill( etr, 'electron_jetpt', bm.pt())
               fill( etr, 'electron_njet', len(event.cleanJets))
           else:
               fill( etr, 'electron_jetpt', -999)
               fill( etr, 'electron_njet', -999)


           self.etree.tree.Fill()

       ttr = self.ttree
       ttr.reset()


       for it in event.taucand:
           fillParticle(ttr, 'tau', it)
           fill(ttr, 'tau_id', it.flag_id)
           fill(ttr, 'tau_iso', it.flag_iso)
           fill(ttr, 'tau_MT', self.returnMT(pfmet, it))
           fill(ttr, 'tau_mass', it.mass())
           fill(ttr, 'tau_decaymode', it.decaymode)
           fill(ttr, 'tau_ep', it.ep)
#           fill(ttr, 'tau_trig_match', it.trig_match)
           fill(ttr, 'tau_againstELoose', it.againstELoose)
           fill(ttr, 'tau_againstELooseArmin', it.againstELooseArmin)
           fill(ttr, 'tau_againstEMedium', it.againstEMedium)
           fill(ttr, 'tau_againstETight', it.againstETight)
           fill(ttr, 'tau_againstE2Loose', it.againstE2Loose)
           fill(ttr, 'tau_againstE2Medium', it.againstE2Medium)
#           fill(ttr, 'tau_againstE0Loose', it.againstE0Loose)
#           fill(ttr, 'tau_againstE0Medium', it.againstE0Medium)
           fill(ttr, 'tau_againstMuLoose', it.againstMuLoose)
           fill(ttr, 'tau_againstMuTight', it.againstMuTight)
           fill(ttr, 'tau_mvaisolation', it.mvaisolation)
           fill(ttr, 'tau_mvaisolation_loose', it.mvaisolation_loose)
           fill(ttr, 'tau_againstERaw', it.againstERaw)
           fill(ttr, 'tau_againstECat', it.againstECat)
           fill(ttr, 'tau_againstE2Raw', it.againstE2Raw)
           fill(ttr, 'tau_againstE2Cat', it.againstE2Cat)
           fill(ttr, 'tau_againstE0Raw', it.againstE0Raw)
#           fill(ttr, 'tau_againstE0Cat', it.againstE0Cat)
           fill(ttr, 'dBisolation', it.dBisolation)
       ## RM new TauIDs
           fill(ttr, 'byIsolationMVA3oldDMwoLTraw'    , it.byIsolationMVA3oldDMwoLTraw    )
           fill(ttr, 'byLooseIsolationMVA3oldDMwoLT'  , it.byLooseIsolationMVA3oldDMwoLT  )
           fill(ttr, 'byMediumIsolationMVA3oldDMwoLT' , it.byMediumIsolationMVA3oldDMwoLT )
           fill(ttr, 'byTightIsolationMVA3oldDMwoLT'  , it.byTightIsolationMVA3oldDMwoLT  )
           fill(ttr, 'byVTightIsolationMVA3oldDMwoLT' , it.byVTightIsolationMVA3oldDMwoLT )
           fill(ttr, 'byVVTightIsolationMVA3oldDMwoLT', it.byVVTightIsolationMVA3oldDMwoLT)

           fill(ttr, 'byIsolationMVA3oldDMwLTraw'     , it.byIsolationMVA3oldDMwLTraw     )
           fill(ttr, 'byLooseIsolationMVA3oldDMwLT'   , it.byLooseIsolationMVA3oldDMwLT   )
           fill(ttr, 'byMediumIsolationMVA3oldDMwLT'  , it.byMediumIsolationMVA3oldDMwLT  )
           fill(ttr, 'byTightIsolationMVA3oldDMwLT'   , it.byTightIsolationMVA3oldDMwLT   )
           fill(ttr, 'byVTightIsolationMVA3oldDMwLT'  , it.byVTightIsolationMVA3oldDMwLT  )
           fill(ttr, 'byVVTightIsolationMVA3oldDMwLT' , it.byVVTightIsolationMVA3oldDMwLT )

           fill(ttr, 'byIsolationMVA3newDMwoLTraw'    , it.byIsolationMVA3newDMwoLTraw    )
           fill(ttr, 'byLooseIsolationMVA3newDMwoLT'  , it.byLooseIsolationMVA3newDMwoLT  )
           fill(ttr, 'byMediumIsolationMVA3newDMwoLT' , it.byMediumIsolationMVA3newDMwoLT )
           fill(ttr, 'byTightIsolationMVA3newDMwoLT'  , it.byTightIsolationMVA3newDMwoLT  )
           fill(ttr, 'byVTightIsolationMVA3newDMwoLT' , it.byVTightIsolationMVA3newDMwoLT )
           fill(ttr, 'byVVTightIsolationMVA3newDMwoLT', it.byVVTightIsolationMVA3newDMwoLT)

           fill(ttr, 'byIsolationMVA3newDMwLTraw'     , it.byIsolationMVA3newDMwLTraw     )
           fill(ttr, 'byLooseIsolationMVA3newDMwLT'   , it.byLooseIsolationMVA3newDMwLT   )
           fill(ttr, 'byMediumIsolationMVA3newDMwLT'  , it.byMediumIsolationMVA3newDMwLT  )
           fill(ttr, 'byTightIsolationMVA3newDMwLT'   , it.byTightIsolationMVA3newDMwLT   )
           fill(ttr, 'byVTightIsolationMVA3newDMwLT'  , it.byVTightIsolationMVA3newDMwLT  )
           fill(ttr, 'byVVTightIsolationMVA3newDMwLT' , it.byVVTightIsolationMVA3newDMwLT )

           fill(ttr, 'againstMuonLoose3'   , it.againstMuonLoose3   )
           fill(ttr, 'againstMuonTight3'   , it.againstMuonTight3   )
           fill(ttr, 'againstMuonMVALoose' , it.againstMuonMVALoose )
           fill(ttr, 'againstMuonMVAMedium', it.againstMuonMVAMedium)
           fill(ttr, 'againstMuonMVATight' , it.againstMuonMVATight )

           fill(ttr, 'againstElectronLoose'     , it.againstElectronLoose     )
           fill(ttr, 'againstElectronMedium'    , it.againstElectronMedium    )
           fill(ttr, 'againstElectronTight'     , it.againstElectronTight     )
           fill(ttr, 'againstElectronLooseMVA5' , it.againstElectronLooseMVA5 )
           fill(ttr, 'againstElectronMediumMVA5', it.againstElectronMediumMVA5)
           fill(ttr, 'againstElectronTightMVA5' , it.againstElectronTightMVA5 )
           fill(ttr, 'againstElectronVTightMVA5', it.againstElectronVTightMVA5)

           self.ttree.tree.Fill()

       vmtr = self.vmtree
       vmtr.reset()
       for im in event.vetomuoncand:
           fillParticle(vmtr, 'veto_muon', im)
           self.vmtree.tree.Fill()

       vetr = self.vetree
       vetr.reset()
       for ie in event.vetoelectroncand:
           fillParticle(vetr, 'veto_electron', ie)
           self.vetree.tree.Fill()

       vttr = self.vttree
       vttr.reset()
       for it in event.vetotaucand:
           fillParticle(vttr, 'veto_tau', it)
           self.vttree.tree.Fill()


       btr = self.btree
       btr.reset()

       for ib in event.cleanBJets:
           fill(btr, 'bjet_pt', ib.pt())
           fill(btr, 'bjet_eta', ib.eta())
           fill(btr, 'bjet_phi', ib.phi())
           fill(btr, 'bjet_flav', ib.partonFlavour())
           fill(btr, 'bjet_mva', ib.btag('combinedSecondaryVertexBJetTags'))
           fill(btr, 'bjet_mass', ib.mass())
           self.btree.tree.Fill()


       jtr = self.jtree
       jtr.reset()

       for ij in event.cleanJets:
           fillJet(jtr, 'jet', ij)
           fill(jtr, 'jet_flav', ij.partonFlavour())
           fill(jtr, 'jet_mass', ij.mass())
           self.jtree.tree.Fill()


       gtr = self.gentree
       gtr.reset()

       if self.cfg_comp.isMC:
           for ig in genParticles:
               fill(gtr, 'gen_pt', ig.pt())
               fill(gtr, 'gen_eta', ig.eta())
               fill(gtr, 'gen_phi', ig.phi())
               fill(gtr, 'gen_pdgid', ig.pdgId())
               self.gentree.tree.Fill()





    def returnMT(self, met, lep):
        dphi = met.phi() - lep.phi()
        MT = 2*met.pt()*lep.pt()*(1-math.cos(dphi))
        return math.sqrt(MT)
