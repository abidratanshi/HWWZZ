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
            double alpha = 0.35;
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


// this function takes the leptons and finds the best pair to have come from a Z
std::vector<int> FindBestZLeptonPair(ROOT::VecOps::RVec<edm4hep::MCParticleData> leptons) {

    double mZ = 91.1876;
    double best_diff = 1e9;

    int best_i = -1;
    int best_j = -1;

    int n = leptons.size();

    for (int i = 0; i < n; i++) {
        for (int j = i+1; j < n; j++) {

            // require opposite charge
            if (leptons[i].charge * leptons[j].charge >= 0) continue;

            // get momenta
            double px1 = leptons[i].momentum.x;
            double py1 = leptons[i].momentum.y;
            double pz1 = leptons[i].momentum.z;
            double m1  = leptons[i].mass;

            double px2 = leptons[j].momentum.x;
            double py2 = leptons[j].momentum.y;
            double pz2 = leptons[j].momentum.z;
            double m2  = leptons[j].mass;

            // compute energies
            double E1 = std::sqrt(px1*px1 + py1*py1 + pz1*pz1 + m1*m1);
            double E2 = std::sqrt(px2*px2 + py2*py2 + pz2*pz2 + m2*m2);

            TLorentzVector l1, l2;
            l1.SetPxPyPzE(px1, py1, pz1, E1);
            l2.SetPxPyPzE(px2, py2, pz2, E2);

            double mass = (l1 + l2).M();
            double diff = std::fabs(mass - mZ);

            if (diff < best_diff) {
                best_diff = diff;
                best_i = i;
                best_j = j;
            }
        }
    }

    return {best_i, best_j};
}


TLorentzVector BuildZFromPair(ROOT::VecOps::RVec<edm4hep::MCParticleData> leptons,
                             std::vector<int> idx) {

    if (idx.size() < 2 || idx[0] < 0 || idx[1] < 0)
        return TLorentzVector(0,0,0,0);

    // first lepton
    double px1 = leptons[idx[0]].momentum.x;
    double py1 = leptons[idx[0]].momentum.y;
    double pz1 = leptons[idx[0]].momentum.z;
    double m1  = leptons[idx[0]].mass;

    // second lepton
    double px2 = leptons[idx[1]].momentum.x;
    double py2 = leptons[idx[1]].momentum.y;
    double pz2 = leptons[idx[1]].momentum.z;
    double m2  = leptons[idx[1]].mass;

    // energies
    double E1 = std::sqrt(px1*px1 + py1*py1 + pz1*pz1 + m1*m1);
    double E2 = std::sqrt(px2*px2 + py2*py2 + pz2*pz2 + m2*m2);

    TLorentzVector l1, l2;
    l1.SetPxPyPzE(px1, py1, pz1, E1);
    l2.SetPxPyPzE(px2, py2, pz2, E2);

    return l1 + l2;
}


// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// reco-level analog of FindBestZLeptonPair
//finds the best OS lepton pair consistent with the Z mass
std::vector<int> FindBestZLeptonPair_reco(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> leptons) {

    double mZ = 91.1876;
    double best_diff = 1e9;

    int best_i = -1;
    int best_j = -1;

    int n = leptons.size();

    for (int i = 0; i < n; i++) {
        for (int j = i+1; j < n; j++) {

            // require opposite charge
            if (leptons[i].charge * leptons[j].charge >= 0) continue;

            TLorentzVector l1, l2;
            l1.SetPxPyPzE(leptons[i].momentum.x, leptons[i].momentum.y,
                          leptons[i].momentum.z, leptons[i].energy);
            l2.SetPxPyPzE(leptons[j].momentum.x, leptons[j].momentum.y,
                          leptons[j].momentum.z, leptons[j].energy);

            double mass = (l1 + l2).M();
            double diff = std::fabs(mass - mZ);

            if (diff < best_diff) {
                best_diff = diff;
                best_i = i;
                best_j = j;
            }
        }
    }

    return {best_i, best_j};
}

// reco-level analog of BuildZFromPair
TLorentzVector BuildZFromPair_reco(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> leptons,
                                    std::vector<int> idx) {

    if (idx.size() < 2 || idx[0] < 0 || idx[1] < 0)
        return TLorentzVector(0,0,0,0);

    TLorentzVector l1, l2;
    l1.SetPxPyPzE(leptons[idx[0]].momentum.x, leptons[idx[0]].momentum.y,
                  leptons[idx[0]].momentum.z, leptons[idx[0]].energy);
    l2.SetPxPyPzE(leptons[idx[1]].momentum.x, leptons[idx[1]].momentum.y,
                  leptons[idx[1]].momentum.z, leptons[idx[1]].energy);

    return l1 + l2;
}


// returns the two leptons selected as the Z pair, for removal from the event
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> GetZLeptons_reco(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> leptons,
    std::vector<int> idx) {

    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;

    if (idx.size() < 2 || idx[0] < 0 || idx[1] < 0)
        return result; // empty if no valid pair found

    result.emplace_back(leptons[idx[0]]);
    result.emplace_back(leptons[idx[1]]);

    return result;
}
// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// // compute angular separation between the first two particles in a collection
// static float deltaR(ROOT::VecOps::RVec<float> eta, ROOT::VecOps::RVec<float> phi) {
    
//     if (eta.size() < 2 || phi.size() < 2) return -1.0;
    
//     double dphi = std::fabs(phi[0] - phi[1]);
//     if (dphi > M_PI) dphi = 2*M_PI - dphi;
    
//     double deta = eta[0] - eta[1];
    
//     return std::sqrt(deta*deta + dphi*dphi);
// }

float deltaR_pair(ROOT::VecOps::RVec<edm4hep::MCParticleData> leptons,
                  std::vector<int> idx) {

    if (idx.size() < 2 || idx[0] < 0 || idx[1] < 0)
        return -1.;

    auto &p1 = leptons[idx[0]];
    auto &p2 = leptons[idx[1]];

    double px1 = p1.momentum.x;
    double py1 = p1.momentum.y;
    double pz1 = p1.momentum.z;

    double px2 = p2.momentum.x;
    double py2 = p2.momentum.y;
    double pz2 = p2.momentum.z;

    double phi1 = std::atan2(py1, px1);
    double phi2 = std::atan2(py2, px2);

    double p1_mag = std::sqrt(px1*px1 + py1*py1 + pz1*pz1);
    double p2_mag = std::sqrt(px2*px2 + py2*py2 + pz2*pz2);

    double eta1 = 0.5 * std::log((p1_mag + pz1)/(p1_mag - pz1));
    double eta2 = 0.5 * std::log((p2_mag + pz2)/(p2_mag - pz2));

    double dphi = std::fabs(phi1 - phi2);
    if (dphi > M_PI) dphi = 2*M_PI - dphi;

    double deta = eta1 - eta2;

    return std::sqrt(deta*deta + dphi*dphi);
}

// this function filters a collection of leptons and returns only those originating from the production Z
ROOT::VecOps::RVec<edm4hep::MCParticleData> GetZProductionLeptons(
    ROOT::VecOps::RVec<edm4hep::MCParticleData> leptons, // lepton collection
    ROOT::VecOps::RVec<edm4hep::MCParticleData> all_mc,  // full MC particle collection
    ROOT::VecOps::RVec<int> ind_p) // parent indices map
{
    ROOT::VecOps::RVec<edm4hep::MCParticleData> result;
    result.reserve(leptons.size());

    for (size_t i = 0; i < leptons.size(); ++i) {
        auto & p = leptons[i];
        bool from_higgs_decay = false;

        // looping through the parents of the current lepton
        for (unsigned j = p.parents_begin; j != p.parents_end; ++j) {
            int index_p = ind_p.at(j);
            auto & parent = all_mc.at(index_p);
            int pdg_parent = std::abs(parent.PDG);

            // check if parent is a Z boson (23) or W boson (24)
            if (pdg_parent == 23 || pdg_parent == 24) {
                
                // looping through parents of this boson (grandparents of the lepton)
                for (unsigned k = parent.parents_begin; k != parent.parents_end; ++k) {
                    int index_gp = ind_p.at(k);
                    int pdg_grandparent = std::abs(all_mc.at(index_gp).PDG);

                    // if the grandparent is a Higgs, flag it
                    if (pdg_grandparent == 25) {
                        from_higgs_decay = true;
                        break; // found a Higgs grandparent, no need to check other grandparents
                    }
                }
            }
            if (from_higgs_decay) break; // no need to check other parents
        }

        // Reversal: if it did not come from a Higgs decay chain, it must belong to the production Z
        if (!from_higgs_decay) {
            result.emplace_back(p);
        }
    }

    return result;
}















// ============================================================================
// DIAGNOSTIC ADDITIONS: isolating the Higgs-decay system (H -> Z Z* -> qq qq)
// and checking reco-level jet energy balance, to investigate the 90 GeV bump
// in RecoH4_mass for H->ZZ* events.
// ============================================================================

// this function filters a collection of MC particles and returns only those
// originating from the HIGGS decay chain (i.e. NOT the production Z).
// this is the mirror image of GetZProductionLeptons: instead of keeping
// particles that do NOT come from H, we keep particles that DO come from H.
// works for both leptons and quarks, since it only looks at PDG codes of
// parents/grandparents, not the particle's own flavor.
ROOT::VecOps::RVec<edm4hep::MCParticleData> GetHiggsDecayProducts(
    ROOT::VecOps::RVec<edm4hep::MCParticleData> particles, // candidate decay products (e.g. quarks)
    ROOT::VecOps::RVec<edm4hep::MCParticleData> all_mc,    // full MC particle collection
    ROOT::VecOps::RVec<int> ind_p)                          // parent indices map
{
    ROOT::VecOps::RVec<edm4hep::MCParticleData> result;
    result.reserve(particles.size());

    for (size_t i = 0; i < particles.size(); ++i) {
        auto & p = particles[i];
        bool from_higgs_decay = false;

        // looping through the parents of the current particle
        for (unsigned j = p.parents_begin; j != p.parents_end; ++j) {
            int index_p = ind_p.at(j);
            auto & parent = all_mc.at(index_p);
            int pdg_parent = std::abs(parent.PDG);

            // check if parent is a Z boson (23) or W boson (24)
            if (pdg_parent == 23 || pdg_parent == 24) {

                // looping through parents of this boson (grandparents of the particle)
                for (unsigned k = parent.parents_begin; k != parent.parents_end; ++k) {
                    int index_gp = ind_p.at(k);
                    int pdg_grandparent = std::abs(all_mc.at(index_gp).PDG);

                    // if the grandparent is a Higgs, flag it
                    if (pdg_grandparent == 25) {
                        from_higgs_decay = true;
                        break;
                    }
                }
            }
            if (from_higgs_decay) break;
        }

        if (from_higgs_decay) {
            result.emplace_back(p);
        }
    }

    return result;
}


// selects stable, visible (non-neutrino) final-state quarks from the Higgs
// decay chain. PDG IDs 1-6 = d,u,s,c,b,t quarks.
ROOT::VecOps::RVec<edm4hep::MCParticleData> sel_quarks(
    ROOT::VecOps::RVec<edm4hep::MCParticleData> particles)
{
    ROOT::VecOps::RVec<edm4hep::MCParticleData> result;
    result.reserve(particles.size());

    for (size_t i = 0; i < particles.size(); ++i) {
        int pdg = std::abs(particles[i].PDG);
        if (pdg >= 1 && pdg <= 6) {
            result.emplace_back(particles[i]);
        }
    }
    return result;
}


// builds a TLorentzVector for a single MCParticleData entry (helper)
TLorentzVector MCParticleToP4(const edm4hep::MCParticleData & p) {
    double px = p.momentum.x;
    double py = p.momentum.y;
    double pz = p.momentum.z;
    double m  = p.mass;
    double E  = std::sqrt(px*px + py*py + pz*pz + m*m);

    TLorentzVector v;
    v.SetPxPyPzE(px, py, pz, E);
    return v;
}


// for H -> V V* -> 4 quarks (V = W or Z), this finds the best pairing of the
// 4 Higgs-decay quarks into two dijet systems, using the SAME scoring logic
// as FindBestJetPairing but at gen level (truth quarks instead of reco jets).
// returns {Va_mass, Va_energy, Vb_mass, Vb_energy} where Va = on-shell (heavier),
// Vb = off-shell (lighter). This lets you check the TRUE on-shell/off-shell
// mass and energy split before any detector/clustering effects.
std::vector<double> GetHiggsVVstarSystem(
    ROOT::VecOps::RVec<edm4hep::MCParticleData> higgs_quarks)
{
    // default failure value
    std::vector<double> fail = {-1., -1., -1., -1.};

    if (higgs_quarks.size() != 4) return fail;

    double best_score = 1e9;
    int best_i=-1, best_j=-1, best_k=-1, best_l=-1;

    int n = 4;
    for (int i = 0; i < n; i++) {
        for (int j = i+1; j < n; j++) {

            std::vector<int> rest;
            for (int x = 0; x < n; x++) {
                if (x != i && x != j) rest.push_back(x);
            }
            int k = rest[0];
            int l = rest[1];

            TLorentzVector V1 = MCParticleToP4(higgs_quarks[i]) + MCParticleToP4(higgs_quarks[j]);
            TLorentzVector V2 = MCParticleToP4(higgs_quarks[k]) + MCParticleToP4(higgs_quarks[l]);

            TLorentzVector Va = V1;
            TLorentzVector Vb = V2;
            if (V2.M() > V1.M()) { Va = V2; Vb = V1; }

            double mV = 85.0;
            double mVstar = 40.0;
            double alpha = 0.35;
            double score = std::pow(Va.M() - mV, 2) + alpha * std::pow(Vb.M() - mVstar, 2);

            if (score < best_score) {
                best_score = score;
                best_i = i; best_j = j; best_k = k; best_l = l;
            }
        }
    }

    TLorentzVector V1 = MCParticleToP4(higgs_quarks[best_i]) + MCParticleToP4(higgs_quarks[best_j]);
    TLorentzVector V2 = MCParticleToP4(higgs_quarks[best_k]) + MCParticleToP4(higgs_quarks[best_l]);

    TLorentzVector Va = V1;
    TLorentzVector Vb = V2;
    if (V2.M() > V1.M()) { Va = V2; Vb = V1; }

    return { Va.M(), Va.E(), Vb.M(), Vb.E() };
}




// given 4 jets and the BestPairing indices [i,j,k,l] from FindBestJetPairing,
// returns {Va_mass, Vb_mass} where Va = on-shell (heavier), Vb = off-shell (lighter).
// This re-derives Va/Vb the same way FindBestJetPairing internally does,
// so the masses are guaranteed consistent with whichever pairing it selected.
std::vector<double> GetPairedBosonMasses(ROOT::VecOps::RVec<TLorentzVector> jets,
                                          std::vector<int> pairing) {

    if (pairing.size() < 4 || pairing[0] < 0) return {-1., -1.};

    TLorentzVector V1 = jets[pairing[0]] + jets[pairing[1]];
    TLorentzVector V2 = jets[pairing[2]] + jets[pairing[3]];

    TLorentzVector Va = V1;
    TLorentzVector Vb = V2;
    if (V2.M() > V1.M()) { Va = V2; Vb = V1; }

    return { Va.M(), Vb.M() };
}







// given 4 jets and the BestPairing indices [i,j,k,l], returns the angular
// separation (deltaR) between the two jets WITHIN each pairing:
// {dR(i,j) -- the Va pair, dR(k,l) -- the Vb pair}
// Small dR means the two jets in that pair are genuinely close/correlated
// (consistent with coming from the same parent boson). Large dR could mean
// the pairing algorithm grouped together jets that don't really belong together.
std::vector<double> GetPairedJetsDeltaR(ROOT::VecOps::RVec<TLorentzVector> jets, std::vector<int> pairing) {

    if (pairing.size() < 4 || pairing[0] < 0) return {-1., -1.};

    double dR_Va_jets = jets[pairing[0]].DeltaR(jets[pairing[1]]);
    double dR_Vb_jets  = jets[pairing[2]].DeltaR(jets[pairing[3]]);

    // need to know which pair ended up being "Va" (heavier) vs "Vb" (lighter)
    // to stay consistent with GetPairedBosonMasses' labeling
    TLorentzVector V1 = jets[pairing[0]] + jets[pairing[1]];
    TLorentzVector V2 = jets[pairing[2]] + jets[pairing[3]];

    if (V2.M() > V1.M()) {
        // V2 (k,l) is actually the heavier/on-shell one -> swap labels
        return { dR_Vb_jets, dR_Va_jets };
    }
    return { dR_Va_jets, dR_Vb_jets };
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
