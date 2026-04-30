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
inputDir       = "/ceph/aratanshi/final_gen_output/"
outdir         = "/web/aratanshi/public_html/plots/gen"

formats        = ['png','pdf']
# formats        = ['png']
# formats        = ['pdf']

#yaxis          = ['lin','log']
yaxis          = ['log']

stacksig       = ['nostack']
# stackbkg       = ['stack']
splitLeg       = True # split legend for backgrounds and signals


variables = [

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

selections = {}
selections['HWWZZ']  = ["sel0"]

extralabel = {}
extralabel["sel0"] = ""

colors = {}
colors['ee_eeH_HWW']   = ROOT.kOrange+2
colors['ee_mumuH_HWW'] = ROOT.kYellow-7
colors['ee_eeH_HZZ']   = ROOT.kRed+2
colors['ee_mumuH_HZZ'] = ROOT.kMagenta+2
# colors['ee_WW']        = ROOT.kBlue+1
# colors['ee_ZZ']        = ROOT.kCyan+2
# colors['ee_tt']        = ROOT.kGreen+3

plots = {}
plots['HWWZZ'] = {'signal':{'ee_eeH_HWW':['wzp6_ee_eeH_HWW_ecm365'],
                            'ee_mumuH_HWW':['wzp6_ee_mumuH_HWW_ecm365'],
                            'ee_eeH_HZZ':['wzp6_ee_eeH_HZZ_ecm365'],
                            'ee_mumuH_HZZ':['wzp6_ee_mumuH_HZZ_ecm365']
                           },

                  # 'backgrounds':{'ee_WW':['p8_ee_WW_ecm365'],
                  #                'ee_ZZ':['p8_ee_ZZ_ecm365'],
                  #                'ee_tt':['p8_ee_tt_ecm365']
                  #               }
}

# the format is TLatex https://root.cern.ch/doc/master/classTLatex.html
legend = {}
legend['ee_eeH_HWW']   = 'e^{+} e^{-} #rightarrow e^{+} e^{-} H, H #rightarrow W W'
legend['ee_mumuH_HWW'] = 'e^{+} e^{-} #rightarrow #mu^{+} #mu^{-} H, H #rightarrow W W'
legend['ee_eeH_HZZ']   = 'e^{+} e^{-} #rightarrow e^{+} e^{-} H, H #rightarrow Z Z'
legend['ee_mumuH_HZZ'] = 'e^{+} e^{-} #rightarrow #mu^{+} #mu^{-} H, H #rightarrow Z Z'
# legend['ee_WW']        = 'e^{+} e^{-} #rightarrow W W'
# legend['ee_ZZ']        = 'e^{+} e^{-} #rightarrow Z Z'
# legend['ee_tt']        = 'e^{+} e^{-} #rightarrow t t'

