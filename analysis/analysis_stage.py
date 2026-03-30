import os, copy
import ROOT
import urllib.request

processList = {    
    
    # Background
    'p8_ee_WW_ecm365':{'fraction':0.0005},
    'p8_ee_ZZ_ecm365':{'fraction':0.0009},
    'p8_ee_tt_ecm365':{'fraction':0.02},

    # Signal
    'wzp6_ee_eeH_HWW_ecm365': {'fraction':0.05},
    'wzp6_ee_eeH_HZZ_ecm365': {'fraction':0.05},
    'wzp6_ee_mumuH_HWW_ecm365': {'fraction':0.05},
    'wzp6_ee_mumuH_HZZ_ecm365': {'fraction':0.07},
}

inputDir = "/ceph/sgiappic/HiggsCP/winter23"
outputDir = "/ceph/aratanshi/stage_output"
includePaths = ["functions.h"]

nCPUS = 8

### necessary to run on HTCondor ###
# eosType = "eosuser"

#Optional running on HTCondor, default is False
# runBatch = True

#Optional batch queue name when running on HTCondor, default is workday
# batchQueue = "longlunch"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
# compGroup = "group_u_CMS.u_zh.users"

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

                .Alias("Particle0", "Particle#0.index")
                .Alias("Particle1", "Particle#1.index")
                .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
                .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

                # all final state gen electrons and positrons
                # gen status==1 means final state particle (FS)
                .Define("GenElectron_PID", "FCCAnalyses::MCParticle::sel_pdgID(11, true)(Particle)")
                .Define("FSGenElectron", "FCCAnalyses::MCParticle::sel_genStatus(1)(GenElectron_PID)") 
                .Define("n_FSGenElectron", "FCCAnalyses::MCParticle::get_n(FSGenElectron)")
                .Define("FSGenElectron_e", "FCCAnalyses::MCParticle::get_e(FSGenElectron)")
                .Define("FSGenElectron_p", "FCCAnalyses::MCParticle::get_p(FSGenElectron)")
                .Define("FSGenElectron_pt", "FCCAnalyses::MCParticle::get_pt(FSGenElectron)")
                .Define("FSGenElectron_px", "FCCAnalyses::MCParticle::get_px(FSGenElectron)")
                .Define("FSGenElectron_py", "FCCAnalyses::MCParticle::get_py(FSGenElectron)")
                .Define("FSGenElectron_pz", "FCCAnalyses::MCParticle::get_pz(FSGenElectron)")
                .Define("FSGenElectron_y", "FCCAnalyses::MCParticle::get_y(FSGenElectron)") # rapidity
                .Define("FSGenElectron_eta", "FCCAnalyses::MCParticle::get_eta(FSGenElectron)") # pseudorapidity
                .Define("FSGenElectron_theta", "FCCAnalyses::MCParticle::get_theta(FSGenElectron)")
                .Define("FSGenElectron_phi", "FCCAnalyses::MCParticle::get_phi(FSGenElectron)") # polar angle in the transverse plane phi
                .Define("FSGenElectron_charge", "FCCAnalyses::MCParticle::get_charge(FSGenElectron)")
                .Define("FSGenElectron_mass", "FCCAnalyses::MCParticle::get_mass(FSGenElectron)")
                .Define("FSGenElectron_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(FSGenElectron,Particle,Particle0)")
                .Define("FSGenElectron_vertex_x", "FCCAnalyses::MCParticle::get_vertex_x( FSGenElectron )")
                .Define("FSGenElectron_vertex_y", "FCCAnalyses::MCParticle::get_vertex_y( FSGenElectron )")
                .Define("FSGenElectron_vertex_z", "FCCAnalyses::MCParticle::get_vertex_z( FSGenElectron )")
                
                # all final state gen muons 
                .Define("GenMuon_PID", "FCCAnalyses::MCParticle::sel_pdgID(13, true)(Particle)")
                .Define("FSGenMuon", "FCCAnalyses::MCParticle::sel_genStatus(1)(GenMuon_PID)")
                .Define("n_FSGenMuon", "FCCAnalyses::MCParticle::get_n(FSGenMuon)")
                .Define("FSGenMuon_e", "FCCAnalyses::MCParticle::get_e(FSGenMuon)")
                .Define("FSGenMuon_p", "FCCAnalyses::MCParticle::get_p(FSGenMuon)")
                .Define("FSGenMuon_pt", "FCCAnalyses::MCParticle::get_pt(FSGenMuon)")
                .Define("FSGenMuon_px", "FCCAnalyses::MCParticle::get_px(FSGenMuon)")
                .Define("FSGenMuon_py", "FCCAnalyses::MCParticle::get_py(FSGenMuon)")
                .Define("FSGenMuon_pz", "FCCAnalyses::MCParticle::get_pz(FSGenMuon)")
                .Define("FSGenMuon_y", "FCCAnalyses::MCParticle::get_y(FSGenMuon)")
                .Define("FSGenMuon_eta", "FCCAnalyses::MCParticle::get_eta(FSGenMuon)")
                .Define("FSGenMuon_theta", "FCCAnalyses::MCParticle::get_theta(FSGenMuon)")
                .Define("FSGenMuon_phi", "FCCAnalyses::MCParticle::get_phi(FSGenMuon)")
                .Define("FSGenMuon_charge", "FCCAnalyses::MCParticle::get_charge(FSGenMuon)")
                .Define("FSGenMuon_mass",   "FCCAnalyses::MCParticle::get_mass(FSGenMuon)")
                .Define("FSGenMuon_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(FSGenMuon,Particle,Particle0)")
                .Define("FSGenMuon_vertex_x", "FCCAnalyses::MCParticle::get_vertex_x( FSGenMuon )")
                .Define("FSGenMuon_vertex_y", "FCCAnalyses::MCParticle::get_vertex_y( FSGenMuon )")
                .Define("FSGenMuon_vertex_z", "FCCAnalyses::MCParticle::get_vertex_z( FSGenMuon )")

                ##################
                # Reco particles #
                ##################

                # ELECTRONS 
                .Alias("Electron0", "Electron#0.index")
                .Define("RecoElectrons",  "ReconstructedParticle::get(Electron0, ReconstructedParticles)")            
                .Define("n_RecoElectrons",  "ReconstructedParticle::get_n(RecoElectrons)")
                .Define("RecoElectron_e",      "ReconstructedParticle::get_e(RecoElectrons)")
                .Define("RecoElectron_p",      "ReconstructedParticle::get_p(RecoElectrons)")
                .Define("RecoElectron_pt",      "ReconstructedParticle::get_pt(RecoElectrons)")
                .Define("RecoElectron_px",      "ReconstructedParticle::get_px(RecoElectrons)")
                .Define("RecoElectron_py",      "ReconstructedParticle::get_py(RecoElectrons)")
                .Define("RecoElectron_pz",      "ReconstructedParticle::get_pz(RecoElectrons)")
                .Define("RecoElectron_y",     "ReconstructedParticle::get_y(RecoElectrons)")
                .Define("RecoElectron_eta",     "ReconstructedParticle::get_eta(RecoElectrons)")
                .Define("RecoElectron_theta",   "ReconstructedParticle::get_theta(RecoElectrons)")
                .Define("RecoElectron_phi",     "ReconstructedParticle::get_phi(RecoElectrons)") 
                .Define("RecoElectron_charge",  "ReconstructedParticle::get_charge(RecoElectrons)")
                .Define("RecoElectron_mass",     "ReconstructedParticle::get_mass(RecoElectrons)")
                .Define("RecoElectronTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoElectrons,EFlowTrack_1))")
                .Define("RecoElectronTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoElectrons,EFlowTrack_1))")
                .Define("RecoElectronTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoElectrons,EFlowTrack_1))") 
                .Define("RecoElectronTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoElectrons,EFlowTrack_1))")
                .Define("RecoElectronTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoElectrons,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoElectronTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoElectrons,EFlowTrack_1)")
                
                # MUONS
                .Alias("Muon0", "Muon#0.index")
                .Define("RecoMuons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)")            
                .Define("n_RecoMuons",  "ReconstructedParticle::get_n(RecoMuons)")
                .Define("RecoMuon_e",      "ReconstructedParticle::get_e(RecoMuons)")
                .Define("RecoMuon_p",      "ReconstructedParticle::get_p(RecoMuons)")
                .Define("RecoMuon_pt",      "ReconstructedParticle::get_pt(RecoMuons)")
                .Define("RecoMuon_px",      "ReconstructedParticle::get_px(RecoMuons)")
                .Define("RecoMuon_py",      "ReconstructedParticle::get_py(RecoMuons)")
                .Define("RecoMuon_pz",      "ReconstructedParticle::get_pz(RecoMuons)")
                .Define("RecoMuon_y",     "ReconstructedParticle::get_y(RecoMuons)")
                .Define("RecoMuon_eta",     "ReconstructedParticle::get_eta(RecoMuons)") 
                .Define("RecoMuon_theta",   "ReconstructedParticle::get_theta(RecoMuons)")
                .Define("RecoMuon_phi",     "ReconstructedParticle::get_phi(RecoMuons)")
                .Define("RecoMuon_charge",  "ReconstructedParticle::get_charge(RecoMuons)")
                .Define("RecoMuon_mass",     "ReconstructedParticle::get_mass(RecoMuons)")
                .Define("RecoMuonTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoMuons,EFlowTrack_1))")
                .Define("RecoMuonTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoMuons,EFlowTrack_1))")
                .Define("RecoMuonTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoMuons,EFlowTrack_1))")
                .Define("RecoMuonTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoMuons,EFlowTrack_1))")
                .Define("RecoMuonTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoMuons,EFlowTrack_1)")
                .Define("RecoMuonTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoMuons,EFlowTrack_1)")
            
                # event selection for Z -> 2L ----------------------    
            
                # require exactly 2 leptons of same flavor and opposite charge
                .Filter("(n_RecoElectrons == 2 && "
                        "RecoElectron_charge[0] != RecoElectron_charge[1] && "
                        "RecoElectron_p[0] > 20 && RecoElectron_p[1] > 20) || "
                        "(n_RecoMuons == 2 && "
                        "RecoMuon_charge[0] != RecoMuon_charge[1] && "
                        "RecoMuon_p[0] > 20 && RecoMuon_p[1] > 20)")
            
                # reconstructing Z
                .Define("RecoZ_p4",     "if (n_RecoElectrons == 2) {"
                                        "    return TLorentzVector(RecoElectron_px[0], RecoElectron_py[0], RecoElectron_pz[0], RecoElectron_e[0]) + "
                                        "           TLorentzVector(RecoElectron_px[1], RecoElectron_py[1], RecoElectron_pz[1], RecoElectron_e[1]);"
                                        "} else {"
                                        "    return TLorentzVector(RecoMuon_px[0], RecoMuon_py[0], RecoMuon_pz[0], RecoMuon_e[0]) + "
                                        "           TLorentzVector(RecoMuon_px[1], RecoMuon_py[1], RecoMuon_pz[1], RecoMuon_e[1]);"
                                        "}")

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
                # .Define("RP_no_leptons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, RecoElectrons + RecoMuons)")
                # check if there is a way to merge RecoElectrons and RecoMuons and then just remove those at once
            
                .Define("Leptons", "FCCAnalyses::ReconstructedParticle::merge(RecoElectrons, RecoMuons)")
                .Define("RP_no_leptons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, Leptons)")
        
        )

        
        # tagging
        
        # define jet and run clustering parameters
        # name of collections in EDM root files
        collections = {
            "GenParticles": "Particle",
            "PFParticles": "RP_no_leptons",
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

        # EXCLUSIVE 4 JETS=
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
                .Define("TagJet_kt4_px", "JetClusteringUtils::get_px({})".format(jetClusteringHelper_kt4.jets))
                .Define("TagJet_kt4_py", "JetClusteringUtils::get_py({})".format(jetClusteringHelper_kt4.jets))
                .Define("TagJet_kt4_pz",     "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_kt4.jets))
                .Define("TagJet_kt4_p",     "JetClusteringUtils::get_p({})".format(jetClusteringHelper_kt4.jets))
                .Define("TagJet_kt4_pt",     "JetClusteringUtils::get_pt({})".format(jetClusteringHelper_kt4.jets))
                .Define("TagJet_kt4_phi",    "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_kt4.jets))
                .Define("TagJet_kt4_eta",    "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_kt4.jets))
                .Define("TagJet_kt4_theta",    "JetClusteringUtils::get_theta({})".format(jetClusteringHelper_kt4.jets))
                .Define("TagJet_kt4_e", "JetClusteringUtils::get_e({})".format(jetClusteringHelper_kt4.jets))
                .Define("TagJet_kt4_mass",   "JetClusteringUtils::get_m({})".format(jetClusteringHelper_kt4.jets))
                .Define("TagJet_kt4_charge",   "JetConstituentsUtils::get_charge_constituents({})".format(jetClusteringHelper_kt4.constituents))
                .Define("TagJet_kt4_flavor",  "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_kt4.jets))
                .Define("n_TagJet_kt4_constituents",  "JetConstituentsUtils::get_n_constituents({})".format(jetClusteringHelper_kt4.constituents))
                .Define("n_TagJet_kt4_charged_constituents", "JetConstituentsUtils::get_ncharged_constituents({})".format(jetClusteringHelper_kt4.constituents))
                .Define("n_TagJet_kt4_neutral_constituents", "JetConstituentsUtils::get_nneutral_constituents({})".format(jetClusteringHelper_kt4.constituents))
                .Define("n_TagJet_kt4", "return int(TagJet_kt4_flavor.size())")
                .Define("TagJet_kt4_cleanup", "JetConstituentsUtils::cleanup_taggedjet({})".format(jetClusteringHelper_kt4.constituents))

                .Define("TagJet_kt4_isG",    "recojet_isG_kt4")
                .Define("TagJet_kt4_isU",    "recojet_isU_kt4")
                .Define("TagJet_kt4_isD",    "recojet_isD_kt4")
                .Define("TagJet_kt4_isS",    "recojet_isS_kt4")
                .Define("TagJet_kt4_isC",    "recojet_isC_kt4")
                .Define("TagJet_kt4_isB",    "recojet_isB_kt4")

                # reconstructing H from 4 jets
                .Define("RecoH_p4",     "TLorentzVector(TagJet_kt4_px[0], TagJet_kt4_py[0], TagJet_kt4_pz[0], TagJet_kt4_e[0]) + "
                                        "TLorentzVector(TagJet_kt4_px[1], TagJet_kt4_py[1], TagJet_kt4_pz[1], TagJet_kt4_e[1]) + "
                                        "TLorentzVector(TagJet_kt4_px[2], TagJet_kt4_py[2], TagJet_kt4_pz[2], TagJet_kt4_e[2]) + "
                                        "TLorentzVector(TagJet_kt4_px[3], TagJet_kt4_py[3], TagJet_kt4_pz[3], TagJet_kt4_e[3])")
                    
                .Define("RecoH_px",    "RecoH_p4.Px()")
                .Define("RecoH_py",    "RecoH_p4.Py()")
                .Define("RecoH_pz",    "RecoH_p4.Pz()")
                .Define("RecoH_p",    "RecoH_p4.P()")
                .Define("RecoH_pt",    "RecoH_p4.Pt()")
                .Define("RecoH_e",     "RecoH_p4.E()")
                .Define("RecoH_eta",    "RecoH_p4.Eta()")
                .Define("RecoH_phi",    "RecoH_p4.Phi()")
                .Define("RecoH_theta",    "RecoH_p4.Theta()")
                .Define("RecoH_y",     "RecoH_p4.Rapidity()")
                .Define("RecoH_mass",    "RecoH_p4.M()")

                
                .Define("Total_p4",    "TLorentzVector(0.,0.,0.,365.)")
                .Define("Recoil_mass", "(Total_p4 - RecoZ_p4).M()")


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
            "RecoElectronTrack_absD0",
            "RecoElectronTrack_absZ0",
            "RecoElectronTrack_absD0sig",
            "RecoElectronTrack_absZ0sig",
            "RecoElectronTrack_D0cov",
            "RecoElectronTrack_Z0cov",

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
            "RecoMuonTrack_absD0",
            "RecoMuonTrack_absZ0",
            "RecoMuonTrack_absD0sig",
            "RecoMuonTrack_absZ0sig",
            "RecoMuonTrack_D0cov",
            "RecoMuonTrack_Z0cov",

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
            "n_TagJet_kt4_constituents",   
            "n_TagJet_kt4_charged_constituents",   
            "n_TagJet_kt4_neutral_constituents",   
            "n_TagJet_kt4",

            "TagJet_kt4_isG",
            "TagJet_kt4_isU",
            "TagJet_kt4_isD",
            "TagJet_kt4_isS",
            "TagJet_kt4_isC",
            "TagJet_kt4_isB",
            
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

            "Recoil_mass"
        ]

        return branchList