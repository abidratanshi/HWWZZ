import ROOT

# global parameters
intLumi = 3e6 # pb^-1, for 365 GeV

# if scaleSig=0 or scaleBack=0, we don't apply any additional scaling, on top of the normalization to cross section and integrated luminosity, as defined in finalSel.py
# if scaleSig or scaleBack is not defined, plots will be normalized to 1
#scaleSig       = 0.
#scaleBack      = 0.
ana_tex        = 'e^{+}e^{-} #rightarrow Z* #rightarrow ZH'
delphesVersion = '3.4.2'
energy         = 365
collider       = 'FCC-ee'
inputDir       = "/ceph/aratanshi/final_output/"
outdir         = "/web/aratanshi/public_html/plots"

formats        = ['png','pdf']
# formats        = ['png']
# formats        = ['pdf']

#yaxis          = ['lin','log']
yaxis          = ['log']

stacksig       = ['nostack']
stackbkg       = ['stack']
splitLeg       = True # split legend for backgrounds and signals


variables = [

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
            # "n_TagJet_kt4_constituents",   
            # "n_TagJet_kt4_charged_constituents",   
            # "n_TagJet_kt4_neutral_constituents",               
            
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

            "Recoil_mass",
        ]

selections = {}
selections['HWWZZ']  = ["sel0"]

extralabel = {}
extralabel["sel0"] = ""

colors = {}
colors['ee_eeH_HWW']   = ROOT.kOrange+2
colors['ee_eeH_HZZ']   = ROOT.kYellow-7
colors['ee_mumuH_HWW'] = ROOT.kRed+2
colors['ee_mumuH_HZZ'] = ROOT.kMagenta+2
colors['ee_WW']        = ROOT.kBlue+1
colors['ee_ZZ']        = ROOT.kCyan+2
colors['ee_tt']        = ROOT.kGreen+3

plots = {}
plots['HWWZZ'] = {'signal':{'ee_eeH_HWW':['wzp6_ee_eeH_HWW_ecm365'],
                            'ee_mumuH_HWW':['wzp6_ee_mumuH_HWW_ecm365'],

                            'ee_eeH_HZZ':['wzp6_ee_eeH_HZZ_ecm365'],
                            'ee_mumuH_HZZ':['wzp6_ee_mumuH_HZZ_ecm365']
                           },
                  
                  'backgrounds':{'ee_WW':['p8_ee_WW_ecm365'],
                                 'ee_ZZ':['p8_ee_ZZ_ecm365'],
                                 'ee_tt':['p8_ee_tt_ecm365']
                                }
}

# the format is TLatex https://root.cern.ch/doc/master/classTLatex.html
legend = {}
legend['ee_eeH_HWW']   = 'e^{+} e^{-} #rightarrow e^{+} e^{-} H, H #rightarrow W W'
legend['ee_mumuH_HWW'] = 'e^{+} e^{-} #rightarrow #mu^{+} #mu^{-} H, H #rightarrow W W'

legend['ee_eeH_HZZ']   = 'e^{+} e^{-} #rightarrow e^{+} e^{-} H, H #rightarrow Z Z'
legend['ee_mumuH_HZZ'] = 'e^{+} e^{-} #rightarrow #mu^{+} #mu^{-} H, H #rightarrow Z Z'

legend['ee_WW']        = 'e^{+} e^{-} #rightarrow W W'
legend['ee_ZZ']        = 'e^{+} e^{-} #rightarrow Z Z'
legend['ee_tt']        = 'e^{+} e^{-} #rightarrow t t'

