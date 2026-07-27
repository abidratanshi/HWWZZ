import glob
import os
import ROOT

base_dir = "/ceph/aratanshi/stage_output"

samples = [
    "wzp6_ee_eeH_HWW_ecm365",
    "wzp6_ee_mumuH_HWW_ecm365",
    "wzp6_ee_eeH_HZZ_ecm365",
    "wzp6_ee_mumuH_HZZ_ecm365",
]

files = []

for sample in samples:
    pattern = os.path.join(base_dir, sample, "chunk_*.root")
    files.extend(sorted(glob.glob(pattern)))

print(f"Found {len(files)} ROOT files.")
for f in files:
    print(f)

df = ROOT.RDataFrame("events", files)


# None = no pT cut
pt_thresholds = [None, 5, 10, 15, 20, 25]

results = {}  # threshold -> (histogram pointer, event count)

for pt_cut in pt_thresholds:

    if pt_cut is None:
        # No pT cut, only require exactly 4 jets
        df_cut = df.Filter(
            "TagJet_kt4_pt.size() == 4",
            "no_pt_cut"
        )
        hist_name = "RecoH_mass_noptcut"
        hist_title = "Reco H mass, no jet p_{T} cut;m_{H} [GeV];Events"
    else:
        # Require all 4 jets to pass the pT threshold
        df_cut = df.Filter(
            f"TagJet_kt4_pt.size() == 4 && "
            f"ROOT::VecOps::Min(TagJet_kt4_pt) > {pt_cut}",
            f"pt_cut_{pt_cut}"
        )
        hist_name = f"RecoH_mass_ptcut{pt_cut}"
        hist_title = (
            f"Reco H mass, jet p_{{T}} > {pt_cut} GeV;"
            f"m_{{H}} [GeV];Events"
        )

    h = df_cut.Histo1D(
        (hist_name, hist_title, 75, 60, 180),
        "RecoH_mass"
    )

    count = df_cut.Count()  # lazy
    results[pt_cut] = (h, count)

# ----------------------------------------------------------------------
# Trigger the event loop and make the plots
# ----------------------------------------------------------------------

# Linear grid
canvas = ROOT.TCanvas("c", "pT scan", 900, 700)
canvas.Divide(2, 3)

# Log-scale grid
canvas_log = ROOT.TCanvas("c_log", "pT scan (log y)", 900, 700)
canvas_log.Divide(2, 3)

colors = [
    ROOT.kBlack,
    ROOT.kBlue,
    ROOT.kRed,
    ROOT.kGreen + 2,
    ROOT.kMagenta,
    ROOT.kOrange + 7,
]

for i, pt_cut in enumerate(pt_thresholds):

    h, count = results[pt_cut]
    n_events = count.GetValue()   # triggers the event loop only once

    label = "No pT cut" if pt_cut is None else f"pT > {pt_cut} GeV"

    print(
        f"{label}: {n_events} events survive, "
        f"histogram integral = {h.Integral()}"
    )

    h.SetLineColor(colors[i % len(colors)])

    # Linear version
    canvas.cd(i + 1)
    h.Draw("hist")

    # Log-y version
    canvas_log.cd(i + 1)
    ROOT.gPad.SetLogy()
    h.Draw("hist")

canvas.SaveAs("pt_scan_grid.png")
canvas_log.SaveAs("pt_scan_grid_logy.png")

# ----------------------------------------------------------------------
# Overlay (normalized)
# ----------------------------------------------------------------------

c2 = ROOT.TCanvas("c2", "pT scan overlay", 800, 600)
legend = ROOT.TLegend(0.60, 0.60, 0.88, 0.88)

kept_hists = []  # keeps clones alive

for i, pt_cut in enumerate(pt_thresholds):

    h, count = results[pt_cut]

    h_norm = h.Clone(f"{h.GetName()}_norm")
    h_norm.SetDirectory(0)

    if h_norm.Integral() > 0:
        h_norm.Scale(1.0 / h_norm.Integral())

    h_norm.SetLineColor(colors[i % len(colors)])
    h_norm.SetLineWidth(2)

    label = "No p_{T} cut" if pt_cut is None else f"p_{{T}} > {pt_cut} GeV"
    legend.AddEntry(h_norm, label, "l")

    h_norm.Draw("hist same" if i > 0 else "hist")

    kept_hists.append(h_norm)

legend.Draw()

c2.SaveAs("pt_scan_overlay.png")