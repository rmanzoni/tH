// -*- C++ -*-
//
// Package:    ESRecoSummary
// Class:      ESRecoSummary
// Original Author:  Martina Malberti
// 
// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Common/interface/EventBase.h"
#include "DataFormats/Provenance/interface/EventAuxiliary.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"


#include "Geometry/CaloTopology/interface/CaloTopology.h"
#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloSubdetectorGeometry.h"
#include "Geometry/CaloEventSetup/interface/CaloTopologyRecord.h"
#include "Geometry/CaloTopology/interface/CaloSubdetectorTopology.h"
#include "DataFormats/GeometryVector/interface/GlobalPoint.h"
#include "Geometry/EcalAlgo/interface/EcalBarrelGeometry.h"
#include "Geometry/EcalAlgo/interface/EcalEndcapGeometry.h"

#include "DataFormats/EcalDetId/interface/EBDetId.h"
#include "DataFormats/EcalDetId/interface/EEDetId.h"
#include "DataFormats/EcalDetId/interface/ESDetId.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "DataFormats/EgammaReco/interface/SuperCluster.h"
#include "DataFormats/EgammaReco/interface/SuperClusterFwd.h"
#include "DataFormats/EgammaReco/interface/BasicCluster.h"
#include "DataFormats/EgammaReco/interface/BasicClusterFwd.h"
#include "DataFormats/EgammaReco/interface/PreshowerCluster.h"
#include "DataFormats/EgammaReco/interface/PreshowerClusterFwd.h"
#include "RecoEcal/EgammaCoreTools/interface/EcalClusterTools.h"
#include "RecoEcal/EgammaCoreTools/interface/EcalTools.h"
#include "RecoLocalCalo/EcalRecAlgos/interface/EcalSeverityLevelAlgo.h"
#include "RecoLocalCalo/EcalRecAlgos/interface/EcalCleaningAlgo.h"
#include "RecoEcal/EgammaCoreTools/interface/EcalRecHitLess.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/JetReco/interface/CaloJetCollection.h"

#include "DQMOffline/Ecal/interface/ESRecoSummary.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "MagneticField/Engine/interface/MagneticField.h"

#include "TVector3.h"

#include <iostream>
#include <cmath>
#include <fstream>

//
// constructors and destructor
//
ESRecoSummary::ESRecoSummary(const edm::ParameterSet& ps)
{

  prefixME_ = ps.getUntrackedParameter<std::string>("prefixME", "");

  //now do what ever initialization is needed
  esRecHitCollection_        = ps.getParameter<edm::InputTag>("recHitCollection_ES");
  esClusterCollectionX_      = ps.getParameter<edm::InputTag>("ClusterCollectionX_ES");
  esClusterCollectionY_      = ps.getParameter<edm::InputTag>("ClusterCollectionY_ES");

  dqmStore_ = edm::Service<DQMStore>().operator->();

  // Monitor Elements (ex THXD)
  dqmStore_->setCurrentFolder(prefixME_ + "/ESRecoSummary"); // to organise the histos in folders

  superClusterCollection_EE_ = ps.getParameter<edm::InputTag>("superClusterCollection_EE");
     
  // Preshower ----------------------------------------------
  h_recHits_ES_energyMax      = dqmStore_->book1D("recHits_ES_energyMax","recHits_ES_energyMax",200,0.,0.01);
  h_recHits_ES_time           = dqmStore_->book1D("recHits_ES_time","recHits_ES_time",200,-100.,100.);

  h_esClusters_energy_plane1 = dqmStore_->book1D("esClusters_energy_plane1","esClusters_energy_plane1",200,0.,0.01);
  h_esClusters_energy_plane2 = dqmStore_->book1D("esClusters_energy_plane2","esClusters_energy_plane2",200,0.,0.01);
  h_esClusters_energy_ratio  = dqmStore_->book1D("esClusters_energy_ratio","esClusters_energy_ratio",200,0.,20.);

}



ESRecoSummary::~ESRecoSummary()
{
        // do anything here that needs to be done at desctruction time
        // (e.g. close files, deallocate resources etc.)
}


//
// member functions
//

// ------------ method called to for each event  ------------
void ESRecoSummary::analyze(const edm::Event& ev, const edm::EventSetup& iSetup)
{
  
  //Get the magnetic field
  edm::ESHandle<MagneticField> theMagField;
  iSetup.get<IdealMagneticFieldRecord>().get(theMagField);

  //Preshower RecHits
  edm::Handle<ESRecHitCollection> recHitsES;
  ev.getByLabel (esRecHitCollection_, recHitsES) ;
  const ESRecHitCollection* thePreShowerRecHits = recHitsES.product () ;

  if ( ! recHitsES.isValid() ) {
    std::cerr << "ESRecoSummary::analyze --> recHitsES not found" << std::endl; 
  }

  float maxRecHitEnergyES = -999.;

  for (ESRecHitCollection::const_iterator esItr = thePreShowerRecHits->begin(); esItr != thePreShowerRecHits->end(); ++esItr) 
    {
      
      h_recHits_ES_time   -> Fill(esItr->time()); 
      if (esItr -> energy() > maxRecHitEnergyES ) maxRecHitEnergyES = esItr -> energy() ;

    } // end loop over ES rec Hits

  h_recHits_ES_energyMax -> Fill(maxRecHitEnergyES ); 

  // ES clusters in X plane
  edm::Handle<reco::PreshowerClusterCollection> esClustersX;
  ev.getByLabel( esClusterCollectionX_, esClustersX);
  const reco::PreshowerClusterCollection *ESclustersX = esClustersX.product();

  // ES clusters in Y plane
  edm::Handle<reco::PreshowerClusterCollection> esClustersY;
  ev.getByLabel( esClusterCollectionY_, esClustersY);
  const reco::PreshowerClusterCollection *ESclustersY = esClustersY.product(); 
  

  // ... endcap
  edm::Handle<reco::SuperClusterCollection> superClusters_EE_h;
  ev.getByLabel( superClusterCollection_EE_, superClusters_EE_h );
  const reco::SuperClusterCollection* theEndcapSuperClusters = superClusters_EE_h.product () ;
  if ( ! superClusters_EE_h.isValid() ) {
    std::cerr << "EcalRecHitSummary::analyze --> superClusters_EE_h not found" << std::endl; 
  }

  // loop over all super clusters
  for (reco::SuperClusterCollection::const_iterator itSC = theEndcapSuperClusters->begin(); 
       itSC != theEndcapSuperClusters->end(); ++itSC ) {
    
    if ( fabs(itSC->eta()) < 1.65 || fabs(itSC->eta()) > 2.6 ) continue;

    // Loop over all ECAL Basic clusters in the supercluster
    for (reco::CaloCluster_iterator ecalBasicCluster = itSC->clustersBegin(); ecalBasicCluster!= itSC->clustersEnd(); 
	 ecalBasicCluster++) {
      const reco::CaloClusterPtr ecalBasicClusterPtr = *(ecalBasicCluster);
      
      float ESenergyPlane1 = -999.;
      float ESenergyPlane2 = -999.;
      
      for (reco::PreshowerClusterCollection::const_iterator iESClus = ESclustersX->begin(); iESClus != ESclustersX->end(); 
	   ++iESClus) {
        const reco::CaloClusterPtr preshBasicCluster = iESClus->basicCluster();
        const reco::PreshowerCluster *esCluster = &*iESClus;
        if (preshBasicCluster == ecalBasicClusterPtr) {
	  ESenergyPlane1 = esCluster->energy();
	  h_esClusters_energy_plane1 ->Fill(esCluster->energy());
	}
      }  // end of x loop
      
      for (reco::PreshowerClusterCollection::const_iterator iESClus = ESclustersY->begin(); iESClus != ESclustersY->end(); 
	   ++iESClus) {
        const reco::CaloClusterPtr preshBasicCluster = iESClus->basicCluster();
        const reco::PreshowerCluster *esCluster = &*iESClus;
        if (preshBasicCluster == ecalBasicClusterPtr) {
	  ESenergyPlane2 = esCluster->energy();
	  h_esClusters_energy_plane2 -> Fill(esCluster->energy());
	}
      } // end of y loop
      
      if ( ESenergyPlane1 != -999. && ESenergyPlane2 != -999. ) 
	h_esClusters_energy_ratio -> Fill(ESenergyPlane1/ESenergyPlane2);
      
      
    } // end loop over all basic clusters in the supercluster
  }// end loop over superclusters

}


// ------------ method called once each job just before starting event loop  ------------
        void 
ESRecoSummary::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
ESRecoSummary::endJob() 
{}

//define this as a plug-in
DEFINE_FWK_MODULE(ESRecoSummary);
