import ROOT
import glob

# load all signal root files
files = glob.glob("/ceph/aratanshi/stage_output/wzp6_ee_*H_*/*.root")
df = ROOT.RDataFrame("events", files)

# event counts
n_total = df.Count()
n4 = df.Filter("abs(RecoH_mass - 125.0) < 20").Count()
n2 = df.Filter("abs(RecoH2_mass - 125.0) < 20").Count()

# efficiencies
eff4 = n4.GetValue() / n_total.GetValue()
eff2 = n2.GetValue() / n_total.GetValue()

print("\nHiggs Reconstruction Efficiency\n")
print(f"Total events: {n_total.GetValue():.0f}")
print(f"4-jet Higgs:  {n4.GetValue():.0f}  -> eff = {eff4:.4f}")
print(f"2-jet Higgs:  {n2.GetValue():.0f}  -> eff = {eff2:.4f}")
