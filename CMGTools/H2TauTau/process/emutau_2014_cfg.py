import copy, os
import shelve
import CMGTools.RootTools.fwlite.Config as cfg
from CMGTools.RootTools.fwlite.Config import printComps

from CMGTools.H2TauTau.triggerMap import pathsAndFilters
from CMGTools.H2TauTau.proto.weights.weighttable import mu_id_taumu_2012, mu_iso_taumu_2012
from CMGTools.RootTools.RootTools import *

# set True when you want to throw the jobs
# jobmode = True
jobmode = False
selector = False

if jobmode:
    selector = False



# Andrew Summer 13 (MC is identical to the previous one)
puFileMC   = '/afs/cern.ch/user/a/agilbert/public/HTT_Pileup/13-09-13/MC_Summer12_PU_S10-600bins.root'
puFileData = '/afs/cern.ch/user/a/agilbert/public/HTT_Pileup/13-09-13/Data_Pileup_2012_ReRecoPixel-600bins.root'

mc_vertexWeight = None

mc_tauEffWeight_mc = 'effTau_muTau_MC_2012ABCDSummer13'
mc_muEffWeight_mc  = 'effMu_muTau_MC_2012ABCD'
mc_tauEffWeight    = 'effTau_muTau_Data_2012ABCDSummer13'
mc_muEffWeight     = 'effMu_muTau_Data_2012ABCDSummer13'

elist = []

print 'eventSelector = ', len(elist)

eventSelector = cfg.Analyzer(
    'EventSelector',
    toSelect = elist
    )

jsonAna = cfg.Analyzer(
    'JSONAnalyzer',
    )

triggerAna = cfg.Analyzer(
    'DiTriggerAnalyzer'
    )

vertexAna = cfg.Analyzer(
    'VertexAnalyzer',
    goodVertices = 'goodPVFilter',
    vertexWeight = mc_vertexWeight,
    fixedWeight = 1,
    verbose = False,
    )

embedWeighter = cfg.Analyzer(
    'EmbedWeighter',
    isRecHit = False,
    verbose = False
    )

pileUpAna = cfg.Analyzer(
    'PileUpAnalyzer',
    true = True
    )

genErsatzAna = cfg.Analyzer(
    'GenErsatzAnalyzer',
    verbose = False
    )

EMuTauAna = cfg.Analyzer(
    'WHEMTAnalyzer',
#    scaleShift1 = tauScaleShift,
#    pt1 = 20,
#    eta1 = 2.3,
#    iso1 = None,
#    pt2 = 20,
#    eta2 = 2.1,
#    iso2 = 0.1,
#    m_min = 10,
#    m_max = 99999,
#    dR_min = 0.5,
    triggerMap = pathsAndFilters,
#    mvametsigs = 'mvaMETTauMu',
#    verbose = False
    )

dyJetsFakeAna = cfg.Analyzer(
    'DYJetsFakeAnalyzer',
    leptonType = 13,
    src = 'genParticlesPruned',
    )

WNJetsAna = cfg.Analyzer(
    'WNJetsAnalyzer',
    verbose = False
    )

NJetsAna = cfg.Analyzer(
    'NJetsAnalyzer',
    fillTree = True,
    verbose = False
    )

WNJetsTreeAna = cfg.Analyzer(
    'WNJetsTreeAnalyzer'
    )

higgsWeighter = cfg.Analyzer(
    'HiggsPtWeighter',
    src = 'genParticlesPruned',
    )

tauDecayModeWeighter = cfg.Analyzer(
    'TauDecayModeWeighter',
    )

tauFakeRateWeighter = cfg.Analyzer(
    'TauFakeRateWeighter'
    )

tauWeighter = cfg.Analyzer(
    'LeptonWeighter_tau',
    effWeight = mc_tauEffWeight,
    effWeightMC = mc_tauEffWeight_mc,
    lepton = 'leg1',
    verbose = False,
    disable = False,
    )

muonWeighter = cfg.Analyzer(
    'LeptonWeighter_mu',
    effWeight = mc_muEffWeight,
    effWeightMC = mc_muEffWeight_mc,
    lepton = 'leg2',
    verbose = False,
    disable = False,
    idWeight = mu_id_taumu_2012,
    isoWeight = mu_iso_taumu_2012
    )



# defined for vbfAna and eventSorter
vbfKwargs = dict( Mjj = 500,
                  deltaEta = 3.5
                  )


jetAna = cfg.Analyzer(
    'JetAnalyzerEMT',
    jetCol = 'cmgPFJetSel',
    jetPt = 20.,
    jetEta = 4.7,
    btagSFseed = 123456,
    relaxJetId = False,
    jerCorr = False,
    #jesCorr = 1.,
    )

vbfSimpleAna = cfg.Analyzer(
    'VBFSimpleAnalyzer',
    vbfMvaWeights = '',
    cjvPtCut = 30.,
    **vbfKwargs
    )


treeProducer = cfg.Analyzer(
    'H2TauTauTreeProducerEMT2'
    )


#########################################################################################
# sample definition
from CMGTools.H2TauTau.proto.samples.run2012.emuTau_YutaFeb12 import *
#########################################################################################

for mc in MC_list:
    mc.puFileMC = puFileMC
    mc.puFileData = puFileData

selectedComponents = []

seq_list = [
            jsonAna,
            triggerAna,
            vertexAna,
            EMuTauAna,
            jetAna,
            pileUpAna,
            treeProducer,
            ]

if jobmode == False and selector:
    seq_list.insert(0, eventSelector)

if jobmode:
    seq_list = [
        jsonAna,
        triggerAna,
        vertexAna,
        EMuTauAna,
        jetAna,
        pileUpAna,
        treeProducer,
        ]

print 'sequence = ', seq_list
sequence = cfg.Sequence(seq_list)


selectedComponents = [comp for comp in selectedComponents if comp.dataset_entries > 0]

selectedComponents = allsamples

if jobmode:
    selectedComponents = allsamples


if not jobmode:
    for comp in selectedComponents:
        comp.splitFactor = 8

config = cfg.Config( components = selectedComponents,
                     sequence = sequence )

printComps(config.components, True)
