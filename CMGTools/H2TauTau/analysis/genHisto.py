from ROOT import TFile, gDirectory, TH1F, gStyle, gROOT, TTree, TMVA, Double
import math, copy, sys, array
import optparse

#process = ['WZ', 'ZZ', 'tt1l', 'tt2l', 'tH_YtMinus1', 'data']
process = ['WZ', 'ZZ', 'tt1l', 'tt2l', 'TTW', 'TTZ', 'tH_YtMinus1', 'TTH', 'data']
region = ['signal','antiE','antiMu','antiEMu']

### For options
parser = optparse.OptionParser()
parser.add_option('--kNN', action="store", dest="kNN", default='50')
parser.add_option('--cr', action="store", dest="cr", default='f12')
options, args = parser.parse_args()

print '[INFO] kNN = ', options.kNN
print '[INFO] Control region = ', options.cr

gROOT.SetBatch(True)

muonreader = [0 for ii in range(len(process))]
electronreader = [0 for ii in range(len(process))]

def returnkNN(iregion, iprocess, weight_electron, weight_muon):

    kNN_weight = 1.
    if iregion=='antiE':
        if weight_electron==1:
            kNN_weight = 0
            print '[WARNING] 0 weight for e', iprocess, iregion
        else:
            kNN_weight = weight_electron/(1-weight_electron)
    elif iregion=='antiMu':
        if weight_muon==1:
            kNN_weight = 0
            print '[WARNING] warning, 0 weight for mu', iprocess, iregion
        else:
            kNN_weight = weight_muon/(1-weight_muon)
    elif iregion=='antiEMu':
        if weight_electron==1 or weight_muon==1:
            kNN_weight = 0
            print '[WARNING] warning, 0 weight for mu*e', iprocess, iregion
        else:
            kNN_weight = weight_muon*weight_electron/((1-weight_muon)*(1-weight_electron))
    elif iregion=='signal':
        kNN_weight = 1.

    return kNN_weight


for index, pn in enumerate(process):

    e_xml = 'kNN_training/weights/KNN_' + pn + '_electron_' + options.kNN + '.xml'
    m_xml = 'kNN_training/weights/KNN_' + pn + '_muon_' + options.kNN + '.xml'

    if pn in ['WZ','ZZ','tt1l','tt2l','data']:
        pass
    else:
        print 'This is the embarassing !'
        e_xml = 'kNN_training/weights/KNN_data_electron_' + options.kNN + '.xml'
        m_xml = 'kNN_training/weights/KNN_data_muon_' + options.kNN + '.xml'
        

    print '[INFO] electron xml file = ', e_xml
    print '[INFO] muon xml file = ', m_xml

    muonreader[index] = TMVA.Reader("!Color:Silent=T:Verbose=F")
    electronreader[index] = TMVA.Reader("!Color:Silent=T:Verbose=F")        
    mvar_map   = {}
    evar_map   = {}
    
    for var in ['lepton_pt', 'lepton_kNN_jetpt', 'evt_njet']:
        mvar_map[var] = array.array('f',[0])
        muonreader[index].AddVariable(var, mvar_map[var])
        
        evar_map[var] = array.array('f',[0])
        electronreader[index].AddVariable(var, evar_map[var])

    mvaname = 'muon_' + pn
    muonreader[index].BookMVA(mvaname, m_xml)

    mvaname = 'electron_' + pn
    electronreader[index].BookMVA(mvaname, e_xml)

    print 'type of the index = ', type(index), index, ' -> ', mvaname


binning = [20, 30, 40, 50, 60, 70, 80, 100, 130, 300]

# Basic quantities :

h_M     = [[0 for ii in range(len(process))] for i in range(len(region))]
h_kNN_M = [[0 for ii in range(len(process))] for i in range(len(region))]

h_nbjet     = [[0 for ii in range(len(process))] for i in range(len(region))]
h_kNN_nbjet = [[0 for ii in range(len(process))] for i in range(len(region))]

h_njet     = [[0 for ii in range(len(process))] for i in range(len(region))]
h_kNN_njet = [[0 for ii in range(len(process))] for i in range(len(region))]

h_njet30     = [[0 for ii in range(len(process))] for i in range(len(region))]
h_kNN_njet30 = [[0 for ii in range(len(process))] for i in range(len(region))]

h_jet_eta     = [[0 for ii in range(len(process))] for i in range(len(region))]
h_kNN_jet_eta = [[0 for ii in range(len(process))] for i in range(len(region))]

h_jet_eta30     = [[0 for ii in range(len(process))] for i in range(len(region))]
h_kNN_jet_eta30 = [[0 for ii in range(len(process))] for i in range(len(region))]


# Muon-related variables :

h_muon_eta     = [[0 for ii in range(len(process))] for i in range(len(region))]
h_kNN_muon_eta = [[0 for ii in range(len(process))] for i in range(len(region))]

h_muon_phi     = [[0 for ii in range(len(process))] for i in range(len(region))]
h_kNN_muon_phi = [[0 for ii in range(len(process))] for i in range(len(region))]

h_muon_pt     = [[0 for ii in range(len(process))] for i in range(len(region))]
h_kNN_muon_pt = [[0 for ii in range(len(process))] for i in range(len(region))]

h_muon_MT     = [[0 for ii in range(len(process))] for i in range(len(region))]
h_kNN_muon_MT = [[0 for ii in range(len(process))] for i in range(len(region))]


# electron-related variables :

h_electron_eta     = [[0 for ii in range(len(process))] for i in range(len(region))]
h_kNN_electron_eta = [[0 for ii in range(len(process))] for i in range(len(region))]

h_electron_phi     = [[0 for ii in range(len(process))] for i in range(len(region))]
h_kNN_electron_phi = [[0 for ii in range(len(process))] for i in range(len(region))]

h_electron_pt     = [[0 for ii in range(len(process))] for i in range(len(region))]
h_kNN_electron_pt = [[0 for ii in range(len(process))] for i in range(len(region))]

h_electron_MT     = [[0 for ii in range(len(process))] for i in range(len(region))]
h_kNN_electron_MT = [[0 for ii in range(len(process))] for i in range(len(region))]


# tau-related variables :

h_tau_eta     = [[0 for ii in range(len(process))] for i in range(len(region))]
h_kNN_tau_eta = [[0 for ii in range(len(process))] for i in range(len(region))]

h_tau_phi     = [[0 for ii in range(len(process))] for i in range(len(region))]
h_kNN_tau_phi = [[0 for ii in range(len(process))] for i in range(len(region))]

h_tau_pt     = [[0 for ii in range(len(process))] for i in range(len(region))]
h_kNN_tau_pt = [[0 for ii in range(len(process))] for i in range(len(region))]

h_tau_MT     = [[0 for ii in range(len(process))] for i in range(len(region))]
h_kNN_tau_MT = [[0 for ii in range(len(process))] for i in range(len(region))]




outfile = TFile('Plot_' + options.cr + '_kNN' + options.kNN + '.root','recreate')

for rindex, iregion in enumerate(region):
    for index, iprocess in enumerate(process):

        print iregion, '(', rindex, ')', iprocess, '(', index, ') is processing'

        hname = 'h_M_' + iregion + '_' + iprocess
        h_M[rindex][index] = TH1F(hname, hname, 10,0,200)
        h_M[rindex][index].Sumw2()

        hname = 'h_kNN_M_' + iregion + '_' + iprocess
        h_kNN_M[rindex][index] = TH1F(hname, hname, 10,0,200)
        h_kNN_M[rindex][index].Sumw2()

        hname = 'h_nbjet_' + iregion + '_' + iprocess
        h_nbjet[rindex][index] = TH1F(hname, hname, 10,0,10)
        h_nbjet[rindex][index].Sumw2()

        hname = 'h_kNN_nbjet_' + iregion + '_' + iprocess
        h_kNN_nbjet[rindex][index] = TH1F(hname, hname, 10,0,10)
        h_kNN_nbjet[rindex][index].Sumw2()

        hname = 'h_njet_' + iregion + '_' + iprocess
        h_njet[rindex][index] = TH1F(hname, hname, 10,0,10)
        h_njet[rindex][index].Sumw2()

        hname = 'h_kNN_njet_' + iregion + '_' + iprocess
        h_kNN_njet[rindex][index] = TH1F(hname, hname, 10,0,10)
        h_kNN_njet[rindex][index].Sumw2()

        hname = 'h_njet30_' + iregion + '_' + iprocess
        h_njet30[rindex][index] = TH1F(hname, hname, 10,0,10)
        h_njet30[rindex][index].Sumw2()

        hname = 'h_kNN_njet30_' + iregion + '_' + iprocess
        h_kNN_njet30[rindex][index] = TH1F(hname, hname, 10,0,10)
        h_kNN_njet30[rindex][index].Sumw2()

        hname = 'h_jet_eta_' + iregion + '_' + iprocess
        h_jet_eta[rindex][index] = TH1F(hname, hname, 10,0,10)
        h_jet_eta[rindex][index].Sumw2()

        hname = 'h_kNN_jet_eta_' + iregion + '_' + iprocess
        h_kNN_jet_eta[rindex][index] = TH1F(hname, hname, 10,0,10)
        h_kNN_jet_eta[rindex][index].Sumw2()

        hname = 'h_jet_eta30_' + iregion + '_' + iprocess
        h_jet_eta30[rindex][index] = TH1F(hname, hname, 10,0,10)
        h_jet_eta30[rindex][index].Sumw2()

        hname = 'h_kNN_jet_eta30_' + iregion + '_' + iprocess
        h_kNN_jet_eta30[rindex][index] = TH1F(hname, hname, 10,0,10)
        h_kNN_jet_eta30[rindex][index].Sumw2()


        hname = 'h_muon_eta_' + iregion + '_' + iprocess
        h_muon_eta[rindex][index] = TH1F(hname, hname, 10,-5,5)
        h_muon_eta[rindex][index].Sumw2()

        hname = 'h_kNN_muon_eta_' + iregion + '_' + iprocess
        h_kNN_muon_eta[rindex][index] = TH1F(hname, hname, 10,-5,5)
        h_kNN_muon_eta[rindex][index].Sumw2()

        hname = 'h_muon_phi_' + iregion + '_' + iprocess
        h_muon_phi[rindex][index] = TH1F(hname, hname, 10,-3.14,3.14)
        h_muon_phi[rindex][index].Sumw2()

        hname = 'h_kNN_muon_phi_' + iregion + '_' + iprocess
        h_kNN_muon_phi[rindex][index] = TH1F(hname, hname, 10,-3.14,3.14)
        h_kNN_muon_phi[rindex][index].Sumw2()

        hname = 'h_muon_pt_' + iregion + '_' + iprocess
        h_muon_pt[rindex][index] = TH1F(hname, hname, 20,0,300)
        h_muon_pt[rindex][index].Sumw2()

        hname = 'h_kNN_muon_pt_' + iregion + '_' + iprocess
        h_kNN_muon_pt[rindex][index] = TH1F(hname, hname, 20,0,300)
        h_kNN_muon_pt[rindex][index].Sumw2()

        hname = 'h_muon_MT_' + iregion + '_' + iprocess
        h_muon_MT[rindex][index] = TH1F(hname, hname, 20,0,300)
        h_muon_MT[rindex][index].Sumw2()

        hname = 'h_kNN_muon_MT_' + iregion + '_' + iprocess
        h_kNN_muon_MT[rindex][index] = TH1F(hname, hname, 20,0,300)
        h_kNN_muon_MT[rindex][index].Sumw2()



        hname = 'h_electron_eta_' + iregion + '_' + iprocess
        h_electron_eta[rindex][index] = TH1F(hname, hname, 10,-5,5)
        h_electron_eta[rindex][index].Sumw2()

        hname = 'h_kNN_electron_eta_' + iregion + '_' + iprocess
        h_kNN_electron_eta[rindex][index] = TH1F(hname, hname, 10,-5,5)
        h_kNN_electron_eta[rindex][index].Sumw2()

        hname = 'h_electron_phi_' + iregion + '_' + iprocess
        h_electron_phi[rindex][index] = TH1F(hname, hname, 10,-3.14,3.14)
        h_electron_phi[rindex][index].Sumw2()

        hname = 'h_kNN_electron_phi_' + iregion + '_' + iprocess
        h_kNN_electron_phi[rindex][index] = TH1F(hname, hname, 10,-3.14,3.14)
        h_kNN_electron_phi[rindex][index].Sumw2()

        hname = 'h_electron_pt_' + iregion + '_' + iprocess
        h_electron_pt[rindex][index] = TH1F(hname, hname, 20,0,300)
        h_electron_pt[rindex][index].Sumw2()

        hname = 'h_kNN_electron_pt_' + iregion + '_' + iprocess
        h_kNN_electron_pt[rindex][index] = TH1F(hname, hname, 20,0,300)
        h_kNN_electron_pt[rindex][index].Sumw2()

        hname = 'h_electron_MT_' + iregion + '_' + iprocess
        h_electron_MT[rindex][index] = TH1F(hname, hname, 20,0,300)
        h_electron_MT[rindex][index].Sumw2()

        hname = 'h_kNN_electron_MT_' + iregion + '_' + iprocess
        h_kNN_electron_MT[rindex][index] = TH1F(hname, hname, 20,0,300)
        h_kNN_electron_MT[rindex][index].Sumw2()


        hname = 'h_tau_eta_' + iregion + '_' + iprocess
        h_tau_eta[rindex][index] = TH1F(hname, hname, 10,-5,5)
        h_tau_eta[rindex][index].Sumw2()

        hname = 'h_kNN_tau_eta_' + iregion + '_' + iprocess
        h_kNN_tau_eta[rindex][index] = TH1F(hname, hname, 10,-5,5)
        h_kNN_tau_eta[rindex][index].Sumw2()

        hname = 'h_tau_phi_' + iregion + '_' + iprocess
        h_tau_phi[rindex][index] = TH1F(hname, hname, 10,-3.14,3.14)
        h_tau_phi[rindex][index].Sumw2()

        hname = 'h_kNN_tau_phi_' + iregion + '_' + iprocess
        h_kNN_tau_phi[rindex][index] = TH1F(hname, hname, 10,-3.14,3.14)
        h_kNN_tau_phi[rindex][index].Sumw2()

        hname = 'h_tau_pt_' + iregion + '_' + iprocess
        h_tau_pt[rindex][index] = TH1F(hname, hname, 20,0,300)
        h_tau_pt[rindex][index].Sumw2()

        hname = 'h_kNN_tau_pt_' + iregion + '_' + iprocess
        h_kNN_tau_pt[rindex][index] = TH1F(hname, hname, 20,0,300)
        h_kNN_tau_pt[rindex][index].Sumw2()

        hname = 'h_tau_MT_' + iregion + '_' + iprocess
        h_tau_MT[rindex][index] = TH1F(hname, hname, 20,0,300)
        h_tau_MT[rindex][index].Sumw2()

        hname = 'h_kNN_tau_MT_' + iregion + '_' + iprocess
        h_kNN_tau_MT[rindex][index] = TH1F(hname, hname, 20,0,300)
        h_kNN_tau_MT[rindex][index].Sumw2()



for rindex, iregion in enumerate(region):
    for index, iprocess in enumerate(process):

        print iregion, '(', rindex, ')', iprocess, '(', index, ') is processing',  'muon_', iprocess

        fname = 'root_process/' + options.cr + '_' + iregion + '_' + iprocess + '.root'
        myfile = TFile(fname)
        main = gDirectory.Get('Tree')

        total = 0

        for jentry in xrange(main.GetEntries()):


            ientry = main.LoadTree(jentry)
            nb = main.GetEntry(jentry)

            total += 1
                    
#            if not main.evt_nbjet==1:
#                continue
        
            weight_muon = 0.5
            weight_electron = 0.5

#            total += 1

            if iregion=='antiMu' or iregion=='antiEMu':

                mvar_map['lepton_pt'][0] = main.muon_pt
                mvar_map['lepton_kNN_jetpt'][0] = main.muon_kNN_jetpt
                mvar_map['evt_njet'][0] = main.evt_njet + 1
                
                mvaname = 'muon_' + iprocess

                weight_muon = muonreader[index].EvaluateMVA(mvaname)
                
            if iregion=='antiE' or iregion=='antiEMu':

                evar_map['lepton_pt'][0] = main.electron_pt
                evar_map['lepton_kNN_jetpt'][0] = main.electron_kNN_jetpt
                evar_map['evt_njet'][0] = main.evt_njet + 1
                
                mvaname = 'electron_' + iprocess
                weight_electron = electronreader[index].EvaluateMVA(mvaname)

            kNN_weight = returnkNN(iregion, iprocess, weight_electron, weight_muon)
            

            h_M[rindex][index].Fill(main.evt_L2T, main.evt_weight)
            h_kNN_M[rindex][index].Fill(main.evt_L2T, main.evt_weight*kNN_weight)

            h_nbjet[rindex][index].Fill(main.evt_nbjet, main.evt_weight)
            h_kNN_nbjet[rindex][index].Fill(main.evt_nbjet, main.evt_weight*kNN_weight)

            h_njet[rindex][index].Fill(main.evt_njet_or, main.evt_weight)
            h_kNN_njet[rindex][index].Fill(main.evt_njet_or, main.evt_weight*kNN_weight)

            h_njet30[rindex][index].Fill(main.evt_njet_or30, main.evt_weight)
            h_kNN_njet30[rindex][index].Fill(main.evt_njet_or30, main.evt_weight*kNN_weight)

            h_jet_eta[rindex][index].Fill(main.evt_max_jet_eta, main.evt_weight)
            h_kNN_jet_eta[rindex][index].Fill(main.evt_max_jet_eta, main.evt_weight*kNN_weight)

            h_jet_eta30[rindex][index].Fill(main.evt_max_jet_eta30, main.evt_weight)
            h_kNN_jet_eta30[rindex][index].Fill(main.evt_max_jet_eta30, main.evt_weight*kNN_weight)


            h_muon_eta[rindex][index].Fill(main.muon_eta, main.evt_weight)
            h_kNN_muon_eta[rindex][index].Fill(main.muon_eta, main.evt_weight*kNN_weight)

            h_muon_phi[rindex][index].Fill(main.muon_phi, main.evt_weight)
            h_kNN_muon_phi[rindex][index].Fill(main.muon_phi, main.evt_weight*kNN_weight)

            h_muon_pt[rindex][index].Fill(main.muon_pt, main.evt_weight)
            h_kNN_muon_pt[rindex][index].Fill(main.muon_pt, main.evt_weight*kNN_weight)

            h_muon_MT[rindex][index].Fill(main.muon_MT, main.evt_weight)
            h_kNN_muon_MT[rindex][index].Fill(main.muon_MT, main.evt_weight*kNN_weight)


            h_electron_eta[rindex][index].Fill(main.electron_eta, main.evt_weight)
            h_kNN_electron_eta[rindex][index].Fill(main.electron_eta, main.evt_weight*kNN_weight)

            h_electron_phi[rindex][index].Fill(main.electron_phi, main.evt_weight)
            h_kNN_electron_phi[rindex][index].Fill(main.electron_phi, main.evt_weight*kNN_weight)

            h_electron_pt[rindex][index].Fill(main.electron_pt, main.evt_weight)
            h_kNN_electron_pt[rindex][index].Fill(main.electron_pt, main.evt_weight*kNN_weight)

            h_electron_MT[rindex][index].Fill(main.electron_MT, main.evt_weight)
            h_kNN_electron_MT[rindex][index].Fill(main.electron_MT, main.evt_weight*kNN_weight)


            h_tau_eta[rindex][index].Fill(main.tau_eta, main.evt_weight)
            h_kNN_tau_eta[rindex][index].Fill(main.tau_eta, main.evt_weight*kNN_weight)

            h_tau_phi[rindex][index].Fill(main.tau_phi, main.evt_weight)
            h_kNN_tau_phi[rindex][index].Fill(main.tau_phi, main.evt_weight*kNN_weight)

            h_tau_pt[rindex][index].Fill(main.tau_pt, main.evt_weight)
            h_kNN_tau_pt[rindex][index].Fill(main.tau_pt, main.evt_weight*kNN_weight)

            h_tau_MT[rindex][index].Fill(main.tau_MT, main.evt_weight)
            h_kNN_tau_MT[rindex][index].Fill(main.tau_MT, main.evt_weight*kNN_weight)


        if iprocess=='data':
            print iregion, total

outfile.Write()
outfile.Close()
