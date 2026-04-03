"""Generate visualization plots for the STEP→mesh geometry pipeline."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(OUT_DIR, exist_ok=True)

COLORS = {
    "bg": "#1a1a2e", "panel": "#16213e", "accent": "#0f3460",
    "highlight": "#e94560", "text": "#eaeaea", "grid": "#2a2a4a",
    "steel": "#4a9eff", "aluminum": "#50c878", "copper": "#ff8c42",
    "pass": "#2ecc71", "fail": "#e74c3c",
}

plt.rcParams.update({
    'figure.facecolor': COLORS["bg"], 'axes.facecolor': COLORS["panel"],
    'axes.edgecolor': COLORS["grid"], 'axes.labelcolor': COLORS["text"],
    'text.color': COLORS["text"], 'xtick.color': COLORS["text"],
    'ytick.color': COLORS["text"], 'grid.color': COLORS["grid"],
    'font.family': 'sans-serif', 'font.size': 11,
})


def plot_geometry_pipeline():
    """Visualize the STEP→mesh→export pipeline with real data."""
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.axis('off')
    fig.suptitle("ANSA Geometry Pipeline: screw.step → Nastran deck", fontsize=16, fontweight='bold')

    steps = [
        ("Load STEP", "base.Open()\n10 FACE\n1 ANSAPART", COLORS["steel"], "1.2s"),
        ("Mesh", "mesh.Mesh(faces)\n1,947 shells\n1,915 grids", COLORS["aluminum"], "0.2s"),
        ("Quality", "CalculateOffElements\n0 violations\n1 property", COLORS["copper"], "<0.1s"),
        ("Material", "CreateEntity(MAT1)\nSteel 4140\nE=210 GPa", COLORS["highlight"], "<0.1s"),
        ("Export", "OutputNastran()\n209 KB .nas\n878 KB .ansa", COLORS["pass"], "0.1s"),
    ]

    box_w = 2.2
    gap = 0.4
    total_w = len(steps) * box_w + (len(steps) - 1) * gap
    x_start = (14 - total_w) / 2

    for i, (title, desc, color, timing) in enumerate(steps):
        x = x_start + i * (box_w + gap)
        y = 1.0

        rect = mpatches.FancyBboxPatch(
            (x, y - 0.3), box_w, 2.6,
            boxstyle="round,pad=0.15",
            facecolor=color, edgecolor='white', linewidth=1.5, alpha=0.85
        )
        ax.add_patch(rect)

        ax.text(x + box_w/2, y + 1.9, f"Step {i+1}", ha='center', va='center',
                fontsize=9, color='white', alpha=0.6)
        ax.text(x + box_w/2, y + 1.5, title, ha='center', va='center',
                fontsize=12, fontweight='bold', color='white')
        ax.text(x + box_w/2, y + 0.6, desc, ha='center', va='center',
                fontsize=9, color='white', alpha=0.9, linespacing=1.4)
        ax.text(x + box_w/2, y - 0.1, timing, ha='center', va='center',
                fontsize=9, fontfamily='monospace', color='#aaaaaa')

        if i < len(steps) - 1:
            ax.annotate('', xy=(x + box_w + gap - 0.1, y + 1.0),
                       xytext=(x + box_w + 0.1, y + 1.0),
                       arrowprops=dict(arrowstyle='->', color=COLORS["text"], lw=2))

    ax.set_xlim(0, 14)
    ax.set_ylim(-0.8, 4.2)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "06_geometry_pipeline.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("  saved 06_geometry_pipeline.png")


def plot_all_tests():
    """Visualize complete test suite results."""
    tests = [
        ("test_ansa_driver", 31, "Phase 1: detect/lint/connect/parse/run", 1.6),
        ("test_runtime", 12, "Phase 2: IAP launch/exec/disconnect", 3.6),
        ("test_pipeline", 5, "Read Nastran → modify → export", 3.7),
        ("test_geometry_pipeline", 6, "STEP → mesh → quality → export", 6.0),
    ]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5), gridspec_kw={'width_ratios': [3, 1]})
    fig.suptitle("ANSA ion Driver — 54 Tests All Passing", fontsize=16, fontweight='bold')

    # Left: test suite breakdown
    ax1.axis('off')
    colors_list = [COLORS["steel"], COLORS["aluminum"], COLORS["copper"], COLORS["highlight"]]
    for i, (name, count, desc, dur) in enumerate(tests):
        y = len(tests) - 1 - i
        color = colors_list[i]
        rect = mpatches.FancyBboxPatch(
            (0, y - 0.35), 7.5, 0.7,
            boxstyle="round,pad=0.1",
            facecolor=COLORS["accent"], edgecolor=color, linewidth=1.5, alpha=0.7
        )
        ax1.add_patch(rect)
        ax1.text(0.3, y, name, ha='left', va='center', fontsize=10, fontweight='bold',
                fontfamily='monospace', color=color)
        ax1.text(3.5, y, desc, ha='left', va='center', fontsize=9, color='#cccccc')
        ax1.text(6.8, y, f"{count}", ha='center', va='center', fontsize=12,
                fontweight='bold', color=COLORS["pass"])
        ax1.text(7.2, y, "PASS", ha='left', va='center', fontsize=10, color=COLORS["pass"])
    ax1.set_xlim(-0.2, 7.8)
    ax1.set_ylim(-0.8, len(tests) - 0.2)

    # Right: pie chart
    sizes = [t[1] for t in tests]
    labels = [f"{t[0]}\n({t[1]})" for t in tests]
    ax2.pie(sizes, labels=labels, colors=colors_list, autopct='%1.0f%%',
            textprops={'color': COLORS["text"], 'fontsize': 8},
            wedgeprops={'edgecolor': COLORS["bg"], 'linewidth': 2})
    ax2.set_title("Test Distribution", fontsize=11, color=COLORS["highlight"])

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "07_all_tests.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("  saved 07_all_tests.png")


if __name__ == "__main__":
    print("Generating geometry pipeline visualizations...")
    plot_geometry_pipeline()
    plot_all_tests()
    print("Done!")
