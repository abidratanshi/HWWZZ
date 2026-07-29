import glob
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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

colors = ['k','r','g','b','y','c']

results = {}  # threshold -> (histogram pointer, event count) - unchanged from original

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
# Trigger the event loop, pull histogram data into numpy, then plot with
# matplotlib instead of ROOT canvases.
# ----------------------------------------------------------------------

# kept_data holds (edges, contents, label) for every threshold, staying
# alive for the whole script.
kept_data = []

for pt_cut in pt_thresholds:
    h, count = results[pt_cut]
    n_events = count.GetValue()  # triggers the event loop only once total, same as original
    label = "No pT cut" if pt_cut is None else f"pT > {pt_cut} GeV"
    print(
        f"{label}: {n_events} events survive, "
        f"histogram integral = {h.Integral()}"
    )

    # pull bin edges/contents out of the ROOT TH1D into numpy arrays
    hist_obj = h.GetValue()  # RResultPtr -> actual TH1D
    n_bins = hist_obj.GetNbinsX()
    edges = np.array([hist_obj.GetBinLowEdge(i) for i in range(1, n_bins + 2)])
    contents = np.array([hist_obj.GetBinContent(i) for i in range(1, n_bins + 1)])

    kept_data.append((edges, contents, label))

# ---- linear-scale grid (2 columns x 3 rows, matching canvas.Divide(2,3)) ----
fig_lin, axes_lin = plt.subplots(3, 2, figsize=(10, 12))
axes_lin = axes_lin.flatten()

for i, (edges, contents, label) in enumerate(kept_data):
    color = colors[i % len(colors)]
    ax = axes_lin[i]
    ax.stairs(contents, edges, color=color)
    ax.set_xlabel(r"$m_H$ [GeV]")
    ax.set_ylabel("Events")
    ax.set_title(label)

fig_lin.tight_layout()
fig_lin.savefig("pt_scan_grid.png", dpi=150)
plt.close(fig_lin)

# ---- log-y grid ----
fig_log, axes_log = plt.subplots(3, 2, figsize=(10, 12))
axes_log = axes_log.flatten()

for i, (edges, contents, label) in enumerate(kept_data):
    color = colors[i % len(colors)]
    ax = axes_log[i]
    ax.stairs(contents, edges, color=color)
    ax.set_yscale("log")
    ax.set_xlabel(r"$m_H$ [GeV]")
    ax.set_ylabel("Events")
    ax.set_title(label)

fig_log.tight_layout()
fig_log.savefig("pt_scan_grid_logy.png", dpi=150)
plt.close(fig_log)