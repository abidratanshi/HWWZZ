import ROOT
import glob

samples = [
    "wzp6_ee_eeH_HWW_ecm365",
    "wzp6_ee_mumuH_HWW_ecm365",
    "wzp6_ee_eeH_HZZ_ecm365",
    "wzp6_ee_mumuH_HZZ_ecm365",
]

# mass windows (GeV) to quantify
Z_WINDOW = (86, 101)
H_WINDOW = (120, 130)

for sample in samples:

    print(f"\n--- Processing Sample: {sample} ---")
    path = f"/ceph/aratanshi/stage_output/{sample}/*.root"
    files = glob.glob(path)
    # validation check to ensure file exists
    if not files:
        print(f"Warning: No .root file found in {path}")
        continue

    # initialize RDataFrame for this sample
    df = ROOT.RDataFrame("events", files)

    # event counting logic
    n_total = df.Count()
    n_zpeak = df.Filter(f"RecoH_mass > {Z_WINDOW[0]} && RecoH_mass < {Z_WINDOW[1]}").Count()
    n_hpeak = df.Filter(f"RecoH_mass > {H_WINDOW[0]} && RecoH_mass < {H_WINDOW[1]}").Count()

    # GetValue() triggers the event loop
    total = n_total.GetValue()
    zpeak = n_zpeak.GetValue()
    hpeak = n_hpeak.GetValue()

    # print results, including percentage over the total
    print(f"n_total: {total:.0f}")
    if total > 0:
        print(f"n_zpeak ({Z_WINDOW[0]}-{Z_WINDOW[1]} GeV): {zpeak:.0f}  ({100*zpeak/total:.2f}% of total)")
        print(f"n_hpeak ({H_WINDOW[0]}-{H_WINDOW[1]} GeV): {hpeak:.0f}  ({100*hpeak/total:.2f}% of total)")
    else:
        print("No events found, skipping percentage calculation.")