#!/usr/bin/env python3

"""
FCC-ee plotting script
Adapted from FCCAnalyses/do_plots.py
"""

# Start timer to measure script run time
import time
START_TIME = time.perf_counter()

import os
import glob
import ROOT

# get CUTS and VARIABLES data from analysis script
from analysis_final import cutList, histoList

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

# Directory containing the final-stage ROOT files
DIRECTORY = "/ceph/aratanshi/final_output/"

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
# VARIABLES = list(histoList)
VARIABLES = ["RecoH_mass_1"]

# Set this to True if you want backgrounds included
PLOT_BACKGROUNDS = True

# Produce linear and logarithmic versions
PLOT_LOG = True
PLOT_LINEAR = True

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

    # "p8_ee_WW_ecm365": {
    #     "label": "ee #rightarrow WW",
    #     "color": "#9467bd",
    # },

    # "p8_ee_ZZ_ecm365": {
    #     "label": "ee #rightarrow ZZ",
    #     "color": "#e377c2",
    # },

    # "p8_ee_tt_ecm365": {
    #     "label": "ee #rightarrow tt",
    #     "color": "#8c564b",
    # },
    
}

BACKGROUNDS = {
    "p8_ee_WW_ecm365": {
        "label": "ee #rightarrow WW",
        "color": "#3B3B3B",
    },

    "p8_ee_ZZ_ecm365": {
        "label": "ee #rightarrow ZZ",
        "color": "#808080",
    },

    "p8_ee_tt_ecm365": {
        "label": "ee #rightarrow tt",
        "color": "#C4C4C4",
    },
}

# Convert hexadecimal colors to ROOT colors once
for process_info in list(SIGNALS.values()) + list(BACKGROUNDS.values()):
    process_info["root_color"] = ROOT.TColor.GetColor(process_info["color"])


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def load_histogram(process, cut, variable):
    """
    Load one histogram from a ROOT file

    Parameters
    ----------
    process : str
        Process name, e.g. 'wzp6_ee_eeH_HWW_ecm365'

    cut : str
        Selection name, e.g. 'selZ'

    variable : str
        Histogram name, e.g. 'Recoil_mass'

    Returns
    -------
    ROOT histogram or None
        A detached copy of the histogram, or None if the file/histogram
        could not be found
    """

    filename = os.path.join(
        DIRECTORY,
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
    background_legend_height = 0.03 * n_background

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
        for process, hist in background_hists:

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

    # Energy
    ss_text = f"#sqrt{{s}} = {ENERGY} GeV,"
    text.SetTextFont(132)
    text.SetTextSize(0.02)
    text.DrawLatex(0.14, 0.91, ss_text)
    
    # Luminosity
    L_text = f"L = {INT_LUMI} ab^{{-1}}"
    text.SetTextFont(132)
    text.SetTextSize(0.02)
    text.DrawLatex(0.26, 0.91, L_text)

    # FCCAnalyses label
    fcc_text = "#bf{FCCAnalyses: FCC-ee Simulation}"
    text.SetTextFont(42)
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
            f"{variable}_{suffix}.{ext}",
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
    print(f" Output directory : {DIR_PLOTS}")
    print(f" Energy           : {ENERGY} GeV")
    print(f" Luminosity       : {INT_LUMI} ab^-1")
    print(f" Cuts             : {CUTS}")
    print(f" Variables        : {VARIABLES}")
    print(f" Backgrounds      : {PLOT_BACKGROUNDS}")
    print("==============================================")
    print()


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
            print(f"Processing: {variable}")
            print(f"Selection : {cut}")
            print("----------------------------------------------")


            # ===============================================================
            # Load signal histograms
            # ===============================================================

            signal_hists = []

            for process in SIGNALS:

                hist = load_histogram(
                    process,
                    cut,
                    variable,
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
            # Load background histograms if requested
            # ===============================================================

            background_hists = []

            if PLOT_BACKGROUNDS:

                for process in BACKGROUNDS:

                    hist = load_histogram(
                        process,
                        cut,
                        variable,
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


    print()
    print("==============================================")
    print(" Plotting finished.")
    # print("==============================================")


# ---------------------------------------------------------------------------
# Run script
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()

    # Gather all file paths in the plots directory recursively
    search_pattern = os.path.join(DIR_PLOTS, "**", "*.*")
    all_files = glob.glob(search_pattern, recursive=True)
    
    # Filter for files that were actually modified or created during this run
    updated_files = [
        file_path for file_path in all_files 
        if os.path.isfile(file_path) and os.path.getmtime(file_path) >= START_TIME
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
    print(f" Elapsed time (H:M:S): {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
    print(f" Total plots produced: {total_plots:,}")
    print("==============================================")
