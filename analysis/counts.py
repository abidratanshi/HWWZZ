import ROOT
import glob

samples = [
    # "wzp6_ee_eeH_HWW_ecm365",
           # "wzp6_ee_mumuH_HWW_ecm365",
           "wzp6_ee_eeH_HZZ_ecm365",
           "wzp6_ee_mumuH_HZZ_ecm365",
          ]

for sample in samples:
    
    print(f"\n--- Processing Sample: {sample} ---")

    path = f"/ceph/aratanshi/stage_output/{sample}/*.root"
    file = glob.glob(path)

    # validation check to ensure file exists
    if not file:
        print(f"Warning: No .root file found in {path}")
        continue

    # initialize RDataFrame for this sample
    df = ROOT.RDataFrame("events", file)

    # event counting logic
    n_bump = df.Filter("RecoH4_mass > 85 && RecoH4_mass < 95").Count()
    # n_peak = df.Filter("RecoH4_mass > 115 && RecoH4_mass < 135").Count()

    # print results
    print(f"n_bump: {n_bump.GetValue():.0f}")
    # print(f"n_peak: {n_peak.GetValue():.0f}")
    