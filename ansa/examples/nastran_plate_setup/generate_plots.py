"""Generate visualization plots for the ANSA cookbook example.

Run with: python generate_plots.py
Requires: matplotlib (system python, not ANSA python)
"""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Color scheme ──
COLORS = {
    "bg": "#1a1a2e",
    "panel": "#16213e",
    "accent": "#0f3460",
    "highlight": "#e94560",
    "text": "#eaeaea",
    "grid": "#2a2a4a",
    "steel": "#4a9eff",
    "aluminum": "#50c878",
    "copper": "#ff8c42",
    "pass": "#2ecc71",
    "fail": "#e74c3c",
}

plt.rcParams.update({
    'figure.facecolor': COLORS["bg"],
    'axes.facecolor': COLORS["panel"],
    'axes.edgecolor': COLORS["grid"],
    'axes.labelcolor': COLORS["text"],
    'text.color': COLORS["text"],
    'xtick.color': COLORS["text"],
    'ytick.color': COLORS["text"],
    'grid.color': COLORS["grid"],
    'font.family': 'sans-serif',
    'font.size': 11,
})


def plot_00_connect():
    """Visualize ion connect result."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Title
    ax.text(5, 5.3, "ion check ansa", fontsize=18, fontweight='bold',
            ha='center', va='center', fontfamily='monospace')

    # Connection info box
    box = mpatches.FancyBboxPatch((1, 1.2), 8, 3.5, boxstyle="round,pad=0.3",
                                   facecolor=COLORS["accent"], edgecolor=COLORS["highlight"],
                                   linewidth=2)
    ax.add_patch(box)

    info_lines = [
        ("solver", "ansa"),
        ("version", "25.0.0"),
        ("status", "ok  ✓"),
        ("path", "E:\\...\\ANSA\\ansa_v25.0.0\\ansa64.bat"),
    ]
    for i, (key, val) in enumerate(info_lines):
        y = 4.2 - i * 0.75
        ax.text(1.8, y, f"{key}:", fontsize=12, fontfamily='monospace',
                color='#888888', va='center')
        color = COLORS["pass"] if val.endswith("✓") else COLORS["text"]
        ax.text(4.5, y, val, fontsize=12, fontfamily='monospace',
                fontweight='bold', color=color, va='center')

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "00_connect.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("  saved 00_connect.png")


def plot_01_materials():
    """Visualize material properties comparison."""
    materials = {
        "Steel\nAISI 304": {"E": 193000, "nu": 0.29, "rho": 8.0, "color": COLORS["steel"]},
        "Aluminum\n6061-T6": {"E": 68900, "nu": 0.33, "rho": 2.7, "color": COLORS["aluminum"]},
        "Copper\nC101":      {"E": 117000, "nu": 0.34, "rho": 8.94, "color": COLORS["copper"]},
    }

    fig, axes = plt.subplots(1, 3, figsize=(12, 4.5))
    fig.suptitle("Material Properties Created in ANSA", fontsize=16, fontweight='bold', y=0.98)

    names = list(materials.keys())
    colors = [materials[n]["color"] for n in names]

    # Young's Modulus
    ax = axes[0]
    vals = [materials[n]["E"] / 1000 for n in names]
    bars = ax.bar(names, vals, color=colors, edgecolor='white', linewidth=0.5, width=0.6)
    ax.set_ylabel("Young's Modulus (GPa)")
    ax.set_title("Stiffness", fontsize=12, color=COLORS["highlight"])
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{v:.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    # Poisson's Ratio
    ax = axes[1]
    vals = [materials[n]["nu"] for n in names]
    bars = ax.bar(names, vals, color=colors, edgecolor='white', linewidth=0.5, width=0.6)
    ax.set_ylabel("Poisson's Ratio")
    ax.set_title("Compressibility", fontsize=12, color=COLORS["highlight"])
    ax.set_ylim(0, 0.45)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                f'{v:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    # Density
    ax = axes[2]
    vals = [materials[n]["rho"] for n in names]
    bars = ax.bar(names, vals, color=colors, edgecolor='white', linewidth=0.5, width=0.6)
    ax.set_ylabel("Density (×10⁻⁹ tonne/mm³)")
    ax.set_title("Weight", fontsize=12, color=COLORS["highlight"])
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f'{v:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "01_materials.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("  saved 01_materials.png")


def plot_02_properties():
    """Visualize shell property stack."""
    props = [
        ("plate_0.5mm\naluminum", 0.5, COLORS["aluminum"], "Aluminum 6061"),
        ("plate_1mm\nsteel", 1.0, COLORS["steel"], "Steel AISI304"),
        ("plate_1.5mm\ncopper", 1.5, COLORS["copper"], "Copper C101"),
        ("plate_2mm\nsteel", 2.0, COLORS["steel"], "Steel AISI304"),
    ]

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.suptitle("Shell Properties (PSHELL) — Thickness Stack", fontsize=16, fontweight='bold')

    # Draw stacked plates visualization
    y_base = 0.5
    x_start = 0.5
    plate_width = 8
    gap = 0.3
    scale = 1.5  # visual scale for thickness

    for i, (name, t, color, mat) in enumerate(props):
        y = y_base + i * (2.0 * scale + gap)
        height = t * scale

        # Plate rectangle
        rect = mpatches.FancyBboxPatch(
            (x_start, y), plate_width, height,
            boxstyle="round,pad=0.05",
            facecolor=color, edgecolor='white', linewidth=1.5, alpha=0.85
        )
        ax.add_patch(rect)

        # Thickness label inside
        ax.text(x_start + plate_width/2, y + height/2,
                f"t = {t} mm", ha='center', va='center',
                fontsize=13, fontweight='bold', color='white',
                fontfamily='monospace')

        # Property name on left
        ax.text(x_start - 0.3, y + height/2, name.replace('\n', ' '),
                ha='right', va='center', fontsize=10, color=color)

        # Material name on right
        ax.text(x_start + plate_width + 0.3, y + height/2,
                f"← {mat}", ha='left', va='center', fontsize=10, color='#aaaaaa')

    ax.set_xlim(-3, 13)
    ax.set_ylim(0, y_base + len(props) * (2.0 * scale + gap) + 0.5)
    ax.axis('off')

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "02_properties.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("  saved 02_properties.png")


def plot_03_deck_support():
    """Visualize supported solver decks."""
    decks = [
        ("NASTRAN", True, "Structural FEA"),
        ("ABAQUS", True, "Nonlinear FEA"),
        ("LS-DYNA", True, "Crash / Explicit"),
        ("FLUENT", True, "CFD"),
        ("PAM-CRASH", True, "Crash"),
        ("RADIOSS", True, "Explicit FEA"),
        ("OptiStruct", True, "Optimization"),
    ]

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.suptitle("ANSA v25.0.0 — Supported Solver Decks", fontsize=16, fontweight='bold')

    for i, (name, available, desc) in enumerate(decks):
        y = len(decks) - 1 - i
        color = COLORS["pass"] if available else COLORS["fail"]
        symbol = "✓" if available else "✗"

        # Background bar
        rect = mpatches.FancyBboxPatch(
            (0.2, y - 0.35), 7.6, 0.7,
            boxstyle="round,pad=0.1",
            facecolor=COLORS["accent"], edgecolor=color, linewidth=1.5, alpha=0.7
        )
        ax.add_patch(rect)

        # Status symbol
        ax.text(0.6, y, symbol, ha='center', va='center',
                fontsize=16, fontweight='bold', color=color)

        # Deck name
        ax.text(1.3, y, name, ha='left', va='center',
                fontsize=13, fontweight='bold', fontfamily='monospace')

        # Description
        ax.text(5.0, y, desc, ha='left', va='center',
                fontsize=11, color='#888888')

    ax.set_xlim(0, 8)
    ax.set_ylim(-0.8, len(decks) - 0.2)
    ax.axis('off')

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "03_deck_support.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("  saved 03_deck_support.png")


def plot_04_test_results():
    """Visualize test execution results."""
    tests = [
        ("EX-06", "Batch Smoke Test", 1.52, "PASS"),
        ("EX-07", "Entity Collection", 1.45, "PASS"),
        ("EX-08", "Deck Query (7 decks)", 1.56, "PASS"),
        ("EX-09", "Material + Property", 1.44, "PASS"),
        ("EX-10", "Nastran Model Build", 1.48, "PASS"),
    ]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={'width_ratios': [2, 1]})
    fig.suptitle("ANSA Execution Tests via ion", fontsize=16, fontweight='bold')

    # Left: test results table
    ax1.axis('off')
    for i, (case_id, desc, duration, status) in enumerate(tests):
        y = len(tests) - 1 - i
        color = COLORS["pass"] if status == "PASS" else COLORS["fail"]

        rect = mpatches.FancyBboxPatch(
            (0, y - 0.35), 6, 0.7,
            boxstyle="round,pad=0.1",
            facecolor=COLORS["accent"], edgecolor=color, linewidth=1.5, alpha=0.7
        )
        ax1.add_patch(rect)

        ax1.text(0.3, y, case_id, ha='left', va='center',
                fontsize=11, fontweight='bold', fontfamily='monospace', color=color)
        ax1.text(1.5, y, desc, ha='left', va='center', fontsize=11)
        ax1.text(4.8, y, f"{duration:.2f}s", ha='right', va='center',
                fontsize=11, fontfamily='monospace', color='#aaaaaa')
        ax1.text(5.5, y, status, ha='center', va='center',
                fontsize=12, fontweight='bold', color=color)

    ax1.set_xlim(-0.2, 6.2)
    ax1.set_ylim(-0.8, len(tests) - 0.2)

    # Right: timing pie/bar
    durations = [t[2] for t in tests]
    labels = [t[0] for t in tests]
    colors_bar = [COLORS["steel"], COLORS["aluminum"], COLORS["copper"],
                  COLORS["highlight"], COLORS["pass"]]

    bars = ax2.barh(labels, durations, color=colors_bar, edgecolor='white', linewidth=0.5, height=0.6)
    ax2.set_xlabel("Duration (seconds)")
    ax2.set_title("Execution Time", fontsize=12, color=COLORS["highlight"])
    ax2.set_xlim(0, 2.0)
    ax2.grid(axis='x', alpha=0.3)
    ax2.invert_yaxis()

    for bar, d in zip(bars, durations):
        ax2.text(bar.get_width() + 0.03, bar.get_y() + bar.get_height()/2,
                f'{d:.2f}s', va='center', fontsize=10, fontfamily='monospace')

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "04_test_results.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("  saved 04_test_results.png")


def plot_05_pipeline():
    """Visualize the ion → ANSA execution pipeline."""
    fig, ax = plt.subplots(figsize=(12, 3.5))
    ax.axis('off')
    fig.suptitle("ion → ANSA Execution Pipeline", fontsize=16, fontweight='bold')

    steps = [
        ("detect()", "Identify\nANSA script", COLORS["steel"]),
        ("lint()", "Validate\nsyntax + imports", COLORS["aluminum"]),
        ("connect()", "Check ANSA\ninstalled", COLORS["copper"]),
        ("run_file()", "Execute via\nansa_win64.exe", COLORS["highlight"]),
        ("parse_output()", "Extract JSON\nfrom stdout", COLORS["pass"]),
    ]

    box_w = 1.8
    gap = 0.5
    total_w = len(steps) * box_w + (len(steps) - 1) * gap
    x_start = (12 - total_w) / 2

    for i, (func, desc, color) in enumerate(steps):
        x = x_start + i * (box_w + gap)
        y = 1.0

        # Box
        rect = mpatches.FancyBboxPatch(
            (x, y - 0.6), box_w, 1.8,
            boxstyle="round,pad=0.15",
            facecolor=color, edgecolor='white', linewidth=1.5, alpha=0.85
        )
        ax.add_patch(rect)

        # Function name
        ax.text(x + box_w/2, y + 0.7, func, ha='center', va='center',
                fontsize=10, fontweight='bold', fontfamily='monospace', color='white')

        # Description
        ax.text(x + box_w/2, y + 0.05, desc, ha='center', va='center',
                fontsize=9, color='white', alpha=0.9)

        # Arrow to next
        if i < len(steps) - 1:
            ax.annotate('', xy=(x + box_w + gap - 0.1, y + 0.4),
                       xytext=(x + box_w + 0.1, y + 0.4),
                       arrowprops=dict(arrowstyle='->', color=COLORS["text"],
                                      lw=2, mutation_scale=15))

    # Step numbers
    for i in range(len(steps)):
        x = x_start + i * (box_w + gap) + box_w/2
        ax.text(x, 0.1, f"Step {i+1}", ha='center', va='center',
                fontsize=9, color='#666666')

    ax.set_xlim(0, 12)
    ax.set_ylim(-0.3, 2.8)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "05_pipeline.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("  saved 05_pipeline.png")


if __name__ == "__main__":
    print("Generating ANSA cookbook visualizations...")
    plot_00_connect()
    plot_01_materials()
    plot_02_properties()
    plot_03_deck_support()
    plot_04_test_results()
    plot_05_pipeline()
    print("Done! All plots saved to screenshots/")
