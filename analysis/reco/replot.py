#code adapted from FCCAnalyses/do_plots.py

import sys
import os
import os.path
import ntpath
import importlib
import copy
import re
import logging
import ROOT

# Set ROOT to batch mode so it doesn't open all the plots
ROOT.gROOT.SetBatch(True)

def sorted_dict_values(dic: dict) -> list:
    '''
    Sort values in the dictionary.
    '''
    keys = sorted(dic)
    return [dic[key] for key in keys]

def make_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        os.system("cp /web/aratanshi/public_html/plots/index.php {}".format(directory)) #copy index to show plots in web page automatically
        print(f"Directory created successfully.")
    else:
        print(f"Directory already exists.")

def file_exists(file_path):
    return os.path.isfile(file_path)

# directory with final stage files
DIRECTORY = "/ceph/aratanshi/final_output/"

# selection tag used in your input file names, e.g. wzp6_ee_eeH_HWW_ecm365_sel0_histo.root
CUT = "sel0"

#now you can list all the histograms that you want to plot
VARIABLES = [

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

        ]

#directory where you want your plots to go
DIR_PLOTS = "/web/aratanshi/public_html/plots/replot/"

energy      = 365
collider    = 'FCC-ee'
intLumi     = 3e6 #ab^-1
LOGY        = True

#list of backgrounds, then legend and colors to be assigned to them
backgrounds_all = []
# backgrounds_all = ["p8_ee_WW_ecm365",
#                    "p8_ee_ZZ_ecm365",
#                    "p8_ee_tt_ecm365"]

legend = {
	"wzp6_ee_eeH_HWW_ecm365":  "ee #rightarrow eeH #rightarrow HWW",
	"wzp6_ee_mumuH_HWW_ecm365":"ee #rightarrow mumuH #rightarrow HWW",
	"wzp6_ee_eeH_HZZ_ecm365":  "ee #rightarrow eeH #rightarrow HZZ",
	"wzp6_ee_mumuH_HZZ_ecm365":"ee #rightarrow mumuH #rightarrow HZZ",

    # "p8_ee_WW_ecm365":"ee #rightarrow WW",
    # "p8_ee_ZZ_ecm365":"ee #rightarrow ZZ",
    # "p8_ee_tt_ecm365":"ee #rightarrow tt",
}

legcolors = {
	'wzp6_ee_eeH_HWW_ecm365':ROOT.TColor.GetColor('#c51b7d'),
	'wzp6_ee_mumuH_HWW_ecm365':ROOT.TColor.GetColor('#2b8cbe'),
	'wzp6_ee_eeH_HZZ_ecm365':ROOT.TColor.GetColor('#fdae6b'),
	'wzp6_ee_mumuH_HZZ_ecm365':ROOT.TColor.GetColor('#762a83'),

    # 'p8_ee_WW_ecm365':ROOT.TColor.GetColor('#d9f0d3'),
    # 'p8_ee_ZZ_ecm365':ROOT.TColor.GetColor('#1b7837'),
    # 'p8_ee_tt_ecm365':ROOT.TColor.GetColor('#7fbf7b'),
}

#list of signals, then legend and colors to be assigned to them
signals = [
	'wzp6_ee_eeH_HWW_ecm365',
	'wzp6_ee_mumuH_HWW_ecm365',
	'wzp6_ee_eeH_HZZ_ecm365',
	'wzp6_ee_mumuH_HZZ_ecm365',
]

# make sure the output directory exists before we start saving into it
make_dir_if_not_exists(DIR_PLOTS)

for variable in VARIABLES:

	directory = DIRECTORY
	print(variable, directory)

	canvas = ROOT.TCanvas("", "", 800, 800)

	nsig = len(signals)
	nbkg = len(backgrounds_all) #put to zero if you only want to look at signals

	#legend coordinates and style
	legsize = 0.04*nsig
	legsize2 = 0.04*nbkg
	leg = ROOT.TLegend(0.16, 0.70 - legsize, 0.45, 0.70)
	leg.SetFillColor(0)
	leg.SetFillStyle(0)
	leg.SetLineColor(0)
	leg.SetShadowColor(0)
	leg.SetTextSize(0.025)
	leg.SetTextFont(42)
	leg.SetBorderSize(0)

	leg2 = ROOT.TLegend(0.45, 0.70 - legsize2, 0.90, 0.70)
	leg2.SetNColumns(2)
	leg2.SetFillColor(0)
	leg2.SetFillStyle(0)
	leg2.SetLineColor(0)
	leg2.SetShadowColor(0)
	leg2.SetTextSize(0.025)
	leg2.SetTextFont(42)
	leg2.SetBorderSize(0)

	#global arrays for histos and colors
	histos = []
	colors = []
	leg_bkg = []

	#loop over files for signals and assign corresponding colors and titles
	for s in signals:
		fin = directory + s + "_" + CUT + "_histo.root"
		if file_exists(fin): #might be an empty file after stage2
			tf = ROOT.TFile.Open(fin, 'READ')
			h = tf.Get(variable)
			hh = copy.deepcopy(h)
			hh.SetDirectory(0)
			histos.append(hh)
			colors.append(legcolors[s])
			leg.AddEntry(histos[-1], legend[s], "l")
			leg_bkg.append(0)
	nsig = len(histos)

	if nbkg != 0:
		#for the common backgrounds i want to keep them separate into different histograms
		for b in backgrounds_all:
			fin = directory + b + "_" + CUT + "_histo.root"
			if file_exists(fin):
				tf = ROOT.TFile.Open(fin, 'READ')
				h = tf.Get(variable)
				hh = copy.deepcopy(h)
				hh.SetDirectory(0)
				histos.append(hh)
				colors.append(legcolors[b])
				leg_bkg.append(b)

		#drawing stack for backgrounds
		hStackBkg = ROOT.THStack("hStackBkg", "")

		BgMCHistYieldsDic = {}
		for i in range(nsig, len(histos)):
			h = histos[i]
			h.SetLineWidth(1)
			h.SetLineColor(ROOT.kBlack)
			h.SetFillColor(colors[i])
			#making sure only histograms with integral positive get added to the stack and legend
			if h.Integral() > 0:
				BgMCHistYieldsDic[h.Integral()] = h
				leg2.AddEntry(h, legend[leg_bkg[i]], "f")
			else:
				BgMCHistYieldsDic[-1*nbkg] = h

		# sort stack by yields (smallest to largest)
		BgMCHistYieldsDic = sorted_dict_values(BgMCHistYieldsDic)
		for h in BgMCHistYieldsDic:
			hStackBkg.Add(h)

		if LOGY == True:
			hStackBkg.SetMinimum(1e-1) #change the range to be plotted
			hStackBkg.SetMaximum(1e10) #leave some space on top for the legend
		else:
			last = 0
			for i in range(len(histos)):
				if last < histos[i].GetMaximum():
					last = histos[i].GetMaximum()
			hStackBkg.SetMinimum(0)
			hStackBkg.SetMaximum(last*3)

		#draw the histograms
		hStackBkg.Draw("HIST")

		# add the signal histograms
		for i in range(nsig):
			h = histos[i]
			h.SetLineWidth(3)
			h.SetLineColor(colors[i])
			h.Draw("HIST SAME")

		hStackBkg.GetYaxis().SetTitle("Events")
		hStackBkg.GetXaxis().SetTitle(histos[0].GetXaxis().GetTitle()) #get x axis label from final stage
		hStackBkg.GetXaxis().SetTitleOffset(1.2)

	else:
		# add the signal histograms
		for i in range(nsig):
			h = histos[i]
			h.SetLineWidth(3)
			h.SetLineColor(colors[i])
			if i == 0:
				h.Draw("HIST")
				h.GetYaxis().SetTitle("Events")
				h.GetXaxis().SetTitle(histos[i].GetXaxis().GetTitle())
				h.GetXaxis().SetTitleOffset(1.2)
				if LOGY == True:
					h.GetYaxis().SetRangeUser(1e-6, 1e8) #range to set if only working with signals
				else:
					max_y = h.GetMaximum()
					h.GetYaxis().SetRangeUser(0, max_y*1.5)
			else:
				h.Draw("HIST SAME")

	if 'ee' in collider:
		leftText = 'FCCAnalyses: FCC-ee Simulation (Delphes)'
	rightText = f'#sqrt{{s}} = {energy} GeV, L={intLumi} ab^{{-1}}'

	latex = ROOT.TLatex()
	latex.SetNDC()

	text = '#bf{#it{'+rightText+'}}'
	latex.SetTextSize(0.03)
	latex.DrawLatex(0.18, 0.84, text)

	latex.SetTextAlign(31)
	text = '#it{' + leftText + '}'
	latex.SetTextSize(0.03)
	latex.DrawLatex(0.92, 0.92, text)

	#fix legend height after having the correct number of processes
	legsize = 0.04*nsig
	legsize2 = 0.03*(len(histos)-nsig)/2
	leg.SetY1(0.70 - legsize)
	leg2.SetY1(0.70 - legsize2)

	leg.Draw()
	leg2.Draw()

	canvas.SetTicks(1, 1)
	canvas.SetLeftMargin(0.14)
	canvas.SetRightMargin(0.08)
	canvas.GetFrame().SetBorderSize(12)

	if LOGY == True:
		canvas.SetLogy()

	canvas.RedrawAxis()
	canvas.Modified()
	canvas.Update()

	suffix = "_logy" if LOGY else "_lin"
	canvas.SaveAs(DIR_PLOTS + variable + "_" + CUT + suffix + ".png")