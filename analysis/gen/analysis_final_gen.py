
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
    
    "n_GenLepton":           {"name":"n_GenLepton",          "title":"Number of gen leptons",                   "bin":50,       "xmin":0,     "xmax":25},
    "GenLepton_pt":          {"name":"GenLepton_pt",          "title":"Gen lepton p_{T} [GeV]",                 "bin":50,      "xmin":0,        "xmax":100},
    "GenLepton_eta":         {"name":"GenLepton_eta",         "title":"Gen lepton #eta",                        "bin":32,      "xmin":-3.2,     "xmax":3.2},

    "n_GenLepton_int":        {"name":"n_GenLepton_int",     "title":"Number of gen intermediate leptons",        "bin":50,       "xmin":0,     "xmax":25},
    "GenLepton_int_pt":      {"name":"GenLepton_int_pt",    "title":"Gen intermediate lepton p_{T} [GeV]",       "bin":50,      "xmin":0,        "xmax":100},
    "GenLepton_int_mass":    {"name":"GenLepton_int_mass",    "title":"Gen intermediate lepton mass [GeV]",       "bin":20,      "xmin":0,        "xmax":1},
    "GenLepton_int_dR":      {"name":"GenLepton_int_dR",       "title":"Gen intermediate lepton dR",              "bin":75,      "xmin":0.,      "xmax":7},

    "n_GenLepton_FS":        {"name":"n_GenLepton_FS",          "title":"Number of gen FS leptons",                 "bin":50,       "xmin":0,     "xmax":25},
    "GenLepton_FS_pt":       {"name":"GenLepton_FS_pt",      "title":"Gen final state lepton p_{T} [GeV]",          "bin":50,      "xmin":0,        "xmax":100},
    "GenLepton_FS_mass":     {"name":"GenLepton_FS_mass",      "title":"Gen final state lepton mass [GeV]",       "bin":20,      "xmin":0,        "xmax":1},

    "GenZ_int_pt":           {"name":"GenZ_int_pt",          "title":"Gen Z intermediate p_{T} [GeV]",                      "bin":50,      "xmin":0,       "xmax":100},
    "GenZ_int_mass":         {"name":"GenZ_int_mass",          "title":"Gen Z (from intermediate leptons) mass [GeV]",      "bin":80,      "xmin":0.,      "xmax":150},

    "n_GenLepton_ZProd":     {"name":"n_GenLepton_ZProd",        "title":"Number of (prod Z) gen leptons",   "bin":50,       "xmin":0,     "xmax":25},
    "GenLepton_ZProd_pt":    {"name":"GenLepton_ZProd_pt",       "title":"(Prod Z) lepton pT [GeV]",         "bin":50,      "xmin":0,        "xmax":100},
    "GenLepton_ZProd_mass":  {"name":"GenLepton_ZProd_mass",     "title":"(Prod Z) lepton mass [GeV]",       "bin":80,      "xmin":0,        "xmax":150},
    "GenLepton_ZProd_dR":    {"name":"GenLepton_ZProd_dR",       "title":"(Prod Z) lepton dR",               "bin":75,      "xmin":0,        "xmax":7},
    
    "GenZ_ZProd_pt":        {"name":"GenZ_ZProd_pt",       "title":"Gen Z (production) pT [GeV]",         "bin":50,      "xmin":0,        "xmax":100},
    "GenZ_ZProd_mass":      {"name":"GenZ_ZProd_mass",     "title":"Gen Z (production) mass [GeV]",       "bin":80,      "xmin":0,        "xmax":150},

}