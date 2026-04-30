import os, copy
import ROOT
import urllib.request

processList = {

    # Signal
    'wzp6_ee_eeH_HWW_ecm365':   {'fraction':0.05},
    'wzp6_ee_mumuH_HWW_ecm365': {'fraction':0.05},
    'wzp6_ee_eeH_HZZ_ecm365':   {'fraction':0.05},
    'wzp6_ee_mumuH_HZZ_ecm365': {'fraction':0.07},

    # Background
    # 'p8_ee_WW_ecm365': {'fraction':0.00005},
    # 'p8_ee_ZZ_ecm365': {'fraction':0.00009},
    # 'p8_ee_tt_ecm365': {'fraction':0.00002},
}

# directories
inputDir = "/ceph/sgiappic/HiggsCP/winter23"
outputDir = "/ceph/aratanshi/stage_gen_output"
# includePaths = ["functions.h"]

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
            .Define("n_GenElectrons",      "FCCAnalyses::MCParticle::get_n(GenElectron)")
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
            .Define("n_GenMuons",      "FCCAnalyses::MCParticle::get_n(GenMuon)")
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
        
            # final state generated electrons (genStatus==1 denotes FS particle)
            .Define("FSGenElectron",        "FCCAnalyses::MCParticle::sel_genStatus(1)(GenElectron)")
            .Define("n_FSGenElectrons",      "FCCAnalyses::MCParticle::get_n(FSGenElectron)")
            .Define("FSGenElectron_e",      "FCCAnalyses::MCParticle::get_e(FSGenElectron)")
            .Define("FSGenElectron_p",      "FCCAnalyses::MCParticle::get_p(FSGenElectron)")
            .Define("FSGenElectron_pt",     "FCCAnalyses::MCParticle::get_pt(FSGenElectron)")
            .Define("FSGenElectron_px",     "FCCAnalyses::MCParticle::get_px(FSGenElectron)")
            .Define("FSGenElectron_py",     "FCCAnalyses::MCParticle::get_py(FSGenElectron)")
            .Define("FSGenElectron_pz",     "FCCAnalyses::MCParticle::get_pz(FSGenElectron)")
            .Define("FSGenElectron_y",      "FCCAnalyses::MCParticle::get_y(FSGenElectron)")
            .Define("FSGenElectron_eta",    "FCCAnalyses::MCParticle::get_eta(FSGenElectron)")
            .Define("FSGenElectron_theta",  "FCCAnalyses::MCParticle::get_theta(FSGenElectron)")
            .Define("FSGenElectron_phi",    "FCCAnalyses::MCParticle::get_phi(FSGenElectron)")
            .Define("FSGenElectron_charge", "FCCAnalyses::MCParticle::get_charge(FSGenElectron)")
            .Define("FSGenElectron_mass",   "FCCAnalyses::MCParticle::get_mass(FSGenElectron)")
            
            # final state generated muons 
            .Define("FSGenMuon",        "FCCAnalyses::MCParticle::sel_genStatus(1)(GenMuon)")
            .Define("n_FSGenMuons",      "FCCAnalyses::MCParticle::get_n(FSGenMuon)")
            .Define("FSGenMuon_e",      "FCCAnalyses::MCParticle::get_e(FSGenMuon)")
            .Define("FSGenMuon_p",      "FCCAnalyses::MCParticle::get_p(FSGenMuon)")
            .Define("FSGenMuon_pt",     "FCCAnalyses::MCParticle::get_pt(FSGenMuon)")
            .Define("FSGenMuon_px",     "FCCAnalyses::MCParticle::get_px(FSGenMuon)")
            .Define("FSGenMuon_py",     "FCCAnalyses::MCParticle::get_py(FSGenMuon)")
            .Define("FSGenMuon_pz",     "FCCAnalyses::MCParticle::get_pz(FSGenMuon)")
            .Define("FSGenMuon_y",      "FCCAnalyses::MCParticle::get_y(FSGenMuon)")
            .Define("FSGenMuon_eta",    "FCCAnalyses::MCParticle::get_eta(FSGenMuon)")
            .Define("FSGenMuon_theta",  "FCCAnalyses::MCParticle::get_theta(FSGenMuon)")
            .Define("FSGenMuon_phi",    "FCCAnalyses::MCParticle::get_phi(FSGenMuon)")
            .Define("FSGenMuon_charge", "FCCAnalyses::MCParticle::get_charge(FSGenMuon)")
            .Define("FSGenMuon_mass",   "FCCAnalyses::MCParticle::get_mass(FSGenMuon)")
            
            # generated electrons from Z
            .Define("GenElectron_Z",        "FCCAnalyses::MCParticle::sel_parentID(23, true, true)(GenElectron, Particle, Particle0)")
            .Define("n_GenElectrons_Z",     "FCCAnalyses::MCParticle::get_n(GenElectron_Z)")
            .Define("GenElectron_Z_e",      "FCCAnalyses::MCParticle::get_e(GenElectron_Z)")
            .Define("GenElectron_Z_p",      "FCCAnalyses::MCParticle::get_p(GenElectron_Z)")
            .Define("GenElectron_Z_pt",     "FCCAnalyses::MCParticle::get_pt(GenElectron_Z)")
            .Define("GenElectron_Z_px",     "FCCAnalyses::MCParticle::get_px(GenElectron_Z)")
            .Define("GenElectron_Z_py",     "FCCAnalyses::MCParticle::get_py(GenElectron_Z)")
            .Define("GenElectron_Z_pz",     "FCCAnalyses::MCParticle::get_pz(GenElectron_Z)")
            .Define("GenElectron_Z_y",      "FCCAnalyses::MCParticle::get_y(GenElectron_Z)")
            .Define("GenElectron_Z_eta",    "FCCAnalyses::MCParticle::get_eta(GenElectron_Z)")
            .Define("GenElectron_Z_theta",  "FCCAnalyses::MCParticle::get_theta(GenElectron_Z)")
            .Define("GenElectron_Z_phi",    "FCCAnalyses::MCParticle::get_phi(GenElectron_Z)")
            .Define("GenElectron_Z_charge", "FCCAnalyses::MCParticle::get_charge(GenElectron_Z)")
            .Define("GenElectron_Z_mass",   "FCCAnalyses::MCParticle::get_mass(GenElectron_Z)")

            # generated muons from Z
            .Define("GenMuon_Z",        "FCCAnalyses::MCParticle::sel_parentID(23, true, true)(GenMuon, Particle, Particle0)")
            .Define("n_GenMuons_Z",     "FCCAnalyses::MCParticle::get_n(GenMuon_Z)")
            .Define("GenMuon_Z_e",      "FCCAnalyses::MCParticle::get_e(GenMuon_Z)")
            .Define("GenMuon_Z_p",      "FCCAnalyses::MCParticle::get_p(GenMuon_Z)")
            .Define("GenMuon_Z_pt",     "FCCAnalyses::MCParticle::get_pt(GenMuon_Z)")
            .Define("GenMuon_Z_px",     "FCCAnalyses::MCParticle::get_px(GenMuon_Z)")
            .Define("GenMuon_Z_py",     "FCCAnalyses::MCParticle::get_py(GenMuon_Z)")
            .Define("GenMuon_Z_pz",     "FCCAnalyses::MCParticle::get_pz(GenMuon_Z)")
            .Define("GenMuon_Z_y",      "FCCAnalyses::MCParticle::get_y(GenMuon_Z)")
            .Define("GenMuon_Z_eta",    "FCCAnalyses::MCParticle::get_eta(GenMuon_Z)")
            .Define("GenMuon_Z_theta",  "FCCAnalyses::MCParticle::get_theta(GenMuon_Z)")
            .Define("GenMuon_Z_phi",    "FCCAnalyses::MCParticle::get_phi(GenMuon_Z)")
            .Define("GenMuon_Z_charge", "FCCAnalyses::MCParticle::get_charge(GenMuon_Z)")
            .Define("GenMuon_Z_mass",   "FCCAnalyses::MCParticle::get_mass(GenMuon_Z)")

            # selection for Z -> 2L
            .Filter("(n_GenElectrons_Z == 2 && GenElectron_Z_charge[0] != GenElectron_Z_charge[1]) || "
                    "(n_GenMuons_Z == 2 && GenMuon_Z_charge[0] != GenMuon_Z_charge[1])")

            # lepton momenta
            .Define("GenElectron_p4", "TLorentzVector(GenElectron_Z_px[0], GenElectron_Z_py[0], GenElectron_Z_pz[0], GenElectron_Z_e[0]) + "
                                      "TLorentzVector(GenElectron_Z_px[1], GenElectron_Z_py[1], GenElectron_Z_pz[1], GenElectron_Z_e[1])")
        
            .Define("GenMuon_p4", "TLorentzVector(GenMuon_Z_px[0], GenMuon_Z_py[0], GenMuon_Z_pz[0], GenMuon_Z_e[0]) + "
                                  "TLorentzVector(GenMuon_Z_px[1], GenMuon_Z_py[1], GenMuon_Z_pz[1], GenMuon_Z_e[1])")

            # angular separation
            .Define("GenElectron_dR", "sqrt(pow(GenElectron_Z_eta[0] - GenElectron_Z_eta[1], 2) + "
                                           "pow(GenElectron_Z_phi[0] - GenElectron_Z_phi[1], 2))")
            .Define("GenMuon_dR", "sqrt(pow(GenMuon_Z_eta[0] - GenMuon_Z_eta[1], 2) + pow(GenMuon_Z_phi[0] - GenMuon_Z_phi[1], 2))")

            # generated Z
            .Define("GenZ_p4", "(n_GenElectrons_Z == 2) ? GenElectron_p4 : GenMuon_p4")

            # Z properties
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
            .Define("GenH",        "FCCAnalyses::MCParticle::sel_pdgID(25, true)(Particle)")
            .Define("GenH_e",      "FCCAnalyses::MCParticle::get_e(GenH)")
            .Define("GenH_p",      "FCCAnalyses::MCParticle::get_p(GenH)")
            .Define("GenH_pt",     "FCCAnalyses::MCParticle::get_pt(GenH)")
            .Define("GenH_px",     "FCCAnalyses::MCParticle::get_px(GenH)")
            .Define("GenH_py",     "FCCAnalyses::MCParticle::get_py(GenH)")
            .Define("GenH_pz",     "FCCAnalyses::MCParticle::get_pz(GenH)")
            .Define("GenH_y",      "FCCAnalyses::MCParticle::get_y(GenH)")
            .Define("GenH_eta",    "FCCAnalyses::MCParticle::get_eta(GenH)")
            .Define("GenH_theta",  "FCCAnalyses::MCParticle::get_theta(GenH)")
            .Define("GenH_phi",    "FCCAnalyses::MCParticle::get_phi(GenH)")
            .Define("GenH_charge", "FCCAnalyses::MCParticle::get_charge(GenH)")
            .Define("GenH_mass",   "FCCAnalyses::MCParticle::get_mass(GenH)")

        )
        return df2

    def output():
        branchList = [

            "n_GenElectrons",     
            "GenElectron_e",     
            "GenElectron_p",     
            "GenElectron_pt",    
            "GenElectron_px",    
            "GenElectron_py",    
            "GenElectron_pz",    
            "GenElectron_y",     
            "GenElectron_eta",   
            "GenElectron_theta", 
            "GenElectron_phi",   
            "GenElectron_charge",
            "GenElectron_mass",  
            
            "n_GenMuons",     
            "GenMuon_e",     
            "GenMuon_p",     
            "GenMuon_pt",    
            "GenMuon_px",    
            "GenMuon_py",    
            "GenMuon_pz",    
            "GenMuon_y",     
            "GenMuon_eta",   
            "GenMuon_theta", 
            "GenMuon_phi",   
            "GenMuon_charge",
            "GenMuon_mass",  
            
            "GenElectron_dR",
            "GenMuon_dR",

            "GenZ_px",   
            "GenZ_py",   
            "GenZ_pz",   
            "GenZ_p",    
            "GenZ_pt",   
            "GenZ_e",    
            "GenZ_eta",  
            "GenZ_phi",  
            "GenZ_theta",
            "GenZ_y",    
            "GenZ_mass", 

            "n_GenH",     
            "GenH_e",     
            "GenH_p",     
            "GenH_pt",    
            "GenH_px",    
            "GenH_py",    
            "GenH_pz",    
            "GenH_y",     
            "GenH_eta",   
            "GenH_theta", 
            "GenH_phi",   
            "GenH_charge",
            "GenH_mass",  
            
        ]

        return branchList
