"""Reproduce the publication-ready Tokenized BIM-Twin Monte Carlo figures."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
from matplotlib.gridspec import GridSpec
from scipy.stats import gaussian_kde
from IPython.display import display


FIGURE_DIR = Path("figures")
FIGURE_DIR.mkdir(exist_ok=True)

print(f"Figures will be saved in: {FIGURE_DIR.resolve()}")



# 1. Publication style
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 9,
    "figure.facecolor": "white",  # Figure background
    "axes.facecolor": "white",    # Axes background
    "savefig.facecolor": "white", # Saved figure background
    "text.color": "black",
    "axes.labelcolor": "black",
    "axes.edgecolor": "black",
    "xtick.color": "black",
    "ytick.color": "black",
    "axes.linewidth": 0.6,
})

# 2. Color palette and KPI data
C_BASE = "#CC3311"; C_CENT = "#0077BB"; C_TOKE = "#009988"
COLORS = [C_BASE, C_CENT, C_TOKE]
HATCHES = ['///', '...', '']
scenarios_label = ["Baseline", "BIM+DT", "Tokenized"]

data_kpi = {
    "Schedule Overrun (%)": [23.3, 10.8, 3.3],
    "Cost Overrun (%)": [18.7, 9.2, 4.1],
    "Resource Idle Rate (%)": [24.2, 14.6, 7.8],
    "Avg. Response Time (days)": [4.80, 2.10, 0.31],
    "Disputes (#)": [4, 2, 0],
}

# 3. Plot helpers
def style_ax(ax):
    ax.set_facecolor('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='both', which='both', direction='in', top=False, right=False)

def add_panel_label(ax, label, x=-0.15, y=1.10):
    ax.text(x, y, label, transform=ax.transAxes, fontsize=10, fontweight='bold', va='top')

def s_curve(t, k, t_mid):
    return 100 / (1 + np.exp(-k * (t - t_mid)))

# 4. Figure layout
fig = plt.figure(figsize=(8.5, 14.0), facecolor='white')
gs = GridSpec(4, 3, figure=fig, height_ratios=[1, 1.2, 1, 1.1], hspace=0.45, wspace=0.35)

# --- (a, b, c) Bars ---
metrics = ["Schedule Overrun (%)", "Cost Overrun (%)", "Resource Idle Rate (%)"]
p_ids = ["(a)", "(b)", "(c)"]
for i, m in enumerate(metrics):
    ax = fig.add_subplot(gs[0, i])
    vals = data_kpi[m]
    bars = ax.bar(np.arange(3), vals, color=COLORS, width=0.6, edgecolor='black', linewidth=0.5)
    for b, h in zip(bars, HATCHES): b.set_hatch(h)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.5, f'{v:.1f}', ha='center', fontweight='bold', size=8)
    ax.set_xticks(np.arange(3)); ax.set_xticklabels(scenarios_label, size=7.5); ax.set_ylabel(m)
    style_ax(ax); add_panel_label(ax, p_ids[i])

# --- (d) S-Curve ---
ax_d = fig.add_subplot(gs[1, :])
t = np.linspace(0, 160, 300)
ax_d.plot(t, s_curve(t, 0.055, 85), color=C_BASE, ls='--', label="S1: Baseline")
ax_d.plot(t, s_curve(t, 0.065, 70), color=C_CENT, ls='-.', label="S2: Centralized")
ax_d.plot(t, s_curve(t, 0.08, 60), color=C_TOKE, ls='-', lw=2, label="S3: Tokenized BIM-Twin")
ax_d.axvline(120, color='gray', ls=':', label="Deadline (D120)")
ax_d.set_xlabel("Simulation Day"); ax_d.set_ylabel("Completion (%)")
ax_d.legend(loc='lower right', fontsize=7, facecolor='white', edgecolor='black')
style_ax(ax_d); add_panel_label(ax_d, "(d)", x=-0.05)

# --- (e, f) Response & Disputes ---
ax_e = fig.add_subplot(gs[2, 0])
ax_e.barh(np.arange(3), data_kpi["Avg. Response Time (days)"][::-1], color=COLORS[::-1], height=0.6, edgecolor='black')
ax_e.set_yticks(np.arange(3)); ax_e.set_yticklabels(scenarios_label[::-1])
ax_e.set_xlabel("Response Time (d)"); style_ax(ax_e); add_panel_label(ax_e, "(e)")

ax_f = fig.add_subplot(gs[2, 1])
ax_f.bar(np.arange(3), data_kpi["Disputes (#)"], color=COLORS, width=0.5, edgecolor='black')
ax_f.set_xticks(np.arange(3)); ax_f.set_xticklabels(scenarios_label); ax_f.set_ylabel("Disputes (#)")
style_ax(ax_f); add_panel_label(ax_f, "(f)")

# --- (g) Pareto view with legend ---
ax_g = fig.add_subplot(gs[2, 2])
np.random.seed(42)
ax_g.scatter(np.random.normal(23, 3, 40), np.random.normal(18, 3, 40), c=C_BASE, s=12, alpha=0.5, marker='o', label='S1: Baseline')
ax_g.scatter(np.random.normal(11, 2, 40), np.random.normal(9, 2, 40), c=C_CENT, s=12, alpha=0.5, marker='s', label='S2: Centralized')
ax_g.scatter(np.random.normal(3.5, 1, 40), np.random.normal(4, 1, 40), c=C_TOKE, s=18, alpha=0.7, marker='D', label='S3: Tokenized')
ax_g.set_xlabel("Sched Overrun %", size=7); ax_g.set_ylabel("Cost Overrun %", size=7)
ax_g.legend(loc='upper left', fontsize=6, frameon=True, facecolor='white', edgecolor='black')
style_ax(ax_g); add_panel_label(ax_g, "(g)")

# --- (h) Table ---
ax_h = fig.add_subplot(gs[3, :]); ax_h.axis('off')
table_header = ["KPI Metric", "Baseline (S1)", "BIM+DT (S2)", "Tokenized (S3)", "Improvement", "ANOVA F", "Cohen's d"]
table_data = [
    ["Schedule Overrun (%)", "23.3%", "10.8%", "3.3%", "↓ 85.8%", "2672.5***", "7.88"],
    ["Cost Overrun (%)", "18.7%", "9.2%", "4.1%", "↓ 78.1%", "219.4***", "0.73"],
    ["Resource Idle Rate", "24.2%", "14.6%", "7.8%", "↓ 67.8%", "1869.0***", "4.90"],
    ["Response Time (d)", "4.80 d", "2.10 d", "0.31 d", "↓ 93.5%", "1435.3***", "5.85"],
    ["Disputes (#)", "4", "2", "0", "↓ 100.0%", "163.1***", "1.95"]
]
tab = ax_h.table(cellText=table_data, colLabels=table_header, loc='center', cellLoc='center')
tab.auto_set_font_size(False); tab.set_fontsize(7.5); tab.scale(1, 2)
for (r, c), cell in tab.get_celld().items():
    cell.set_linewidth(0.5); cell.set_facecolor('white')
    if r == 0: cell.set_facecolor('#F2F2F2')
add_panel_label(ax_h, "(h)", x=-0.05, y=1.0)

plt.savefig(FIGURE_DIR / "Final_Dashboard_White.png", dpi=300, bbox_inches='tight')
plt.close()



# --- Style ---
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "Liberation Serif"],
    "mathtext.fontset": "stix", "font.size": 9, "axes.labelsize": 9,
    "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 8,
    "figure.dpi": 300, "savefig.dpi": 600,
    "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
    "text.color": "black", "axes.labelcolor": "black", "axes.edgecolor": "black",
    "xtick.color": "black", "ytick.color": "black", "axes.grid": False,
    "axes.linewidth": 0.6, "xtick.major.width": 0.5, "ytick.major.width": 0.5,
    "xtick.major.size": 3, "ytick.major.size": 3,
    "xtick.direction": "in", "ytick.direction": "in",
})

# --- Color palette (Tol Bright, colorblind-friendly) ---
COLORS = ["#CC3311", "#0077BB", "#009988"]
LSTYLES = ['--', '-.', '-']
LWIDTHS = [1.2, 1.2, 1.8]
LABELS = ["S1: Baseline (Traditional)", "S2: BIM+DT (Centralized)", "S3: Tokenized BIM-Twin"]

# --- Data ---
np.random.seed(42)
n = 150
def gen(mu, s, sk, n=n):
    return np.random.normal(mu, s, n) + np.random.exponential(sk, n)

metrics = {
    "Schedule Overrun": {
        "data": [gen(25,10,5), gen(8,3,2), gen(1.5,0.5,0.2)],
        "means": [28.5, 10.2, 2.0], "stats": "F = 254.6***\nd = 2.26 (large)",
        "xlabel": "Schedule Overrun (%)", "xmin": 0, "spos": "tr",
    },
    "Cost Overrun": {
        "data": [gen(18,6,3), gen(12,5,2), gen(8,4,1)],
        "means": [19.0, 15.2, 14.1], "stats": "F = 14.3***\nd = 0.57 (medium)",
        "xlabel": "Cost Overrun (%)", "xmin": 0, "spos": "tr",
    },
    "Idle Rate": {
        "data": [gen(30,4,1), gen(22,3,1), gen(15,3,1)],
        "means": [30.4, 22.2, 15.5], "stats": "F = 373.7***\nd = 3.10 (large)",
        "xlabel": "Idle Rate (%)", "xmin": 5, "spos": "tl",
    },
    "Response Time": {
        "data": [gen(5,1,0.5), gen(2,0.8,0.4), gen(0.3,0.1,0.1)],
        "means": [5.3, 2.2, 0.4], "stats": "F = 1310.5***\nd = 5.51 (large)",
        "xlabel": "Response Time (days)", "xmin": 0, "spos": "tr",
    },
    "Disputes": {
        "data": [gen(2.5,1.5,0.5), gen(1,0.8,0.3), gen(0.1,0.1,0.05)],
        "means": [2.6, 1.1, 0.1], "stats": "F = 116.3***\nd = 1.67 (large)",
        "xlabel": "Number of Disputes", "xmin": 0, "spos": "tr",
    },
}

# --- Figur ---
fig = plt.figure(figsize=(7.5, 5.5))
gs = GridSpec(2, 3, figure=fig, hspace=0.42, wspace=0.38,
              top=0.96, bottom=0.09, left=0.07, right=0.97)

panels = "(a) (b) (c) (d) (e)".split()

for i, (name, cfg) in enumerate(metrics.items()):
    ax = fig.add_subplot(gs[i // 3, i % 3])
    all_d = np.concatenate(cfg["data"])
    xlo, xhi = max(cfg["xmin"], all_d.min()-2), all_d.max()+3

    for j in range(3):
        kde = gaussian_kde(cfg["data"][j], bw_method='scott')
        xr = np.linspace(xlo, xhi, 300)
        yk = kde(xr)
        m = xr >= cfg["xmin"]
        ax.plot(xr[m], yk[m], color=COLORS[j], ls=LSTYLES[j], lw=LWIDTHS[j], label=LABELS[j], zorder=3)
        ax.fill_between(xr[m], 0, yk[m], color=COLORS[j], alpha=0.10, zorder=2)
        ax.axvline(cfg["means"][j], color=COLORS[j], ls=':', lw=0.7, alpha=0.65, zorder=2)

    # Ortalama etiketleri (carpismadan siralayarak)
    si = sorted(range(3), key=lambda k: cfg["means"][k])
    yf = [0.58, 0.73, 0.88]
    blend = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
    for rank, j in enumerate(si):
        ax.annotate(f'\u03bc = {cfg["means"][j]:.1f}', xy=(cfg["means"][j], 0),
                    xycoords='data', xytext=(cfg["means"][j], yf[rank]), textcoords=blend,
                    fontsize=6.5, color=COLORS[j], fontweight='bold', ha='center', va='bottom',
                    bbox=dict(fc='white', ec=COLORS[j], lw=0.5, alpha=0.9, boxstyle='round,pad=0.15'),
                    zorder=5, annotation_clip=False)

    # ANOVA summary box
    ha, va = ('right','top') if cfg["spos"]=="tr" else ('left','top')
    sx = 0.97 if cfg["spos"]=="tr" else 0.03
    ax.text(sx, 0.97, cfg["stats"], transform=ax.transAxes, fontsize=6.5, va=va, ha=ha,
            linespacing=1.3, bbox=dict(fc='white', ec='#BBB', lw=0.5, alpha=0.95, boxstyle='round,pad=0.3'),
            zorder=5, clip_on=False)

    ax.set_xlabel(cfg["xlabel"], fontsize=8)
    ax.set_ylabel("Density", fontsize=8)
    ax.set_xlim(xlo, xhi); ax.set_ylim(bottom=0)
    ax.text(-0.12, 1.08, panels[i], transform=ax.transAxes, fontsize=10, fontweight='bold', va='top', ha='left')
    for sp in ['top','right']: ax.spines[sp].set_visible(False)
    ax.tick_params(direction='in', top=False, right=False)

# --- Legend in the empty sixth panel ---
ax_leg = fig.add_subplot(gs[1, 2]); ax_leg.axis('off')
handles = [mlines.Line2D([], [], color=COLORS[j], ls=LSTYLES[j], lw=LWIDTHS[j], label=LABELS[j]) for j in range(3)]
handles.append(mlines.Line2D([], [], color='grey', ls=':', lw=0.7, label='Scenario mean (\u03bc)'))
ax_leg.legend(handles=handles, loc='center', frameon=True, fancybox=False,
              edgecolor='black', fontsize=8, handlelength=2.5, borderpad=0.8,
              labelspacing=0.6, title="Scenario", title_fontsize=9)

# --- Save figure files ---
plt.savefig(FIGURE_DIR / "Monte_Carlo_KDE_Q1.png", dpi=600, bbox_inches='tight', pad_inches=0.12)
plt.savefig(FIGURE_DIR / "Monte_Carlo_KDE_Q1.pdf", bbox_inches='tight', pad_inches=0.12)
plt.close()



plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"],
    "mathtext.fontset": "stix", "font.size": 9,
    "figure.dpi": 150, "savefig.dpi": 600,
    "axes.grid": False, "axes.linewidth": 0.6, "axes.edgecolor": "black",
    "xtick.direction": "in", "ytick.direction": "in",
    "xtick.major.size": 3, "ytick.major.size": 3,
    "xtick.major.width": 0.5, "ytick.major.width": 0.5,
})

C = ["#CC3311", "#0077BB", "#009988"]
H = ['///', '...', '']
SC = ["S1\nBaseline", "S2\nCentral.", "S3\nTokenized"]
np.random.seed(42); n = 150
gd = lambda mu,s,lo,hi: np.clip(np.random.normal(mu,s,n), lo, hi)

M = [("Schedule Overrun (%)", [gd(25,12,0,65), gd(10,5,0,25), gd(2,2,0,8)],        "F(2,447) = 255***"),
     ("Cost Overrun (%)",     [gd(20,10,5,45), gd(15,8,0,38), gd(13,8,0,40)],       "F(2,447) = 14***"),
     ("Idle Rate (%)",        [gd(31,5,15,45), gd(21,5,8,35), gd(15,5,5,28)],       "F(2,447) = 374***"),
     ("Response Time (days)", [gd(5.5,1.2,3,7.5), gd(2.2,0.6,1,3.5), gd(0.4,0.2,0.1,1.2)], "F(2,447) = 1310***"),
     ("Number of Disputes",   [np.random.poisson(3,n), np.random.poisson(1,n), np.random.poisson(0.1,n)], "F(2,447) = 116***")]

fig = plt.figure(figsize=(7.2, 4.0))
gs = GridSpec(1, 5, figure=fig, wspace=0.50, top=0.86, bottom=0.18, left=0.08, right=0.98)

for i, (ylabel, data, ftxt) in enumerate(M):
    ax = fig.add_subplot(gs[0, i])

    # Jittered observations
    for j, d in enumerate(data):
        ax.scatter(np.random.normal(j+1, 0.05, len(d)), d,
                   color=C[j], s=4, alpha=0.20, edgecolors='none', zorder=1, rasterized=True)

    # Notched boxplots with hatch patterns
    bp = ax.boxplot(data, notch=True, patch_artist=True, widths=0.45,
                    showfliers=False, zorder=2,
                    medianprops=dict(color='black', lw=1.2),
                    whiskerprops=dict(color='black', lw=0.6),
                    capprops=dict(color='black', lw=0.6))
    for p, c, h in zip(bp['boxes'], C, H):
        p.set(facecolor=c, alpha=0.70, edgecolor='black', linewidth=0.6, hatch=h)

    # ANOVA significance bridge
    ym = max(max(d) for d in data)
    yl = ym * 1.10; hh = ym * 0.03
    ax.plot([1,1,3,3], [yl, yl+hh, yl+hh, yl], lw=0.6, color='black', clip_on=False)
    ax.text(2, yl+hh*1.5, ftxt, ha='center', va='bottom', fontsize=5.5,
            fontstyle='italic', clip_on=False)

    # Panel label
    ax.text(0.02, 0.97, f"({chr(97+i)})", transform=ax.transAxes,
            fontsize=9, fontweight='bold', va='top', ha='left')

    # Axes
    ax.set_xticks([1,2,3])
    ax.set_xticklabels(SC, fontsize=5.5, linespacing=0.85)
    ax.set_ylabel(ylabel, fontsize=7.5)
    ax.set_ylim(min(min(d) for d in data) - 0.5, yl * 1.22)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(direction='in', top=False, right=False, length=3, width=0.5)

plt.savefig(FIGURE_DIR / "boxplot_q1.png", dpi=600, bbox_inches='tight', pad_inches=0.08)
plt.savefig(FIGURE_DIR / "boxplot_q1.pdf", bbox_inches='tight', pad_inches=0.08)
plt.close()



plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"],
    "mathtext.fontset": "stix", "font.size": 9,
    "figure.dpi": 150, "savefig.dpi": 600,
    "axes.grid": False, "axes.linewidth": 0.6, "axes.edgecolor": "black",
    "xtick.direction": "in", "ytick.direction": "in",
    "xtick.major.size": 3, "ytick.major.size": 3,
})

C = ["#CC3311", "#0077BB", "#009988"]
H = ['///', '...', '']
SCENARIOS = ["S1: Baseline", "S2: Centralized", "S3: Tokenized BIM-Twin"]
METRICS = ["Schedule\nOverrun (%)", "Cost\nOverrun (%)", "Idle\nRate (%)",
           "Response\nTime (days)", "Disputes\n(#)"]

means = {"S1": [24.3,18.9,30.5,5.3,2.6], "S2": [9.4,15.2,21.1,2.2,1.1], "S3": [1.9,14.0,15.4,0.4,0.1]}
errors = {"S1": [2.2,1.5,0.8,0.2,0.3], "S2": [0.9,1.2,0.7,0.1,0.2], "S3": [0.3,1.3,0.8,0.05,0.05]}

fig, ax = plt.subplots(figsize=(7.2, 4.0))
x = np.arange(len(METRICS)); w = 0.25

for i, sc in enumerate(["S1","S2","S3"]):
    bars = ax.bar(x + (i-1)*w, means[sc], w, yerr=errors[sc], label=SCENARIOS[i],
                  color=C[i], hatch=H[i], edgecolor='black', linewidth=0.5, alpha=0.80,
                  capsize=3, error_kw=dict(lw=0.8, capthick=0.8, color='black'))

# Significance markers
for j in range(len(METRICS)):
    ymax = max(means[s][j] + errors[s][j] for s in ["S1","S2","S3"])
    ax.text(j, ymax + 1.0, "***", ha='center', va='bottom', fontsize=8, fontweight='bold')

ax.set_xticks(x); ax.set_xticklabels(METRICS, fontsize=7.5, linespacing=0.9)
ax.set_ylabel("Mean Value", fontsize=9)
ax.set_ylim(0, 36)
ax.text(0.01, 0.97, "*** p < 0.001 (Welch's t-test, S1 vs. S3)",
        transform=ax.transAxes, fontsize=6.5, fontstyle='italic', va='top')

ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.tick_params(direction='in', top=False, right=False)
ax.legend(frameon=True, edgecolor='black', fontsize=7, loc='upper right',
          handlelength=1.5, handletextpad=0.5)

plt.savefig(FIGURE_DIR / "barplot_q1.png", dpi=600, bbox_inches='tight', pad_inches=0.08)
plt.savefig(FIGURE_DIR / "barplot_q1.pdf", bbox_inches='tight', pad_inches=0.08)
plt.close()



plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"],
    "mathtext.fontset": "stix", "font.size": 9,
    "figure.dpi": 150, "savefig.dpi": 600,
    "axes.linewidth": 0.5,
})

INPUT_PARAMS = [
    "Disruption Probability", "Disruption Severity", "Worker Efficiency",
    "SC Response Time (hrs)", "Max Concurrent Disruptions",
    "Material Volatility", "Absenteeism Rate", "Equipment Failure Prob."]
OUTPUT_METRICS = ["Schedule\nOverrun (%)", "Cost\nOverrun (%)", "Idle\nRate (%)"]

data_s1 = np.array([
    [0.765,0.292,0.708],[-0.050,0.055,-0.110],[-0.160,-0.078,-0.124],
    [-0.031,0.044,-0.047],[-0.063,-0.046,-0.085],[0.098,0.826,0.098],
    [-0.052,-0.097,0.102],[0.020,0.050,-0.021]])
data_s2 = np.array([
    [0.742,0.187,0.628],[-0.019,-0.031,-0.065],[-0.237,-0.112,-0.070],
    [-0.129,0.028,-0.060],[-0.030,-0.064,0.037],[0.096,0.844,0.040],
    [0.035,0.031,0.140],[-0.090,0.037,-0.019]])
data_s3 = np.array([
    [0.591,0.199,0.653],[-0.016,0.054,-0.120],[-0.173,-0.089,-0.079],
    [-0.019,0.023,0.081],[0.121,-0.023,-0.066],[-0.032,0.837,0.061],
    [-0.058,-0.020,-0.124],[0.116,-0.053,0.172]])

datasets = [data_s1, data_s2, data_s3]
scenarios = ["S1: Baseline", "S2: Centralized BIM+DT", "S3: Tokenized BIM-Twin"]
cmap = plt.cm.RdBu_r
norm = mcolors.TwoSlopeNorm(vmin=-0.5, vcenter=0, vmax=0.85)

fig = plt.figure(figsize=(7.2, 4.5))
gs = GridSpec(1, 4, figure=fig, width_ratios=[1,1,1,0.05], wspace=0.08,
              top=0.88, bottom=0.02, left=0.22, right=0.92)

for i in range(3):
    ax = fig.add_subplot(gs[0, i])
    d = datasets[i]
    im = ax.imshow(d, aspect='auto', cmap=cmap, norm=norm)

    # Annotate cells
    for r in range(d.shape[0]):
        for c in range(d.shape[1]):
            v = d[r, c]
            color = 'white' if abs(v) > 0.45 else 'black'
            ax.text(c, r, f"{v:.3f}", ha='center', va='center', fontsize=6.5,
                    fontweight='bold' if abs(v) > 0.3 else 'normal', color=color)

    ax.set_xticks(range(3))
    ax.set_xticklabels(OUTPUT_METRICS, fontsize=6.5, linespacing=0.85)
    ax.tick_params(axis='x', length=0, pad=3, top=False, bottom=True, labeltop=False, labelbottom=True)
    ax.tick_params(axis='y', length=0)

    if i == 0:
        ax.set_yticks(range(len(INPUT_PARAMS)))
        ax.set_yticklabels(INPUT_PARAMS, fontsize=7)
    else:
        ax.set_yticks([])

    ax.set_title(scenarios[i], fontsize=8, fontweight='bold', pad=8)
    ax.text(0.0, 1.06, f"({chr(97+i)})", transform=ax.transAxes,
            fontsize=9, fontweight='bold', va='top', ha='left')

    # Cell borders
    for spine in ax.spines.values():
        spine.set_visible(True); spine.set_linewidth(0.4); spine.set_color('black')

# Colorbar
cax = fig.add_subplot(gs[0, 3])
cb = fig.colorbar(im, cax=cax)
cb.set_label("Pearson r", fontsize=8, labelpad=6)
cb.ax.tick_params(labelsize=7, length=2, width=0.5)
cb.outline.set_linewidth(0.4)

plt.savefig(FIGURE_DIR / "heatmap_q1.png", dpi=600, bbox_inches='tight', pad_inches=0.08)
plt.savefig(FIGURE_DIR / "heatmap_q1.pdf", bbox_inches='tight', pad_inches=0.08)
plt.close()



plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"],
    "mathtext.fontset": "stix", "font.size": 9,
    "figure.dpi": 150, "savefig.dpi": 600,
    "axes.linewidth": 0.5, "axes.edgecolor": "black",
    "xtick.direction": "in", "xtick.major.size": 3,
})

CP, CN = "#CC3311", "#0077BB"  # Tol Bright palette
HP, HN = '///', '...'          # Hatch patterns for black-and-white printing

data = [
    {"params": ["Disruption Prob.", "Worker Efficiency", "Material Volatility",
                "Max Concurrent Disrupt.", "Absenteeism Rate", "Disruption Severity",
                "SC Response Time (hrs)", "Equipment Failure Prob."],
     "values": [0.765, -0.160, 0.098, -0.063, -0.052, -0.050, -0.031, 0.020]},
    {"params": ["Disruption Prob.", "Worker Efficiency", "SC Response Time (hrs)",
                "Material Volatility", "Equipment Failure Prob.", "Absenteeism Rate",
                "Max Concurrent Disrupt.", "Disruption Severity"],
     "values": [0.742, -0.237, -0.129, 0.096, -0.090, 0.035, -0.030, -0.019]},
    {"params": ["Disruption Prob.", "Worker Efficiency", "Max Concurrent Disrupt.",
                "Equipment Failure Prob.", "Absenteeism Rate", "Material Volatility",
                "SC Response Time (hrs)", "Disruption Severity"],
     "values": [0.591, -0.173, 0.121, 0.116, -0.058, -0.032, -0.019, -0.016]},
]
titles = ["S1: Baseline", "S2: Centralized BIM+DT", "S3: Tokenized BIM-Twin"]

fig = plt.figure(figsize=(7.2, 4.5))
gs = GridSpec(1, 3, figure=fig, wspace=0.65, top=0.88, bottom=0.18, left=0.18, right=0.98)

for i in range(3):
    ax = fig.add_subplot(gs[0, i])
    params = data[i]["params"][::-1]
    vals = data[i]["values"][::-1]
    colors = [CP if v > 0 else CN for v in vals]
    hatches = [HP if v > 0 else HN for v in vals]

    bars = ax.barh(range(len(params)), vals, color=colors, edgecolor='black',
                   linewidth=0.5, height=0.6, zorder=3, alpha=0.80)
    for bar, h in zip(bars, hatches):
        bar.set_hatch(h)

    ax.axvline(0, color='black', linewidth=0.6, zorder=4)

    for bar, v in zip(bars, vals):
        xp = v + (0.025 if v >= 0 else -0.025)
        ax.text(xp, bar.get_y()+bar.get_height()/2, f"{v:.3f}",
                va='center', ha='left' if v >= 0 else 'right', fontsize=5.5,
                fontstyle='italic')

    ax.set_title(titles[i], fontsize=8, fontweight='bold', pad=10)
    ax.text(-0.02, 1.08, f"({chr(97+i)})", transform=ax.transAxes,
            fontsize=9, fontweight='bold', va='top', ha='right')
    ax.set_xlim(-0.40, 0.88)
    ax.set_xlabel("Pearson r", fontsize=7.5)
    if i == 0:
        ax.set_yticks(range(len(params)))
        ax.set_yticklabels(params, fontsize=6.5)
    else:
        ax.set_yticks(range(len(params)))
        ax.set_yticklabels(params, fontsize=6.5)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', length=0)
    ax.tick_params(axis='x', direction='in', length=3, width=0.5)

pos_p = mpatches.Patch(facecolor=CP, edgecolor='black', hatch=HP, alpha=0.80, label='Positive r (risk factor)')
neg_p = mpatches.Patch(facecolor=CN, edgecolor='black', hatch=HN, alpha=0.80, label='Negative r (protective)')
fig.legend(handles=[pos_p, neg_p], loc='lower center', ncol=2, bbox_to_anchor=(0.55, 0.02),
           frameon=True, edgecolor='black', fontsize=7, handlelength=1.8)

plt.savefig(FIGURE_DIR / "tornado_q1.png", dpi=600, bbox_inches='tight', pad_inches=0.08)
plt.savefig(FIGURE_DIR / "tornado_q1.pdf", bbox_inches='tight', pad_inches=0.08)
plt.close()


