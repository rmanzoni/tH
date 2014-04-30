#!/bin/bash

#/eos/cms/store/cmst3/user/cmgtools/CMG/DoubleMu/StoreResults-Run2012C_PromptReco_v2_embedded_trans1_tau132_pttau1_17had2_17_v2-5ef1c0fd428eb740081f19333520fdc8/USER/V5_B/PAT_CMG_V5_14_0

#ProductionTasks.py -w '*.root' -c -N 1 -q 2nd -t <PAT_CMG_X_X_X> --output_wildcard '*.root' --cfg <yuta's_skimming_cfg> `cat samples.txt` 
#cmgtools%/DoubleMu/StoreResults-Run2012C_PromptReco_v2_embedded_trans1_tau132_pttau1_17had2_17_v2-5ef1c0fd428eb740081f19333520fdc8/USER/V5_B/PAT_CMG_V5_14_0

ProductionTasks.py -w '*.root' -c -N 5 -q 1nd -t ETauTau_Yuta_Mar11 --batch_user htautau_group --output_wildcard '*.root' --cfg skim_etautau_cfg.py `cat samples_skim.txt`
