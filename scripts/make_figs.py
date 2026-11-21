"""Figure generation for the aphantasia imaging audit manuscript."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["STIXGeneral", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 8.5,
        "axes.labelsize": 8.5,
        "axes.titlesize": 9,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "legend.fontsize": 7.5,
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
    }
)

INK = "#1a1a1a"
BLUE = "#2b5c8a"
GREY = "#8a8a8a"
LIGHT = "#c8c8c8"
ACCENT = "#a3452f"


def power_two_sample(d, n1, n2=None, alpha=0.05, two_sided=True):
    n2 = n1 if n2 is None else n2
    df = n1 + n2 - 2
    lam = d / np.sqrt(1.0 / n1 + 1.0 / n2)
    tc = stats.t.ppf(1 - alpha / 2, df) if two_sided else stats.t.ppf(1 - alpha, df)
    return stats.nct.sf(tc, df, lam)


def detectable_d(n1, n2=None, alpha=0.05, power=0.8, two_sided=True):
    n2 = n1 if n2 is None else n2
    lo, hi = 0.01, 6.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if power_two_sample(mid, n1, n2, alpha, two_sided) < power:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# ---------------------------------------------------------------- figure 1
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.7, 2.55))

ns = np.arange(4, 61)
for d, col, ls in ((0.5, GREY, ":"), (0.6, BLUE, "-"), (0.8, INK, "-")):
    ax1.plot(ns, [power_two_sample(d, n) for n in ns], ls, color=col, lw=1.1,
             label=fr"$d = {d}$")
ax1.axhline(0.8, color=LIGHT, lw=0.8, zorder=0)
ax1.text(5.5, 0.825, "80% power", ha="left", va="bottom", color=GREY, fontsize=7)

studies = [(10, 10, "Liu et al."), (14, 16, "Monzel et al."), (17, 17, "Wu & Yu"), (35, 35, "pooled")]
for n1, n2, lab in studies:
    n_eff = 2 / (1 / n1 + 1 / n2)
    ax1.axvline(n_eff, color=ACCENT, lw=0.55, ls=(0, (1, 2)), alpha=0.75, zorder=1)

ax1.set_xlim(4, 60)
ax1.set_ylim(0, 1.0)
ax1.set_xlabel("Participants per group")
ax1.set_ylabel("Power")
ax1.set_title("(a) Power to detect a given effect", loc="left")
ax1.legend(frameon=False, loc="lower right", handlelength=1.6, borderaxespad=0.35)


grid = np.arange(4, 61)
det = [detectable_d(n) for n in grid]
ax2.plot(grid, det, "-", color=INK, lw=1.2)
ax2.axhline(1.0, color=LIGHT, lw=0.8, zorder=0)
ax2.text(58, 1.03, r"$d = 1.0$", ha="right", va="bottom", color=GREY, fontsize=7)
ax2.axvspan(4, 18, color=ACCENT, alpha=0.06, lw=0)

marks = [(10, 10, "Liu\n10 vs 10", 1.32), (14, 16, "Monzel\n14 vs 16", 1.06),
         (17, 17, "Wu & Yu\n17 vs 17", 0.99), (35, 35, "pooled\n35 vs 35", 0.68)]
for n1, n2, lab, val in marks:
    n_eff = 2 / (1 / n1 + 1 / n2)
    ax2.plot([n_eff], [val], "o", ms=4.2, mfc="white", mec=ACCENT, mew=1.0, zorder=3)

ax2.annotate("Liu 10 vs 10\n1.32", xy=(10, 1.32), xytext=(11.5, 1.78), fontsize=6.6, color=ACCENT,
             arrowprops=dict(arrowstyle="-", lw=0.5, color=ACCENT, shrinkA=0, shrinkB=2))
ax2.annotate("Monzel 14 vs 16\n1.06", xy=(14.93, 1.06), xytext=(21.5, 1.46), fontsize=6.6, color=ACCENT,
             arrowprops=dict(arrowstyle="-", lw=0.5, color=ACCENT, shrinkA=0, shrinkB=2))
ax2.annotate("Wu & Yu 17 vs 17\n0.99", xy=(17, 0.99), xytext=(28, 1.12), fontsize=6.6, color=ACCENT,
             arrowprops=dict(arrowstyle="-", lw=0.5, color=ACCENT, shrinkA=0, shrinkB=2))
ax2.annotate("pooled 35 vs 35\n0.68", xy=(35, 0.68), xytext=(38.5, 0.88), fontsize=6.6, color=ACCENT,
             arrowprops=dict(arrowstyle="-", lw=0.5, color=ACCENT, shrinkA=0, shrinkB=2))

ax2.set_xlim(4, 60)
ax2.set_ylim(0.5, 2.0)
ax2.set_xlabel("Participants per group")
ax2.set_ylabel("Smallest detectable effect ($d$)")
ax2.set_title("(b) Effect size detectable at 80% power", loc="left")

fig.tight_layout()
fig.savefig("figs/fig1_power.pdf")
fig.savefig("figs/fig1_power.png", dpi=220)
plt.close(fig)

# ---------------------------------------------------------------- figure 2
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.7, 2.5))

patterns = [
    ("Reports the aphantasia–control null", 0),
    ("States hyperphantasia comparison\nthroughout", 4),
    ("States it once, then drops it", 2),
    ("Omits the comparison group", 4),
    ("States it wrongly", 0),
]
ypos = np.arange(len(patterns))[::-1]
vals = [p[1] for p in patterns]
bars = ax1.barh(ypos, vals, height=0.62, color=[GREY, BLUE, BLUE, BLUE, GREY], alpha=0.9)
for y, v in zip(ypos, vals):
    ax1.text(v + 0.12, y, str(v), va="center", fontsize=7.5, color=INK)
ax1.set_yticks(ypos)
ax1.set_yticklabels([p[0] for p in patterns], fontsize=6.9)
ax1.set_xlim(0, 5.2)
ax1.set_xlabel("Sources (of 10 citing Milton et al. for connectivity)")
ax1.set_title("(a) How the comparison group is reported", loc="left")
ax1.tick_params(axis="y", length=0)

features = [
    ("Causal or mechanistic wording", 9, 15),
    ("Cites Fulford et al. for connectivity", 4, 11),
    ("Labels the effect ``frontoparietal''", 6, 10),
    ("Gives the sample size", 2, 10),
    ("Reports the null result", 0, 10),
]
ypos2 = np.arange(len(features))[::-1]
props = [f[1] / f[2] for f in features]
ax2.barh(ypos2, [1] * len(features), height=0.62, color="#eeeeee", edgecolor="none")
ax2.barh(ypos2, props, height=0.62, color=ACCENT, alpha=0.85)
for y, f in zip(ypos2, features):
    ax2.text(1.03, y, f"{f[1]}/{f[2]}", va="center", fontsize=7, color=INK)
ax2.set_yticks(ypos2)
ax2.set_yticklabels([f[0] for f in features], fontsize=6.9)
ax2.set_xlim(0, 1.0)
ax2.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax2.set_xticklabels(["0", "25", "50", "75", "100%"])
ax2.set_xlabel("Proportion of scholarly sources")
ax2.set_title("(b) Secondary features of the citing passages", loc="left")
ax2.tick_params(axis="y", length=0)

fig.tight_layout()
fig.savefig("figs/fig2_citation.pdf")
fig.savefig("figs/fig2_citation.png", dpi=220)
plt.close(fig)

# report the numbers the manuscript will quote
print("detectable d (two-sided, 80% power):")
for n1, n2 in ((10, 10), (14, 16), (17, 17), (35, 35)):
    print(f"  {n1} vs {n2}: smallest d = {detectable_d(n1, n2):.2f} | "
          f"power at d=0.5: {power_two_sample(0.5, n1, n2):.2f} | "
          f"at d=0.8: {power_two_sample(0.8, n1, n2):.2f}")
print("power at d=0.5, one-sided n=14 vs 16:", round(power_two_sample(0.5, 14, 16, two_sided=False), 2))
print("figures written")
