
inputDir = "/ceph/aratanshi/stage_output"
outputDir = "/ceph/aratanshi/final_output"

intLumi = 3e6 # pb^-1

# Scale event yields by intLumi and cross section (optional)
# if scaling, both the number of events in the table and in the histograms will be scaled
doScale = True

#Save event yields in a table (optional)
saveTabular = False

nCPUs = 8

#produces ROOT TTrees, default is False
doTree = False

processList = {

    # Signal
    'wzp6_ee_eeH_HWW_ecm365':   {},
    'wzp6_ee_mumuH_HWW_ecm365': {},
    'wzp6_ee_eeH_HZZ_ecm365':   {},
    'wzp6_ee_mumuH_HZZ_ecm365': {},

    # Background
    'p8_ee_WW_ecm365': {},
    'p8_ee_ZZ_ecm365': {},
    'p8_ee_tt_ecm365': {},
}

# Dictionary for prettier names of processes (optional, they don't do anything, maybe only in table)
processLabels = {}

#Link to the dictonary that contains all the cross section information etc...
procDict = "FCCee_procDict_winter2023_IDEA.json"

# Add provate samples as it is not an offical process
procDictAdd = {}

# Dictionary of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
    # no selection, `true`, just builds the histograms, it will not be shown in the latex table or change anything
    "sel0": "true",
}

# Dictionary for the ouput variable/hitograms
# The key is the name of the variable in the output files.
# "name" is the name of the variable in the input file,
# "title" is the x-axis label of the histogram,
# "bin" the number of bins of the histogram,
# "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {

    "n_RecoElectrons":                  {"name":"n_RecoElectrons",                  "title":"Number of reco electrons",                     "bin":5, "xmin":-0.5, "xmax":4.5},
    "RecoElectron_e":                   {"name":"RecoElectron_e",                   "title":"Reco electron energy [GeV]",                   "bin":50,"xmin":0 ,"xmax":100},
    "RecoElectron_p":                   {"name":"RecoElectron_p",                   "title":"Reco electron p [GeV]",                        "bin":50,"xmin":0 ,"xmax":100},
    "RecoElectron_pt":                  {"name":"RecoElectron_pt",                  "title":"Reco electron p_{T} [GeV]",                    "bin":50,"xmin":0 ,"xmax":100},
    "RecoElectron_px":                  {"name":"RecoElectron_px",                  "title":"Reco electron p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoElectron_py":                  {"name":"RecoElectron_py",                  "title":"Reco electron p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoElectron_pz":                  {"name":"RecoElectron_pz",                  "title":"Reco electron p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoElectron_y":                   {"name":"RecoElectron_y",                   "title":"Reco electron rapidity",                       "bin":40, "xmin":-4., "xmax":4.},
    "RecoElectron_eta":                 {"name":"RecoElectron_eta",                 "title":"Reco electron #eta",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoElectron_theta":               {"name":"RecoElectron_theta",               "title":"Reco electron #theta",                         "bin":16, "xmin":0,"xmax":3.2},
    "RecoElectron_phi":                 {"name":"RecoElectron_phi",                 "title":"Reco electron #phi",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoElectron_charge":              {"name":"RecoElectron_charge",              "title":"Reco electron charge",                         "bin":3, "xmin":-1.5,"xmax":1.5},
    "RecoElectron_mass":                {"name":"RecoElectron_mass",                "title":"Reco electron mass [GeV]",                     "bin":20, "xmin":0., "xmax":1},

    "n_RecoElectrons_sel":         {"name":"n_RecoElectrons_sel",                  "title":"Number of reco electrons sel",                     "bin":5, "xmin":-0.5, "xmax":4.5},
    "RecoElectron_sel_e":          {"name":"RecoElectron_sel_e",                   "title":"Reco electron sel energy [GeV]",                   "bin":50,"xmin":0 ,"xmax":100},
    "RecoElectron_sel_p":          {"name":"RecoElectron_sel_p",                   "title":"Reco electron sel p [GeV]",                        "bin":50,"xmin":0 ,"xmax":100},
    "RecoElectron_sel_pt":         {"name":"RecoElectron_sel_pt",                  "title":"Reco electron sel p_{T} [GeV]",                    "bin":50,"xmin":0 ,"xmax":100},
    "RecoElectron_sel_px":         {"name":"RecoElectron_sel_px",                  "title":"Reco electron sel p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoElectron_sel_py":         {"name":"RecoElectron_sel_py",                  "title":"Reco electron sel p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoElectron_sel_pz":         {"name":"RecoElectron_sel_pz",                  "title":"Reco electron sel p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoElectron_sel_y":          {"name":"RecoElectron_sel_y",                   "title":"Reco electron sel rapidity",                       "bin":40, "xmin":-4., "xmax":4.},
    "RecoElectron_sel_eta":        {"name":"RecoElectron_sel_eta",                 "title":"Reco electron sel #eta",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoElectron_sel_theta":      {"name":"RecoElectron_sel_theta",               "title":"Reco electron sel #theta",                         "bin":16, "xmin":0,"xmax":3.2},
    "RecoElectron_sel_phi":        {"name":"RecoElectron_sel_phi",                 "title":"Reco electron sel #phi",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoElectron_sel_charge":     {"name":"RecoElectron_sel_charge",              "title":"Reco electron sel charge",                         "bin":3, "xmin":-1.5,"xmax":1.5},
    "RecoElectron_sel_mass":       {"name":"RecoElectron_sel_mass",                "title":"Reco electron sel mass [GeV]",                     "bin":20, "xmin":0., "xmax":1},

    "n_RecoMuons":                  {"name":"n_RecoMuons",                  "title":"Number of reco muons",                     "bin":5, "xmin":-0.5, "xmax":4.5},
    "RecoMuon_e":                   {"name":"RecoMuon_e",                   "title":"Reco muon energy [GeV]",                   "bin":50,"xmin":0 ,"xmax":100},
    "RecoMuon_p":                   {"name":"RecoMuon_p",                   "title":"Reco muon p [GeV]",                        "bin":50,"xmin":0 ,"xmax":100},
    "RecoMuon_pt":                  {"name":"RecoMuon_pt",                  "title":"Reco muon p_{T} [GeV]",                    "bin":50,"xmin":0 ,"xmax":100},
    "RecoMuon_px":                  {"name":"RecoMuon_px",                  "title":"Reco muon p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoMuon_py":                  {"name":"RecoMuon_py",                  "title":"Reco muon p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoMuon_pz":                  {"name":"RecoMuon_pz",                  "title":"Reco muon p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoMuon_y":                   {"name":"RecoMuon_y",                   "title":"Reco muon rapidity",                       "bin":40, "xmin":-4., "xmax":4.},
    "RecoMuon_eta":                 {"name":"RecoMuon_eta",                 "title":"Reco muon #eta",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoMuon_theta":               {"name":"RecoMuon_theta",               "title":"Reco muon #theta",                         "bin":16, "xmin":0,"xmax":3.2},
    "RecoMuon_phi":                 {"name":"RecoMuon_phi",                 "title":"Reco muon #phi",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoMuon_charge":              {"name":"RecoMuon_charge",              "title":"Reco muon charge",                         "bin":3, "xmin":-1.5,"xmax":1.5},
    "RecoMuon_mass":                {"name":"RecoMuon_mass",                "title":"Reco muon mass [GeV]",                     "bin":20, "xmin":0., "xmax":0.2},

    "n_RecoMuons_sel":         {"name":"n_RecoMuons_sel",                  "title":"Number of reco muons sel",                     "bin":5, "xmin":-0.5, "xmax":4.5},
    "RecoMuon_sel_e":          {"name":"RecoMuon_sel_e",                   "title":"Reco muon sel energy [GeV]",                   "bin":50,"xmin":0 ,"xmax":100},
    "RecoMuon_sel_p":          {"name":"RecoMuon_sel_p",                   "title":"Reco muon sel p [GeV]",                        "bin":50,"xmin":0 ,"xmax":100},
    "RecoMuon_sel_pt":         {"name":"RecoMuon_sel_pt",                  "title":"Reco muon sel p_{T} [GeV]",                    "bin":50,"xmin":0 ,"xmax":100},
    "RecoMuon_sel_px":         {"name":"RecoMuon_sel_px",                  "title":"Reco muon sel p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoMuon_sel_py":         {"name":"RecoMuon_sel_py",                  "title":"Reco muon sel p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoMuon_sel_pz":         {"name":"RecoMuon_sel_pz",                  "title":"Reco muon sel p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoMuon_sel_y":          {"name":"RecoMuon_sel_y",                   "title":"Reco muon sel rapidity",                       "bin":40, "xmin":-4., "xmax":4.},
    "RecoMuon_sel_eta":        {"name":"RecoMuon_sel_eta",                 "title":"Reco muon sel #eta",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoMuon_sel_theta":      {"name":"RecoMuon_sel_theta",               "title":"Reco muon sel #theta",                         "bin":16, "xmin":0,"xmax":3.2},
    "RecoMuon_sel_phi":        {"name":"RecoMuon_sel_phi",                 "title":"Reco muon sel #phi",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoMuon_sel_charge":     {"name":"RecoMuon_sel_charge",              "title":"Reco muon sel charge",                         "bin":3, "xmin":-1.5,"xmax":1.5},
    "RecoMuon_sel_mass":       {"name":"RecoMuon_sel_mass",                "title":"Reco muon sel mass [GeV]",                     "bin":20, "xmin":0., "xmax":1},

    "n_RecoPhotons":            {"name":"n_RecoPhotons",                  "title":"Number of reco photons",                     "bin":5, "xmin":-0.5, "xmax":4.5},
    "RecoPhoton_e":             {"name":"RecoPhoton_e",                   "title":"Reco photon energy [GeV]",                   "bin":50,"xmin":0 ,"xmax":100},
    "RecoPhoton_p":             {"name":"RecoPhoton_p",                   "title":"Reco photon p [GeV]",                        "bin":50,"xmin":0 ,"xmax":100},
    "RecoPhoton_pt":            {"name":"RecoPhoton_pt",                  "title":"Reco photon p_{T} [GeV]",                    "bin":50,"xmin":0 ,"xmax":100},
    "RecoPhoton_px":            {"name":"RecoPhoton_px",                  "title":"Reco photon p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoPhoton_py":            {"name":"RecoPhoton_py",                  "title":"Reco photon p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoPhoton_pz":            {"name":"RecoPhoton_pz",                  "title":"Reco photon p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoPhoton_y":             {"name":"RecoPhoton_y",                   "title":"Reco photon rapidity",                       "bin":40, "xmin":-4., "xmax":4.},
    "RecoPhoton_eta":           {"name":"RecoPhoton_eta",                 "title":"Reco photon #eta",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoPhoton_theta":         {"name":"RecoPhoton_theta",               "title":"Reco photon #theta",                         "bin":16, "xmin":0,"xmax":3.2},
    "RecoPhoton_phi":           {"name":"RecoPhoton_phi",                 "title":"Reco photon #phi",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoPhoton_charge":        {"name":"RecoPhoton_charge",              "title":"Reco photon charge",                         "bin":3, "xmin":-1.5,"xmax":1.5},
    "RecoPhoton_mass":          {"name":"RecoPhoton_mass",                 "title":"Reco photon mass [GeV]",                    "bin":50, "xmin":-0.05,"xmax":0.05},

    "TagJet_kt4_e":                       {"name":"TagJet_kt4_e",                       "title":"kt4 jet energy [GeV]",          "bin":50,"xmin":0 ,"xmax":100},
    "TagJet_kt4_p":                       {"name":"TagJet_kt4_p",                       "title":"kt4 jet p [GeV]",               "bin":50,"xmin":0 ,"xmax":100},
    "TagJet_kt4_pt":                      {"name":"TagJet_kt4_pt",                      "title":"kt4 jet p_{T} [GeV]",           "bin":50,"xmin":0 ,"xmax":100},
    "TagJet_kt4_px":                      {"name":"TagJet_kt4_px",                      "title":"kt4 jet p_{x} [GeV]",           "bin":50,"xmin":-100 ,"xmax":100},
    "TagJet_kt4_py":                      {"name":"TagJet_kt4_py",                      "title":"kt4 jet p_{y} [GeV]",           "bin":50,"xmin":-100 ,"xmax":100},
    "TagJet_kt4_pz":                      {"name":"TagJet_kt4_pz",                      "title":"kt4 jet p_{z} [GeV]",           "bin":50,"xmin":-100 ,"xmax":100},
    "TagJet_kt4_eta":                     {"name":"TagJet_kt4_eta",                     "title":"kt4 jet #eta",                  "bin":32, "xmin":-3.2,"xmax":3.2},
    "TagJet_kt4_theta":                   {"name":"TagJet_kt4_theta",                   "title":"kt4 jet #theta",                "bin":16, "xmin":0,"xmax":3.2},
    "TagJet_kt4_phi":                     {"name":"TagJet_kt4_phi",                     "title":"kt4 jet #phi",                  "bin":32, "xmin":-3.2,"xmax":3.2},
    "TagJet_kt4_mass":                    {"name":"TagJet_kt4_mass",                    "title":"kt4 jet mass [GeV]",            "bin":20, "xmin":0., "xmax":200.},
    "TagJet_kt4_charge":                  {"name":"TagJet_kt4_charge",                  "title":"kt4 jet charge",                "bin":10, "xmin":-5., "xmax":5.},
    "TagJet_kt4_flavor":                  {"name":"TagJet_kt4_flavor",                  "title":"kt4 jet flavor",                "bin":10, "xmin":-5., "xmax":5.},
    "n_TagJet_kt4":                       {"name":"n_TagJet_kt4",                       "title":"Number of kt4 jet",             "bin":5, "xmin":-0.5, "xmax":4.5},
    # "n_TagJet_kt4_constituents":          {"name":"n_TagJet_kt4_constituents",          "title":"kt4 jet constituents",          "bin":20, "xmin":0., "xmax":20.},
    # "n_TagJet_kt4_charged_constituents":  {"name":"n_TagJet_kt4_charged_constituents",  "title":"kt4 jet charged constituents",  "bin":20, "xmin":0., "xmax":20.},
    # "n_TagJet_kt4_neutral_constituents":  {"name":"n_TagJet_kt4_neutral_constituents",  "title":"kt4 jet neutral constituents",  "bin":20, "xmin":0., "xmax":20.},

    "RecoZ_px":                 {"name":"RecoZ_px",                 "title":"Reco Z p_{x} [GeV]",            "bin":50,"xmin":-200 ,"xmax":200},
    "RecoZ_py":                 {"name":"RecoZ_py",                 "title":"Reco Z p_{y} [GeV]",            "bin":50,"xmin":-200 ,"xmax":200},
    "RecoZ_pz":                 {"name":"RecoZ_pz",                 "title":"Reco Z p_{z} [GeV]",            "bin":50,"xmin":-200 ,"xmax":200},
    "RecoZ_p":                  {"name":"RecoZ_p",                  "title":"Reco Z p [GeV]",                "bin":75, "xmin":0 ,"xmax":200},
    "RecoZ_pt":                 {"name":"RecoZ_pt",                 "title":"Reco Z p_{T} [GeV]",            "bin":75, "xmin":0 ,"xmax":200},
    "RecoZ_e":                  {"name":"RecoZ_e",                  "title":"Reco Z energy [GeV]",           "bin":75, "xmin":0 ,"xmax":200},
    "RecoZ_eta":                {"name":"RecoZ_eta",                "title":"Reco Z #eta",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoZ_phi":                {"name":"RecoZ_phi",                "title":"Reco Z #phi",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoZ_theta":              {"name":"RecoZ_theta",              "title":"Reco Z #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "RecoZ_y":                  {"name":"RecoZ_y",                  "title":"Reco Z rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "RecoZ_mass":               {"name":"RecoZ_mass",               "title":"Reco Z mass [GeV]",             "bin":100, "xmin":50., "xmax":150},

    "RecoH_px":                 {"name":"RecoH_px",                 "title":"Reco H p_{x} [GeV]",            "bin":50,"xmin":-200 ,"xmax":200},
    "RecoH_py":                 {"name":"RecoH_py",                 "title":"Reco H p_{y} [GeV]",            "bin":50,"xmin":-200 ,"xmax":200},
    "RecoH_pz":                 {"name":"RecoH_pz",                 "title":"Reco H p_{z} [GeV]",            "bin":50,"xmin":-200 ,"xmax":200},
    "RecoH_p":                  {"name":"RecoH_p",                  "title":"Reco H p [GeV]",                "bin":75, "xmin":0 ,"xmax":200},
    "RecoH_pt":                 {"name":"RecoH_pt",                 "title":"Reco H p_{T} [GeV]",            "bin":75, "xmin":0 ,"xmax":200},
    "RecoH_e":                  {"name":"RecoH_e",                  "title":"Reco H energy [GeV]",           "bin":75, "xmin":0 ,"xmax":200},
    "RecoH_eta":                {"name":"RecoH_eta",                "title":"Reco H #eta",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoH_phi":                {"name":"RecoH_phi",                "title":"Reco H #phi",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoH_theta":              {"name":"RecoH_theta",              "title":"Reco H #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "RecoH_y":                  {"name":"RecoH_y",                  "title":"Reco H rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "RecoH_mass":               {"name":"RecoH_mass",               "title":"Reco H mass [GeV]",             "bin":75, "xmin":0 ,"xmax":200},

    "V1_mass":               {"name":"V1_mass",               "title":"V1 mass [GeV]",             "bin":75, "xmin":0 ,"xmax":200},
    "V2_mass":               {"name":"V2_mass",               "title":"V2 mass [GeV]",             "bin":75, "xmin":0 ,"xmax":200},

    "Recoil_mass":              {"name":"Recoil_mass",              "title":"Recoil mass [GeV]",             "bin":75, "xmin":0 ,"xmax":200},

}
