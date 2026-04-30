
inputDir = "/ceph/aratanshi/stage_gen_output"
outputDir = "/ceph/aratanshi/final_gen_output"

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
    # 'p8_ee_WW_ecm365': {},
    # 'p8_ee_ZZ_ecm365': {},
    # 'p8_ee_tt_ecm365': {},
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

    "n_GenElectrons":                    {"name":"n_GenElectrons",                     "title":"Number of gen electrons",        "bin":5,       "xmin":-0.5,     "xmax":4.5},
    "GenElectron_e":                     {"name":"GenElectron_e",                      "title":"Gen electron energy [GeV]",      "bin":50,      "xmin":0,        "xmax":100},
    "GenElectron_p":                     {"name":"GenElectron_p",                      "title":"Gen electron p [GeV]",           "bin":50,      "xmin":0,        "xmax":100},
    "GenElectron_pt":                    {"name":"GenElectron_pt",                     "title":"Gen electron p_{T} [GeV]",       "bin":50,      "xmin":0,        "xmax":100},
    "GenElectron_px":                    {"name":"GenElectron_px",                     "title":"Gen electron p_{x} [GeV]",       "bin":50,      "xmin":-100,     "xmax":100},
    "GenElectron_py":                    {"name":"GenElectron_py",                     "title":"Gen electron p_{y} [GeV]",       "bin":50,      "xmin":-100,     "xmax":100},
    "GenElectron_pz":                    {"name":"GenElectron_pz",                     "title":"Gen electron p_{z} [GeV]",       "bin":50,      "xmin":-100,     "xmax":100},
    "GenElectron_y":                     {"name":"GenElectron_y",                      "title":"Gen electron rapidity",          "bin":40,      "xmin":-4.,      "xmax":4.},
    "GenElectron_eta":                   {"name":"GenElectron_eta",                    "title":"Gen electron #eta",              "bin":32,      "xmin":-3.2,     "xmax":3.2},
    "GenElectron_theta":                 {"name":"GenElectron_theta",                  "title":"Gen electron #theta",            "bin":16,      "xmin":0,        "xmax":3.2},
    "GenElectron_phi":                   {"name":"GenElectron_phi",                    "title":"Gen electron #phi",              "bin":32,      "xmin":-3.2,     "xmax":3.2},
    "GenElectron_charge":                {"name":"GenElectron_charge",                 "title":"Gen electron charge",            "bin":3,       "xmin":-1.5,     "xmax":1.5},
    "GenElectron_mass":                  {"name":"GenElectron_mass",                   "title":"Gen electron mass [GeV]",        "bin":20,      "xmin":0.,       "xmax":1},

    "n_GenMuons":                    {"name":"n_GenMuons",                     "title":"Number of gen muons",         "bin":5,       "xmin":-0.5,     "xmax":4.5},
    "GenMuon_e":                     {"name":"GenMuon_e",                      "title":"Gen muons energy [GeV]",      "bin":50,      "xmin":0,        "xmax":100},
    "GenMuon_p":                     {"name":"GenMuon_p",                      "title":"Gen muons p [GeV]",           "bin":50,      "xmin":0,        "xmax":100},
    "GenMuon_pt":                    {"name":"GenMuon_pt",                     "title":"Gen muons p_{T} [GeV]",       "bin":50,      "xmin":0,        "xmax":100},
    "GenMuon_px":                    {"name":"GenMuon_px",                     "title":"Gen muons p_{x} [GeV]",       "bin":50,      "xmin":-100,     "xmax":100},
    "GenMuon_py":                    {"name":"GenMuon_py",                     "title":"Gen muons p_{y} [GeV]",       "bin":50,      "xmin":-100,     "xmax":100},
    "GenMuon_pz":                    {"name":"GenMuon_pz",                     "title":"Gen muons p_{z} [GeV]",       "bin":50,      "xmin":-100,     "xmax":100},
    "GenMuon_y":                     {"name":"GenMuon_y",                      "title":"Gen muons rapidity",          "bin":40,      "xmin":-4.,      "xmax":4.},
    "GenMuon_eta":                   {"name":"GenMuon_eta",                    "title":"Gen muons #eta",              "bin":32,      "xmin":-3.2,     "xmax":3.2},
    "GenMuon_theta":                 {"name":"GenMuon_theta",                  "title":"Gen muons #theta",            "bin":16,      "xmin":0,        "xmax":3.2},
    "GenMuon_phi":                   {"name":"GenMuon_phi",                    "title":"Gen muons #phi",              "bin":32,      "xmin":-3.2,     "xmax":3.2},
    "GenMuon_charge":                {"name":"GenMuon_charge",                 "title":"Gen muons charge",            "bin":3,       "xmin":-1.5,     "xmax":1.5},
    "GenMuon_mass":                  {"name":"GenMuon_mass",                   "title":"Gen muons mass [GeV]",        "bin":20,      "xmin":0.,       "xmax":1},
                
    "GenElectron_dR":                {"name":"GenElectron_dR",                     "title":"gen electron dR [GeV]",           "bin":75,      "xmin":0,        "xmax":100},
    "GenMuon_dR":                    {"name":"GenMuon_dR",                         "title":"gen muon dR [GeV]",               "bin":75,      "xmin":0,        "xmax":100},

    "GenZ_px":                           {"name":"GenZ_px",                            "title":"Gen Z p_{x} [GeV]",              "bin":50,      "xmin":-200,     "xmax":200},
    "GenZ_py":                           {"name":"GenZ_py",                            "title":"Gen Z p_{y} [GeV]",              "bin":50,      "xmin":-200,     "xmax":200},
    "GenZ_pz":                           {"name":"GenZ_pz",                            "title":"Gen Z p_{z} [GeV]",              "bin":50,      "xmin":-200,     "xmax":200},
    "GenZ_p":                            {"name":"GenZ_p",                             "title":"Gen Z p [GeV]",                  "bin":75,      "xmin":0,        "xmax":200},
    "GenZ_pt":                           {"name":"GenZ_pt",                            "title":"Gen Z p_{T} [GeV]",              "bin":75,      "xmin":0,        "xmax":200},
    "GenZ_e":                            {"name":"GenZ_e",                             "title":"Gen Z energy [GeV]",             "bin":75,      "xmin":0,        "xmax":200},
    "GenZ_eta":                          {"name":"GenZ_eta",                           "title":"Gen Z #eta",                     "bin":32,      "xmin":-3.2,     "xmax":3.2},
    "GenZ_phi":                          {"name":"GenZ_phi",                           "title":"Gen Z #phi",                     "bin":32,      "xmin":-3.2,     "xmax":3.2},
    "GenZ_theta":                        {"name":"GenZ_theta",                         "title":"Gen Z #theta",                   "bin":16,      "xmin":0,        "xmax":3.2},
    "GenZ_y":                            {"name":"GenZ_y",                             "title":"Gen Z rapidity",                 "bin":40,      "xmin":-4.,      "xmax":4.},
    "GenZ_mass":                         {"name":"GenZ_mass",                          "title":"Gen Z mass [GeV]",               "bin":80,      "xmin":50.,      "xmax":150},
       
    "GenH_px":                          {"name":"GenH_px",                           "title":"Gen H p_{x} [GeV]",             "bin":50,      "xmin":-200,     "xmax":200},
    "GenH_py":                          {"name":"GenH_py",                           "title":"Gen H p_{y} [GeV]",             "bin":50,      "xmin":-200,     "xmax":200},
    "GenH_pz":                          {"name":"GenH_pz",                           "title":"Gen H p_{z} [GeV]",             "bin":50,      "xmin":-200,     "xmax":200},
    "GenH_p":                           {"name":"GenH_p",                            "title":"Gen H p [GeV]",                 "bin":75,      "xmin":0,        "xmax":200},
    "GenH_pt":                          {"name":"GenH_pt",                           "title":"Gen H p_{T} [GeV]",             "bin":75,      "xmin":0,        "xmax":200},
    "GenH_e":                           {"name":"GenH_e",                            "title":"Gen H energy [GeV]",            "bin":75,      "xmin":0,        "xmax":200},
    "GenH_eta":                         {"name":"GenH_eta",                          "title":"Gen H #eta",                    "bin":32,      "xmin":-3.2,     "xmax":3.2},
    "GenH_phi":                         {"name":"GenH_phi",                          "title":"Gen H #phi",                    "bin":32,      "xmin":-3.2,     "xmax":3.2},
    "GenH_theta":                       {"name":"GenH_theta",                        "title":"Gen H #theta",                  "bin":16,      "xmin":0,        "xmax":3.2},
    "GenH_y":                           {"name":"GenH_y",                            "title":"Gen H rapidity",                "bin":40,      "xmin":-4.,      "xmax":4.},
    "GenH_mass":                        {"name":"GenH_mass",                         "title":"Gen H mass [GeV]",              "bin":75,      "xmin":0,        "xmax":200},
}
