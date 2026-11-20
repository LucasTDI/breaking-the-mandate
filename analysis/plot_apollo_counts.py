"""Plot insider trading and concealment for GPT-4 (32k) across seven versions of Apollo Research's prompt.

Usage:
    python analysis/plot_apollo_counts.py analysis/apollo_gpt4_32k_counts.csv figures/apollo_gpt4_32k.svg
"""
import csv
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

VERSIONS = [
    ("default", "Full pressure (original)"),
    ("pressure/No poor performance message", "Manager's shutdown message removed"),
    ("pressure/No failed low and medium-risk trades", "Failed searches for safer trades removed"),
    ("pressure/No economic downturn message", "Colleague's downturn warning removed"),
    ("pressure/No pressure", "All pressure removed"),
    ("countermeasures/Strongly discouraging", "Instructions strongly prohibit insider trading"),
    ("caught_likelihood/Very high risk", "Tip warns risk of getting caught is very high"),
]
TRADED, HID = "#2a78d6", "#eb6834"
SURFACE, INK, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e0"

rows = {r["variation"]: r for r in csv.DictReader(open(sys.argv[1]))}
labels = [label for _, label in VERSIONS]
traded = [int(rows[key]["traded_pct"]) for key, _ in VERSIONS]
hid = [int(rows[key]["hid_pct_of_traded"]) if rows[key]["hid_pct_of_traded"] else None for key, _ in VERSIONS]
traded_n = [f'{rows[key]["traded"]}/{rows[key]["runs"]}' for key, _ in VERSIONS]
hid_n = [f'{rows[key]["hid"]}/{rows[key]["traded"]}' for key, _ in VERSIONS]

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "svg.fonttype": "none"})
fig, ax = plt.subplots(figsize=(9, 5.2), facecolor=SURFACE)
ax.set_facecolor(SURFACE)
height = 0.36
for i, (t, h, tn, hn) in enumerate(zip(traded, hid, traded_n, hid_n)):
    y = len(labels) - 1 - i
    ax.barh(y + height / 2 + 0.02, t, height, color=TRADED, edgecolor=SURFACE, linewidth=0)
    ax.text(t + 1, y + height / 2 + 0.02, f"{t}%  ({tn})", va="center", color=MUTED, fontsize=9)
    if h is None:
        ax.text(1, y - height / 2 - 0.02, "no trades to hide", va="center", color=MUTED, fontsize=9, style="italic")
    else:
        ax.barh(y - height / 2 - 0.02, h, height, color=HID, edgecolor=SURFACE, linewidth=0)
        ax.text(h + 1, y - height / 2 - 0.02, f"{h}%  ({hn})", va="center", color=MUTED, fontsize=9)
ax.set_yticks(range(len(labels)))
ax.set_yticklabels(list(reversed(labels)), color=INK)
ax.set_xlim(0, 118)
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], color=MUTED)
ax.xaxis.grid(True, color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.tick_params(length=0)
from matplotlib.patches import Patch

fig.suptitle("GPT-4 (32k) in Apollo Research's insider trading scenario", x=0.01, ha="left", color=INK, fontsize=12)
fig.legend(handles=[Patch(color=TRADED, label="Made the insider trade (of 300 runs)"),
                    Patch(color=HID, label="Hid it from its manager (of runs that traded)")],
           loc="upper left", bbox_to_anchor=(0.005, 0.95), ncol=2, frameon=False, fontsize=9,
           handlelength=1, handleheight=1, labelcolor=INK)
fig.text(0.01, 0.01, "Source: our count of the labels in Apollo Research's public results (github.com/apolloresearch/insider-trading).",
         color=MUTED, fontsize=8)
fig.tight_layout(rect=(0, 0.03, 1, 0.93))
fig.savefig(sys.argv[2], facecolor=SURFACE)
