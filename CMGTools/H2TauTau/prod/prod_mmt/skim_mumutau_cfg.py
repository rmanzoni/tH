import FWCore.ParameterSet.Config as cms

from CMGTools.Common.Tools.cmsswRelease import cmsswIs44X,cmsswIs52X

sep_line = '-'*70

########## CONTROL CARDS

process = cms.Process("MUTAUTAU")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(3000) )

process.maxLuminosityBlocks = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
    )

# -1 : process all files
numberOfFilesToProcess = 5




# Input  & JSON             -------------------------------------------------


# process.setName_('H2TAUTAU')


dataset_user = 'cmgtools'
#dataset_name = '/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_8_0'
#dataset_name = '/WH_ZH_TTH_HToTauTau_M-125_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_8_0'
#dataset_name = '/WH_ZH_TTH_HToTauTau_M-125_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5/PAT_CMG_V5_10_0'
#dataset_name = '/DoubleMu/Run2012A-22Jan2013-v1/AOD/PAT_CMG_V5_15_0'
dataset_name = '/MuEG/Run2012A-22Jan2013-v1/AOD/PAT_CMG_V5_15_0'
#dataset_name = '/TTH_Inclusive_M-125_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5/PAT_CMG_V5_17_0'
dataset_files = 'cmgTuple.*root'


# creating the source
from CMGTools.Production.datasetToSource import *
process.source = datasetToSource(
    dataset_user,
    dataset_name,
    dataset_files,
    )

# restricting the number of files to process to a given number
if numberOfFilesToProcess>0:
    process.source.fileNames = process.source.fileNames[:numberOfFilesToProcess]


###ProductionTaskHook$$$

#process.load('CMGTools.Common.skims.cmgDiMuonSel_cfi')
#process.load('CMGTools.Common.skims.cmgDiMuonCount_cfi')
process.load('CMGTools.Common.skims.cmgTauSel_cfi')
process.load('CMGTools.Common.skims.cmgTauCount_cfi')
process.load('CMGTools.Common.skims.cmgMuonSel_cfi')
process.load('CMGTools.Common.skims.cmgMuonCount_cfi')
process.load('CMGTools.Common.skims.cmgElectronSel_cfi')
process.load('CMGTools.Common.skims.cmgElectronCount_cfi')

#process.cmgDiMuonSel.src = 'cmgDiMuonSel'
#process.cmgDiMuonSel.cut = ('leg1().pt() >20 && leg2().pt() > 10 && abs(leg1.eta()) < 2.4 && abs(leg2().eta()) < 2.4')
#process.cmgDiMuonCount.minNumber = 1

process.cmgMuonSel.src = 'cmgMuonSel'
process.cmgMuonSel.cut = ('pt() > 10 && abs(eta()) < 2.1')
#process.cmgMuonSel.cut = ('pt() > 10 && abs(eta()) < 2.4')
#process.cmgMuonSel.cut = ('pt() > 5 && abs(eta()) < 2.4')
process.cmgMuonCount.minNumber = 2

process.cmgElectronSel.src = 'cmgElectronSel'
process.cmgElectronSel.cut = ('pt() > 10 && abs(eta()) < 2.5')
process.cmgElectronCount.minNumber = 1


process.cmgTauSel.src = 'cmgTauSel'
process.cmgTauSel.cut = ('pt() > 20 && abs(eta()) < 2.3 && tauID("decayModeFinding")')
#process.cmgTauSel.cut = ('pt() > 20 && abs(eta()) < 2.5 && tauID("decayModeFinding")')
process.cmgTauCount.minNumber = 1

#process.p = cms.Path( process.cmgDiMuonSel +
#                      process.cmgTauSel +
#                      process.cmgDiMuonCount +
#                      process.cmgTauCount)

process.p = cms.Path( process.cmgMuonSel +
#                      process.cmgElectronSel +
                      process.cmgTauSel +
                      process.cmgMuonCount +
#                      process.cmgElectronCount +
                      process.cmgTauCount)

process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string('cmgTuple.root'),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    # save PAT Layer 1 output; you need a '*' to
    # unpack the list of commands 'patEventContent'
    outputCommands = cms.untracked.vstring('keep *')
    )

process.endpath = cms.EndPath(process.out)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

