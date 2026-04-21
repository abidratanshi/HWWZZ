#ifndef ZHfunctions_H
#define ZHfunctions_H

#include <cmath>
#include <vector>
#include <math.h>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"
#include "ReconstructedParticle2MC.h"


namespace FCCAnalyses { namespace ZHfunctions {


// this function takes 4 jets and finds the best way to pair them into two bosons
// returns 4 indices [i, j, k, l]
// [i, j] = first jet pair
// [k, l] = second jet pair
std::vector<int> FindBestJetPairing(ROOT::VecOps::RVec<TLorentzVector> jets) {

    double best_score = 1e9; // start with a very large number to be minimized
    int best_i=-1, best_j=-1, best_k=-1, best_l=-1;

    int n = jets.size(); // number of jets

    // loop over all possible ways to pick 2 jets out of 4
    for (int i = 0; i < n; i++) {
        for (int j = i+1; j < n; j++) {

            // now get the OTHER two jets (not i and j)
            std::vector<int> rest;  // stores the remaining indices

            for (int x = 0; x < n; x++) {
                if (x != i && x != j) {
                    rest.push_back(x);
                }
            }

            int k = rest[0];
            int l = rest[1];

            // build two boson candidates (dijet systems)
            TLorentzVector V1 = jets[i] + jets[j];
            TLorentzVector V2 = jets[k] + jets[l];

            // we want to identify:
            // one boson ~ on-shell (W/Z)
            // one boson off-shell (lighter)
            TLorentzVector Va = V1;
            TLorentzVector Vb = V2;

            // ensure Va is the heavier one
            if (V2.M() > V1.M()) {
                Va = V2;
                Vb = V1;
            }

            // define a score:
            // Va should be near W/Z mass
            // Vb should be off-shell
            // first term: penalize deviation from W/Z mass
            // second term: penalize deviation from off-shell mass
            double mV = 85.0;
    	    double mVstar = 40.0;
            double alpha = 0.20;
    	    // consider turning this into a chi2 like score later where SUM_i[(Vi-mi)/sigmai)^2]
            double score = std::pow(Va.M() - mV, 2) + alpha * std::pow(Vb.M() - mVstar, 2);

            // Keep the best pairing (smallest score)
            if (score < best_score) {
                best_score = score;
                best_i = i;
                best_j = j;
                best_k = k;
                best_l = l;
            }
        }
    }

    return {best_i, best_j, best_k, best_l};
}

// this function checks if the higgs candidate is built only from jets or from the leptonic Z as well
int CheckHiggsTopology(ROOT::VecOps::RVec<TLorentzVector> jets, TLorentzVector Z_lep, std::vector<int> pairing) {

    double mH = 125.0;

    int i = pairing[0];
    int j = pairing[1];
    int k = pairing[2];
    int l = pairing[3];

    // build the two bosons from jets
    TLorentzVector V1 = jets[i] + jets[j];
    TLorentzVector V2 = jets[k] + jets[l];

    // higgs from jets only (signal hypothesis)
    double m_jets = (V1 + V2).M();

    // fake higgs using leptonic Z + jet pair
    double m_ZV1  = (Z_lep + V1).M();
    double m_ZV2  = (Z_lep + V2).M();

    // compare how close each is to 125 GeV
    double d_jets = std::abs(m_jets - mH);
    double d_ZV1  = std::abs(m_ZV1  - mH);
    double d_ZV2  = std::abs(m_ZV2  - mH);

    // if jets-only combination is best then accept event
    if (d_jets < d_ZV1 && d_jets < d_ZV2) {
        return 1;
    }

    // otherwise reject event
    return 0;
}


// --------------------------------------------------------------------------------------------------------------------------


struct sel_iso {
    sel_iso(float arg_max_iso);
    float m_max_iso = .25;
    Vec_rp operator() (Vec_rp in, Vec_f iso);
  };

sel_iso::sel_iso(float arg_max_iso) : m_max_iso(arg_max_iso) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  sel_iso::operator() (Vec_rp in, Vec_f iso) {
    Vec_rp result;
    result.reserve(in.size());
    for (size_t i = 0; i < in.size(); ++i) {
        auto & p = in[i];
        if (iso[i] < m_max_iso) {
            result.emplace_back(p);
        }
    }
    return result;
}

 
// compute the cone isolation for reco particles
struct coneIsolation {

    coneIsolation(float arg_dr_min, float arg_dr_max);
    double deltaR(double eta1, double phi1, double eta2, double phi2) { return TMath::Sqrt(TMath::Power(eta1-eta2, 2) + (TMath::Power(phi1-phi2, 2))); };

    float dr_min = 0;
    float dr_max = 0.4;
    Vec_f operator() (Vec_rp in, Vec_rp rps);
};

coneIsolation::coneIsolation(float arg_dr_min, float arg_dr_max) : dr_min(arg_dr_min), dr_max( arg_dr_max ) { };
Vec_f coneIsolation::coneIsolation::operator() (Vec_rp in, Vec_rp rps) {
  
    Vec_f result;
    result.reserve(in.size());

    std::vector<ROOT::Math::PxPyPzEVector> lv_reco;
    std::vector<ROOT::Math::PxPyPzEVector> lv_charged;
    std::vector<ROOT::Math::PxPyPzEVector> lv_neutral;

    for(size_t i = 0; i < rps.size(); ++i) {

        ROOT::Math::PxPyPzEVector tlv;
        tlv.SetPxPyPzE(rps.at(i).momentum.x, rps.at(i).momentum.y, rps.at(i).momentum.z, rps.at(i).energy);
        
        if(rps.at(i).charge == 0) lv_neutral.push_back(tlv);
        else lv_charged.push_back(tlv);
    }
    
    for(size_t i = 0; i < in.size(); ++i) {

        ROOT::Math::PxPyPzEVector tlv;
        tlv.SetPxPyPzE(in.at(i).momentum.x, in.at(i).momentum.y, in.at(i).momentum.z, in.at(i).energy);
        lv_reco.push_back(tlv);
    }

    
    // compute the isolation (see https://github.com/delphes/delphes/blob/master/modules/Isolation.cc#L154) 
    for (auto & lv_reco_ : lv_reco) {
    
        double sumNeutral = 0.0;
        double sumCharged = 0.0;
    
        // charged
        for (auto & lv_charged_ : lv_charged) {
    
            double dr = coneIsolation::deltaR(lv_reco_.Eta(), lv_reco_.Phi(), lv_charged_.Eta(), lv_charged_.Phi());
            if(dr > dr_min && dr < dr_max) sumCharged += lv_charged_.P();
        }
        
        // neutral
        for (auto & lv_neutral_ : lv_neutral) {
    
            double dr = coneIsolation::deltaR(lv_reco_.Eta(), lv_reco_.Phi(), lv_neutral_.Eta(), lv_neutral_.Phi());
            if(dr > dr_min && dr < dr_max) sumNeutral += lv_neutral_.P();
        }
        
        double sum = sumCharged + sumNeutral;
        double ratio= sum / lv_reco_.P();
        result.emplace_back(ratio);
    }
    return result;
}

}}

#endif
