import os, copy
import ROOT
import urllib.request

processList = {

    # Signal
    'wzp6_ee_eeH_HWW_ecm365':   {'fraction':0.001},
    'wzp6_ee_mumuH_HWW_ecm365': {'fraction':0.001},
    'wzp6_ee_eeH_HZZ_ecm365':   {'fraction':0.001},
    'wzp6_ee_mumuH_HZZ_ecm365': {'fraction':0.001},

    # Background
    # 'p8_ee_WW_ecm365': {'fraction':0.00005},
    # 'p8_ee_ZZ_ecm365': {'fraction':0.00009},
    # 'p8_ee_tt_ecm365': {'fraction':0.00002},
}

# directories
inputDir = "/ceph/sgiappic/HiggsCP/winter23"
outputDir = "/ceph/aratanshi/stage_gen_output"
includePaths = ["../functions.h"]

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

            # generated electrons
            .Define("GenElectron",        "FCCAnalyses::MCParticle::sel_pdgID(11, true)(Particle)")
            .Define("n_GenElectron",      "FCCAnalyses::MCParticle::get_n(GenElectron)")
            .Define("GenElectron_e",      "FCCAnalyses::MCParticle::get_e(GenElectron)")
            .Define("GenElectron_p",      "FCCAnalyses::MCParticle::get_p(GenElectron)")
            .Define("GenElectron_pt",     "FCCAnalyses::MCParticle::get_pt(GenElectron)")
            .Define("GenElectron_px",     "FCCAnalyses::MCParticle::get_px(GenElectron)")
            .Define("GenElectron_py",     "FCCAnalyses::MCParticle::get_py(GenElectron)")
            .Define("GenElectron_pz",     "FCCAnalyses::MCParticle::get_pz(GenElectron)")
            .Define("GenElectron_y",      "FCCAnalyses::MCParticle::get_y(GenElectron)") # rapidity
            .Define("GenElectron_eta",    "FCCAnalyses::MCParticle::get_eta(GenElectron)") # pseudorapidity
            .Define("GenElectron_theta",  "FCCAnalyses::MCParticle::get_theta(GenElectron)")
            .Define("GenElectron_phi",    "FCCAnalyses::MCParticle::get_phi(GenElectron)") # polar angle in the transverse plane phi
            .Define("GenElectron_charge", "FCCAnalyses::MCParticle::get_charge(GenElectron)")
            .Define("GenElectron_mass",   "FCCAnalyses::MCParticle::get_mass(GenElectron)")

            # generated muons
            .Define("GenMuon",        "FCCAnalyses::MCParticle::sel_pdgID(13, true)(Particle)")
            .Define("n_GenMuon",      "FCCAnalyses::MCParticle::get_n(GenMuon)")
            .Define("GenMuon_e",      "FCCAnalyses::MCParticle::get_e(GenMuon)")
            .Define("GenMuon_p",      "FCCAnalyses::MCParticle::get_p(GenMuon)")
            .Define("GenMuon_pt",     "FCCAnalyses::MCParticle::get_pt(GenMuon)")
            .Define("GenMuon_px",     "FCCAnalyses::MCParticle::get_px(GenMuon)")
            .Define("GenMuon_py",     "FCCAnalyses::MCParticle::get_py(GenMuon)")
            .Define("GenMuon_pz",     "FCCAnalyses::MCParticle::get_pz(GenMuon)")
            .Define("GenMuon_y",      "FCCAnalyses::MCParticle::get_y(GenMuon)")
            .Define("GenMuon_eta",    "FCCAnalyses::MCParticle::get_eta(GenMuon)")
            .Define("GenMuon_theta",  "FCCAnalyses::MCParticle::get_theta(GenMuon)")
            .Define("GenMuon_phi",    "FCCAnalyses::MCParticle::get_phi(GenMuon)")
            .Define("GenMuon_charge", "FCCAnalyses::MCParticle::get_charge(GenMuon)")
            .Define("GenMuon_mass",   "FCCAnalyses::MCParticle::get_mass(GenMuon)")

            # merge electrons and muons
            .Define("GenLepton",        "FCCAnalyses::MCParticle::mergeParticles(GenElectron, GenMuon)")
            .Define("n_GenLepton",      "FCCAnalyses::MCParticle::get_n(GenLepton)")
            .Define("GenLepton_e",      "FCCAnalyses::MCParticle::get_e(GenLepton)")
            .Define("GenLepton_p",      "FCCAnalyses::MCParticle::get_p(GenLepton)")
            .Define("GenLepton_pt",     "FCCAnalyses::MCParticle::get_pt(GenLepton)")
            .Define("GenLepton_px",     "FCCAnalyses::MCParticle::get_px(GenLepton)")
            .Define("GenLepton_py",     "FCCAnalyses::MCParticle::get_py(GenLepton)")
            .Define("GenLepton_pz",     "FCCAnalyses::MCParticle::get_pz(GenLepton)")
            .Define("GenLepton_y",      "FCCAnalyses::MCParticle::get_y(GenLepton)")
            .Define("GenLepton_eta",    "FCCAnalyses::MCParticle::get_eta(GenLepton)")
            .Define("GenLepton_theta",  "FCCAnalyses::MCParticle::get_theta(GenLepton)")
            .Define("GenLepton_phi",    "FCCAnalyses::MCParticle::get_phi(GenLepton)")
            .Define("GenLepton_charge", "FCCAnalyses::MCParticle::get_charge(GenLepton)")
            .Define("GenLepton_mass",   "FCCAnalyses::MCParticle::get_mass(GenLepton)")

            # ---------------------------------
            #
            # Considering two types of leptons:
            #
            # intermediate
            # final state
            #
            # ---------------------------------

            # INTERMEDIATE
            # these are leptons before FSR, sequentially chosen such that they do not come from Z,W,e,mu respectively
            .Define("GenLepton_int_1", "FCCAnalyses::MCParticle::sel_parentID(23, false, true)(GenLepton, Particle, Particle0)") 
            .Define("GenLepton_int_2", "FCCAnalyses::MCParticle::sel_parentID(24, false, true)(GenLepton_int_1, Particle, Particle0)")
            .Define("GenLepton_int_3", "FCCAnalyses::MCParticle::sel_parentID(11, false, true)(GenLepton_int_2, Particle, Particle0)")
            .Define("GenLepton_int",   "FCCAnalyses::MCParticle::sel_parentID(13, false, true)(GenLepton_int_3, Particle, Particle0)")

            .Define("n_GenLepton_int",      "FCCAnalyses::MCParticle::get_n(GenLepton_int)")
            .Define("GenLepton_int_e",      "FCCAnalyses::MCParticle::get_e(GenLepton_int)")
            .Define("GenLepton_int_pt",     "FCCAnalyses::MCParticle::get_pt(GenLepton_int)")
            .Define("GenLepton_int_px",     "FCCAnalyses::MCParticle::get_px(GenLepton_int)")
            .Define("GenLepton_int_py",     "FCCAnalyses::MCParticle::get_py(GenLepton_int)")
            .Define("GenLepton_int_pz",     "FCCAnalyses::MCParticle::get_pz(GenLepton_int)")
            .Define("GenLepton_int_eta",    "FCCAnalyses::MCParticle::get_eta(GenLepton_int)")
            .Define("GenLepton_int_phi",    "FCCAnalyses::MCParticle::get_phi(GenLepton_int)")
            .Define("GenLepton_int_charge", "FCCAnalyses::MCParticle::get_charge(GenLepton_int)")
            .Define("GenLepton_int_mass",   "FCCAnalyses::MCParticle::get_mass(GenLepton_int)")
                        
            # FINAL STATE (from Final State Radiation)
            # leptons chosen such that they do not come from Z,W
            .Define("GenLepton_FS_1", "FCCAnalyses::MCParticle::sel_parentID(23, false, true)(GenLepton, Particle, Particle0)")
            .Define("GenLepton_FS_2", "FCCAnalyses::MCParticle::sel_parentID(24, false, true)(GenLepton_FS_1, Particle, Particle0)")
            # keep only leptons coming from leptons e,mu respectively
            .Define("GenLepton_FS_3", "FCCAnalyses::MCParticle::sel_parentID(11, true, true)(GenLepton_FS_2, Particle, Particle0)")
            .Define("GenLepton_FS_4", "FCCAnalyses::MCParticle::sel_parentID(13, true, true)(GenLepton_FS_2, Particle, Particle0)")
            # merge because lepton flavor does not matter right now
            .Define("GenLepton_FS",   "FCCAnalyses::MCParticle::mergeParticles(GenLepton_FS_3, GenLepton_FS_4)")

            .Define("n_GenLepton_FS",      "FCCAnalyses::MCParticle::get_n(GenLepton_FS)")
            .Define("GenLepton_FS_e",      "FCCAnalyses::MCParticle::get_e(GenLepton_FS)")
            .Define("GenLepton_FS_pt",     "FCCAnalyses::MCParticle::get_pt(GenLepton_FS)")
            .Define("GenLepton_FS_px",     "FCCAnalyses::MCParticle::get_px(GenLepton_FS)")
            .Define("GenLepton_FS_py",     "FCCAnalyses::MCParticle::get_py(GenLepton_FS)")
            .Define("GenLepton_FS_pz",     "FCCAnalyses::MCParticle::get_pz(GenLepton_FS)")
            .Define("GenLepton_FS_eta",    "FCCAnalyses::MCParticle::get_eta(GenLepton_FS)")
            .Define("GenLepton_FS_phi",    "FCCAnalyses::MCParticle::get_phi(GenLepton_FS)")
            .Define("GenLepton_FS_charge", "FCCAnalyses::MCParticle::get_charge(GenLepton_FS)")
            .Define("GenLepton_FS_mass",   "FCCAnalyses::MCParticle::get_mass(GenLepton_FS)")

            # generated Z from intermediate leptons
            .Define("GenZ_int_idx", "FCCAnalyses::ZHfunctions::FindBestZLeptonPair(GenLepton_int)") # finds best lepton pair and gets those indicies
            .Define("GenZ_int_p4", "FCCAnalyses::ZHfunctions::BuildZFromPair(GenLepton_int, GenZ_int_idx)")
        
            .Define("GenZ_int_px",    "GenZ_int_p4.Px()")
            .Define("GenZ_int_py",    "GenZ_int_p4.Py()")
            .Define("GenZ_int_pz",    "GenZ_int_p4.Pz()")
            .Define("GenZ_int_p",     "GenZ_int_p4.P()")
            .Define("GenZ_int_pt",    "GenZ_int_p4.Pt()")
            .Define("GenZ_int_e",     "GenZ_int_p4.E()")
            .Define("GenZ_int_eta",   "GenZ_int_p4.Eta()")
            .Define("GenZ_int_phi",   "GenZ_int_p4.Phi()")
            .Define("GenZ_int_theta", "GenZ_int_p4.Theta()")
            .Define("GenZ_int_y",     "GenZ_int_p4.Rapidity()")
            .Define("GenZ_int_mass",  "GenZ_int_p4.M()")
            # angular seperation
            .Define("GenLepton_int_dR", "FCCAnalyses::ZHfunctions::deltaR_pair(GenLepton_int, GenZ_int_idx)")


            ######### Production Z #########
            
            # isolating the leptons belonging to the production Z
            .Define("GenLepton_ZProd",        "FCCAnalyses::ZHfunctions::GetZProductionLeptons(GenLepton, Particle, Particle0)")
            .Define("n_GenLepton_ZProd",      "FCCAnalyses::MCParticle::get_n(GenLepton_ZProd)")
            .Define("GenLepton_ZProd_e",      "FCCAnalyses::MCParticle::get_e(GenLepton_ZProd)")
            .Define("GenLepton_ZProd_pt",     "FCCAnalyses::MCParticle::get_pt(GenLepton_ZProd)")
            .Define("GenLepton_ZProd_px",     "FCCAnalyses::MCParticle::get_px(GenLepton_ZProd)")
            .Define("GenLepton_ZProd_py",     "FCCAnalyses::MCParticle::get_py(GenLepton_ZProd)")
            .Define("GenLepton_ZProd_pz",     "FCCAnalyses::MCParticle::get_pz(GenLepton_ZProd)")
            .Define("GenLepton_ZProd_eta",    "FCCAnalyses::MCParticle::get_eta(GenLepton_ZProd)")
            .Define("GenLepton_ZProd_phi",    "FCCAnalyses::MCParticle::get_phi(GenLepton_ZProd)")
            .Define("GenLepton_ZProd_charge", "FCCAnalyses::MCParticle::get_charge(GenLepton_ZProd)")
            .Define("GenLepton_ZProd_mass",   "FCCAnalyses::MCParticle::get_mass(GenLepton_ZProd)")
            
            # feeding these specific leptons into the pairing/building functions
            .Define("GenZ_ZProd_idx", "FCCAnalyses::ZHfunctions::FindBestZLeptonPair(GenLepton_ZProd)") 
            .Define("GenZ_ZProd_p4",  "FCCAnalyses::ZHfunctions::BuildZFromPair(GenLepton_ZProd, GenZ_ZProd_idx)")
            
            # physical properties of the production Z
            .Define("GenZ_ZProd_pt", "GenZ_ZProd_p4.Pt()")
            .Define("GenZ_ZProd_mass", "GenZ_ZProd_p4.M()")
            # dR for prod Z leptons
            .Define("GenLepton_ZProd_dR", "FCCAnalyses::ZHfunctions::deltaR_pair(GenLepton_ZProd, GenZ_ZProd_idx)")

            ######### Recoil mass #########
            
            .Define("p4_initial", "TLorentzVector(0., 0., 0., 365.0)")
            .Define("GenHiggs_recoil_mass", "(p4_initial - GenZ_ZProd_p4).M()")






        
            ######### Higgs decay system: H -> Z Z* or W W* -> 4 quarks #########

            # all quarks in the event
            .Define("GenQuarks", "FCCAnalyses::ZHfunctions::sel_quarks(Particle)")

            # quarks specifically from the Higgs decay chain (not production Z)
            .Define("GenQuarks_HiggsDecay", "FCCAnalyses::ZHfunctions::GetHiggsDecayProducts(GenQuarks, Particle, Particle0)")
            .Define("n_GenQuarks_HiggsDecay", "FCCAnalyses::MCParticle::get_n(GenQuarks_HiggsDecay)")

            # on-shell/off-shell V* system built from truth Higgs-decay quarks
            # returns [Va_mass, Va_energy, Vb_mass, Vb_energy]
            # Va = on-shell (heavier), Vb = off-shell (lighter)
            .Define("GenHiggsVVstar", "FCCAnalyses::ZHfunctions::GetHiggsVVstarSystem(GenQuarks_HiggsDecay)")
            .Define("GenVa_mass",   "GenHiggsVVstar[0]")
            .Define("GenVa_energy", "GenHiggsVVstar[1]")
            .Define("GenVb_mass",   "GenHiggsVVstar[2]")
            .Define("GenVb_energy", "GenHiggsVVstar[3]")

            # fraction of total Higgs-decay energy carried by the off-shell V*
            # small values => off-shell system is "starved" of energy
            .Define("GenVb_energy_fraction", 
                    "(GenVa_energy + GenVb_energy > 0) ? GenVb_energy / (GenVa_energy + GenVb_energy) : -1.")
            
        )
        return df2

    def output():
        branchList = [
            "n_GenLepton",
            "GenLepton_pt",
            "GenLepton_eta",

            "n_GenLepton_int",
            "GenLepton_int_pt",
            "GenLepton_int_mass",
            "GenLepton_int_dR",

            "n_GenLepton_FS",
            "GenLepton_FS_pt",
            "GenLepton_FS_mass",

            "GenZ_int_pt",
            "GenZ_int_mass",

            "n_GenLepton_ZProd",
            "GenLepton_ZProd_pt",
            "GenLepton_ZProd_eta",
            "GenLepton_ZProd_phi",
            "GenLepton_ZProd_mass",
            "GenLepton_ZProd_dR",
            
            "GenZ_ZProd_pt",
            "GenZ_ZProd_mass",  

            "GenHiggs_recoil_mass",


            "n_GenQuarks_HiggsDecay",
            "GenVa_mass",
            "GenVa_energy",
            "GenVb_mass",
            "GenVb_energy",
            "GenVb_energy_fraction",


            
        ]

        return branchList
