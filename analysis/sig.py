sig_processes = ['wzp6_ee_eeH_HWW_ecm365','wzp6_ee_mumuH_HWW_ecm365',
                 'wzp6_ee_eeH_HZZ_ecm365','wzp6_ee_mumuH_HZZ_ecm365']
bkg_processes = ['p8_ee_WW_ecm365','p8_ee_ZZ_ecm365','p8_ee_tt_ecm365']

processes = sig_processes+bkg_processes

events = dict.fromkeys(processes)
selections = None

path = "/ceph/aratanshi/final_output/outputTabular.txt"
file = open(path)

for line in file:
    li = line.split()

    # this stops the loop before the second table
    if li[0] == "\\end{table}": break

    # gets row of selections
    elif li[0] == "&":
        selections = li[1:-1:2]

    elif li[0] in processes:
        process = li[0]
        events[process] = {k:float(v) for k,v in zip(selections,li[2:-1:2])}

S_total = 0
B_total = 0

for sel in selections:
    S = 0
    B = 0
    for process in events:
        if process in sig_processes:
            S += events[process][sel]
        elif process in bkg_processes:
            B += events[process][sel]

    # saving initial sig/bkg counts with no cuts to compare to
    if sel == "sel0":
        S_total = S
        B_total = B
    
    if sel == selections[0]: print()
    print(sel)
    print(f"S =        {S:.3e}, {S/S_total*100:.0f}% of total sig events")
    print(f"B =        {B:.3e}, {B/B_total*100:.0f}% of total bkg events")
    print(f"S/√(S+B) = {S/(S+B)**(1/2):.3f}")
    if sel != selections[-1]: print()