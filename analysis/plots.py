#!/usr/bin/env python3

"""
FCC-ee plotting script
Adapted from FCCAnalyses/do_plots.py

Includes a merging step: individual background processes are summed into
groups (defined in BKG_GROUPS below) and written to MERGED_DIRECTORY, then
the plots are made from the merged files. Signals are read unchanged from
DIRECTORY.
"""

# Start timer to measure script run time
import time
START_TIME = time.perf_counter()

import os
import glob
import ROOT
import numpy as np

# get processes from analysis stage script
from analysis_stage import processList
# get CUTS and VARIABLES data from analysis final script
from analysis_final import cutList, histoList
# to generate colors for background processes
import matplotlib.pyplot as plt

# Run ROOT in batch mode: does not open graphical windows
ROOT.gROOT.SetBatch(True)
# Surpress all but ROOT warinings
ROOT.gErrorIgnoreLevel = ROOT.kWarning
# Gives a square physical paper size for the PDF
ROOT.gStyle.SetPaperSize(20, 20)
# Max number of digits before exp notation in axes
# ROOT.TGaxis.SetMaxDigits(4)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Directory containing the final-stage ROOT files (one per process, per cut)
DIRECTORY = "/ceph/aratanshi/final_output/"

# Directory where the merged background files are written / read
MERGED_DIRECTORY = "/ceph/aratanshi/final_output_merged/"

# Directory where plots will be saved
DIR_PLOTS = "/web/aratanshi/public_html/plots/"

# Centre-of-mass energy and integrated luminosity
ENERGY = 365   # GeV
INT_LUMI = 3   # ab^-1

# Selections to plot
# the imported cutList is a dictionary and so this just gets the keys
CUTS = list(cutList)

# Histograms to plot
# the imported histoList is a dictionary and so this just gets the keys
VARIABLES = list(histoList)

# Set this to True if you want backgrounds included
PLOT_BACKGROUNDS = True

# Produce linear and logarithmic versions
PLOT_LOG = True
PLOT_LINEAR = True

# Run the merging step at the start of main()
MERGE_BACKGROUNDS = True

# Re-merge every group even if its merged file is already newer than all of
# its inputs. Set to True after editing BKG_GROUPS (a removed member would
# otherwise stay in an old merged file) or after re-running the final stage
# in a way that does not change file modification times.
FORCE_REMERGE = False

# Each process contains:
#   label = text displayed in the legend
#   color = line/fill color

SIGNALS = {
    "wzp6_ee_eeH_HWW_ecm365": {
        "label": "ee #rightarrow eeH #rightarrow HWW",
        "color": "#1f77b4",
    },

    "wzp6_ee_mumuH_HWW_ecm365": {
        "label": "ee #rightarrow #mu#muH #rightarrow HWW",
        "color": "#2ca02c",
    },

    "wzp6_ee_eeH_HZZ_ecm365": {
        "label": "ee #rightarrow eeH #rightarrow HZZ",
        "color": "#ff7f0e",
    },

    "wzp6_ee_mumuH_HZZ_ecm365": {
        "label": "ee #rightarrow #mu#muH #rightarrow HZZ",
        "color": "#d62728",
    },
}

# ---------------------------------------------------------------------------
# Background groups
#
# Each key is the name of the MERGED sample (file name will be
# <key>_<cut>_histo.root in MERGED_DIRECTORY). "members" are the processes
# that are summed into it. Edit this to change the grouping.
# ---------------------------------------------------------------------------

ECM = f"ecm{ENERGY}"

# Higgs decay classes
HQQ = ["Hbb", "Hcc", "Hss", "Hgg"]   # hadronic Higgs decays
HVV = ["HWW", "HZZ"]
HTT = ["Htautau"]


def _higgs(prods, decays):
    """All wzp6_ee_<prod>_<decay>_ecmXXX names for the given productions/decays."""
    return [f"wzp6_ee_{p}_{d}_{ECM}" for p in prods for d in decays]


BKG_GROUPS = {
    # ---- main backgrounds (kept on their own) -----------------------------
    f"p8_ee_WW_{ECM}": {
        "label": "ee #rightarrow WW",
        "members": [f"p8_ee_WW_{ECM}"],
    },
    f"p8_ee_ZZ_{ECM}": {
        "label": "ee #rightarrow ZZ",
        "members": [f"p8_ee_ZZ_{ECM}"],
    },
    f"p8_ee_tt_{ECM}": {
        "label": "ee #rightarrow tt",
        "members": [f"p8_ee_tt_{ECM}"],
    },
    f"p8_ee_WW_tautau_{ECM}": {      # skipped automatically if not on disk
        "label": "ee #rightarrow WW #rightarrow #tau#tau",
        "members": [f"p8_ee_WW_tautau_{ECM}"],
    },

    # ---- Z / diboson-like -------------------------------------------------
    f"p8_ee_ZQQ_{ECM}": {
        "label": "ee #rightarrow Z #rightarrow qq",
        "members": [f"p8_ee_{z}_{ECM}" for z in ("Zqq", "Zbb", "Zcc", "Zss")],
    },
    f"wzp6_ee_LL_{ECM}": {
        "label": "ee #rightarrow ll (e,#mu,#tau)",
        "members": [
            f"wzp6_ee_mumu_{ECM}",
            f"wzp6_ee_ee_Mee_30_150_{ECM}",
            f"wzp6_ee_tautau_{ECM}",
        ],
    },
    f"wzp6_egamma_eZ_ZLL_{ECM}": {
        "label": "e#gamma #rightarrow eZ #rightarrow e ll",
        "members": [
            f"wzp6_egamma_eZ_Zmumu_{ECM}",
            f"wzp6_egamma_eZ_Zee_{ECM}",
            f"wzp6_gammae_eZ_Zmumu_{ECM}",
            f"wzp6_gammae_eZ_Zee_{ECM}",
        ],
    },
    f"wzp6_gaga_LL_60_{ECM}": {
        "label": "#gamma#gamma #rightarrow ll",
        "members": [
            f"wzp6_gaga_tautau_60_{ECM}",
            f"wzp6_gaga_mumu_60_{ECM}",
            f"wzp6_gaga_ee_60_{ECM}",
        ],
    },
    f"wzp6_ee_nuenueZ_{ECM}": {
        "label": "ee #rightarrow #nu_{e}#nu_{e}Z",
        "members": [f"wzp6_ee_nuenueZ_{ECM}"],
    },

    # ---- tautauH ----------------------------------------------------------
    f"wzp6_ee_tautauH_HQQ_{ECM}": {
        "label": "ee #rightarrow #tau#tauH, H #rightarrow qq/gg",
        "members": _higgs(["tautauH"], HQQ),
    },
    f"wzp6_ee_tautauH_HVV_{ECM}": {
        "label": "ee #rightarrow #tau#tauH, H #rightarrow VV",
        "members": _higgs(["tautauH"], HVV),
    },
    f"wzp6_ee_tautauH_Htautau_{ECM}": {
        "label": "ee #rightarrow #tau#tauH, H #rightarrow #tau#tau",
        "members": _higgs(["tautauH"], HTT),
    },

    # ---- nunuH ------------------------------------------------------------
    f"wzp6_ee_nunuH_HQQ_{ECM}": {
        "label": "ee #rightarrow #nu#nuH, H #rightarrow qq/gg",
        "members": _higgs(["nunuH"], HQQ),
    },
    f"wzp6_ee_nunuH_HVV_{ECM}": {
        "label": "ee #rightarrow #nu#nuH, H #rightarrow VV",
        "members": _higgs(["nunuH"], HVV),
    },
    f"wzp6_ee_nunuH_Htautau_{ECM}": {
        "label": "ee #rightarrow #nu#nuH, H #rightarrow #tau#tau",
        "members": _higgs(["nunuH"], HTT),
    },

    # ---- eeH + mumuH, non-signal decays (HWW/HZZ are the signal) ----------
    f"wzp6_ee_LLH_HQQ_{ECM}": {
        "label": "ee #rightarrow (ee,#mu#mu)H, H #rightarrow qq/gg",
        "members": _higgs(["eeH", "mumuH"], HQQ),
    },
    f"wzp6_ee_LLH_Htautau_{ECM}": {
        "label": "ee #rightarrow (ee,#mu#mu)H, H #rightarrow #tau#tau",
        "members": _higgs(["eeH", "mumuH"], HTT),
    },

    # ---- quark-pair + H (bbH, ccH, ssH, qqH) ------------------------------
    f"wzp6_ee_QQH_HQQ_{ECM}": {
        "label": "ee #rightarrow QQH, H #rightarrow qq/gg",
        "members": _higgs(["bbH", "ccH", "ssH", "qqH"], HQQ),
    },
    f"wzp6_ee_QQH_HVV_{ECM}": {
        "label": "ee #rightarrow QQH, H #rightarrow VV",
        "members": _higgs(["bbH", "ccH", "ssH", "qqH"], HVV),
    },
    f"wzp6_ee_QQH_Htautau_{ECM}": {
        "label": "ee #rightarrow QQH, H #rightarrow #tau#tau",
        "members": _higgs(["bbH", "ccH", "ssH", "qqH"], HTT),
    },
}

# Colours: the three main backgrounds keep their greys, every other group
# gets an evenly spaced colour from viridis
MAIN_COLORS = {
    f"p8_ee_WW_{ECM}": "#3B3B3B",
    f"p8_ee_ZZ_{ECM}": "#808080",
    f"p8_ee_tt_{ECM}": "#C4C4C4",
}

_other_groups = [g for g in BKG_GROUPS if g not in MAIN_COLORS]
_viridis = iter(
    map(plt.cm.colors.to_hex, plt.cm.viridis(np.linspace(0, 1, len(_other_groups))))
)

BACKGROUNDS = {
    group: {
        "label": info["label"],
        "color": MAIN_COLORS.get(group) or next(_viridis),
    }
    for group, info in BKG_GROUPS.items()
}

# Convert hexadecimal colors to ROOT colors once
for process_info in list(SIGNALS.values()) + list(BACKGROUNDS.values()):
    process_info["root_color"] = ROOT.TColor.GetColor(process_info["color"])


# ---------------------------------------------------------------------------
# Merging
# ---------------------------------------------------------------------------

def check_coverage():
    """
    Warn about processes in processList that are in no group and not a
    signal, and about processes that appear in more than one group
    (which would double count)
    """

    seen = {}

    for group, info in BKG_GROUPS.items():
        for proc in info["members"]:
            if proc in seen:
                print(
                    f"  WARNING: {proc} is in both '{seen[proc]}' "
                    f"and '{group}' (double counting!)"
                )
            seen[proc] = group

    covered = set(seen) | set(SIGNALS)

    for proc in processList:
        if proc not in covered:
            print(
                f"  WARNING: {proc} is in processList but in no "
                f"background group and is not a signal"
            )


def merge_group(group, members, cut, force=False):
    """
    Sum the histograms of all member processes for one cut and write them
    to a single file: MERGED_DIRECTORY/<group>_<cut>_histo.root

    Every histogram in each member file is summed (the file is opened once),
    so no variable list is needed. The inputs are already scaled to
    cross section * luminosity by the final stage (doScale = True), so
    adding them is correct.
    """

    out_path = os.path.join(MERGED_DIRECTORY, f"{group}_{cut}_histo.root")

    in_paths = []
    for proc in members:
        path = os.path.join(DIRECTORY, f"{proc}_{cut}_histo.root")
        if os.path.isfile(path):
            in_paths.append((proc, path))
        else:
            print(f"    [skip] {proc}: no file for cut '{cut}'")

    if not in_paths:
        print(f"  [none] {group}: no member files for cut '{cut}', nothing written")
        return

    # Skip if the merged file is already newer than every input
    if not force and os.path.isfile(out_path):
        newest_input = max(os.path.getmtime(p) for _, p in in_paths)
        if os.path.getmtime(out_path) >= newest_input:
            print(f"  [up to date] {group}")
            return

    merged = {}      # histogram name -> summed histogram
    n_files = 0

    for proc, path in in_paths:

        tf = ROOT.TFile.Open(path, "READ")

        if not tf or tf.IsZombie():
            print(f"    [skip] {proc}: could not open {path}")
            continue

        n_files += 1

        for key in tf.GetListOfKeys():
            obj = key.ReadObj()

            if not obj.InheritsFrom("TH1"):
                continue

            name = key.GetName()

            if name not in merged:
                h = obj.Clone()
                h.SetDirectory(0)      # detach so it survives tf.Close()
                merged[name] = h
            else:
                merged[name].Add(obj)

        tf.Close()

    if n_files == 0:
        print(f"  [none] {group}: could not open any member file for cut '{cut}'")
        return

    out = ROOT.TFile.Open(out_path, "RECREATE")
    out.cd()

    for h in merged.values():
        h.Write()

    out.Close()

    print(
        f"  [merged] {group}: {n_files}/{len(members)} files, "
        f"{len(merged)} histograms"
    )


def merge_backgrounds(cuts=None, force=False):
    """
    Merge all background groups for every cut
    """

    if cuts is None:
        cuts = CUTS

    os.makedirs(MERGED_DIRECTORY, exist_ok=True)

    print()
    print("----------------------------------------------")
    print(" Merging backgrounds")
    print("----------------------------------------------")

    check_coverage()

    for cut in cuts:
        print(f" Selection: {cut}")

        for group, info in BKG_GROUPS.items():
            merge_group(group, info["members"], cut, force=force)

    print(f" Merged files are in {MERGED_DIRECTORY}")


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def load_histogram(process, cut, variable, directory=DIRECTORY):
    """
    Load one histogram from a ROOT file

    Parameters
    ----------
    process : str
        Process (or merged group) name, e.g. 'wzp6_ee_eeH_HWW_ecm365'

    cut : str
        Selection name, e.g. 'selZ'

    variable : str
        Histogram name, e.g. 'Recoil_mass'

    directory : str
        Directory containing the file. Signals live in DIRECTORY,
        merged backgrounds in MERGED_DIRECTORY

    Returns
    -------
    ROOT histogram or None
        A detached copy of the histogram, or None if the file/histogram
        could not be found
    """

    filename = os.path.join(
        directory,
        f"{process}_{cut}_histo.root"
    )

    # Check whether the ROOT file exists
    if not os.path.isfile(filename):
        print(f"  WARNING: file not found: {filename}")
        return None

    # Open ROOT file
    tf = ROOT.TFile.Open(filename, "READ")

    # Check whether ROOT successfully opened the file
    if not tf or tf.IsZombie():
        print(f"  WARNING: could not open ROOT file: {filename}")

        if tf:
            tf.Close()

        return None

    # Retrieve histogram
    hist = tf.Get(variable)

    if not hist:
        print(
            f"  WARNING: histogram '{variable}' "
            f"not found in {filename}"
        )

        tf.Close()
        return None

    # Clone the histogram so it survives after closing the ROOT file
    hist = hist.Clone()

    # Detach histogram from the ROOT file
    hist.SetDirectory(0)

    # Close input ROOT file
    tf.Close()

    return hist


def configure_legend(legend, n_columns=1):
    """
    Apply common styling to a ROOT legend
    """

    legend.SetNColumns(n_columns)
    legend.SetFillStyle(0)
    legend.SetLineColor(2)
    legend.SetShadowColor(0)
    legend.SetTextSize(0.025)
    legend.SetTextFont(42)
    legend.SetBorderSize(0)


def get_positive_max(histograms):
    """
    Return the largest positive bin content among a list of histograms

    Returns 0 if no positive bin content is found
    """

    maximum = 0.0

    for hist in histograms:
        hist_max = hist.GetMaximum()

        if hist_max > maximum:
            maximum = hist_max

    return maximum


def get_positive_min(histograms):
    """
    Find the smallest positive bin content among histograms

    This is useful for choosing a sensible lower limit on a logarithmic
    y-axis

    Returns 0 if no positive bin content exists
    """

    minimum = float("inf")

    for hist in histograms:

        for bin_number in range(1, hist.GetNbinsX() + 1):
            value = hist.GetBinContent(bin_number)

            if value > 0 and value < minimum:
                minimum = value

    if minimum == float("inf"):
        return 0.0

    return minimum


def style_signal_histogram(hist, process):
    """
    Apply signal histogram styling
    """

    hist.SetLineWidth(3)
    hist.SetLineColor(SIGNALS[process]["root_color"])
    hist.SetFillStyle(0)


def style_background_histogram(hist, process):
    """
    Apply background histogram styling
    """

    hist.SetLineWidth(1)
    hist.SetLineColor(ROOT.kBlack)
    hist.SetFillColor(BACKGROUNDS[process]["root_color"])


# ---------------------------------------------------------------------------
# Plotting function
# ---------------------------------------------------------------------------

def make_plot(
    signal_hists,
    background_hists,
    variable,
    cut,
    logy=False,
):
    """
    Create and save one plot

    Parameters
    ----------
    signal_hists : list of tuples
        [(process_name, histogram), ...]

    background_hists : list of tuples
        [(process_name, histogram), ...]

    variable : str
        Histogram/variable name

    cut : str
        Selection name

    logy : bool
        If True, use logarithmic y-axis
    """

    if not signal_hists:
        print(
            f"  No signal histograms available for "
            f"{variable}, {cut}. Skipping."
        )
        return

    # -----------------------------------------------------------------------
    # Canvas
    # -----------------------------------------------------------------------

    canvas = ROOT.TCanvas(
        f"canvas_{variable}_{cut}",
        "",
        800,
        800,
    )

    canvas.SetTicks(1, 1)
    canvas.SetLeftMargin(0.14)
    canvas.SetRightMargin(0.08)
    canvas.GetFrame().SetBorderSize(12)

    if logy:
        canvas.SetLogy()


    # -----------------------------------------------------------------------
    # Legends
    # -----------------------------------------------------------------------

    n_signal = len(signal_hists)
    n_background = len(background_hists)

    signal_legend_height = 0.03 * n_signal

    signal_legend = ROOT.TLegend(
        0.40,
        0.85 - signal_legend_height,
        0.70,
        0.85,
    )

    configure_legend(signal_legend)


    # Background legend
    background_legend_height = 0.01 * n_background

    background_legend = ROOT.TLegend(
        0.70,
        0.85 - background_legend_height,
        1.00,
        0.85,
    )

    configure_legend(background_legend)


    # -----------------------------------------------------------------------
    # Prepare signal histograms
    # -----------------------------------------------------------------------

    for process, hist in signal_hists:

        style_signal_histogram(hist, process)

        signal_legend.AddEntry(
            hist,
            SIGNALS[process]["label"],
            "l",
        )


    # -----------------------------------------------------------------------
    # Prepare background histograms
    # -----------------------------------------------------------------------

    # Sort backgrounds from smallest to largest total yield
    background_hists_sorted = sorted(
        background_hists,
        key=lambda item: item[1].Integral(),
    )

    background_stack = None

    if background_hists_sorted:

        background_stack = ROOT.THStack(
            f"background_stack_{variable}_{cut}",
            "",
        )

        for process, hist in background_hists_sorted:

            style_background_histogram(hist, process)

            background_stack.Add(hist)

        # Using unsorted list here so that the order of the legend is always the same
        # for process, hist in background_hists:

            # Only add positive-yield backgrounds to the legend
            if hist.Integral() > 0:
                background_legend.AddEntry(
                    hist,
                    BACKGROUNDS[process]["label"],
                    "f",
                )


    # -----------------------------------------------------------------------
    # Determine axis ranges
    # -----------------------------------------------------------------------

    all_hists = [hist for _, hist in signal_hists]

    if background_hists_sorted:
        all_hists += [
            hist for _, hist in background_hists_sorted
        ]

    maximum = get_positive_max(all_hists)

    if maximum <= 0:
        maximum = 1.0


    # -----------------------------------------------------------------------
    # Draw background stack
    # -----------------------------------------------------------------------

    if background_stack:

        if logy:

            positive_min = get_positive_min(
                [hist for _, hist in background_hists_sorted]
            )

            if positive_min <= 0:
                positive_min = maximum * 1e-5

            background_stack.SetMinimum(
                positive_min * 0.5
            )

            background_stack.SetMaximum(
                maximum * 10
            )

        else:

            background_stack.SetMinimum(0)
            background_stack.SetMaximum(maximum * 1.5)

        background_stack.Draw("HIST")

        background_stack.GetYaxis().SetTitle("Events")

        # Use the x-axis title from the first signal histogram
        background_stack.GetXaxis().SetTitle(
            signal_hists[0][1].GetXaxis().GetTitle()
        )

        background_stack.GetXaxis().SetTitleOffset(1.2)


    # -----------------------------------------------------------------------
    # Draw signal histograms
    # -----------------------------------------------------------------------

    if background_stack:

        # Background stack already established the axes
        for _, hist in signal_hists:
            hist.Draw("HIST SAME")

    else:

        # No background: first signal establishes the axes
        first_hist = signal_hists[0][1]

        if logy:

            positive_min = get_positive_min(
                [hist for _, hist in signal_hists]
            )

            if positive_min <= 0:
                positive_min = maximum * 1e-5

            first_hist.SetMinimum(
                positive_min * 0.5
            )

            first_hist.SetMaximum(
                maximum * 10
            )

        else:

            first_hist.SetMinimum(0)
            first_hist.SetMaximum(maximum * 1.5)

        first_hist.Draw("HIST")

        first_hist.GetYaxis().SetTitle("Events")
        first_hist.GetXaxis().SetTitle(
            first_hist.GetXaxis().GetTitle()
        )
        first_hist.GetXaxis().SetTitleOffset(1.2)

        # Draw remaining signal histograms on top
        for _, hist in signal_hists[1:]:
            hist.Draw("HIST SAME")


    # -----------------------------------------------------------------------
    # Add text
    # -----------------------------------------------------------------------

    text = ROOT.TLatex()
    text.SetNDC()
    text.SetTextFont(42)

    # Energy
    ss_text = f"#sqrt{{s}} = {ENERGY} GeV,"
    text.SetTextSize(0.022)
    text.DrawLatex(0.14, 0.91, ss_text)

    # Luminosity
    L_text = f"L = {INT_LUMI} ab^{{-1}}"
    # text.SetTextFont(42)
    text.SetTextSize(0.022)
    text.DrawLatex(0.28, 0.91, L_text)

    # FCCAnalyses label
    fcc_text = "#bf{FCCAnalyses: FCC-ee Simulation}"
    # text.SetTextFont(42)
    text.SetTextSize(0.03)
    text.DrawLatex(0.48, 0.91, fcc_text)


    # -----------------------------------------------------------------------
    # Draw legends
    # -----------------------------------------------------------------------

    signal_legend.Draw()

    if background_hists_sorted:
        background_legend.Draw()


    # -----------------------------------------------------------------------
    # Final canvas update
    # -----------------------------------------------------------------------

    canvas.RedrawAxis()
    canvas.Modified()
    canvas.Update()


    # -----------------------------------------------------------------------
    # Save
    # -----------------------------------------------------------------------

    suffix = "log" if logy else "lin"

    cut_dir = os.path.join(DIR_PLOTS, cut)
    os.makedirs(cut_dir, exist_ok=True)

    # file type extensions to be produced
    exts = ("pdf", "png")

    for ext in exts:
        output_file = os.path.join(
            cut_dir,
            # f"{variable}_{suffix}.{ext}",
            f"{variable}_{cut}_{suffix}.{ext}",
        )

        canvas.SaveAs(output_file)
        print(f"  Saved: {output_file}")

    # Explicitly delete canvas to avoid accumulating ROOT objects
    canvas.Close()


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def main():

    print()
    print("==============================================")
    print(" FCC-ee histogram plotting")
    print("==============================================")
    print(f" Input directory  : {DIRECTORY}")
    print(f" Merged directory : {MERGED_DIRECTORY}")
    print(f" Output directory : {DIR_PLOTS}")
    print(f" Energy           : {ENERGY} GeV")
    print(f" Luminosity       : {INT_LUMI} ab^-1")
    print(f" Cuts             : {CUTS}")
    print(f" Variables        : {VARIABLES}")
    print(f" Backgrounds      : {PLOT_BACKGROUNDS}")
    print(f" Merge first      : {MERGE_BACKGROUNDS} (force: {FORCE_REMERGE})")
    print("==============================================")
    print()


    # -----------------------------------------------------------------------
    # Merge backgrounds into groups (only needed if they will be plotted)
    # -----------------------------------------------------------------------

    if MERGE_BACKGROUNDS and PLOT_BACKGROUNDS:
        merge_backgrounds(CUTS, force=FORCE_REMERGE)


    # -----------------------------------------------------------------------
    # Main loop
    #
    # Histograms are loaded ONCE for each cut/variable combination
    # Then the same histograms are used to make both linear and log plots
    #
    # This avoids opening the same ROOT files twice
    # -----------------------------------------------------------------------

    for cut in CUTS:

        for variable in VARIABLES:

            print()
            print("----------------------------------------------")
            print(f" Processing: {variable}")
            print(f" Selection : {cut}")
            print("----------------------------------------------")


            # ===============================================================
            # Load signal histograms (unmerged, from DIRECTORY)
            # ===============================================================

            signal_hists = []

            for process in SIGNALS:

                hist = load_histogram(
                    process,
                    cut,
                    variable,
                    directory=DIRECTORY,
                )

                if hist is None:
                    continue

                signal_hists.append(
                    (process, hist)
                )


            # If no signal histogram was found, there is nothing to plot
            if not signal_hists:

                print(
                    f"  No signal histograms found for "
                    f"{variable}, {cut}."
                )

                continue


            print(
                f"  Found {len(signal_hists)} "
                f"signal histogram(s)."
            )


            # ===============================================================
            # Load merged background histograms if requested
            # ===============================================================

            background_hists = []

            if PLOT_BACKGROUNDS:

                for process in BACKGROUNDS:

                    hist = load_histogram(
                        process,
                        cut,
                        variable,
                        directory=MERGED_DIRECTORY,
                    )

                    if hist is None:
                        continue

                    background_hists.append(
                        (process, hist)
                    )

                print(
                    f"  Found {len(background_hists)} "
                    f"background histogram(s)."
                )


            # ===============================================================
            # Make linear plot
            # ===============================================================

            if PLOT_LINEAR:

                print("  Creating linear plot...")

                make_plot(
                    signal_hists=signal_hists,
                    background_hists=background_hists,
                    variable=variable,
                    cut=cut,
                    logy=False,
                )


            # ===============================================================
            # Make logarithmic plot
            # ===============================================================

            if PLOT_LOG:

                print("  Creating logarithmic plot...")

                make_plot(
                    signal_hists=signal_hists,
                    background_hists=background_hists,
                    variable=variable,
                    cut=cut,
                    logy=True,
                )


            # ===============================================================
            # Clean up histograms
            # ===============================================================

            # Histograms are detached from their ROOT files, so they are
            # safe to delete here
            signal_hists.clear()
            background_hists.clear()


# ---------------------------------------------------------------------------
# Run script
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()

    # Gather all file paths in the plots directory recursively
    search_pattern = os.path.join(DIR_PLOTS, "**", "*.*")
    all_files = glob.glob(search_pattern, recursive=True)

    # Calculate the epoch time when the script started using your existing START_TIME
    epoch_start_time = time.time() - (time.perf_counter() - START_TIME)

    # Filter for files that were actually modified or created during this run
    updated_files = [
        file_path for file_path in all_files
        if os.path.isfile(file_path) and os.path.getmtime(file_path) >= epoch_start_time
    ]
    total_plots = len(updated_files)

    # Calculate total elapsed run time
    END_TIME = time.perf_counter()
    total_seconds = END_TIME - START_TIME

    # Split into whole minutes and remaining seconds
    total_minutes, seconds = divmod(total_seconds, 60)

    # Split into whole hours and remaining minutes
    hours, minutes = divmod(total_minutes, 60)

    # Output summary
    print()
    print("==============================================")
    print(f" Plotting finished.")
    print(f" Elapsed time (H:M:S): {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
    print(f" Total plots produced: {total_plots:,}")
    print("==============================================")
