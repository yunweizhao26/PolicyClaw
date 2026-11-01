import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "figures"
OUT.mkdir(exist_ok=True)
D = json.load(open(HERE / "out/figures.json"))

mpl.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "Nimbus Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix", "font.size": 8.5, "axes.titlesize": 9, "axes.labelsize": 8.5,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "axes.spines.top": False, "axes.spines.right": False,
    "axes.linewidth": 0.6, "lines.linewidth": 1.4, "figure.dpi": 150, "savefig.dpi": 300, "pdf.fonttype": 42,
})
RED, GREEN, BLUE, GRAY = "#c23b22", "#2e7d32", "#1f78b4", "#777777"
ORANGE = "#d98e04"


def save(fig, name):
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"{name}.{ext}")
    plt.close(fig)
    print("wrote", OUT / f"{name}.png")


SMALL = {"font.size": 7, "axes.titlesize": 7.5, "axes.labelsize": 7, "xtick.labelsize": 6.5, "ytick.labelsize": 6.5, "lines.linewidth": 1.1}


def overview():
    a, b, d = (D["fig1"][k]["all"] for k in "abd")
    with mpl.rc_context(SMALL):
        fig = plt.figure(figsize=(3.33, 2.2), layout="constrained")
        fig.get_layout_engine().set(w_pad=0.02, h_pad=0.02, hspace=0.02, wspace=0.03)
        top, bottom = fig.subfigures(2, 1, height_ratios=[1.45, 1])
        ax_a, ax_b = top.subplots(1, 2)
        ax_c = bottom.subplots()

        n = np.array(a["rules_per_policy_sorted"])
        lg = np.log10(n)
        hist, edges = np.histogram(lg, bins=np.linspace(lg.min(), lg.max(), 28), density=True)
        ctr = (edges[:-1] + edges[1:]) / 2
        ax_a.fill_between(ctr, hist, color=RED, alpha=0.30, linewidth=0)
        ax_a.plot(ctr, hist, color=RED)
        ax_a.axvline(np.log10(a["median"]), color=GRAY, linestyle=":", linewidth=0.9)
        ax_a.text(0.03, 0.95, f"median\n{a['median']:.0f} rules", transform=ax_a.transAxes, fontsize=6.5, color="#444444", va="top", ha="left")
        ticks = [10, 100, 1000]
        ax_a.set_xticks(np.log10(ticks))
        ax_a.set_xticklabels(["10", "100", "1,000"])
        ax_a.set_xlabel("Rules (log scale)")
        ax_a.set_ylabel("Density")
        ax_a.set_title(f"(a) Rules per policy, n={len(n)}", loc="left")

        x = np.sort(b["overlap_candidates_per_policy_sorted"])
        cdf = np.arange(1, len(x) + 1) / len(x)
        ax_b.step(np.r_[0, x], np.r_[0, cdf] * 100, where="post", color=BLUE)
        ax_b.set_xscale("symlog", linthresh=10, linscale=0.6)
        ax_b.set_xlim(0, x.max() * 1.3)
        ax_b.set_xticks([0, 10, 100, 1000])
        ax_b.set_xticklabels(["0", "10", "100", "1,000"])
        ax_b.minorticks_off()
        ax_b.set_ylim(0, 102)
        ax_b.set_xlabel("Candidates per policy")
        ax_b.set_ylabel("Cumulative %")
        ax_b.set_title("(b) Overlap candidates", loc="left")

        bars = [("Untranslated condition text", d["guard_with_untranslated_quote_pct"], d["guard_with_untranslated_quote"]),
                ("Cited law, section, or document", d["rules_with_a_reference_pct"], d["rules_with_a_reference"]),
                ("Disclosure without a recipient", d["disclosure_without_recipient_pct_of_rules"], d["disclosure_without_recipient"])]
        for y, (lab, p, k) in enumerate(bars[::-1]):
            ax_c.barh(y, p, color=GREEN, alpha=0.8, height=0.6, edgecolor="white")
            ax_c.text(p + 0.5, y, f"{p:.1f}% ({k:,})", va="center", fontsize=6.5)
        ax_c.set_yticks(range(3))
        ax_c.set_yticklabels([b_[0] for b_ in bars[::-1]])
        ax_c.set_xlim(0, 40)
        ax_c.set_xlabel("Percentage of rules")
        ax_c.set_title(f"(c) Rule properties that leave ambiguity, n={d['rules']:,}", loc="left", x=-0.72)
        save(fig, "fig_overview")


def scaling():
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(2092 / 300, 712 / 300), constrained_layout=True)
    style = {"all": ("All 600 policies", None, 1.6, "o")}
    for s, (lab, col, lw, mk) in style.items():
        dec = D["fig2"][s]
        x = [e["rules_median"] for e in dec]
        for ax, key, c0 in ((ax_a, "pairs_per_policy", RED), (ax_b, "policies_with_pair_pct", BLUE)):
            ax.plot(x, [e[key] for e in dec], color=col or c0, linewidth=lw, marker=mk, markersize=4.5 if s == "all" else 3,
                    label=lab, zorder=3 if s == "all" else 2, linestyle="-" if s == "all" else "--")
    for ax in (ax_a, ax_b):
        ax.set_xscale("log")
        ax.set_xticks([30, 100, 300, 1000])
        ax.set_xticklabels(["30", "100", "300", "1,000"])
        ax.minorticks_off()
        ax.set_xlabel("Median number of rules in the size decile")
    ax_a.set_ylabel("Opposing pairs per policy")
    ax_a.set_title("(a) Opposing pairs vs. policy size")
    ax_b.set_ylabel("Percentage of policies with\nat least one opposing pair")
    ax_b.set_ylim(0, 105)
    ax_b.set_title("(b) Policies with a pair vs. policy size")
    save(fig, "fig_scaling")


if __name__ == "__main__":
    overview()
    scaling()
