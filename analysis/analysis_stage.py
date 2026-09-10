import os, copy
import ROOT
import urllib.request

processList = {

    # Signal
    'wzp6_ee_eeH_HWW_ecm365':   {'fraction':0.001},
    'wzp6_ee_mumuH_HWW_ecm365': {'fraction':0.001},
    'wzp6_ee_eeH_HZZ_ecm365':   {'fraction':0.001},
    'wzp6_ee_mumuH_HZZ_ecm365': {'fraction':0.001},

    # # Background
    'p8_ee_WW_ecm365': {'fraction':0.000001},
    'p8_ee_ZZ_ecm365': {'fraction':0.000001},
    'p8_ee_tt_ecm365': {'fraction':0.000001},
}

# directories
inputDir = "/ceph/sgiappic/HiggsCP/winter23"
outputDir = "/ceph/aratanshi/stage_output"
includePaths = ["functions.h"]

nCPUS = 8

## tagging -------------------------------
## latest particle transformer model, trained on 9M jets in winter2023 samples
model_name = "fccee_flavtagging_edm4hep_wc"

## model files needed for unit testing in CI
url_model_dir = "https://fccsw.web.cern.ch/fccsw/testsamples/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
url_preproc = "{}/{}.json".format(url_model_dir, model_name)
url_model = "{}/{}.onnx".format(url_model_dir, model_name)

## model files locally stored on /eos
model_dir = "/ceph/sgiappic/FCCAnalyses/addons/jet_flavor_tagging/winter2023/wc_pt_7classes_12_04_2023/"
local_preproc = "{}/{}.json".format(model_dir, model_name)
local_model = "{}/{}.onnx".format(model_dir, model_name)

## get local file, else download from url
def get_file_path(url, filename):
    if os.path.exists(filename):
        return os.path.abspath(filename)

weaver_preproc = get_file_path(url_preproc, local_preproc)
weaver_model = get_file_path(url_model, local_model)

from addons.ONNXRuntime.jetFlavourHelper import JetFlavourHelper
from addons.FastJet.jetClusteringHelper import (
    ExclusiveJetClusteringHelper,
    InclusiveJetClusteringHelper,
)

class RDFanalysis():
    def analysers(df):
        df2 = (df

            .Alias("Particle0", "Particle#0.index")
            .Alias("Particle1", "Particle#1.index")
            .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
            .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

            # ELECTRONS 
            .Alias("Electron0",            "Electron#0.index")
            .Define("RecoElectrons",       "ReconstructedParticle::get(Electron0, ReconstructedParticles)")            
            .Define("n_RecoElectrons",     "ReconstructedParticle::get_n(RecoElectrons)")
            .Define("RecoElectron_e",      "ReconstructedParticle::get_e(RecoElectrons)")
            .Define("RecoElectron_p",      "ReconstructedParticle::get_p(RecoElectrons)")
            .Define("RecoElectron_pt",     "ReconstructedParticle::get_pt(RecoElectrons)")
            .Define("RecoElectron_px",     "ReconstructedParticle::get_px(RecoElectrons)")
            .Define("RecoElectron_py",     "ReconstructedParticle::get_py(RecoElectrons)")
            .Define("RecoElectron_pz",     "ReconstructedParticle::get_pz(RecoElectrons)")
            .Define("RecoElectron_y",      "ReconstructedParticle::get_y(RecoElectrons)")
            .Define("RecoElectron_eta",    "ReconstructedParticle::get_eta(RecoElectrons)")
            .Define("RecoElectron_theta",  "ReconstructedParticle::get_theta(RecoElectrons)")
            .Define("RecoElectron_phi",    "ReconstructedParticle::get_phi(RecoElectrons)") 
            .Define("RecoElectron_charge", "ReconstructedParticle::get_charge(RecoElectrons)")
            .Define("RecoElectron_mass",   "ReconstructedParticle::get_mass(RecoElectrons)")
        
            .Define("RecoElectrons_hard", "FCCAnalyses::ReconstructedParticle::sel_p(20)(RecoElectrons)")
            .Define("RecoElectrons_iso",  "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(RecoElectrons_hard, ReconstructedParticles)")
            .Define("RecoElectrons_sel",  "FCCAnalyses::ZHfunctions::sel_iso(0.25)(RecoElectrons_hard, RecoElectrons_iso)")

            .Define("n_RecoElectrons_sel",     "ReconstructedParticle::get_n(RecoElectrons_sel)") 
            .Define("RecoElectron_sel_e",      "ReconstructedParticle::get_e(RecoElectrons_sel)")
            .Define("RecoElectron_sel_p",      "ReconstructedParticle::get_p(RecoElectrons_sel)")
            .Define("RecoElectron_sel_pt",     "ReconstructedParticle::get_pt(RecoElectrons_sel)")
            .Define("RecoElectron_sel_px",     "ReconstructedParticle::get_px(RecoElectrons_sel)")
            .Define("RecoElectron_sel_py",     "ReconstructedParticle::get_py(RecoElectrons_sel)")
            .Define("RecoElectron_sel_pz",     "ReconstructedParticle::get_pz(RecoElectrons_sel)")
            .Define("RecoElectron_sel_y",      "ReconstructedParticle::get_y(RecoElectrons_sel)")
            .Define("RecoElectron_sel_eta",    "ReconstructedParticle::get_eta(RecoElectrons_sel)")
            .Define("RecoElectron_sel_theta",  "ReconstructedParticle::get_theta(RecoElectrons_sel)")
            .Define("RecoElectron_sel_phi",    "ReconstructedParticle::get_phi(RecoElectrons_sel)")
            .Define("RecoElectron_sel_charge", "ReconstructedParticle::get_charge(RecoElectrons_sel)")
            .Define("RecoElectron_sel_mass",   "ReconstructedParticle::get_mass(RecoElectrons_sel)")
            
            # MUONS
            .Alias("Muon0",            "Muon#0.index")
            .Define("RecoMuons",       "ReconstructedParticle::get(Muon0, ReconstructedParticles)")            
            .Define("n_RecoMuons",     "ReconstructedParticle::get_n(RecoMuons)")
            .Define("RecoMuon_e",      "ReconstructedParticle::get_e(RecoMuons)")
            .Define("RecoMuon_p",      "ReconstructedParticle::get_p(RecoMuons)")
            .Define("RecoMuon_pt",     "ReconstructedParticle::get_pt(RecoMuons)")
            .Define("RecoMuon_px",     "ReconstructedParticle::get_px(RecoMuons)")
            .Define("RecoMuon_py",     "ReconstructedParticle::get_py(RecoMuons)")
            .Define("RecoMuon_pz",     "ReconstructedParticle::get_pz(RecoMuons)")
            .Define("RecoMuon_y",      "ReconstructedParticle::get_y(RecoMuons)")
            .Define("RecoMuon_eta",    "ReconstructedParticle::get_eta(RecoMuons)") 
            .Define("RecoMuon_theta",  "ReconstructedParticle::get_theta(RecoMuons)")
            .Define("RecoMuon_phi",    "ReconstructedParticle::get_phi(RecoMuons)")
            .Define("RecoMuon_charge", "ReconstructedParticle::get_charge(RecoMuons)")
            .Define("RecoMuon_mass",   "ReconstructedParticle::get_mass(RecoMuons)")

            .Define("RecoMuons_hard", "FCCAnalyses::ReconstructedParticle::sel_p(20)(RecoMuons)")
            .Define("RecoMuons_iso",  "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(RecoMuons_hard, ReconstructedParticles)")
            .Define("RecoMuons_sel",  "FCCAnalyses::ZHfunctions::sel_iso(0.25)(RecoMuons_hard, RecoMuons_iso)")
            
            .Define("n_RecoMuons_sel",     "ReconstructedParticle::get_n(RecoMuons_sel)") 
            .Define("RecoMuon_sel_e",      "ReconstructedParticle::get_e(RecoMuons_sel)")
            .Define("RecoMuon_sel_p",      "ReconstructedParticle::get_p(RecoMuons_sel)")
            .Define("RecoMuon_sel_pt",     "ReconstructedParticle::get_pt(RecoMuons_sel)")
            .Define("RecoMuon_sel_px",     "ReconstructedParticle::get_px(RecoMuons_sel)")
            .Define("RecoMuon_sel_py",     "ReconstructedParticle::get_py(RecoMuons_sel)")
            .Define("RecoMuon_sel_pz",     "ReconstructedParticle::get_pz(RecoMuons_sel)")
            .Define("RecoMuon_sel_y",      "ReconstructedParticle::get_y(RecoMuons_sel)")
            .Define("RecoMuon_sel_eta",    "ReconstructedParticle::get_eta(RecoMuons_sel)")
            .Define("RecoMuon_sel_theta",  "ReconstructedParticle::get_theta(RecoMuons_sel)")
            .Define("RecoMuon_sel_phi",    "ReconstructedParticle::get_phi(RecoMuons_sel)")
            .Define("RecoMuon_sel_charge", "ReconstructedParticle::get_charge(RecoMuons_sel)")
            .Define("RecoMuon_sel_mass",   "ReconstructedParticle::get_mass(RecoMuons_sel)")

            #PHOTONS
            .Alias("Photon0",            "Photon#0.index") 
            .Define("RecoPhotons",       "ReconstructedParticle::get(Photon0, ReconstructedParticles)")
            .Define("n_RecoPhotons",     "ReconstructedParticle::get_n(RecoPhotons)")
            .Define("RecoPhoton_e",      "ReconstructedParticle::get_e(RecoPhotons)")
            .Define("RecoPhoton_p",      "ReconstructedParticle::get_p(RecoPhotons)")
            .Define("RecoPhoton_pt",     "ReconstructedParticle::get_pt(RecoPhotons)")
            .Define("RecoPhoton_px",     "ReconstructedParticle::get_px(RecoPhotons)")
            .Define("RecoPhoton_py",     "ReconstructedParticle::get_py(RecoPhotons)")
            .Define("RecoPhoton_pz",     "ReconstructedParticle::get_pz(RecoPhotons)")
            .Define("RecoPhoton_y",      "ReconstructedParticle::get_y(RecoPhotons)") 
            .Define("RecoPhoton_eta",    "ReconstructedParticle::get_eta(RecoPhotons)")
            .Define("RecoPhoton_theta",  "ReconstructedParticle::get_theta(RecoPhotons)")
            .Define("RecoPhoton_phi",    "ReconstructedParticle::get_phi(RecoPhotons)")
            .Define("RecoPhoton_charge", "ReconstructedParticle::get_charge(RecoPhotons)")
            .Define("RecoPhoton_mass",   "ReconstructedParticle::get_mass(RecoPhotons)")

            # different definition of missing energy from fccanalysis classes instead of edm4hep
            .Define("RecoEmiss", "FCCAnalyses::ZHfunctions::missingEnergy(365, ReconstructedParticles)") #ecm 
            .Define("RecoEmiss_px",  "RecoEmiss[0].momentum.x")
            .Define("RecoEmiss_py",  "RecoEmiss[0].momentum.y")
            .Define("RecoEmiss_pz",  "RecoEmiss[0].momentum.z")
            .Define("RecoEmiss_pt",  "return sqrt(RecoEmiss_px*RecoEmiss_px + RecoEmiss_py*RecoEmiss_py)")
            .Define("RecoEmiss_p",  "return sqrt(RecoEmiss_px*RecoEmiss_px + RecoEmiss_py*RecoEmiss_py + RecoEmiss_pz*RecoEmiss_pz)")
            .Define("RecoEmiss_e",   "RecoEmiss[0].energy")
            .Define("RecoEmiss_p4",  "TLorentzVector(RecoEmiss_px, RecoEmiss_py, RecoEmiss_pz, RecoEmiss_e)")
            .Define("RecoEmiss_eta",    "RecoEmiss_p4.Eta()")
            .Define("RecoEmiss_phi",    "RecoEmiss_p4.Phi()")
            .Define("RecoEmiss_theta",    "RecoEmiss_p4.Theta()")
            .Define("RecoEmiss_y",    "RecoEmiss_p4.Rapidity()")
            .Define("RecoEmiss_costheta",   "abs(std::cos(RecoEmiss_theta))")

            # GEN LEVEL NEUTRINOS 
            .Define("GenElectronNeutrino_PID", "FCCAnalyses::MCParticle::sel_pdgID(12, true)(Particle)") 
            .Define("GenMuonNeutrino_PID",     "FCCAnalyses::MCParticle::sel_pdgID(14, true)(Particle)") 
            .Define("GenTauNeutrino_PID",      "FCCAnalyses::MCParticle::sel_pdgID(16, true)(Particle)") 
            # merge all the neutrino flavors into one class, takes two arguments only so we do it twice
            .Define("GenNeutrino1_PID", "FCCAnalyses::MCParticle::mergeParticles(GenElectronNeutrino_PID, GenMuonNeutrino_PID)") 
            .Define("GenNeutrino_PID",  "FCCAnalyses::MCParticle::mergeParticles(GenNeutrino1_PID, GenTauNeutrino_PID)") 
            .Define("FSGenNeutrino",    "FCCAnalyses::MCParticle::sel_genStatus(1)(GenNeutrino_PID)") 
            # neutrino properties
            .Define("n_FSGenNeutrino",     "FCCAnalyses::MCParticle::get_n(FSGenNeutrino)")
            .Define("FSGenNeutrino_e",     "FCCAnalyses::MCParticle::get_e(FSGenNeutrino)")
            .Define("FSGenNeutrino_p",     "FCCAnalyses::MCParticle::get_p(FSGenNeutrino)")
            .Define("FSGenNeutrino_pt",    "FCCAnalyses::MCParticle::get_pt(FSGenNeutrino)")
            .Define("FSGenNeutrino_px",    "FCCAnalyses::MCParticle::get_px(FSGenNeutrino)")
            .Define("FSGenNeutrino_py",    "FCCAnalyses::MCParticle::get_py(FSGenNeutrino)")
            .Define("FSGenNeutrino_pz",    "FCCAnalyses::MCParticle::get_pz(FSGenNeutrino)")
            .Define("FSGenNeutrino_y",     "FCCAnalyses::MCParticle::get_y(FSGenNeutrino)")
            .Define("FSGenNeutrino_eta",   "FCCAnalyses::MCParticle::get_eta(FSGenNeutrino)")
            .Define("FSGenNeutrino_theta", "FCCAnalyses::MCParticle::get_theta(FSGenNeutrino)")
            .Define("FSGenNeutrino_phi",   "FCCAnalyses::MCParticle::get_phi(FSGenNeutrino)")
            # keep neutrinos where the parent is a Z boson (pdg id 23)
            # arguments: (Z boson pdg id, true = keep only these parents, true = charge conjugate/include anti-Z if applicable)
            .Define("ZGenNeutrino", "FCCAnalyses::MCParticle::sel_parentID(23, true, true)(GenNeutrino_PID, Particle, Particle0)")
            # Z-neutrino properties
            .Define("n_ZGenNeutrino",     "FCCAnalyses::MCParticle::get_n(ZGenNeutrino)")
            .Define("ZGenNeutrino_e",     "FCCAnalyses::MCParticle::get_e(ZGenNeutrino)")
            .Define("ZGenNeutrino_p",     "FCCAnalyses::MCParticle::get_p(ZGenNeutrino)")
            .Define("ZGenNeutrino_pt",    "FCCAnalyses::MCParticle::get_pt(ZGenNeutrino)")
            .Define("ZGenNeutrino_px",    "FCCAnalyses::MCParticle::get_px(ZGenNeutrino)")
            .Define("ZGenNeutrino_py",    "FCCAnalyses::MCParticle::get_py(ZGenNeutrino)")
            .Define("ZGenNeutrino_pz",    "FCCAnalyses::MCParticle::get_pz(ZGenNeutrino)")
            .Define("ZGenNeutrino_y",     "FCCAnalyses::MCParticle::get_y(ZGenNeutrino)")
            .Define("ZGenNeutrino_eta",   "FCCAnalyses::MCParticle::get_eta(ZGenNeutrino)")
            .Define("ZGenNeutrino_theta", "FCCAnalyses::MCParticle::get_theta(ZGenNeutrino)")
            .Define("ZGenNeutrino_phi",   "FCCAnalyses::MCParticle::get_phi(ZGenNeutrino)")

            # event selection for Z -> 2L
            # require exactly 2 leptons of same flavor and opposite charge
            .Filter("(n_RecoElectrons_sel == 2 && RecoElectron_sel_charge[0] != RecoElectron_sel_charge[1]) || "
                    "(n_RecoMuons_sel == 2 && RecoMuon_sel_charge[0] != RecoMuon_sel_charge[1])")

            # reconstructing Z
            .Define("RecoElectron_p4", "TLorentzVector(RecoElectron_sel_px[0], RecoElectron_sel_py[0], RecoElectron_sel_pz[0], RecoElectron_sel_e[0]) + "
                                       "TLorentzVector(RecoElectron_sel_px[1], RecoElectron_sel_py[1], RecoElectron_sel_pz[1], RecoElectron_sel_e[1])")
            
            .Define("RecoMuon_p4", "TLorentzVector(RecoMuon_sel_px[0], RecoMuon_sel_py[0], RecoMuon_sel_pz[0], RecoMuon_sel_e[0]) + "
                                   "TLorentzVector(RecoMuon_sel_px[1], RecoMuon_sel_py[1], RecoMuon_sel_pz[1], RecoMuon_sel_e[1])")
            
            .Define("RecoZ_p4", "(n_RecoElectrons_sel == 2) ? RecoElectron_p4 : RecoMuon_p4")

            # Z properties
            .Define("RecoZ_px",    "RecoZ_p4.Px()")
            .Define("RecoZ_py",    "RecoZ_p4.Py()")
            .Define("RecoZ_pz",    "RecoZ_p4.Pz()")
            .Define("RecoZ_p",     "RecoZ_p4.P()")
            .Define("RecoZ_pt",    "RecoZ_p4.Pt()")
            .Define("RecoZ_e",     "RecoZ_p4.E()")
            .Define("RecoZ_eta",   "RecoZ_p4.Eta()")
            .Define("RecoZ_phi",   "RecoZ_p4.Phi()")
            .Define("RecoZ_theta", "RecoZ_p4.Theta()")
            .Define("RecoZ_y",     "RecoZ_p4.Rapidity()")
            .Define("RecoZ_mass",  "RecoZ_p4.M()")
        
            # remove Z leptons from rest of particles in order to recluster the jets
            .Define("Z_leptons", "(n_RecoElectrons_sel == 2) ? RecoElectrons_sel : RecoMuons_sel")
            .Define("ReconstructedParticles_no_Z", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, Z_leptons)")

        )
        
        # jet tagging
        # define jet and run clustering parameters
        # name of collections in EDM root files
        collections = {
            "GenParticles": "Particle",
            "PFParticles": "ReconstructedParticles_no_Z",
            "PFTracks": "EFlowTrack",
            "PFPhotons": "EFlowPhoton",
            "PFNeutralHadrons": "EFlowNeutralHadron",
            "TrackState": "EFlowTrack_1",
            "TrackerHits": "TrackerHits",
            "CalorimeterHits": "CalorimeterHits",
            "dNdx": "EFlowTrack_2",
            "PathLength": "EFlowTrack_L",
            "Bz": "magFieldBz",
        }

        # EXCLUSIVE 4 JETS
        jetClusteringHelper_kt4  = ExclusiveJetClusteringHelper(
            collections["PFParticles"], 4, "kt4"
        )
        df2 = jetClusteringHelper_kt4.define(df2)

        # define jet flavour tagging parameters
        jetFlavourHelper_kt4 = JetFlavourHelper(
            collections,
            jetClusteringHelper_kt4.jets,
            jetClusteringHelper_kt4.constituents,
            "kt4",
        )
        
        # define observables for tagger
        df2 = jetFlavourHelper_kt4.define(df2)

        # tagger inference
        df2 = jetFlavourHelper_kt4.inference(weaver_preproc, weaver_model, df2)

        df2 = (df2
                .Define("TagJet_kt4_px",                     "JetClusteringUtils::get_px({})".format(jetClusteringHelper_kt4.jets))
                .Define("TagJet_kt4_py",                     "JetClusteringUtils::get_py({})".format(jetClusteringHelper_kt4.jets))
                .Define("TagJet_kt4_pz",                     "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_kt4.jets))
                .Define("TagJet_kt4_p",                      "JetClusteringUtils::get_p({})".format(jetClusteringHelper_kt4.jets))
                .Define("TagJet_kt4_pt",                     "JetClusteringUtils::get_pt({})".format(jetClusteringHelper_kt4.jets))
                .Define("TagJet_kt4_phi",                    "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_kt4.jets))
                .Define("TagJet_kt4_eta",                    "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_kt4.jets))
                .Define("TagJet_kt4_theta",                  "JetClusteringUtils::get_theta({})".format(jetClusteringHelper_kt4.jets))
                .Define("TagJet_kt4_e",                      "JetClusteringUtils::get_e({})".format(jetClusteringHelper_kt4.jets))
                .Define("TagJet_kt4_mass",                   "JetClusteringUtils::get_m({})".format(jetClusteringHelper_kt4.jets))
                .Define("TagJet_kt4_charge",                 "JetConstituentsUtils::get_charge_constituents({})".format(jetClusteringHelper_kt4.constituents))
                .Define("TagJet_kt4_flavor",                 "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_kt4.jets))
                .Define("n_TagJet_kt4",                      "return int(TagJet_kt4_flavor.size())")
                .Define("n_TagJet_kt4_constituents",         "JetConstituentsUtils::get_n_constituents({})".format(jetClusteringHelper_kt4.constituents))
                .Define("n_TagJet_kt4_charged_constituents", "JetConstituentsUtils::get_ncharged_constituents({})".format(jetClusteringHelper_kt4.constituents))
                .Define("n_TagJet_kt4_neutral_constituents", "JetConstituentsUtils::get_nneutral_constituents({})".format(jetClusteringHelper_kt4.constituents))
                .Define("TagJet_kt4_cleanup",                "JetConstituentsUtils::cleanup_taggedjet({})".format(jetClusteringHelper_kt4.constituents)) 

                # array of TLVs for all 4 jets
                .Define("Jets_p4", "ROOT::VecOps::Construct<TLorentzVector>(TagJet_kt4_px, TagJet_kt4_py, TagJet_kt4_pz, TagJet_kt4_e)")

                # get best jet pairings
                .Define("BestPairing", "FCCAnalyses::ZHfunctions::FindBestJetPairing(Jets_p4)")
            
                # reconstructing H from 4 jets
                .Define("RecoH_p4", "Jets_p4[BestPairing[0]] + Jets_p4[BestPairing[1]] + "
                                    "Jets_p4[BestPairing[2]] + Jets_p4[BestPairing[3]]")

                # H properties
                .Define("RecoH_px",    "RecoH_p4.Px()")
                .Define("RecoH_py",    "RecoH_p4.Py()")
                .Define("RecoH_pz",    "RecoH_p4.Pz()")
                .Define("RecoH_p",     "RecoH_p4.P()")
                .Define("RecoH_pt",    "RecoH_p4.Pt()")
                .Define("RecoH_e",     "RecoH_p4.E()")
                .Define("RecoH_eta",   "RecoH_p4.Eta()")
                .Define("RecoH_phi",   "RecoH_p4.Phi()")
                .Define("RecoH_theta", "RecoH_p4.Theta()")
                .Define("RecoH_y",     "RecoH_p4.Rapidity()")
                .Define("RecoH_mass",  "RecoH_p4.M()")

                # recoil mass
                .Define("Total_p4",    "TLorentzVector(0.,0.,0.,365.)")
                .Define("Recoil_mass", "(Total_p4 - RecoZ_p4).M()")

                # dijet masses from BestPairing to see if one is on-shell/off-shell
                .Define("dijet_pair1_p4",   "Jets_p4[BestPairing[0]] + Jets_p4[BestPairing[1]]")
                .Define("dijet_pair2_p4",   "Jets_p4[BestPairing[2]] + Jets_p4[BestPairing[3]]")
                .Define("dijet_pair1_mass", "dijet_pair1_p4.M()")
                .Define("dijet_pair2_mass", "dijet_pair2_p4.M()")


        )
        return df2

    def output():
        branchList = [

            "n_RecoElectrons",
            "RecoElectron_e",
            "RecoElectron_p",
            "RecoElectron_pt",
            "RecoElectron_px",
            "RecoElectron_py",
            "RecoElectron_pz",
            "RecoElectron_y",
            "RecoElectron_eta",
            "RecoElectron_theta",
            "RecoElectron_phi",
            "RecoElectron_charge",
            "RecoElectron_mass",

            "n_RecoElectrons_sel",
            "RecoElectron_sel_e",
            "RecoElectron_sel_p",
            "RecoElectron_sel_pt",
            "RecoElectron_sel_px",
            "RecoElectron_sel_py",
            "RecoElectron_sel_pz",
            "RecoElectron_sel_y",
            "RecoElectron_sel_eta",
            "RecoElectron_sel_theta",
            "RecoElectron_sel_phi",
            "RecoElectron_sel_charge",
            "RecoElectron_sel_mass",

            "n_RecoMuons",
            "RecoMuon_e",
            "RecoMuon_p",
            "RecoMuon_pt",
            "RecoMuon_px",
            "RecoMuon_py",
            "RecoMuon_pz",
            "RecoMuon_y",
            "RecoMuon_eta",
            "RecoMuon_theta",
            "RecoMuon_phi",
            "RecoMuon_charge",
            "RecoMuon_mass",

            "n_RecoMuons_sel",
            "RecoMuon_sel_e",
            "RecoMuon_sel_p",
            "RecoMuon_sel_pt",
            "RecoMuon_sel_px",
            "RecoMuon_sel_py",
            "RecoMuon_sel_pz",
            "RecoMuon_sel_y",
            "RecoMuon_sel_eta",
            "RecoMuon_sel_theta",
            "RecoMuon_sel_phi",
            "RecoMuon_sel_charge",
            "RecoMuon_sel_mass",

            "n_RecoPhotons",
            "RecoPhoton_e",
            "RecoPhoton_p",
            "RecoPhoton_pt",
            "RecoPhoton_px",
            "RecoPhoton_py",
            "RecoPhoton_pz",
            "RecoPhoton_y",
            "RecoPhoton_eta",
            "RecoPhoton_theta",
            "RecoPhoton_phi",
            "RecoPhoton_charge",
            "RecoPhoton_mass",

            "RecoEmiss_px",
            "RecoEmiss_py",
            "RecoEmiss_pz",
            "RecoEmiss_pt",
            "RecoEmiss_p",
            "RecoEmiss_e",
            "RecoEmiss_eta",
            "RecoEmiss_phi",
            "RecoEmiss_theta",
            "RecoEmiss_y",
            "RecoEmiss_costheta",

            "n_FSGenNeutrino",
            "FSGenNeutrino_e",
            "FSGenNeutrino_p",
            "FSGenNeutrino_pt",
            "FSGenNeutrino_px",
            "FSGenNeutrino_py",
            "FSGenNeutrino_pz",
            "FSGenNeutrino_y",
            "FSGenNeutrino_eta",
            "FSGenNeutrino_theta",
            "FSGenNeutrino_phi",

            "n_ZGenNeutrino",
            "ZGenNeutrino_e",
            "ZGenNeutrino_p",
            "ZGenNeutrino_pt",
            "ZGenNeutrino_px",
            "ZGenNeutrino_py",
            "ZGenNeutrino_pz",
            "ZGenNeutrino_y",
            "ZGenNeutrino_eta",
            "ZGenNeutrino_theta",
            "ZGenNeutrino_phi",

            "RecoZ_px",
            "RecoZ_py",
            "RecoZ_pz",
            "RecoZ_p",
            "RecoZ_pt",
            "RecoZ_e",
            "RecoZ_eta",
            "RecoZ_phi",
            "RecoZ_theta",
            "RecoZ_y",
            "RecoZ_mass",

            "TagJet_kt4_px", 
            "TagJet_kt4_py",    
            "TagJet_kt4_pz",      
            "TagJet_kt4_p",  
            "TagJet_kt4_pt",    
            "TagJet_kt4_phi", 
            "TagJet_kt4_eta",     
            "TagJet_kt4_theta",          
            "TagJet_kt4_e",     
            "TagJet_kt4_mass",        
            "TagJet_kt4_charge",       
            "TagJet_kt4_flavor",
            "n_TagJet_kt4",
            "n_TagJet_kt4_constituents",
            "n_TagJet_kt4_charged_constituents",
            "n_TagJet_kt4_neutral_constituents",

            "RecoH_px",
            "RecoH_py",
            "RecoH_pz",
            "RecoH_p",
            "RecoH_pt",
            "RecoH_e",
            "RecoH_eta",
            "RecoH_phi",
            "RecoH_theta",
            "RecoH_y",
            "RecoH_mass",

            "Recoil_mass",

            "dijet_pair1_mass",
            "dijet_pair2_mass",
            
        ]

        return branchList
