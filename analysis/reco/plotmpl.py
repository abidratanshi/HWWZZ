#!/usr/bin/env python3
"""
Matplotlib port of the ROOT-based FCCAnalyses plotting script.

Reads TH1D histograms out of the final-stage ROOT files (no ROOT drawing
involved) and re-plots them with matplotlib. Produces the same set of
per-variable, per-cut, log/lin PNGs as the original script.
"""

import os
import copy
import numpy as np
import matplotlib
matplotlib.use("Agg")  # batch mode, equivalent to ROOT.gROOT.SetBatch(True)
import matplotlib.pyplot as plt
import ROOT

ROOT.gROOT.SetBatch(True)

# ----------------------------------------------------------------------
# Config (same as original script)
# ----------------------------------------------------------------------

DIRECTORY = "/ceph/aratanshi/final_output/"

# NOTE: the original script had CUT as a list but used it as a string in
# the filename ("_" + CUT + "_histo.root"), which only works for a single
# string. Fixed here by looping over each cut explicitly.
CUTS = ["sel0", "sel1", "sel2"]

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

DIR_PLOTS = "/web/aratanshi/public_html/plots/plotmpl/"

energy = 365
collider = "FCC-ee"
intLumi = 3  # ab^-1

backgrounds_all = ["p8_ee_WW_ecm365", "p8_ee_ZZ_ecm365", "p8_ee_tt_ecm365"]

legend = {
    "wzp6_ee_eeH_HWW_ecm365":   "ee #rightarrow eeH #rightarrow HWW",
    "wzp6_ee_mumuH_HWW_ecm365": "ee #rightarrow mumuH #rightarrow HWW",
    "wzp6_ee_eeH_HZZ_ecm365":   "ee #rightarrow eeH #rightarrow HZZ",
    "wzp6_ee_mumuH_HZZ_ecm365": "ee #rightarrow mumuH #rightarrow HZZ",
    "p8_ee_WW_ecm365": "ee #rightarrow WW",
    "p8_ee_ZZ_ecm365": "ee #rightarrow ZZ",
    "p8_ee_tt_ecm365": "ee #rightarrow tt",
}

# matplotlib doesn't use ROOT TLatex syntax, so a plain-text legend map is
# used for labels (kept separate from `legend` above, which still uses
# ROOT's "#rightarrow" syntax in case you want it for anything else)
legend_mpl = {
    "wzp6_ee_eeH_HWW_ecm365":   r"ee $\rightarrow$ eeH $\rightarrow$ HWW",
    "wzp6_ee_mumuH_HWW_ecm365": r"ee $\rightarrow$ $\mu\mu$H $\rightarrow$ HWW",
    "wzp6_ee_eeH_HZZ_ecm365":   r"ee $\rightarrow$ eeH $\rightarrow$ HZZ",
    "wzp6_ee_mumuH_HZZ_ecm365": r"ee $\rightarrow$ $\mu\mu$H $\rightarrow$ HZZ",
    "p8_ee_WW_ecm365": r"ee $\rightarrow$ WW",
    "p8_ee_ZZ_ecm365": r"ee $\rightarrow$ ZZ",
    "p8_ee_tt_ecm365": r"ee $\rightarrow$ tt",
}

legcolors = {
    "wzp6_ee_eeH_HWW_ecm365":   "#c51b7d",
    "wzp6_ee_mumuH_HWW_ecm365": "#2b8cbe",
    "wzp6_ee_eeH_HZZ_ecm365":   "#fdae6b",
    "wzp6_ee_mumuH_HZZ_ecm365": "#762a83",
    "p8_ee_WW_ecm365": "#d9f0d3",
    "p8_ee_ZZ_ecm365": "#1b7837",
    "p8_ee_tt_ecm365": "#7fbf7b",
}

signals = [
    "wzp6_ee_eeH_HWW_ecm365",
    "wzp6_ee_mumuH_HWW_ecm365",
    "wzp6_ee_eeH_HZZ_ecm365",
    "wzp6_ee_mumuH_HZZ_ecm365",
]


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def make_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        index_src = "/web/aratanshi/public_html/plots/index.php"
        if os.path.isfile(index_src):
            os.system(f"cp {index_src} {directory}")
        print("Directory created successfully.")
    else:
        print("Directory already exists.")


def file_exists(file_path):
    return os.path.isfile(file_path)


def th1_to_arrays(h):
    """
    Convert a ROOT TH1D into (bin_edges, contents, xlabel).
    bin_edges has length n_bins+1, contents has length n_bins - the
    standard format matplotlib's stairs/step functions expect.
    """
    n_bins = h.GetNbinsX()
    edges = np.array([h.GetBinLowEdge(i) for i in range(1, n_bins + 2)])
    contents = np.array([h.GetBinContent(i) for i in range(1, n_bins + 1)])
    xlabel = h.GetXaxis().GetTitle()
    return edges, contents, xlabel


def load_histogram(directory, process, cut, variable):
    """Open one final-stage file and pull out one histogram as numpy arrays."""
    fin = os.path.join(directory, f"{process}_{cut}_histo.root")
    if not file_exists(fin):
        return None
    tf = ROOT.TFile.Open(fin, "READ")
    h = tf.Get(variable)
    if not h:
        tf.Close()
        return None
    edges, contents, xlabel = th1_to_arrays(copy.deepcopy(h))
    tf.Close()
    return edges, contents, xlabel


# ----------------------------------------------------------------------
# Main plotting loop
# ----------------------------------------------------------------------

make_dir_if_not_exists(DIR_PLOTS)

# single mathtext expression, no nested $...$ (matplotlib mathtext can't
# parse a $ inside a $ block) - \mathbf{} makes it bold, matching the
# original ROOT #bf{#it{...}} styling
right_text = (
    rf"$\mathbf{{\sqrt{{s}}\ =\ {energy}\ GeV,\ L={intLumi}\ ab^{{-1}}}}$"
)
left_text = "FCCAnalyses: FCC-ee Simulation (Delphes)" if "ee" in collider else ""

for cut in CUTS:
    for variable in VARIABLES:

        print(variable, cut, DIRECTORY)

        # ---- load signal histograms ----
        sig_data = []  # list of (edges, contents, xlabel, color, label)
        for s in signals:
            result = load_histogram(DIRECTORY, s, cut, variable)
            if result is None:
                continue
            edges, contents, xlabel = result
            sig_data.append((edges, contents, xlabel, legcolors[s], legend_mpl[s]))

        if not sig_data:
            print(f"  no signal histograms found for {variable}, {cut} - skipping")
            continue

        # ---- load background histograms (kept separate, for stacking) ----
        bkg_data = []
        for b in backgrounds_all:
            result = load_histogram(DIRECTORY, b, cut, variable)
            if result is None:
                continue
            edges, contents, xlabel = result
            bkg_data.append((edges, contents, xlabel, legcolors[b], legend_mpl.get(b, b), contents.sum()))

        # sort backgrounds smallest to largest integral, same as original THStack ordering
        bkg_data.sort(key=lambda t: t[5])

        xlabel = sig_data[0][2]

        # ---- produce one figure per y-scale ----
        for logy in (True, False):

            fig, ax = plt.subplots(figsize=(8, 8))

            # background stack (drawn first, so it sits behind signal lines)
            if bkg_data:
                bottom = np.zeros(len(bkg_data[0][1]))
                for edges, contents, _, color, label, _ in bkg_data:
                    centers = 0.5 * (edges[:-1] + edges[1:])
                    widths = np.diff(edges)
                    ax.bar(centers, contents, width=widths, bottom=bottom,
                           color=color, edgecolor="black", linewidth=0.5,
                           label=label, zorder=1)
                    bottom += contents

            # signal lines (unstacked, drawn on top)
            for edges, contents, _, color, label in sig_data:
                ax.stairs(contents, edges, color=color, linewidth=2.5,
                          label=label, zorder=2)

            ax.set_xlabel(xlabel if xlabel else variable, fontsize=12)
            ax.set_ylabel("Events", fontsize=12)

            if logy:
                ax.set_yscale("log")
                ax.set_ylim(1e-1, 1e10)
            else:
                all_contents = [c for _, c, _, _, _ in sig_data]
                if bkg_data:
                    all_contents.append(bottom)  # top of the stack
                max_y = max(c.max() if len(c) else 0 for c in all_contents)
                ax.set_ylim(0, max_y * 1.5 if max_y > 0 else 1)

            ax.tick_params(direction="in", top=True, right=True)

            # annotation text, roughly matching the ROOT TLatex placement
            # right_text is already a complete mathtext string (bold);
            # left_text is plain text, italicized via matplotlib's fontstyle
            # instead of mathtext (avoids another nested-$ issue with
            # arbitrary text like process/collider names)
            ax.text(0.03, 0.94, right_text, transform=ax.transAxes,
                    fontsize=10, ha="left", va="top")
            ax.text(0.98, 1.01, left_text, transform=ax.transAxes,
                    fontsize=10, ha="right", va="bottom", fontstyle="italic")

            ax.legend(loc="upper left", bbox_to_anchor=(0.03, 0.85),
                      frameon=False, fontsize=9)

            fig.tight_layout()

            suffix = "_log" if logy else "_lin"
            outpath = os.path.join(DIR_PLOTS, f"{variable}_{cut}{suffix}.png")
            fig.savefig(outpath, dpi=150)
            plt.close(fig)