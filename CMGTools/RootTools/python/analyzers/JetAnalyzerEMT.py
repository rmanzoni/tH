import random
from CMGTools.RootTools.fwlite.Analyzer import Analyzer
from CMGTools.RootTools.fwlite.AutoHandle import AutoHandle
from CMGTools.RootTools.physicsobjects.PhysicsObjects import Jet, GenJet
from CMGTools.RootTools.utils.DeltaR import cleanObjectCollection, matchObjectCollection
# from CMGTools.RootTools.physicsobjects.VBF import VBF
from CMGTools.RootTools.statistics.Counter import Counter, Counters
from CMGTools.RootTools.physicsobjects.BTagSF import BTagSF
from CMGTools.RootTools.physicsobjects.PhysicsObjects import GenParticle
from CMGTools.RootTools.utils.DeltaR import deltaR2
from CMGTools.RootTools.utils.cmsswRelease import isNewerThan

class JetAnalyzerEMT( Analyzer ):
    """Analyze jets ;-)

    This analyzer filters the jets that do not correspond to the leptons
    stored in event.selectedLeptons, and puts in the event:
    - jets: all jets passing the pt and eta cuts
    - cleanJets: the collection of clean jets
    - bJets: the bjets passing testBJet (see this method)

    Example configuration:

    jetAna = cfg.Analyzer(
      'JetAnalyzerEMT',
      # cmg jet input collection
      jetCol = 'cmgPFJetSel',
      # pt threshold
      jetPt = 30,
      # eta range definition
      jetEta = 5.0,
      # seed for the btag scale factor
      btagSFseed = 123456,
      # if True, the PF and PU jet ID are not applied, and the jets get flagged
      relaxJetId = False,
    )
    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(JetAnalyzerEMT,self).__init__(cfg_ana, cfg_comp, looperName)
        self.btagSF = BTagSF (cfg_ana.btagSFseed)
        self.is2012 = isNewerThan('CMSSW_5_2_0')

    def declareHandles(self):
        super(JetAnalyzerEMT, self).declareHandles()

        self.handles['jets'] = AutoHandle( self.cfg_ana.jetCol,
                                           'std::vector<cmg::PFJet>' )
        if self.cfg_comp.isMC:
            # and ("BB" in self.cfg_comp.name):
            self.mchandles['genParticles'] = AutoHandle( 'genParticlesPruned',
                                                         'std::vector<reco::GenParticle>' )
            self.mchandles['genJets'] = AutoHandle('genJetSel',
                                                   'std::vector<cmg::PhysicsObjectWithPtr< edm::Ptr<reco::GenJet> > >')
##             self.mchandles['genJetsP'] = AutoHandle('ak5GenJetsNoNu',
##                                                     'std::vector< reco::GenJet >')

    def beginLoop(self):
        super(JetAnalyzerEMT,self).beginLoop()
        self.counters.addCounter('jets')
        count = self.counters.counter('jets')
        count.register('all events')
        count.register('No b jets')
#        count.register('at least 2 good jets')
#        count.register('at least 2 clean jets')
        
    def process(self, iEvent, event):
        
        self.readCollections( iEvent )
        cmgJets = self.handles['jets'].product()

        print 'cmgJets = ', len(cmgJets)

        allJets = []
        event.jets = []
        event.bJets = []
        event.cleanJets = []
        event.cleanBJets = []

#        import pdb; pdb.set_trace();

        leptons = []
        if hasattr(event, 'selectedLeptons'):
            leptons = event.selectedLeptons
#        elif hasattr(event, 'muoncand'):
##            leptons = event.muoncand + event.electroncand + event.taucand
#            leptons = event.muon + event.electron + event.tau
#            print '# of leptons = ', len(leptons)

        genJets = None
        if self.cfg_comp.isMC:
            genJets = map( GenJet, self.mchandles['genJets'].product() ) 
            
        for cmgJet in cmgJets:
            jet = Jet( cmgJet )
            allJets.append( jet )
            if self.cfg_comp.isMC and hasattr( self.cfg_comp, 'jetScale'):
                scale = random.gauss( self.cfg_comp.jetScale,
                                      self.cfg_comp.jetSmear )
                jet.scaleEnergy( scale )
            if genJets:
                # Use DeltaR = 0.25 matching like JetMET
                pairs = matchObjectCollection( [jet], genJets, 0.25*0.25)
                if pairs[jet] is None:
                    pass
                    #jet.genJet = None
                else:
                    jet.genJet = pairs[jet] 
                # print jet, jet.genJet

            #Add JER correction for MC jets. Requires gen-jet matching. 
            if self.cfg_comp.isMC and hasattr(self.cfg_ana, 'jerCorr') and self.cfg_ana.jerCorr:
                self.jerCorrection(jet)

            #Add JES correction for MC jets.
            if self.cfg_comp.isMC and hasattr(self.cfg_ana, 'jesCorr'):
                self.jesCorrection(jet, self.cfg_ana.jesCorr)
            if self.testJet( jet ):
                event.jets.append(jet)
            if self.testBJet(jet):
                event.bJets.append(jet)


                
        self.counters.counter('jets').inc('all events')

#        print 'check =', len(event.muon), len(event,electron), len(event.tau)


#        if isinstance(event.muoncand, list):
#            event.cleanBJets, dummy = cleanObjectCollection( event.bJets,
#                                                             masks = event.muoncand,
#                                                             deltaRMin = 0.4 )
#
#            event.cleanJets, dummy = cleanObjectCollection( event.jets,
#                                                            masks = event.muoncand,
#                                                            deltaRMin = 0.4 )
#
#        else:
#            event.cleanBJets, dummy = cleanObjectCollection( event.bJets,
#                                                             masks = [event.muoncand],
#                                                             deltaRMin = 0.4 )
#            
#            event.cleanJets, dummy = cleanObjectCollection( event.jets,
#                                                            masks = [event.muoncand],
#                                                            deltaRMin = 0.4 )
#
#        if isinstance(event.electroncand, list):
#            event.cleanBJets, dummy = cleanObjectCollection( event.cleanBJets,
#                                                             masks = event.electroncand,
#                                                             deltaRMin = 0.4 )
#
#            event.cleanJets, dummy = cleanObjectCollection( event.cleanJets,
#                                                            masks = event.electroncand,
#                                                            deltaRMin = 0.4 )
#
#        else:
#            event.cleanBJets, dummy = cleanObjectCollection( event.cleanBJets,
#                                                             masks = [event.electroncand],
#                                                             deltaRMin = 0.4 )
#            
#            
#            event.cleanJets, dummy = cleanObjectCollection( event.cleanJets,
#                                                            masks = [event.electroncand],
#                                                            deltaRMin = 0.4 )
#
#
#        if isinstance(event.taucand, list):
#            event.cleanBJets, dummy = cleanObjectCollection( event.cleanBJets,
#                                                             masks = event.taucand,
#                                                             deltaRMin = 0.4 )
#
#            event.cleanJets, dummy = cleanObjectCollection( event.cleanJets,
#                                                            masks = event.taucand,
#                                                            deltaRMin = 0.4 )
#
#        else:
#            event.cleanBJets, dummy = cleanObjectCollection( event.cleanBJets,
#                                                             masks = [event.taucand],
#                                                             deltaRMin = 0.4 )
#            
#            
#            event.cleanJets, dummy = cleanObjectCollection( event.cleanJets,
#                                                            masks = [event.taucand],
#                                                            deltaRMin = 0.4 )


        
        pairs = matchObjectCollection( leptons, allJets, 0.5*0.5)


        # associating a jet to each lepton
        for lepton in leptons:
            jet = pairs[lepton]
            if jet is None:
                lepton.jet = lepton
            else:
                lepton.jet = jet

        # associating a leg to each clean jet
        invpairs = matchObjectCollection( event.cleanJets, leptons, 99999. )
        for jet in event.cleanJets:
            leg = invpairs[jet]
            jet.leg = leg

        for jet in event.cleanJets:
            jet.matchGenParton=999.0

        if self.cfg_comp.isMC and "BB" in self.cfg_comp.name:
            genParticles = self.mchandles['genParticles'].product()
            event.genParticles = map( GenParticle, genParticles)
            for gen in genParticles:
                if abs(gen.pdgId())==5 and gen.mother() and abs(gen.mother().pdgId())==21:
                    for jet in event.cleanJets:
                        dR=deltaR2(jet.eta(), jet.phi(), gen.eta(), gen.phi() )
                        if dR<jet.matchGenParton:
                            jet.matchGenParton=dR

        event.jets30 = [jet for jet in event.jets if jet.pt()>30]
        event.cleanJets30 = [jet for jet in event.cleanJets if jet.pt()>30]
        
#        if len( event.jets30 )>=2:
#            self.counters.counter('jets').inc('at least 2 good jets')
               
#        if len( event.cleanJets30 )>=2:
#            self.counters.counter('jets').inc('at least 2 clean jets')

        event.cleanJets = event.jets
        event.cleanBJets = event.bJets

#        print 'cleanJets = ', len(event.jets)
#        print 'clean_bJets = ', len(event.bJets)

#        if len(event.bJets)>0:
#        if len(event.cleanBJets)>0:
#            import pdb; pdb.set_trace()
#            return False

        self.counters.counter('jets').inc('No b jets')
        return True

    def jerCorrection(self, jet):
        ''' Adds JER correction according to first method at
        https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution

        Requires some attention when genJet matching fails.
        '''
        if not hasattr(jet, 'genJet'):
            return

        #import pdb; pdb.set_trace()
        corrections = [0.052, 0.057, 0.096, 0.134, 0.288]
        maxEtas = [0.5, 1.1, 1.7, 2.3, 5.0]
        eta = abs(jet.eta())

        for i, maxEta in enumerate(maxEtas):
            if eta < maxEta:
                pt = jet.pt()
                deltaPt = (pt - jet.genJet.pt()) * corrections[i]
                totalScale = (pt + deltaPt) / pt

                if totalScale < 0.:
                    totalScale = 0.
                jet.scaleEnergy(totalScale)
                break        

    def jesCorrection(self, jet, scale=0.):
        ''' Adds JES correction in number of sigmas (scale)
        '''
        # Do nothing if nothing to change
        if scale == 0.:
            return

        unc = jet.uncOnFourVectorScale()

        totalScale = 1. + scale * unc

        if totalScale < 0.:
            totalScale = 0.
        jet.scaleEnergy(totalScale)

    def testJetID(self, jet):
        jet.puJetIdPassed = jet.puJetId(wp53x=True)
        jet.pfJetIdPassed = jet.looseJetId()

        if self.cfg_ana.relaxJetId:
            return True
        else:
            return jet.puJetIdPassed and jet.pfJetIdPassed
#            return jet.pfJetIdPassed        
        
    def testJet( self, jet ):
        # 2 is loose pile-up jet id
        return jet.pt() > self.cfg_ana.jetPt and \
               abs( jet.eta() ) < self.cfg_ana.jetEta and \
               self.testJetID(jet)
               # jet.passPuJetId('full', 2)


    def testBJet(self, jet):
        # medium csv working point
        # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BTagPerformanceOP#B_tagging_Operating_Points_for_3
        jet.btagMVA = jet.btag("combinedSecondaryVertexBJetTags")
        jet.btagFlag = self.btagSF.BTagSFcalc.isbtagged(jet.pt(), 
                          jet.eta(),
                          jet.btag("combinedSecondaryVertexBJetTags"),
                          abs(jet.partonFlavour()),
                          not self.cfg_comp.isMC,
                          0,0,
                          self.is2012 )

#        import pdb; pdb.set_trace()
#        print 'btag=', jet.btagMVA, self.testJetID(jet), jet.btagFlag

#               jet.btagFlag and \

        return jet.pt()>20 and \
               abs( jet.eta() ) < 2.4 and \
               jet.btagMVA > 0.679 and \
               self.testJetID(jet)
