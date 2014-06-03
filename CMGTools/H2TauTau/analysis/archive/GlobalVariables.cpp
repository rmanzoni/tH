#include "pxl/hep.hh"
#include "pxl/core.hh"
#include "pxl/core/macros.hh"
#include "pxl/core/PluginManager.hh"
#include "pxl/modules/Module.hh"
#include "pxl/modules/ModuleFactory.hh"
#include "string.h"

#include "TVectorD.h"
#include "TMatrixD.h"

// Jan Steggemann
// New, October 2012

static pxl::Logger loggerGlobalVariables("GlobalVariables");

class GlobalVariables : public pxl::Module
{
private:
    pxl::Source* _source;

    double _minJetPt;
    double _maxJetEta;
    double _minJetCSV;
    
    double _minLeptonPt;
    double _maxLeptonEta;
    
    int64_t _njets;
    
    bool _minChi2System;

    std::string _jetName;
    std::string _neutrinoName;
    std::string _leptonName;
    
    std::string _eventViewName;

public:
    GlobalVariables() : Module(), _minJetPt(30.), _maxJetEta(2.5)
    {
        addOption("jetName", "Name of jet", "Jet");
        addOption("neutrinoName", "Name of neutrino", "Neutrino");
        addOption("leptonName", "Name of lepton", "Muon");

        addOption("eventViewName", "Name of eventview", "Reconstructed");

        addOption("minJetPt", "Minimal pt of jet", 30.);
        addOption("maxJetEta", "Maximum abs(eta) of jet", 2.5);
        addOption("minJetCSV", "Minimum CSV value to be considered as a b jet", 0.679);

        addOption("minLeptonPt", "Minimal pt of lepton", 20.);
        addOption("maxLeptonEta", "Maximum abs(eta) of lepton", 2.5);

        addSink("input", "Input");
        addSource("output", "Output");

    }

    ~GlobalVariables()
    {
    }

    // every Module needs a unique type
    static const std::string &getStaticType()
    {
        static std::string type ("GlobalVariables");
        return type;
    }

    // static and dynamic methods are needed
    const std::string &getType() const
    {
        return getStaticType();
    }

    bool isRunnable() const
    {
        // this module does not provide events, so return false
        return false;
    }

    /*
    void initialize() throw (std::runtime_error)
    {
    }*/

    void beginJob()
    {
        getOption("jetName", _jetName);
        getOption("leptonName", _leptonName);
        getOption("neutrinoName", _neutrinoName);

        getOption("eventViewName", _eventViewName);

        getOption("minJetPt", _minJetPt);
        getOption("maxJetEta", _maxJetEta);
        getOption("minJetCSV", _minJetCSV);
        getOption("minLeptonPt", _minLeptonPt);
        getOption("maxLeptonEta", _maxLeptonEta);

        loggerGlobalVariables(pxl::LOG_LEVEL_INFO, "Begin job");

        _source = getSource("output");
    }
    
    void endJob()
    {
    }

    bool analyse(pxl::Sink *sink)
    {
        try
        {
            pxl::Event *event  = dynamic_cast<pxl::Event *> (sink->get());

            int jetCounter = 0;
            if (!event)
            {
                loggerGlobalVariables(pxl::LOG_LEVEL_ERROR, "No event passed");
                return false;
            }

            std::vector<pxl::EventView*> myEventviews;
            event->getObjectsOfType(myEventviews);
            
            pxl::EventView* recEvtView = 0;
            
            for (std::vector<pxl::EventView*>::const_iterator it= myEventviews.begin(); it!= myEventviews.end(); ++it)
            {
                if ((*it)->getName() == _eventViewName)
                {
                    recEvtView = *it;
                }
            }
            
            if (recEvtView == 0)
            {
                loggerGlobalVariables(pxl::LOG_LEVEL_ERROR, "Rec eventview not found");
                return false;
            }
            
            std::vector<pxl::Particle*> particles;
            recEvtView->getObjectsOfType(particles);
            
            std::vector<pxl::Particle*> jets;
            std::vector<pxl::Particle*> bjets;
            std::vector<pxl::Particle*> ljets;
            pxl::Particle* lepton = 0;
            pxl::Particle* neutrino = 0;
            
            // find all jets, the lepton, and the neutrino
            for (size_t i = 0; i < particles.size(); ++i)
            {
                pxl::Particle* p = particles[i];

                if (p->getName() == _jetName && p->getPt() > _minJetPt && fabs(p->getEta()) < _maxJetEta)
                {
                    jets.push_back(p);
                    if (double(p->getUserRecord("bid_combinedSecondaryVertexBJetTags")) > _minJetCSV)
                        bjets.push_back(p);
                    else
                        ljets.push_back(p);

                }
                else if (p->getName() == _leptonName && p->getPt() > _minLeptonPt && fabs(p->getEta()) < _maxLeptonEta)
                {
                    if (p->hasUserRecord("selected") && p->getUserRecord("selected"))
                        lepton = p;
                }
                else if (p->getName() == _neutrinoName)
                    neutrino = p;
            }
            
            std::vector<pxl::Particle*> allParticles(jets);
            allParticles.push_back(lepton);
            allParticles.push_back(neutrino);
            
            recEvtView->setUserRecord("sumJetPt", calculateSumPt(jets));
            recEvtView->setUserRecord("sumBJetPt", calculateSumPt(bjets));
            recEvtView->setUserRecord("sumLJetPt", calculateSumPt(ljets));
            recEvtView->setUserRecord("sumAllPt", calculateSumPt(allParticles));

            recEvtView->setUserRecord("sumJetVectorPt", calculateVectorPt(jets));
            recEvtView->setUserRecord("sumBJetVectorPt", calculateVectorPt(bjets));
            recEvtView->setUserRecord("sumLJetVectorPt", calculateVectorPt(ljets));
            recEvtView->setUserRecord("sumAllVectorPt", calculateVectorPt(allParticles));
            
            recEvtView->setUserRecord("sumJetVectorPz", calculateVectorPz(jets));
            recEvtView->setUserRecord("sumBJetVectorPz", calculateVectorPz(bjets));
            recEvtView->setUserRecord("sumLJetVectorPz", calculateVectorPz(ljets));
            recEvtView->setUserRecord("sumAllVectorPz", calculateVectorPz(allParticles));
            
            recEvtView->setUserRecord("sumJetE", calculateSumE(jets));
            recEvtView->setUserRecord("sumBJetE", calculateSumE(bjets));
            recEvtView->setUserRecord("sumLJetE", calculateSumE(ljets));
            recEvtView->setUserRecord("sumAllE", calculateSumE(allParticles));

            recEvtView->setUserRecord("massJets", calculateMass(jets));
            recEvtView->setUserRecord("massBJets", calculateMass(bjets));
            recEvtView->setUserRecord("massLJets", calculateMass(ljets));
            recEvtView->setUserRecord("massAll", calculateMass(allParticles));
            
            std::pair<double, double> ptMassMax = maxMass(bjets);
            recEvtView->setUserRecord("maxMassBJets", ptMassMax.first);
            recEvtView->setUserRecord("ptMaxMassBJets", ptMassMax.second);
            
            std::pair<double, double> ptMassMin = minMass(bjets);
            recEvtView->setUserRecord("minMassBJets", ptMassMin.first);
            recEvtView->setUserRecord("ptMinMassBJets", ptMassMin.second);
            
            recEvtView->setUserRecord("maxDeltaPhiBJets", maxDeltaPhi(bjets));
            recEvtView->setUserRecord("minDeltaPhiBJets", minDeltaPhi(bjets));
            
            std::pair<double, double> ptMassClosest = massPtClosest(bjets);
            recEvtView->setUserRecord("massClosestBJets", ptMassClosest.first);
            recEvtView->setUserRecord("ptClosestBJets", ptMassClosest.second);
            
            std::pair<double, double> ptMassFurthest = massPtFurthest(bjets);
            recEvtView->setUserRecord("massFurthestBJets", ptMassFurthest.first);
            recEvtView->setUserRecord("ptFurthestBJets", ptMassFurthest.second);
            
            recEvtView->setUserRecord("rapidityJets", calculateRapidity(jets));
            recEvtView->setUserRecord("rapidityBJets", calculateRapidity(bjets));
            recEvtView->setUserRecord("rapidityLJets", calculateRapidity(ljets));
            recEvtView->setUserRecord("rapidityAll", calculateRapidity(allParticles));
            
            recEvtView->setUserRecord("aplanarity", calculateAplanarity(recEvtView, allParticles, ""));
            recEvtView->setUserRecord("aplanarityJets", calculateAplanarity(recEvtView, jets, "jets"));
            recEvtView->setUserRecord("aplanarityBJets", calculateAplanarity(recEvtView, bjets, "bjets"));
            recEvtView->setUserRecord("aplanarityLJets", calculateAplanarity(recEvtView, ljets, "ljets"));
            
            recEvtView->setUserRecord("sphericity", calculateSphericity(recEvtView, allParticles, ""));
            recEvtView->setUserRecord("sphericityJets", calculateSphericity(recEvtView, jets, "jets"));
            recEvtView->setUserRecord("sphericityBJets", calculateSphericity(recEvtView, bjets, "bjets"));
            recEvtView->setUserRecord("sphericityLJets", calculateSphericity(recEvtView, ljets, "ljets"));
            
            recEvtView->setUserRecord("foxWolfram0", foxWolframN(0, allParticles));
            recEvtView->setUserRecord("foxWolfram1", foxWolframN(1, allParticles));
            recEvtView->setUserRecord("foxWolfram2", foxWolframN(2, allParticles));
            recEvtView->setUserRecord("foxWolfram3", foxWolframN(3, allParticles));
            recEvtView->setUserRecord("foxWolfram4", foxWolframN(4, allParticles));
            
            recEvtView->setUserRecord("sumAbsJetChargeJets", sumAbsJetCharge(jets));
            recEvtView->setUserRecord("sumAbsJetChargeBJets", sumAbsJetCharge(bjets));
            recEvtView->setUserRecord("sumAbsJetChargeLJets", sumAbsJetCharge(ljets));
            
            recEvtView->setUserRecord("sumJetChargeJets", sumJetCharge(jets));
            recEvtView->setUserRecord("sumJetChargeBJets", sumJetCharge(bjets));
            recEvtView->setUserRecord("sumJetChargeLJets", sumJetCharge(ljets));
            
            recEvtView->setUserRecord("maxDeltaJetChargeJets", maxDeltaJetCharge(jets));
            recEvtView->setUserRecord("maxDeltaJetChargeBJets", maxDeltaJetCharge(bjets));
            recEvtView->setUserRecord("maxDeltaJetChargeLJets", maxDeltaJetCharge(ljets));
            
            recEvtView->setUserRecord("minCSV", minCSV(bjets));
            recEvtView->setUserRecord("maxCSV", maxCSV(bjets));
            recEvtView->setUserRecord("sumCSV", sumCSV(bjets));
            recEvtView->setUserRecord("averageCSV", averageCSV(bjets));
            
            recEvtView->setUserRecord("n_tchpt_jets", countBJets("bid_trackCountingHighPurBJetTags", 3.41, jets));
            recEvtView->setUserRecord("n_jpl_jets", countBJets("bid_jetProbabilityBJetTags", 0.275, jets));
            recEvtView->setUserRecord("n_jpm_jets", countBJets("bid_jetProbabilityBJetTags", 0.545, jets));
            recEvtView->setUserRecord("n_jpt_jets", countBJets("bid_jetProbabilityBJetTags", 0.790, jets));
            recEvtView->setUserRecord("n_csvl_jets", countBJets("bid_combinedSecondaryVertexBJetTags", 0.244, jets));
            recEvtView->setUserRecord("n_csvm_jets", countBJets("bid_combinedSecondaryVertexBJetTags", 0.679, jets));
            recEvtView->setUserRecord("n_csvt_jets", countBJets("bid_combinedSecondaryVertexBJetTags", 0.898, jets));
            recEvtView->setUserRecord("n_softmuonl_jets", countBJets("bid_softMuonBJetTags", 0., jets));
            recEvtView->setUserRecord("n_softmuonm_jets", countBJets("bid_softMuonBJetTags", 0.1, jets));
            recEvtView->setUserRecord("n_softmuont_jets", countBJets("bid_softMuonBJetTags", 0.2, jets));
            
            
            pxl::Particle* minCSVbjet = minCSVJet(bjets);
            
            recEvtView->setUserRecord("dl2dMinCSV", minCSVbjet->hasUserRecord("dl_2D") ? float(minCSVbjet->getUserRecord("dl_2D")) : 0. );
            recEvtView->setUserRecord("dl3dMinCSV", minCSVbjet->hasUserRecord("dl_3D") ? float(minCSVbjet->getUserRecord("dl_3D")) : 0. );
            recEvtView->setUserRecord("secvtxMassMinCSV", minCSVbjet->hasUserRecord("secvtxMass") ? float(minCSVbjet->getUserRecord("secvtxMass")) : 0. );

            recEvtView->setUserRecord("averageCSVLjets", averageCSV(ljets));
            recEvtView->setUserRecord("sumCSVLjets", sumCSV(ljets));
            recEvtView->setUserRecord("maxCSVLjets", sumCSV(ljets));
            recEvtView->setUserRecord("averageCSValljets", averageCSV(jets));

            recEvtView->setUserRecord("minDeltaRjets", minDeltaR(jets));
            recEvtView->setUserRecord("minDeltaRBjets", minDeltaR(bjets));
            recEvtView->setUserRecord("minDeltaRLjets", minDeltaR(ljets));
            
            recEvtView->setUserRecord("maxDeltaRjets", maxDeltaR(jets));
            recEvtView->setUserRecord("maxDeltaRBjets", maxDeltaR(bjets));
            recEvtView->setUserRecord("maxDeltaRLjets", maxDeltaR(ljets));
            
            recEvtView->setUserRecord("maxDeltaRSeparationjets", maxDeltaRSeparation(jets));
            recEvtView->setUserRecord("maxDeltaRSeparationBjets", maxDeltaRSeparation(bjets));
            recEvtView->setUserRecord("maxDeltaRSeparationLjets", maxDeltaRSeparation(ljets));
            
            recEvtView->setUserRecord("maxDeltaEtajets", maxDeltaEta(jets));
            recEvtView->setUserRecord("maxDeltaEtaBjets", maxDeltaEta(bjets));
            recEvtView->setUserRecord("maxDeltaEtaLjets", maxDeltaEta(ljets));
            
            recEvtView->setUserRecord("minDeltaEtajets", minDeltaEta(jets));
            recEvtView->setUserRecord("minDeltaEtaBjets", minDeltaEta(bjets));
            recEvtView->setUserRecord("minDeltaEtaLjets", minDeltaEta(ljets));
            
            recEvtView->setUserRecord("maxDeltaEtaSeparationjets", maxDeltaEtaSeparation(jets));
            recEvtView->setUserRecord("maxDeltaEtaSeparationBjets", maxDeltaEtaSeparation(bjets));
            recEvtView->setUserRecord("maxDeltaEtaSeparationLjets", maxDeltaEtaSeparation(ljets));
            
            recEvtView->setUserRecord("minDeltaRleptonjets", minDeltaR(lepton, jets));
            recEvtView->setUserRecord("minDeltaRleptonBjets", minDeltaR(lepton, bjets));
            recEvtView->setUserRecord("minDeltaRleptonLjets", minDeltaR(lepton, ljets));
            
            recEvtView->setUserRecord("maxDeltaRleptonjets", maxDeltaR(lepton, jets));
            recEvtView->setUserRecord("maxDeltaRleptonBjets", maxDeltaR(lepton, bjets));
            recEvtView->setUserRecord("maxDeltaRleptonLjets", maxDeltaR(lepton, ljets));
            
            recEvtView->setUserRecord("maxDeltaEtaleptonjets", maxDeltaEta(lepton, jets));
            recEvtView->setUserRecord("maxDeltaEtaleptonBjets", maxDeltaEta(lepton, bjets));
            recEvtView->setUserRecord("maxDeltaEtaleptonLjets", maxDeltaEta(lepton, ljets));
            
            recEvtView->setUserRecord("maxDeltaEtaJetPairSeparationJets", maxDeltaEtaPairSeparation(jets, jets));
            recEvtView->setUserRecord("maxDeltaRJetPairSeparationJets", maxDeltaRPairSeparation(jets, jets));
            
            recEvtView->setUserRecord("maxDeltaEtaBJetPairSeparationJets", maxDeltaEtaPairSeparation(bjets, jets));
            recEvtView->setUserRecord("maxDeltaRBJetPairSeparationJets", maxDeltaRPairSeparation(bjets, jets));
            
            recEvtView->setUserRecord("maxDeltaEtaLJetPairSeparationJets", maxDeltaEtaPairSeparation(ljets, jets));
            recEvtView->setUserRecord("maxDeltaRLJetPairSeparationJets", maxDeltaRPairSeparation(ljets, jets));

            recEvtView->setUserRecord("maxDeltaEtaJetPairSeparationLepton", maxDeltaEtaPairSeparation(jets, lepton));
            recEvtView->setUserRecord("maxDeltaRJetPairSeparationLepton", maxDeltaRPairSeparation(jets, lepton));
            
            recEvtView->setUserRecord("maxDeltaEtaBJetPairSeparationLepton", maxDeltaEtaPairSeparation(bjets, lepton));
            recEvtView->setUserRecord("maxDeltaRBJetPairSeparationLepton", maxDeltaRPairSeparation(bjets, lepton));
            
            recEvtView->setUserRecord("maxDeltaEtaLJetPairSeparationLepton", maxDeltaEtaPairSeparation(ljets, lepton));
            recEvtView->setUserRecord("maxDeltaRLJetPairSeparationLepton", maxDeltaRPairSeparation(ljets, lepton));

            double ptWeightedEta = calculatePtWeightedEta(allParticles);
            double ptWeightedEtaJets = calculatePtWeightedEta(jets);
            
            recEvtView->setUserRecord("ptWeightedEta", ptWeightedEta);
            recEvtView->setUserRecord("ptWeightedEtaJets", ptWeightedEtaJets);
            
            recEvtView->setUserRecord("maxDeltaEtaJetsAverageAll", maxDeltaEta(ptWeightedEta, jets));
            recEvtView->setUserRecord("maxDeltaEtaJetsAverageJets", maxDeltaEta(ptWeightedEtaJets, jets));
            
            recEvtView->setUserRecord("maxDeltaEtaBJetsAverageAll", maxDeltaEta(ptWeightedEta, bjets));
            recEvtView->setUserRecord("maxDeltaEtaBJetsAverageJets", maxDeltaEta(ptWeightedEtaJets, bjets));
            
            recEvtView->setUserRecord("maxDeltaEtaLJetsAverageAll", maxDeltaEta(ptWeightedEta, ljets));
            recEvtView->setUserRecord("maxDeltaEtaLJetsAverageJets", maxDeltaEta(ptWeightedEtaJets, ljets));
            
            _source->setTargets(event);
            return _source->processTargets();
        }
        catch(std::exception &e)
        {
            throw std::runtime_error(getName()+": "+e.what());
        }
        catch(...)
        {
            throw std::runtime_error(getName()+": unknown exception");
        }

        loggerGlobalVariables(pxl::LOG_LEVEL_ERROR, "Should not be here");
        return false;
    }
    
    int32_t countBJets(const std::string& algo, double minVal, const std::vector<pxl::Particle*>& particles)
    {
        int32_t nbjets = 0;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            if (double(particles[i]->getUserRecord(algo)) > minVal)
                nbjets++;
        }
        return nbjets;
    }
    
    double calculateSumPt(const std::vector<pxl::Particle*>& particles)
    {
        double sum = 0.;
        for (size_t i = 0; i < particles.size(); ++i)
            sum += particles[i]->getPt();
        return sum;
    }
    
    double calculateVectorPt(const std::vector<pxl::Particle*>& particles)
    {
        double sumpx = 0.;
        double sumpy = 0.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            sumpx += particles[i]->getPx();
            sumpy += particles[i]->getPy();
        }
        return std::sqrt(sumpx * sumpx + sumpy * sumpy);
    }
    
    double calculateVectorPz(const std::vector<pxl::Particle*>& particles)
    {
        double sumpz = 0.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            sumpz += particles[i]->getPz();
        }
        return sumpz;
    }
    
    double calculatePtWeightedEta(const std::vector<pxl::Particle*>& particles)
    {
        double sumEta;
        double sumPt;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            sumEta += particles[i]->getEta() * particles[i]->getPt();
            sumPt += particles[i]->getPt();
        }
        return sumEta/sumPt;
    }
    
    double calculateSumE(const std::vector<pxl::Particle*>& particles)
    {
        double sum = 0.;
        for (size_t i = 0; i < particles.size(); ++i)
            sum += particles[i]->getE();
        return sum;
    }
    
    double calculateMass(pxl::Particle* p1, pxl::Particle* p2, pxl::Particle* p3 = 0)
    {
        // FIXME: Explicit implementation without vector is faster...
        std::vector<pxl::Particle*> particles;
        particles.reserve(3);
        particles.push_back(p1);
        particles.push_back(p2);
        if (p3 != 0)
            particles.push_back(p3);
        return calculateMass(particles);
    }
    
    double calculateMass(const std::vector<pxl::Particle*>& particles)
    {
        double E = 0., px = 0., py = 0., pz = 0.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            E += particles[i]->getE();
            px += particles[i]->getPx();
            py += particles[i]->getPy();
            pz += particles[i]->getPz();
        }
        double m2 = E*E - px * px - py * py - pz * pz;
        if (m2 >= 0.)
            return std::sqrt(m2);
        else
            return -1.;
    }
    
        
    double calculateRapidity(pxl::Particle* p1, pxl::Particle* p2, pxl::Particle* p3 = 0)
    {
        // FIXME: Explicit implementation without vector is faster...
        std::vector<pxl::Particle*> particles;
        particles.reserve(3);
        particles.push_back(p1);
        particles.push_back(p2);
        if (p3 != 0)
            particles.push_back(p3);
        return calculateRapidity(particles);
    }
    
    double calculateRapidity(const std::vector<pxl::Particle*>& particles)
    {
        double E = 0., px = 0., py = 0., pz = 0.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            E += particles[i]->getE();
            px += particles[i]->getPx();
            py += particles[i]->getPy();
            pz += particles[i]->getPz();
        }
        return 0.5 * log((E + pz)/(E - pz));
    }
    
    double CosTheta(pxl::Particle* particle1, pxl::Particle* particle2)
    {
        if (particle1 == particle2)
            return 1.;
        
        double px1 = particle1->getPx();
        double py1 = particle1->getPy();
        double pz1 = particle1->getPy();
        double px2 = particle2->getPx();
        double py2 = particle2->getPy();
        double pz2 = particle2->getPy();
        
        double cos_angle = double(px1 * px2 + py1 * py2 + pz1 * pz2);
        cos_angle = cos_angle / sqrt(px1 * px1 + py1 * py1 + pz1 * pz1);
        cos_angle = cos_angle / sqrt(px2 * px2 + py2 * py2 + pz2 * pz2);
        return cos_angle;
    }
    
    double CosTheta2(pxl::Particle* particle1, pxl::Particle* particle2)
    {
        if (particle1 == particle2)
            return 1.;
        
        double px1 = particle1->getPx();
        double py1 = particle1->getPy();
        double pz1 = particle1->getPy();
        double px2 = particle2->getPx();
        double py2 = particle2->getPy();
        double pz2 = particle2->getPy();
        
        double cos_angle2 = double(px1 * px2 + py1 * py2 + pz1 * pz2);
        cos_angle2 *= cos_angle2;
        cos_angle2 = cos_angle2 / (px1 * px1 + py1 * py1 + pz1 * pz1);
        cos_angle2 = cos_angle2 / (px2 * px2 + py2 * py2 + pz2 * pz2);
        return cos_angle2;
    }

    
    double calculateAplanarity(pxl::EventView* eventview, const std::vector<pxl::Particle*>& particles, const std::string& label = "")
    {
        double lambda3 = 0.;
        if (eventview->hasUserRecord("SphericityLambda3"+label))
            lambda3 = double(eventview->getUserRecord("SphericityLambda3"+label));
        else
        {
            calculateSphericityEigenVectors(eventview, particles, label);
            if (eventview->hasUserRecord("SphericityLambda3"+label))
                lambda3 = eventview->getUserRecord("SphericityLambda3"+label);
            else
                loggerGlobalVariables(pxl::LOG_LEVEL_ERROR, "Calculating sphericity failed");
        }

        return (3. / 2. * lambda3);
    }

    double calculateSphericity(pxl::EventView* eventview, const std::vector<pxl::Particle*>& particles, const std::string& label = "")
    {
        double lambda2 = 0.;
        double lambda3 = 0.;

        if (! (eventview->hasUserRecord("SphericityLambda3"+label) && eventview->hasUserRecord("SphericityLambda2"+label)))
        {
            calculateSphericityEigenVectors(eventview, particles, label);
            if (! (eventview->hasUserRecord("SphericityLambda3"+label) && eventview->hasUserRecord("SphericityLambda2"+label)))
            {
                loggerGlobalVariables(pxl::LOG_LEVEL_ERROR, "Ccalculating sphericity failed");
            }
        }

        lambda2 = double(eventview->getUserRecord("SphericityLambda2"+label));
        lambda3 = double(eventview->getUserRecord("SphericityLambda3"+label));

        return (3. / 2. * (lambda2 + lambda3));
    }

    void calculateSphericityEigenVectors(pxl::EventView* eventview, const std::vector<pxl::Particle*>& particles, const std::string& label = "")
    {
        TMatrixD momentumTensor(3, 3);
        double p2_sum = 0.;

        for (std::vector<pxl::Particle*>::const_iterator itParticle= particles.begin(); itParticle!= particles.end(); itParticle++)
        {
            double px = (*itParticle)->getPx();
            double py = (*itParticle)->getPy();
            double pz = (*itParticle)->getPz();

            //fill momentumTensor by hand
            momentumTensor(0, 0) += px * px;
            momentumTensor(0,1) += px * py;
            momentumTensor(0,2) += px * pz;
            momentumTensor(1,0) += py * px;
            momentumTensor(1,1) += py * py;
            momentumTensor(1,2) += py * pz;
            momentumTensor(2,0) += pz * px;
            momentumTensor(2,1) += pz * py;
            momentumTensor(2,2) += pz * pz;

            //add 3 momentum squared to sum
            p2_sum += (px * px + py * py + pz * pz);
        }
        //Divide the sums with the p2 sum
        if (p2_sum != 0.)
        {
            for (int i=0; i<3; i++) //px, py, pz
            {
                for (int j=0; j<3; j++)//px, py, pz
                {
                    momentumTensor(i,j) = momentumTensor(i,j) / p2_sum;
                }
            }
        }

        TVectorD ev(3);
        momentumTensor.EigenVectors(ev);

        //some checks & limited precision of TVectorD
        double ev0 = fabs(ev[0]) < 0.000000000000001 ? 0 : ev[0];
        double ev1 = fabs(ev[1]) < 0.000000000000001 ? 0 : ev[1];
        double ev2 = fabs(ev[2]) < 0.000000000000001 ? 0 : ev[2];

        if ((ev0 < ev1) || (ev1 < ev2))
        {
            std::cout << "0: "<<ev0<<std::endl;
            std::cout << "1: "<< ev1 <<std::endl;
            std::cout << "2: "<<ev2<<std::endl;
            loggerGlobalVariables(pxl::LOG_LEVEL_ERROR, "Calculating eigenvectors failed.");
        }

        eventview->setUserRecord("SphericityLambda1"+label, ev0);
        eventview->setUserRecord("SphericityLambda2"+label, ev1);
        eventview->setUserRecord("SphericityLambda3"+label, ev2);

    }
    
    double foxWolframN(int n, const std::vector<pxl::Particle*>& particles)
    {
        double evis = 0.; // visible energy
        double res = 0.; // fox-wolfram-moment
        
        for (size_t i = 0; i < particles.size(); ++i)
        {
            pxl::Particle* p1 = particles[i];
            evis += p1->getE();
            for (size_t j = 0; j < particles.size(); ++j)
            {
                pxl::Particle* p2 = particles[j];
                res += p1->getP() * p2->getP() * legendreN(n, p1, p2);
            }
        }
        
        res = res/evis/evis; // divide by (E_vis)^2
        return res;
    }
    
    double averageCSV(const std::vector<pxl::Particle*>& jets)
    {
        double sum = 0.;
        for (size_t i = 0; i < jets.size(); ++i)
        {
            sum += double(jets[i]->getUserRecord("bid_combinedSecondaryVertexBJetTags"));
        }
        return sum/double(jets.size());
    }
    
    double sumCSV(const std::vector<pxl::Particle*>& jets)
    {
        double sum = 0.;
        for (size_t i = 0; i < jets.size(); ++i)
        {
            sum += double(jets[i]->getUserRecord("bid_combinedSecondaryVertexBJetTags"));
        }
        return sum;
    }
    
    double maxCSV(const std::vector<pxl::Particle*>& jets)
    {
        double max = 0.;
        for (size_t i = 0; i < jets.size(); ++i)
        {
            double csv = jets[i]->getUserRecord("bid_combinedSecondaryVertexBJetTags");
            if (csv > max)
                max = csv;
        }
        return max;
    }
    
    double minCSV(const std::vector<pxl::Particle*>& jets)
    {
        double min = 99999999.;
        for (size_t i = 0; i < jets.size(); ++i)
        {
            double csv = jets[i]->getUserRecord("bid_combinedSecondaryVertexBJetTags");
            if (csv < min)
                min = csv;
        }
        return min;
    }
    
    pxl::Particle* minCSVJet(const std::vector<pxl::Particle*>& jets)
    {
        double min = 99999999.;
        pxl::Particle* minJet = 0;
        for (size_t i = 0; i < jets.size(); ++i)
        {
            double csv = jets[i]->getUserRecord("bid_combinedSecondaryVertexBJetTags");
            if (csv < min)
            {
                min = csv;
                minJet = jets[i];
            }
        }
        return minJet;
    }
    
    double sumJetCharge(const std::vector<pxl::Particle*>& jets)
    {
        double sum = 0.;
        for (size_t i = 0; i < jets.size(); ++i)
        {
            sum += double(jets[i]->getUserRecord("jetCharge"));
        }
        return sum;
    }
    
    double sumAbsJetCharge(const std::vector<pxl::Particle*>& jets)
    {
        double sum = 0.;
        for (size_t i = 0; i < jets.size(); ++i)
        {
            sum += fabs(double(jets[i]->getUserRecord("jetCharge")));
        }
        return sum;
    }
    
    
    double maxDeltaJetCharge(const std::vector<pxl::Particle*>& jets)
    {
        double max = 0.;
        for (size_t i = 0; i < jets.size(); ++i)
        {
            for (size_t j = i + 1; j < jets.size(); ++j)
            {
                double val = fabs(float(jets[i]->getUserRecord("jetCharge")) - float(jets[j]->getUserRecord("jetCharge")));
                if (val > max)
                {
                    max = val;
                }
            }
        }
        return max;
    }
    
    
    
    double minDeltaR(const std::vector<pxl::Particle*>& particles)
    {
        double min = 99999999.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            for (size_t j = i + 1; j < particles.size(); ++j)
            {
                double dr = particles[i]->getVector().deltaR(&particles[j]->getVector());
                if (dr < min)
                    min = dr;
            }
        }
        return min;
    }
    
    std::pair<double, double> massPtClosest(const std::vector<pxl::Particle*>& particles)
    {
        double min = 99999999.;
        double mass = 0.;
        double pt = 0.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            for (size_t j = i + 1; j < particles.size(); ++j)
            {
                double dr = particles[i]->getVector().deltaR(&particles[j]->getVector());
                if (dr < min)
                {
                    min = dr;
                    mass = (particles[i]->getVector() + particles[j]->getVector()).getMass();
                    pt = (particles[i]->getVector() + particles[j]->getVector()).getPt();
                }
            }
        }
        return std::pair<double, double>(mass, pt);
    }
    
    std::pair<double, double> massPtFurthest(const std::vector<pxl::Particle*>& particles)
    {
        double max = 0.;
        double mass = 0.;
        double pt = 0.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            for (size_t j = i + 1; j < particles.size(); ++j)
            {
                double dr = particles[i]->getVector().deltaR(&particles[j]->getVector());
                if (dr > max)
                {
                    max = dr;
                    mass = (particles[i]->getVector() + particles[j]->getVector()).getMass();
                    pt = (particles[i]->getVector() + particles[j]->getVector()).getPt();
                }
            }
        }
        return std::pair<double, double>(mass, pt);
    }
    
    double maxDeltaR(const std::vector<pxl::Particle*>& particles)
    {
        double max = 0.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            for (size_t j = i + 1; j < particles.size(); ++j)
            {
                double dr = particles[i]->getVector().deltaR(&particles[j]->getVector());
                if (dr > max)
                    max = dr;
            }
        }
        return max;
    }
    
    double maxDeltaEta(const std::vector<pxl::Particle*>& particles)
    {
        double max = 0.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            for (size_t j = i + 1; j < particles.size(); ++j)
            {
                double deta = fabs(particles[i]->getVector().deltaEta(&particles[j]->getVector()));
                if (deta > max)
                    max = deta;
            }
        }
        return max;
    }
    
    double minDeltaEta(const std::vector<pxl::Particle*>& particles)
    {
        double min = 99999999.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            for (size_t j = i + 1; j < particles.size(); ++j)
            {
                double deta = fabs(particles[i]->getVector().deltaEta(&particles[j]->getVector()));
                if (deta < min)
                    min = deta;
            }
        }
        return min;
    }
    
    double maxDeltaPhi(const std::vector<pxl::Particle*>& particles)
    {
        double max = 0.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            for (size_t j = i + 1; j < particles.size(); ++j)
            {
                double dphi = fabs(particles[i]->getVector().deltaPhi(&particles[j]->getVector()));
                if (dphi > max)
                    max = dphi;
            }
        }
        return max;
    }
    
    double minDeltaPhi(const std::vector<pxl::Particle*>& particles)
    {
        double min = 99999999.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            for (size_t j = i + 1; j < particles.size(); ++j)
            {
                double dphi = fabs(particles[i]->getVector().deltaPhi(&particles[j]->getVector()));
                if (dphi < min)
                    min = dphi;
            }
        }
        return min;
    }
    
    std::pair<double, double> minMass(const std::vector<pxl::Particle*>& particles)
    {
        double min = 99999999.;
        double pt = 0.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            for (size_t j = i + 1; j < particles.size(); ++j)
            {
                double mass = (particles[i]->getVector() + particles[j]->getVector()).getMass();
                if (mass < min)
                {
                    min = mass;
                    pt = (particles[i]->getVector() + particles[j]->getVector()).getPt();
                }
            }
        }
        return std::pair<double, double>(min, pt);
    }
    
    std::pair<double, double> maxMass(const std::vector<pxl::Particle*>& particles)
    {
        double max = 0.;
        double pt = 0.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            for (size_t j = i + 1; j < particles.size(); ++j)
            {
                double mass = (particles[i]->getVector() + particles[j]->getVector()).getMass();
                if (mass > max)
                {
                    max = mass;
                    pt = (particles[i]->getVector() + particles[j]->getVector()).getPt();
                }
            }
        }
        return std::pair<double, double>(max, pt);
    }
    
    
    double minDeltaR(const pxl::Particle* particle, const std::vector<pxl::Particle*>& particles)
    {
        double min = 99999999.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            double dr = particles[i]->getVector().deltaR(&particle->getVector());
            if (dr < min)
                min = dr;

        }
        return min;
    }
    
    double maxDeltaR(const pxl::Particle* particle, const std::vector<pxl::Particle*>& particles)
    {
        double max = 0.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            double dr = particles[i]->getVector().deltaR(&particle->getVector());
            if (dr > max)
                max = dr;

        }
        return max;
    }
    
    double maxDeltaEta(const pxl::Particle* particle, const std::vector<pxl::Particle*>& particles)
    {
        double max = 0.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            double deta = fabs(particles[i]->getVector().deltaEta(&particle->getVector()));
            if (deta > max)
                max = deta;

        }
        return max;
    }
    
        
    double maxDeltaEta(double eta, const std::vector<pxl::Particle*>& particles)
    {
        double max = 0.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            double deta = fabs(particles[i]->getVector().getEta() - eta);
            if (deta > max)
                max = deta;

        }
        return max;
    }
    
    // Find particle that is most separated from all other particles. 
    // Metric: Closest DeltaR to other particle. Return according deltaR
    double maxDeltaRSeparation(const std::vector<pxl::Particle*>& particles)
    {
        double max = 0.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            pxl::Particle* p1 = particles[i];
            double min = 99999999.;
            for (size_t j = 0; j < particles.size(); ++j)
            {
                if (i != j)
                {
                double dr = p1->getVector().deltaR(&particles[j]->getVector());
                if (dr < min)
                    min = dr;
                }
            }
            
            if (min > max)
                max = min;
        }
        return max;
    }
    
    // Find particle that is most separated from all other particles. 
    // Metric: Closest abs(DeltaEta) to other particle. Return according abs(deltaEta)
    double maxDeltaEtaSeparation(const std::vector<pxl::Particle*>& particles)
    {
        double max = 0.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            pxl::Particle* p1 = particles[i];
            double min = 99999999.;
            for (size_t j = 0; j < particles.size(); ++j)
            {
                if (i != j)
                {
                    double deta = fabs(p1->getVector().deltaEta(&particles[j]->getVector()));
                    if (deta < min)
                        min = deta;
                }
            }
            
            if (min > max)
                max = min;
        }
        return max;
    }
    
    double maxDeltaEtaPairSeparation(const std::vector<pxl::Particle*>& particles, const std::vector<pxl::Particle*>& targets)
    {
        double max = 0.;
        if (particles.size() < 2 || targets.size() == 0)
            return -1.;
        for (size_t i = 0; i < particles.size(); ++i)
        {
            pxl::Particle* p1 = particles[i];
            for (size_t i2 = 0; i2 < particles.size(); ++i2)
            {
                if (i != i2)
                {
                    
                    pxl::Particle* p2 = particles[i2];
//                     pxl::LorentzVector combVector;
//                     combVector += particles[i]->getVector();
//                     combVector += particles[i2]->getVector();
                    double weightedEta = (p1->getEta() * p1->getPt() + p2->getEta() * p2->getPt())/(p1->getPt() + p2->getPt());
                    double min = 99999999.;
                    for (size_t j = 0; j < targets.size(); ++j)
                    {
                        pxl::Particle* t = targets[j];
                        if (p1 != t && p2 != t)
                        {
                            double deta = fabs(weightedEta - t->getEta());
                            if (deta < min)
                                min = deta;
                        }
                    }
                    if (min > max)
                        max = min;
                }
            }
        }
        return max;
    }
    
    double maxDeltaRPairSeparation(const std::vector<pxl::Particle*>& particles, const std::vector<pxl::Particle*>& targets)
    {
        double max = 0.;
        if (particles.size() < 2 || targets.size() == 0)
            return -1.;
        
        for (size_t i = 0; i < particles.size(); ++i)
        {
            pxl::Particle* p1 = particles[i];
            
            for (size_t i2 = 0; i2 < particles.size(); ++i2)
            {
                if (i != i2)
                {
                    pxl::Particle* p2 = particles[i2];
                    
                    pxl::LorentzVector combVector;
                    combVector += p1->getVector();
                    combVector += p2->getVector();
                    
                    double min = 99999999.;
                    for (size_t j = 0; j < targets.size(); ++j)
                    {
                        pxl::Particle* t = targets[j];
                        if (p1 != t && p2 != t)
                        {
                            double dr = combVector.deltaR(&t->getVector());
                            if (dr < min)
                                min = dr;
                        }

                    }
                    if (min > max)
                        max = min;
                }
            }
        }
        return max;
    }
    
    double maxDeltaEtaPairSeparation(const std::vector<pxl::Particle*>& particles, pxl::Particle* p)
    {
        std::vector<pxl::Particle*> v;
        v.push_back(p);
        return maxDeltaEtaPairSeparation(particles, v);
    }

    double maxDeltaRPairSeparation(const std::vector<pxl::Particle*>& particles, pxl::Particle* p)
    {
        std::vector<pxl::Particle*> v;
        v.push_back(p);
        return maxDeltaRPairSeparation(particles, v);
    }
    
    double legendreN(int n, pxl::Particle* p1, pxl::Particle* p2)
    {
        if (n == 0)
            return 1.;
        else if (n == 1)
            return CosTheta(p1, p2);
        else if (n == 2)
            return 0.5 * (3. * CosTheta2(p1, p2) - 1.);
        else if (n == 3)
        {
            double x = CosTheta(p1, p2);
            return 0.5 * (5. * x * x * x - 3. * x);
        }
        else if (n == 4)
        {
            double x = CosTheta2(p1, p2);
            return 0.125 * (35. * x * x - 30. * x + 3.);
        }
        
        loggerGlobalVariables(pxl::LOG_LEVEL_ERROR, "Legendre polynomials beyond n = 4 not implemented.");
        return 0.;
    }
    
    void destroy()
    {
        delete this;
    }
};

PXL_MODULE_INIT(GlobalVariables)
PXL_PLUGIN_INIT
