import FWCore.ParameterSet.Config as cms

process = cms.Process("EMUTAU")

process.source = cms.Source("PoolSource",
    noEventSort = cms.untracked.bool(True),
    duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
    fileNames = cms.untracked.vstring('/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_10_1_SOs.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_11_1_Q5y.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_12_1_pAv.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_13_1_b41.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_14_1_hkT.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_15_1_D3d.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_16_1_YQU.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_17_1_SWJ.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_18_1_S8N.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_19_1_kRV.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_1_1_2y8.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_20_1_b5Q.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_21_1_e1Y.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_22_1_VIj.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_23_1_N6c.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_24_1_Mom.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_25_1_MsT.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_26_1_fyY.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_27_1_ghs.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_29_1_DmM.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_2_1_0Lr.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_30_1_K7P.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_31_1_Xke.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_32_1_d43.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_33_1_3pC.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_34_1_3jm.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_35_1_E9G.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_36_1_JoN.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_37_1_NgG.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_38_1_8a9.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_39_1_Lcg.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_3_1_x74.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_40_1_z1G.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_41_1_C5F.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_42_1_a4w.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_43_1_DXe.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_44_1_z2U.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_45_1_z7S.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_46_1_FoX.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_47_1_hFv.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_48_1_VNf.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_49_1_vAp.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_4_1_sFo.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_50_1_1lg.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_51_1_op5.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_52_1_u1t.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_53_1_Lbq.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_54_1_6ds.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_55_1_d5n.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_56_1_FVE.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_57_1_qXi.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_58_1_IS7.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_59_1_5lL.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_5_1_hix.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_60_1_Ku7.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_61_1_LWa.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_62_1_K3C.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_63_1_3Ta.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_64_1_lOk.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_65_1_iue.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_66_1_Zyb.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_67_1_y02.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_68_1_xqc.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_69_1_7Kv.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_6_1_8mv.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_70_1_oc2.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_71_1_wfR.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_72_1_9sn.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_73_1_Uww.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_74_1_0pV.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_75_1_WqF.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_76_1_qh5.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_77_1_Jfd.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_78_1_o8F.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_79_1_Q9o.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_7_1_nnA.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_80_1_Diw.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_81_1_ANx.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_82_1_p5i.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_83_1_3C4.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_84_1_JFE.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_85_1_0RR.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_86_1_zts.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_87_1_Zut.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_88_1_ivE.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_89_1_ibf.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_8_1_0q7.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_90_1_iN3.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_91_1_gdo.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_92_1_xae.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_93_1_Ho7.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_94_1_Yfn.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_95_1_JHq.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_96_1_dUq.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_97_1_6eX.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_98_1_xnu.root', 
        '/store/cmst3/group/htautau/CMG/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_16_0/EMuTau_Yuta_Feb26/cmgTuple_9_1_iND.root')
)
process.cmgElectronCount = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("cmgElectronSel"),
    minNumber = cms.uint32(1)
)


process.cmgElectronSel = cms.EDFilter("CmgElectronSelector",
    src = cms.InputTag("cmgElectronSel"),
    cut = cms.string('pt() > 10 && abs(eta()) < 2.5')
)


process.cmgMuonCount = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("cmgMuonSel"),
    minNumber = cms.uint32(1)
)


process.cmgMuonSel = cms.EDFilter("CmgMuonSelector",
    src = cms.InputTag("cmgMuonSel"),
    cut = cms.string('pt() > 10 && abs(eta()) < 2.4')
)


process.cmgTauCount = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("cmgTauSel"),
    minNumber = cms.uint32(1)
)


process.cmgTauSel = cms.EDFilter("CmgTauSelector",
    src = cms.InputTag("cmgTauSel"),
    cut = cms.string('pt() > 20 && abs(eta()) < 2.3 && tauID("decayModeFinding")')
)


process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('cmgTuple.root'),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('p')
    ),
    outputCommands = cms.untracked.vstring('keep *')
)


process.p = cms.Path(process.cmgMuonSel+process.cmgElectronSel+process.cmgTauSel+process.cmgMuonCount+process.cmgElectronCount+process.cmgTauCount)


process.endpath = cms.EndPath(process.out)


process.MessageLogger = cms.Service("MessageLogger",
    suppressInfo = cms.untracked.vstring(),
    debugs = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    suppressDebug = cms.untracked.vstring(),
    cout = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    cerr_stats = cms.untracked.PSet(
        threshold = cms.untracked.string('WARNING'),
        output = cms.untracked.string('cerr'),
        optionalPSet = cms.untracked.bool(True)
    ),
    warnings = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    default = cms.untracked.PSet(

    ),
    statistics = cms.untracked.vstring('cerr_stats'),
    cerr = cms.untracked.PSet(
        INFO = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        noTimeStamps = cms.untracked.bool(False),
        FwkReport = cms.untracked.PSet(
            reportEvery = cms.untracked.int32(5),
            optionalPSet = cms.untracked.bool(True),
            limit = cms.untracked.int32(10000000)
        ),
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000)
        ),
        Root_NoDictionary = cms.untracked.PSet(
            optionalPSet = cms.untracked.bool(True),
            limit = cms.untracked.int32(0)
        ),
        threshold = cms.untracked.string('INFO'),
        FwkJob = cms.untracked.PSet(
            optionalPSet = cms.untracked.bool(True),
            limit = cms.untracked.int32(0)
        ),
        FwkSummary = cms.untracked.PSet(
            reportEvery = cms.untracked.int32(1),
            optionalPSet = cms.untracked.bool(True),
            limit = cms.untracked.int32(10000000)
        ),
        optionalPSet = cms.untracked.bool(True)
    ),
    FrameworkJobReport = cms.untracked.PSet(
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        optionalPSet = cms.untracked.bool(True),
        FwkJob = cms.untracked.PSet(
            optionalPSet = cms.untracked.bool(True),
            limit = cms.untracked.int32(10000000)
        )
    ),
    suppressWarning = cms.untracked.vstring(),
    errors = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    destinations = cms.untracked.vstring('warnings', 
        'errors', 
        'infos', 
        'debugs', 
        'cout', 
        'cerr'),
    debugModules = cms.untracked.vstring(),
    infos = cms.untracked.PSet(
        optionalPSet = cms.untracked.bool(True),
        Root_NoDictionary = cms.untracked.PSet(
            optionalPSet = cms.untracked.bool(True),
            limit = cms.untracked.int32(0)
        ),
        placeholder = cms.untracked.bool(True)
    ),
    categories = cms.untracked.vstring('FwkJob', 
        'FwkReport', 
        'FwkSummary', 
        'Root_NoDictionary'),
    fwkJobReports = cms.untracked.vstring('FrameworkJobReport')
)


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.maxLuminosityBlocks = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

