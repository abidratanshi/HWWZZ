import ROOT

# global parameters
intLumi = 3e6 # pb^-1, for 365 GeV

###If scaleSig=0 or scaleBack=0, we don't apply any additional scaling, on top of the normalization to cross section and integrated luminosity, as defined in finalSel.py
###If scaleSig or scaleBack is not defined, plots will be normalized to 1
#scaleSig       = 0.
#scaleBack      = 0.
ana_tex        = 'e^{+} e^{-} #rightarrow #ell^{+} #ell^{-} H, H #rightarrow WW/ZZ'
delphesVersion = '3.4.2'
energy         = 365
collider       = 'FCC-ee'
inputDir       = "/ceph/aratanshi/final_output/"
# outdir         = "/ceph/aratanshi/plots"
outdir         = "/web/aratanshi/public_html/plots"

## you can save the plots in png or pdf or both
# formats        = ['png']
formats        = ['pdf']

## you can choose to plot in logarithmic or linear scale the y axis
#yaxis          = ['lin','log']
yaxis          = ['log']

## hree you can choose to stack or not your signals and backgrounds separately
stacksig       = ['nostack']
stackbkg       = ['stack']
splitLeg       = True ### to split legend for backgrounds and signals ###


## add the list of variable that you want to plot here, the name correspond to the name of the histogram saved in final
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
    
            "Recoil_mass",
    
        ]

    
#Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
## add your selections from final
selections = {}
selections['HWWZZ']  = ["sel0"]
# selections['HWWZZ']  = ["sel0","selZ","selH"]



## pretty labels for the selections, they will appear on your plots
extralabel = {}
extralabel["sel0"] = "none"
# extralabel["selZ"] = "$80 < M_Z < 100$"
# extralabel["selH"] = "$100 < M_H < 150$"


## colors are from the ROOT color wheel or color table, assigned to each process
colors = {}
colors['ee_eeH_HWW']   = ROOT.kOrange+2
colors['ee_eeH_HZZ']   = ROOT.kYellow-7
colors['ee_mumuH_HWW'] = ROOT.kRed+2
colors['ee_mumuH_HZZ'] = ROOT.kMagenta+2
colors['ee_WW']        = ROOT.kBlue+1
colors['ee_ZZ']        = ROOT.kCyan+2
colors['ee_tt']        = ROOT.kGreen+3


## we decide what is going to be plotted as a signal (line histogram) or background (filled histogram)
## remember that you have to have at least one background for this to work
plots = {}
plots['HWWZZ'] = {'signal':{'ee_eeH_HWW':['wzp6_ee_eeH_HWW_ecm365'],
                                 'ee_eeH_HZZ':['wzp6_ee_eeH_HZZ_ecm365'],
                                 'ee_mumuH_HWW':['wzp6_ee_mumuH_HWW_ecm365'],
                                 'ee_mumuH_HZZ':['wzp6_ee_mumuH_HZZ_ecm365']
                                },
                       
                       'backgrounds':{'ee_WW':['p8_ee_WW_ecm365'],
                                      'ee_ZZ':['p8_ee_ZZ_ecm365'],
                                      'ee_tt':['p8_ee_tt_ecm365']
                                     }
}

## pretty names for the processes, the format is TLatex https://root.cern.ch/doc/master/classTLatex.html
legend = {}
legend['ee_eeH_HWW']   = 'e^{+} e^{-} #rightarrow e^{+} e^{-} H, H #rightarrow W W'
legend['ee_eeH_HZZ']   = 'e^{+} e^{-} #rightarrow #mu^{+} #mu^{-} H, H #rightarrow Z Z'
legend['ee_mumuH_HWW'] = 'e^{+} e^{-} #rightarrow e^{+} e^{-} H, H #rightarrow W W'
legend['ee_mumuH_HZZ'] = 'e^{+} e^{-} #rightarrow #mu^{+} #mu^{-} H, H #rightarrow Z Z'
legend['ee_WW']        = 'e^{+} e^{-} #rightarrow W W'
legend['ee_ZZ']        = 'e^{+} e^{-} #rightarrow Z Z'
legend['ee_tt']        = 'e^{+} e^{-} #rightarrow t t'

