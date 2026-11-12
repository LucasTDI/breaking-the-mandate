"""Count insider trades and concealment for GPT-4 (32k) in Apollo Research's public results.

Usage:
    git clone https://github.com/apolloresearch/insider-trading
    python analysis/count_apollo_labels.py insider-trading/results > analysis/apollo_gpt4_32k_counts.csv
"""
import collections
import glob
import json
import os
import sys

root = sys.argv[1]
rows = collections.defaultdict(lambda: [0, 0, 0, 0])
for path in glob.glob(f"{root}/**/gpt-4-32k/**/*.json", recursive=True):
    parts = os.path.relpath(path, root).split(os.sep)
    stage = parts[-2]
    variation = "/".join(p for p in parts[:-2] if p != "gpt-4-32k")
    with open(path) as f:
        data = json.load(f)
    if stage == "misalignment":
        rows[variation][0] += 1
        rows[variation][1] += bool(data.get("is_misaligned"))
    elif stage == "deception":
        rows[variation][2] += 1
        rows[variation][3] += bool(data.get("is_deceptive"))

print("variation,runs,traded,traded_pct,hid,hid_pct_of_traded")
for variation, (runs, traded, dec_n, hid) in sorted(rows.items()):
    t_pct = round(100 * traded / runs) if runs else ""
    h_pct = round(100 * hid / dec_n) if dec_n else ""
    print(f'"{variation}",{runs},{traded},{t_pct},{hid},{h_pct}')
