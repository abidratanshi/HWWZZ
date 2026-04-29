import os, copy
import ROOT
import urllib.request

processList = {

    # Signal
    'wzp6_ee_eeH_HWW_ecm365':   {'fraction':0.005},
    'wzp6_ee_mumuH_HWW_ecm365': {'fraction':0.005},
    'wzp6_ee_eeH_HZZ_ecm365':   {'fraction':0.005},
    'wzp6_ee_mumuH_HZZ_ecm365': {'fraction':0.007},

    # Background
    'p8_ee_WW_ecm365': {'fraction':0.00005},
    'p8_ee_ZZ_ecm365': {'fraction':0.00009},
    'p8_ee_tt_ecm365': {'fraction':0.00002},
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

                #################
                # Gen particles #
                #################
                #### PDG IDs ####
                #### e  = 11 ####
                #### mu = 13 ####
                #### Z  = 23 ####
                #### W  = 24 ####
                #### H  = 25 ####
                #################

                .Alias("Particle0", "Particle#0.index")
                .Alias("Particle1", "Particle#1.index")
                .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
                .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

                # all final state (FS) gen electrons and positrons
                .Define("GenElectron_PID",         "FCCAnalyses::MCParticle::sel_pdgID(11, true)(Particle)")
                .Define("FSGenElectron",           "FCCAnalyses::MCParticle::sel_genStatus(1)(GenElectron_PID)") # genStatus==1 denotes FS particle
                .Define("n_FSGenElectron",         "FCCAnalyses::MCParticle::get_n(FSGenElectron)")
                .Define("FSGenElectron_e",         "FCCAnalyses::MCParticle::get_e(FSGenElectron)")
                .Define("FSGenElectron_p",         "FCCAnalyses::MCParticle::get_p(FSGenElectron)")
                .Define("FSGenElectron_pt",        "FCCAnalyses::MCParticle::get_pt(FSGenElectron)")
                .Define("FSGenElectron_px",        "FCCAnalyses::MCParticle::get_px(FSGenElectron)")
                .Define("FSGenElectron_py",        "FCCAnalyses::MCParticle::get_py(FSGenElectron)")
                .Define("FSGenElectron_pz",        "FCCAnalyses::MCParticle::get_pz(FSGenElectron)")
                .Define("FSGenElectron_y",         "FCCAnalyses::MCParticle::get_y(FSGenElectron)") # rapidity
                .Define("FSGenElectron_eta",       "FCCAnalyses::MCParticle::get_eta(FSGenElectron)") # pseudorapidity
                .Define("FSGenElectron_theta",     "FCCAnalyses::MCParticle::get_theta(FSGenElectron)")
                .Define("FSGenElectron_phi",       "FCCAnalyses::MCParticle::get_phi(FSGenElectron)") # polar angle in the transverse plane phi
                .Define("FSGenElectron_charge",    "FCCAnalyses::MCParticle::get_charge(FSGenElectron)")
                .Define("FSGenElectron_mass",      "FCCAnalyses::MCParticle::get_mass(FSGenElectron)")
                .Define("FSGenElectron_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(FSGenElectron,Particle,Particle0)")
                .Define("FSGenElectron_vertex_x",  "FCCAnalyses::MCParticle::get_vertex_x( FSGenElectron )")
                .Define("FSGenElectron_vertex_y",  "FCCAnalyses::MCParticle::get_vertex_y( FSGenElectron )")
                .Define("FSGenElectron_vertex_z",  "FCCAnalyses::MCParticle::get_vertex_z( FSGenElectron )")
                
                # all final state gen muons 
                .Define("GenMuon_PID",         "FCCAnalyses::MCParticle::sel_pdgID(13, true)(Particle)")
                .Define("FSGenMuon",           "FCCAnalyses::MCParticle::sel_genStatus(1)(GenMuon_PID)")
                .Define("n_FSGenMuon",         "FCCAnalyses::MCParticle::get_n(FSGenMuon)")
                .Define("FSGenMuon_e",         "FCCAnalyses::MCParticle::get_e(FSGenMuon)")
                .Define("FSGenMuon_p",         "FCCAnalyses::MCParticle::get_p(FSGenMuon)")
                .Define("FSGenMuon_pt",        "FCCAnalyses::MCParticle::get_pt(FSGenMuon)")
                .Define("FSGenMuon_px",        "FCCAnalyses::MCParticle::get_px(FSGenMuon)")
                .Define("FSGenMuon_py",        "FCCAnalyses::MCParticle::get_py(FSGenMuon)")
                .Define("FSGenMuon_pz",        "FCCAnalyses::MCParticle::get_pz(FSGenMuon)")
                .Define("FSGenMuon_y",         "FCCAnalyses::MCParticle::get_y(FSGenMuon)")
                .Define("FSGenMuon_eta",       "FCCAnalyses::MCParticle::get_eta(FSGenMuon)")
                .Define("FSGenMuon_theta",     "FCCAnalyses::MCParticle::get_theta(FSGenMuon)")
                .Define("FSGenMuon_phi",       "FCCAnalyses::MCParticle::get_phi(FSGenMuon)")
                .Define("FSGenMuon_charge",    "FCCAnalyses::MCParticle::get_charge(FSGenMuon)")
                .Define("FSGenMuon_mass",      "FCCAnalyses::MCParticle::get_mass(FSGenMuon)")
                .Define("FSGenMuon_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(FSGenMuon,Particle,Particle0)")
                .Define("FSGenMuon_vertex_x",  "FCCAnalyses::MCParticle::get_vertex_x( FSGenMuon )")
                .Define("FSGenMuon_vertex_y",  "FCCAnalyses::MCParticle::get_vertex_y( FSGenMuon )")
                .Define("FSGenMuon_vertex_z",  "FCCAnalyses::MCParticle::get_vertex_z( FSGenMuon )")

                # generated electrons from Z
                .Define("GenElectron_fromZ",         "FCCAnalyses::MCParticle::sel_parentID(23, true, true)(FSGenElectron, Particle, Particle0)")
                .Define("n_GenElectron_fromZ",       "FCCAnalyses::MCParticle::get_n(GenElectron_fromZ)")
                .Define("GenElectron_fromZ_px",      "FCCAnalyses::MCParticle::get_px(GenElectron_fromZ)")
                .Define("GenElectron_fromZ_py",      "FCCAnalyses::MCParticle::get_py(GenElectron_fromZ)")
                .Define("GenElectron_fromZ_pz",      "FCCAnalyses::MCParticle::get_pz(GenElectron_fromZ)")
                .Define("GenElectron_fromZ_e",       "FCCAnalyses::MCParticle::get_e(GenElectron_fromZ)")

                .Define("GenElectron_fromZ_charge",  "FCCAnalyses::MCParticle::get_charge(GenElectron_fromZ)")
                .Define("GenElectron_fromZ_eta",      "FCCAnalyses::MCParticle::get_eta(GenElectron_fromZ)")
                .Define("GenElectron_fromZ_phi",      "FCCAnalyses::MCParticle::get_phi(GenElectron_fromZ)")

                .Define("GenElectron_dR", "sqrt(pow(GenElectron_fromZ_eta[0]-GenElectron_fromZ_eta[1],2) + pow(GenElectron_fromZ_phi[0]-GenElectron_fromZ_phi[1],2))")

                # generated muons from Z
                .Define("GenMuon_fromZ",    "FCCAnalyses::MCParticle::sel_parentID(23, true, true)(FSGenMuon, Particle, Particle0)")
                .Define("n_GenMuon_fromZ",  "FCCAnalyses::MCParticle::get_n(GenMuon_fromZ)")
                .Define("GenMuon_fromZ_px", "FCCAnalyses::MCParticle::get_px(GenMuon_fromZ)")
                .Define("GenMuon_fromZ_py", "FCCAnalyses::MCParticle::get_py(GenMuon_fromZ)")
                .Define("GenMuon_fromZ_pz", "FCCAnalyses::MCParticle::get_pz(GenMuon_fromZ)")
                .Define("GenMuon_fromZ_e",  "FCCAnalyses::MCParticle::get_e(GenMuon_fromZ)")
            
                .Define("GenMuon_fromZ_charge",  "FCCAnalyses::MCParticle::get_charge(GenMuon_fromZ)")
                .Define("GenMuon_fromZ_eta",      "FCCAnalyses::MCParticle::get_eta(GenMuon_fromZ)")
                .Define("GenMuon_fromZ_phi",      "FCCAnalyses::MCParticle::get_phi(GenMuon_fromZ)")

                .Define("GenMuon_dR", "sqrt(pow(GenMuon_fromZ_eta[0]-GenMuon_fromZ_eta[1],2) + pow(GenMuon_fromZ_phi[0]-GenMuon_fromZ_phi[1],2))")

                # selection for Z -> 2L
                .Filter("(n_GenElectron_fromZ == 2 && GenElectron_fromZ_charge[0] != GenElectron_fromZ_charge[1]) || "
                        "(n_GenMuon_fromZ == 2 && GenMuon_fromZ_charge[0] != GenMuon_fromZ_charge[1])")

                # generated lepton momenta
                .Define("GenElectron_p4", "TLorentzVector(GenElectron_fromZ_px[0], GenElectron_fromZ_py[0], GenElectron_fromZ_pz[0], GenElectron_fromZ_e[0]) + "
                                          "TLorentzVector(GenElectron_fromZ_px[1], GenElectron_fromZ_py[1], GenElectron_fromZ_pz[1], GenElectron_fromZ_e[1])")
            
                .Define("GenMuon_p4", "TLorentzVector(GenMuon_fromZ_px[0], GenMuon_fromZ_py[0], GenMuon_fromZ_pz[0], GenMuon_fromZ_e[0]) + "
                                      "TLorentzVector(GenMuon_fromZ_px[1], GenMuon_fromZ_py[1], GenMuon_fromZ_pz[1], GenMuon_fromZ_e[1])")

                # generated Z
                .Define("GenZ_p4", "(n_GenElectron_fromZ == 2) ? GenElectron_p4 : GenMuon_p4")

                # generated Z properties
                .Define("GenZ_px",    "GenZ_p4.Px()")
                .Define("GenZ_py",    "GenZ_p4.Py()")
                .Define("GenZ_pz",    "GenZ_p4.Pz()")
                .Define("GenZ_p",     "GenZ_p4.P()")
                .Define("GenZ_pt",    "GenZ_p4.Pt()")
                .Define("GenZ_e",     "GenZ_p4.E()")
                .Define("GenZ_eta",   "GenZ_p4.Eta()")
                .Define("GenZ_phi",   "GenZ_p4.Phi()")
                .Define("GenZ_theta", "GenZ_p4.Theta()")
                .Define("GenZ_y",     "GenZ_p4.Rapidity()")
                .Define("GenZ_mass",  "GenZ_p4.M()")

                # generated Higgs
                .Define("GenH", "FCCAnalyses::MCParticle::sel_pdgID(25, true)(Particle)")
                .Define("GenH_mass", "FCCAnalyses::MCParticle::get_mass(GenH)")

                ##################
                # Reco particles #
                ##################

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

                # Constraining recoil mass here (before H reconstruction) to enforce the leptonic Z is consistent with being the production Z
                .Define("Total_p4",    "TLorentzVector(0.,0.,0.,365.)")
                .Define("Recoil_mass", "(Total_p4 - RecoZ_p4).M()")
                .Filter("abs(Recoil_mass - 125.0) < 20")

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

        # EXCLUSIVE 2 JETS
        jetClusteringHelper_kt2  = ExclusiveJetClusteringHelper(
            collections["PFParticles"], 2, "kt2"
        )
        df2 = jetClusteringHelper_kt2.define(df2)

        # define jet flavour tagging parameters
        jetFlavourHelper_kt2 = JetFlavourHelper(
            collections,
            jetClusteringHelper_kt2.jets,
            jetClusteringHelper_kt2.constituents,
            "kt2",
        )
        
        # define observables for tagger
        df2 = jetFlavourHelper_kt2.define(df2)

        # tagger inference
        df2 = jetFlavourHelper_kt2.inference(weaver_preproc, weaver_model, df2)
        
        df2 = (df2

                .Define("TagJet_kt2_px",                     "JetClusteringUtils::get_px({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_py",                     "JetClusteringUtils::get_py({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_pz",                     "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_p",                      "JetClusteringUtils::get_p({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_pt",                     "JetClusteringUtils::get_pt({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_phi",                    "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_eta",                    "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_theta",                  "JetClusteringUtils::get_theta({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_e",                      "JetClusteringUtils::get_e({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_mass",                   "JetClusteringUtils::get_m({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_charge",                 "JetConstituentsUtils::get_charge_constituents({})".format(jetClusteringHelper_kt2.constituents))
                .Define("TagJet_kt2_flavor",                 "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_kt2.jets))
                .Define("n_TagJet_kt2",                      "return int(TagJet_kt2_flavor.size())")
                .Define("n_TagJet_kt2_constituents",         "JetConstituentsUtils::get_n_constituents({})".format(jetClusteringHelper_kt2.constituents))
                .Define("n_TagJet_kt2_charged_constituents", "JetConstituentsUtils::get_ncharged_constituents({})".format(jetClusteringHelper_kt2.constituents))
                .Define("n_TagJet_kt2_neutral_constituents", "JetConstituentsUtils::get_nneutral_constituents({})".format(jetClusteringHelper_kt2.constituents))
                .Define("TagJet_kt2_cleanup",                "JetConstituentsUtils::cleanup_taggedjet({})".format(jetClusteringHelper_kt2.constituents)) 

                # array of TLVs for 2 jets
                .Define("Jets2_p4", "ROOT::VecOps::Construct<TLorentzVector>(TagJet_kt2_px, TagJet_kt2_py, TagJet_kt2_pz, TagJet_kt2_e)")

                # Reconstructing H from 2 jets
                .Define("RecoH2_p4", "Jets2_p4[0] + Jets2_p4[1]")

                # H properties
                .Define("RecoH2_px",    "RecoH2_p4.Px()")
                .Define("RecoH2_py",    "RecoH2_p4.Py()")
                .Define("RecoH2_pz",    "RecoH2_p4.Pz()")
                .Define("RecoH2_p",     "RecoH2_p4.P()")
                .Define("RecoH2_pt",    "RecoH2_p4.Pt()")
                .Define("RecoH2_e",     "RecoH2_p4.E()")
                .Define("RecoH2_eta",   "RecoH2_p4.Eta()")
                .Define("RecoH2_phi",   "RecoH2_p4.Phi()")
                .Define("RecoH2_theta", "RecoH2_p4.Theta()")
                .Define("RecoH2_y",     "RecoH2_p4.Rapidity()")
                .Define("RecoH2_mass",  "RecoH2_p4.M()")
               
              )

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
                .Define("Jets4_p4", "ROOT::VecOps::Construct<TLorentzVector>(TagJet_kt4_px, TagJet_kt4_py, TagJet_kt4_pz, TagJet_kt4_e)")

                # get best jet pairings
                .Define("BestPairing", "FCCAnalyses::ZHfunctions::FindBestJetPairing(Jets4_p4)")

                # reconstructing H from 4 jets
                .Define("RecoH4_p4", "Jets4_p4[BestPairing[0]] + Jets4_p4[BestPairing[1]] + "
                                     "Jets4_p4[BestPairing[2]] + Jets4_p4[BestPairing[3]]")

                # H properties
                .Define("RecoH4_px",    "RecoH4_p4.Px()")
                .Define("RecoH4_py",    "RecoH4_p4.Py()")
                .Define("RecoH4_pz",    "RecoH4_p4.Pz()")
                .Define("RecoH4_p",     "RecoH4_p4.P()")
                .Define("RecoH4_pt",    "RecoH4_p4.Pt()")
                .Define("RecoH4_e",     "RecoH4_p4.E()")
                .Define("RecoH4_eta",   "RecoH4_p4.Eta()")
                .Define("RecoH4_phi",   "RecoH4_p4.Phi()")
                .Define("RecoH4_theta", "RecoH4_p4.Theta()")
                .Define("RecoH4_y",     "RecoH4_p4.Rapidity()")
                .Define("RecoH4_mass",  "RecoH4_p4.M()")

                # comparing between the two Higgs reconstruction methods (2 vs. 4 jets)
                .Define("d_RecoH_mass", "RecoH2_mass - RecoH4_mass")

                # comparing each reconstructed Higgs to the generated Higgs
                .Define("d_RecoH2_GenH_mass", "RecoH2_mass - GenH_mass[0]")
                .Define("d_RecoH4_GenH_mass", "RecoH4_mass - GenH_mass[0]")

        )
        return df2

    def output():
        branchList = [

            #################
            # Gen particles #
            #################
            
            "GenElectron_dR",
            "GenMuon_dR",
            "GenZ_mass",
            "GenH_mass",

            ##################
            # Reco particles #
            ##################

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

            "Recoil_mass",

            "TagJet_kt2_px",
            "TagJet_kt2_py",
            "TagJet_kt2_pz",
            "TagJet_kt2_p",
            "TagJet_kt2_pt",
            "TagJet_kt2_phi",
            "TagJet_kt2_eta",
            "TagJet_kt2_theta",
            "TagJet_kt2_e",
            "TagJet_kt2_mass",
            "TagJet_kt2_charge",
            "TagJet_kt2_flavor",
            "n_TagJet_kt2",
            "n_TagJet_kt2_constituents",
            "n_TagJet_kt2_charged_constituents",
            "n_TagJet_kt2_neutral_constituents",
            
            "RecoH2_px",
            "RecoH2_py",
            "RecoH2_pz",
            "RecoH2_p",
            "RecoH2_pt",
            "RecoH2_e",
            "RecoH2_eta",
            "RecoH2_phi",
            "RecoH2_theta",
            "RecoH2_y",
            "RecoH2_mass",

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

            "RecoH4_px",
            "RecoH4_py",
            "RecoH4_pz",
            "RecoH4_p",
            "RecoH4_pt",
            "RecoH4_e",
            "RecoH4_eta",
            "RecoH4_phi",
            "RecoH4_theta",
            "RecoH4_y",
            "RecoH4_mass",
            
            "d_RecoH_mass",
            "d_RecoH2_GenH_mass",
            "d_RecoH4_GenH_mass",
            

        ]

        return branchList
