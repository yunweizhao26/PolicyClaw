import sys
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1])
mpl.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "Nimbus Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix", "font.size": 8, "axes.titlesize": 8.5, "axes.labelsize": 8,
    "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.6,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "savefig.dpi": 300, "pdf.fonttype": 42,
})
RED, GREEN, BLUE, ORANGE, INK = "#c23b22", "#2e7d32", "#1f78b4", "#d98e04", "#333333"
KS = [8, 16, 32, 64, 128]
QUERIES = {"exclusion": "-", "implication": "--"}


def rows():
    lines = (HERE / "RESULTS_RQ3.md").read_text().splitlines()
    joins, batch, section = {}, {}, None
    for line in lines:
        if line in ("batch", "single_LOW", "single_HIGH"):
            section = line
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) == 13 and cells[0] in ("LOW", "HIGH"):
            joins[cells[0], cells[1]] = {"rec": float(cells[6]), "full": float(cells[9]), "sec": float(cells[11]), "solver": float(cells[12])}
        if section == "batch" and len(cells) == 8 and cells[0].endswith("/128"):
            batch[cells[0].split("/")[0]] = {"rec": float(cells[4]), "full": float(cells[6]), "sec": float(cells[7]) / 16}
    return joins, batch


def series(joins, level, query, key):
    return [joins[level, f"{query}/{k}"][key] for k in KS]


def label(ax, x, y, text, **kw):
    ax.annotate(text, (x, y), textcoords="offset points", fontsize=7, color=INK, **kw)


def main():
    joins, batch = rows()
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 1.85))
    fig.subplots_adjust(left=0.075, right=0.99, top=0.75, bottom=0.21, wspace=0.36)
    panels = (("rec", "(a) Share of answers found", "Recall (%)"),
              ("full", "(b) Whole set right", "Queries (%)"),
              ("sec", "(c) Latency per query", "Seconds (log scale)"))
    for ax, (key, title, ylabel) in zip(axes, panels):
        for query, style in QUERIES.items():
            ax.plot(KS, series(joins, "LOW", query, key), style, color=RED, marker="o", ms=3.5, lw=1.3)
            ax.plot(KS, series(joins, "HIGH", query, key), style, color=BLUE, marker="s", ms=3.2, lw=1.3)
            if key == "sec":
                ax.plot(KS, series(joins, "LOW", query, "solver"), style, color=GREEN, marker="^", ms=3.5, lw=1.3)
            ax.plot([128], [batch[query][key]], marker="D", ms=4, color=ORANGE, mec="white", mew=0.5, ls="none", zorder=5)
        if key != "sec":
            ax.plot(KS, [100] * len(KS), color=GREEN, marker="^", ms=3.5, lw=1.0, zorder=1)
        ax.set_xscale("log", base=2)
        ax.set_xticks(KS, [str(k) for k in KS])
        ax.minorticks_off()
        ax.set_xlim(7, 250)
        ax.set_xlabel("Guards in the join, $k$")
        ax.set_ylabel(ylabel)
        ax.set_title(title, loc="left", pad=3)
        ax.grid(axis="y", color="#dddddd", lw=0.5)
        ax.set_axisbelow(True)
    a, b, c = axes
    a.set_ylim(50, 103)
    b.set_ylim(0, 104)
    c.set_yscale("log")
    c.set_ylim(0.015, 900)
    c.set_yticks([0.1, 1, 10, 100], ["0.1", "1", "10", "100"])
    g = lambda level, query, key: joins[level, f"{query}/128"][key]
    label(a, 128, g("LOW", "exclusion", "rec"), f"{g('LOW', 'exclusion', 'rec'):.1f}", xytext=(4, 2))
    label(a, 128, g("LOW", "implication", "rec"), f"{g('LOW', 'implication', 'rec'):.1f}", xytext=(4, -6))
    label(b, 128, g("LOW", "exclusion", "full"), f"{g('LOW', 'exclusion', 'full'):.1f}", xytext=(4, 1))
    label(b, 128, g("LOW", "implication", "full"), f"{g('LOW', 'implication', 'full'):.1f}", xytext=(5, -1))
    a.text(0.03, 0.05, "Solver, high thinking, and\nsplit plan: 98 to 100", transform=a.transAxes, fontsize=7, color=INK, va="bottom")
    label(b, 128, g("HIGH", "exclusion", "full"), f"{g('HIGH', 'exclusion', 'full'):.1f}", xytext=(4, 1))
    label(b, 128, g("HIGH", "implication", "full"), f"{g('HIGH', 'implication', 'full'):.1f}", xytext=(4, -7))
    label(b, 128, batch["implication"]["full"], f"{batch['implication']['full']:.1f}", xytext=(4, 1))
    label(b, 128, batch["exclusion"]["full"], f"{batch['exclusion']['full']:.1f}", xytext=(4, -7))
    label(c, 128, g("HIGH", "exclusion", "sec"), f"{g('HIGH', 'exclusion', 'sec'):.0f}", xytext=(4, 0))
    label(c, 128, batch["exclusion"]["sec"], f"{batch['exclusion']['sec']:.0f}", xytext=(4, -2))
    label(c, 128, g("LOW", "exclusion", "sec"), f"{g('LOW', 'exclusion', 'sec'):.0f}", xytext=(4, -3))
    label(c, 128, joins["LOW", "implication/128"]["solver"], f"{joins['LOW', 'implication/128']['solver']:.1f}", xytext=(4, 0))
    label(c, 128, joins["LOW", "exclusion/128"]["solver"], f"{joins['LOW', 'exclusion/128']['solver']:.1f}", xytext=(4, -6))
    handles = [Line2D([], [], color=GREEN, marker="^", ms=3.5, lw=1.3, label="Solver"),
               Line2D([], [], color=BLUE, marker="s", ms=3.2, lw=1.3, label="One high-thinking call"),
               Line2D([], [], color=RED, marker="o", ms=3.5, lw=1.3, label="One low-thinking call"),
               Line2D([], [], color=ORANGE, marker="D", ms=4, ls="none", label="Split plan"),
               Line2D([], [], color=INK, ls="-", lw=1.3, label="Exclusion join"),
               Line2D([], [], color=INK, ls="--", lw=1.3, label="Implication join")]
    fig.legend(handles=handles, loc="upper center", ncol=6, frameon=False, fontsize=7, handlelength=1.8, handletextpad=0.4, columnspacing=0.8, borderaxespad=0.1)
    fig.savefig(OUT / "fig_join.pdf")
    fig.savefig(OUT / "fig_join.png")


if __name__ == "__main__":
    main()
