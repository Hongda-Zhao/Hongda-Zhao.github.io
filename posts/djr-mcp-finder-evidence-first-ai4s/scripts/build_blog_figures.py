#!/usr/bin/env python3
"""Render the web figures for the DJR-MCP Finder evidence-first AI4S note.

The script reads only the compact, reviewable values in source-data/figure-data.json.
Conceptual elements are labelled as schematics; quantitative panels preserve the
frozen project values or the explicitly described row-split expectation formula.
"""

from __future__ import annotations

import json
import math
import textwrap
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "source-data" / "figure-data.json"
OUTPUT_DIR = ROOT / "figures"

PAPER = "#faf9f6"
INK = "#222725"
MUTED = "#66706b"
LINE = "#c8ccc8"
GREEN = "#2f6b4f"
GREEN_LIGHT = "#dfece5"
BLUE = "#356a8a"
BLUE_LIGHT = "#dce9f0"
AMBER = "#c27a10"
AMBER_LIGHT = "#f4e7cd"
RED = "#a8443f"
RED_LIGHT = "#f2dfdc"
BROWN = "#654a38"
WHITE = "#ffffff"


def configure_matplotlib() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": [
                "Hiragino Sans GB",
                "Heiti SC",
                "Arial Unicode MS",
                "Arial",
                "Helvetica",
                "DejaVu Sans",
                "sans-serif",
            ],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "font.size": 10,
            "axes.spines.right": False,
            "axes.spines.top": False,
            "axes.linewidth": 0.8,
            "legend.frameon": False,
            "figure.facecolor": PAPER,
            "savefig.facecolor": PAPER,
        }
    )


def load_data() -> dict:
    with DATA_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def canvas(width: float, height: float) -> tuple[plt.Figure, plt.Axes]:
    fig = plt.figure(figsize=(width, height), facecolor=PAPER)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def rounded_box(
    ax: plt.Axes,
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    face: str = WHITE,
    edge: str = LINE,
    linewidth: float = 1.2,
    radius: float = 0.018,
    zorder: int = 2,
) -> FancyBboxPatch:
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle=f"round,pad=0.008,rounding_size={radius}",
        facecolor=face,
        edgecolor=edge,
        linewidth=linewidth,
        zorder=zorder,
    )
    ax.add_patch(patch)
    return patch


def arrow(
    ax: plt.Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    color: str = MUTED,
    linewidth: float = 1.5,
    style: str = "-|>",
    mutation_scale: float = 12,
    zorder: int = 3,
) -> None:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle=style,
            mutation_scale=mutation_scale,
            linewidth=linewidth,
            color=color,
            shrinkA=2,
            shrinkB=2,
            zorder=zorder,
        )
    )


def wrap(text: str, width: int) -> str:
    return "\n".join(textwrap.wrap(text, width=width, break_long_words=False))


def save(fig: plt.Figure, stem: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    svg_path = OUTPUT_DIR / f"{stem}.svg"
    fig.savefig(svg_path, dpi=320, metadata={"Creator": "matplotlib"})
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
    )
    fig.savefig(OUTPUT_DIR / f"{stem}.pdf", dpi=320, metadata={"Creator": "matplotlib"})
    fig.savefig(OUTPUT_DIR / f"{stem}.png", dpi=320, metadata={"Software": "matplotlib"})
    plt.close(fig)


def cover(data: dict) -> None:
    fig, ax = canvas(12.0, 6.75)
    ax.text(
        0.06,
        0.91,
        "V0.1 · RELEASED 2026-07-30",
        fontsize=14,
        color=GREEN,
        fontweight="bold",
        va="center",
    )
    ax.text(
        0.06,
        0.82,
        "做 DJR-MCP Finder 的两个月\nAI-assisted 结构生物学工具加速病毒演化学分析",
        fontsize=27,
        color=INK,
        fontweight="bold",
        va="top",
        linespacing=1.08,
    )
    ax.text(
        0.06,
        0.60,
        "从标签、HardNeg 和 component split，\n到模型选择与 Agent 协作。",
        fontsize=14,
        color=MUTED,
        va="top",
        linespacing=1.45,
    )

    # Main evidence path.
    stages = [
        ("证据分层", "Gold / Silver\nconditional labels", BLUE_LIGHT, BLUE),
        ("边界样本", "5,000 HardNeg\n2 quarantined", AMBER_LIGHT, AMBER),
        ("关系隔离", "27,427-node graph\ncomponent-safe split", GREEN_LIGHT, GREEN),
        ("开发选择", "14 models\nhead gates + paired SE", BLUE_LIGHT, BLUE),
    ]
    x0, y0, w, h, gap = 0.055, 0.27, 0.185, 0.16, 0.025
    for index, (title, subtitle, face, edge) in enumerate(stages):
        x = x0 + index * (w + gap)
        rounded_box(ax, (x, y0), w, h, face=face, edge=edge, linewidth=1.5)
        ax.text(x + 0.018, y0 + 0.115, title, fontsize=13, fontweight="bold", color=INK)
        ax.text(x + 0.018, y0 + 0.073, subtitle, fontsize=9.5, color=MUTED, va="top")
        if index < len(stages) - 1:
            arrow(ax, (x + w + 0.004, y0 + h / 2), (x + w + gap - 0.004, y0 + h / 2))

    # Release and Test firewall.
    rx = 0.86
    rounded_box(ax, (rx, 0.43), 0.105, 0.19, face=GREEN_LIGHT, edge=GREEN, linewidth=1.8)
    ax.text(rx + 0.0525, 0.56, "V0", ha="center", fontsize=18, fontweight="bold", color=GREEN)
    ax.text(rx + 0.0525, 0.505, "ESM-C 6B", ha="center", fontsize=10.5, fontweight="bold", color=INK)
    ax.text(rx + 0.0525, 0.466, "S = 0.997145", ha="center", fontsize=9.5, color=MUTED)
    arrow(ax, (0.82, y0 + h / 2), (rx, 0.50), color=GREEN, linewidth=1.8)

    rounded_box(ax, (rx, 0.20), 0.105, 0.15, face=RED_LIGHT, edge=RED, linewidth=1.6)
    ax.text(rx + 0.0525, 0.302, "V0 / TEST", ha="center", fontsize=11.2, fontweight="bold", color=RED)
    ax.text(rx + 0.0525, 0.256, "not_evaluated", ha="center", fontsize=8.9, color=INK)
    ax.text(rx + 0.0525, 0.224, "历史 cohort", ha="center", fontsize=8.6, color=MUTED)
    ax.plot([rx + 0.014, rx + 0.091], [0.365, 0.365], color=RED, linewidth=4, solid_capstyle="round")
    ax.text(rx + 0.0525, 0.385, "firewall", ha="center", fontsize=8.2, color=RED, fontweight="bold")

    ax.text(
        0.055,
        0.105,
        "先把科学问题定义清楚，再谈模型分数。",
        fontsize=13,
        fontweight="bold",
        color=BROWN,
    )
    ax.text(
        0.055,
        0.065,
        "V0.1 · released 2026-07-30 16:09 JST",
        fontsize=9.5,
        color=MUTED,
    )
    save(fig, "cover-evidence-first")


def labels_and_hardneg(data: dict) -> None:
    fig = plt.figure(figsize=(12.0, 7.4), facecolor=PAPER)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.04, 0.96], left=0.06, right=0.97, top=0.86, bottom=0.10, wspace=0.19)
    ax_l = fig.add_subplot(gs[0, 0])
    ax_r = fig.add_subplot(gs[0, 1])

    fig.text(0.06, 0.94, "同一条 cellular DJR，为什么会有两个标签", fontsize=23, fontweight="bold", color=INK)
    fig.text(
        0.06,
        0.895,
        "同一条 cellular DJR 在 H1 是正例、在 H2 却是负例；HardNeg 则专门逼近 H1 的决策边界。",
        fontsize=11.5,
        color=MUTED,
    )

    # Left: task-dependent label matrix.
    ax_l.set_xlim(0, 1)
    ax_l.set_ylim(0, 1)
    ax_l.axis("off")
    ax_l.text(0.0, 0.98, "a  标签随问题变化", fontsize=15, fontweight="bold", color=INK, va="top")
    rows = [
        ("VMA-DJR", "560", "正", "正", "已知类 / reject"),
        ("cellular DJR", "500", "正", "负", "不适用"),
        ("HardNeg", "5,000", "负", "—", "—"),
        ("background", "5,000", "负", "—", "—"),
    ]
    columns = ["数据组", "n", "H1", "H2", "H3"]
    col_x = [0.0, 0.39, 0.55, 0.70, 0.85]
    y_header = 0.86
    ax_l.add_patch(Rectangle((0, y_header - 0.055), 1.0, 0.075, facecolor=BROWN, edgecolor="none"))
    for x, label in zip(col_x, columns):
        ax_l.text(x + (0.015 if x == 0 else 0), y_header - 0.017, label, color=WHITE, fontsize=10.5, fontweight="bold", va="center")
    for idx, row in enumerate(rows):
        y = 0.72 - idx * 0.14
        face = WHITE if idx % 2 == 0 else "#f0efeb"
        ax_l.add_patch(Rectangle((0, y - 0.055), 1.0, 0.12, facecolor=face, edgecolor="none"))
        for j, value in enumerate(row):
            x = col_x[j] + (0.015 if j == 0 else 0)
            color = INK
            weight = "normal"
            if value == "正":
                color, weight = GREEN, "bold"
            elif value == "负":
                color, weight = RED, "bold"
            ax_l.text(x, y, value, fontsize=10.5 if j != 4 else 9.2, color=color, fontweight=weight, va="center")

    rounded_box(ax_l, (0.0, 0.05), 1.0, 0.19, face=BLUE_LIGHT, edge=BLUE, linewidth=1.3)
    ax_l.text(0.025, 0.197, "正类也有证据层级", fontsize=11.5, fontweight="bold", color=BLUE)
    ax_l.text(0.025, 0.153, "65 Gold + 495 Silver_R3 = 560 条 exact-unique VMA-DJR", fontsize=10.4, color=INK)
    ax_l.text(0.025, 0.113, "H3 只用 532 条拟合两个样本充分的门；其余 28 条只做 reject diagnostic。", fontsize=9.5, color=MUTED)
    ax_l.text(0.025, 0.078, "unknown/other = 拒绝强分，而不是“发现未知病毒”。", fontsize=9.5, color=RED, fontweight="bold")

    # Right: funnel.
    ax_r.set_xlim(0, 1)
    ax_r.set_ylim(0, 1)
    ax_r.axis("off")
    ax_r.text(0.0, 0.98, "b  Hard-negative 构造漏斗", fontsize=15, fontweight="bold", color=INK, va="top")
    funnel = data["hardnegative_funnel"]
    max_count = max(row["count"] for row in funnel)
    center = 0.50
    top = 0.86
    step_h = 0.095
    for idx, row in enumerate(funnel):
        fraction = math.sqrt(row["count"] / max_count)
        width = 0.28 + 0.64 * fraction
        x = center - width / 2
        y = top - idx * step_h
        face = AMBER_LIGHT if idx < len(funnel) - 1 else GREEN_LIGHT
        edge = AMBER if idx < len(funnel) - 1 else GREEN
        rounded_box(ax_r, (x, y - 0.055), width, 0.072, face=face, edge=edge, linewidth=1.1, radius=0.012)
        stage_label = row["stage"].replace("MMseqs2 representatives", "MMseqs2 reps")
        ax_r.text(x + 0.018, y - 0.020, stage_label, fontsize=9.1, color=INK, va="center")
        ax_r.text(x + width - 0.018, y - 0.020, f"{row['count']:,}", fontsize=10.5, color=edge, fontweight="bold", ha="right", va="center")
        if idx < len(funnel) - 1:
            arrow(ax_r, (center, y - 0.060), (center, y - step_h + 0.025), color=MUTED, linewidth=1.0, mutation_scale=9)

    ax_r.text(0.05, 0.145, "2 个 near-positive representatives 被 quarantine", fontsize=10.2, color=RED, fontweight="bold")
    ax_r.text(0.05, 0.104, "exact / MMseqs2 / HMM / Foldseek 对 DJR positives 全部排除", fontsize=9.4, color=MUTED)
    ax_r.text(0.05, 0.066, "G0–G6：7/7 operational recovery gates PASS", fontsize=9.4, color=GREEN, fontweight="bold")

    fig.text(
        0.06,
        0.035,
        "图 1｜三级任务中的标签变化与 HardNeg 构建。项目没有 HardNeg 有/无消融，因此不报告因果增益。",
        fontsize=8.8,
        color=MUTED,
    )
    save(fig, "figure-1-labels-hard-negatives")


def cluster_split(data: dict) -> None:
    split = data["split"]
    fig = plt.figure(figsize=(12.0, 7.2), facecolor=PAPER)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 0.95], left=0.055, right=0.97, top=0.84, bottom=0.12, wspace=0.18)
    ax_l = fig.add_subplot(gs[0, 0])
    ax_r = fig.add_subplot(gs[0, 1])
    fig.text(0.055, 0.94, "我把有关联的序列一起分到同一组", fontsize=23, fontweight="bold", color=INK)
    fig.text(
        0.055,
        0.892,
        "先连接 exact、source cluster、legacy component 与 MMseqs2 关系，再按整个 component 切分。",
        fontsize=11.3,
        color=MUTED,
    )

    # Left conceptual comparison.
    ax_l.set_xlim(0, 1)
    ax_l.set_ylim(0, 1)
    ax_l.axis("off")
    ax_l.text(0.0, 0.98, "a  row-wise split 会把“亲戚”分到两边", fontsize=14.5, fontweight="bold", color=INK, va="top")
    families = [
        [(0.12, 0.74), (0.21, 0.69), (0.29, 0.76), (0.36, 0.66)],
        [(0.18, 0.46), (0.28, 0.42), (0.38, 0.49)],
        [(0.46, 0.76), (0.55, 0.70), (0.62, 0.79), (0.69, 0.69), (0.75, 0.76)],
    ]
    split_colors = [GREEN, BLUE, RED]
    for f_idx, nodes in enumerate(families):
        for i in range(len(nodes) - 1):
            ax_l.plot([nodes[i][0], nodes[i + 1][0]], [nodes[i][1], nodes[i + 1][1]], color=LINE, linewidth=2, zorder=1)
        for n_idx, (x, y) in enumerate(nodes):
            color = split_colors[(n_idx + f_idx) % 3]
            ax_l.scatter(x, y, s=150, color=color, edgecolor=WHITE, linewidth=1.3, zorder=3)
    ax_l.text(0.03, 0.58, "逐行随机", fontsize=10.5, color=RED, fontweight="bold")
    ax_l.text(0.03, 0.545, "同一连通分量跨 Train / Validation / Test", fontsize=9.3, color=MUTED)

    arrow(ax_l, (0.48, 0.37), (0.48, 0.29), color=GREEN, linewidth=1.8)
    ax_l.text(0.53, 0.33, "collapse into components", fontsize=9.0, color=GREEN, va="center")
    component_specs = [
        (0.05, 0.08, 0.25, 0.14, GREEN_LIGHT, GREEN, "Train"),
        (0.37, 0.08, 0.25, 0.14, BLUE_LIGHT, BLUE, "Validation"),
        (0.69, 0.08, 0.25, 0.14, RED_LIGHT, RED, "Test"),
    ]
    for x, y, w, h, face, edge, label in component_specs:
        rounded_box(ax_l, (x, y), w, h, face=face, edge=edge, linewidth=1.5)
        ax_l.text(x + w / 2, y + h - 0.035, label, ha="center", fontsize=10.5, fontweight="bold", color=edge)
        for j in range(3):
            cx = x + 0.06 + j * 0.065
            cy = y + 0.047 + (j % 2) * 0.018
            ax_l.scatter(cx, cy, s=65, color=edge, alpha=0.86, edgecolor=WHITE, linewidth=0.8)
            if j:
                ax_l.plot([cx - 0.065, cx], [y + 0.047 + ((j - 1) % 2) * 0.018, cy], color=edge, linewidth=1.1, alpha=0.55)

    # Right quantitative summary.
    ax_r.set_xlim(0, 1)
    ax_r.set_ylim(0, 1)
    ax_r.axis("off")
    ax_r.text(0.0, 0.98, "b  冻结数据上的泄漏审计", fontsize=14.5, fontweight="bold", color=INK, va="top")

    stats = [
        ("11,060", "model representatives", BLUE_LIGHT, BLUE),
        ("27,427", "graph nodes", AMBER_LIGHT, AMBER),
        ("9,262", "model-bearing components", GREEN_LIGHT, GREEN),
    ]
    for idx, (value, label, face, edge) in enumerate(stats):
        x = idx * 0.33
        rounded_box(ax_r, (x, 0.72), 0.29, 0.14, face=face, edge=edge, linewidth=1.2)
        ax_r.text(x + 0.145, 0.795, value, ha="center", fontsize=17, fontweight="bold", color=edge)
        ax_r.text(x + 0.145, 0.752, wrap(label, 18), ha="center", fontsize=8.1, color=MUTED, linespacing=1.05)

    ax_r.text(0.0, 0.64, "同样的 60/20/20 比例", fontsize=10.3, color=INK, fontweight="bold")
    expected = split["expected_spanning_components_if_independent_row_split_60_20_20"]
    values = [round(expected), split["residual_qualifying_cross_split_edges"]]
    labels = ["逐行独立分配的\n理论期望", "component-safe 后\n独立全搜索审计"]
    colors = [RED, GREEN]
    x_positions = [0.25, 0.72]
    max_bar = max(values) * 1.15
    for x, value, label, color in zip(x_positions, values, labels, colors):
        height = 0.31 * (value / max_bar) if value else 0.012
        ax_r.add_patch(Rectangle((x - 0.095, 0.23), 0.19, height, facecolor=color, alpha=0.86, edgecolor="none"))
        ax_r.text(x, 0.23 + height + 0.028, f"{value:,}", ha="center", fontsize=18, fontweight="bold", color=color)
        ax_r.text(x, 0.165, label, ha="center", va="top", fontsize=9.3, color=INK, linespacing=1.25)
    ax_r.plot([0.08, 0.92], [0.23, 0.23], color=INK, linewidth=1.0)

    ax_r.text(0.0, 0.085, "理论值 = Σ components [1 - (0.6^n + 0.2^n + 0.2^n)]", fontsize=9.2, color=MUTED)
    ax_r.text(0.0, 0.047, "n 为冻结 component size；这是分割风险推导，不是模型性能消融。", fontsize=8.9, color=MUTED)

    fig.text(
        0.055,
        0.04,
        "图 2｜Cluster-aware split。审计阈值为 MMseqs2 identity ≥30%、双向 coverage ≥80%；0 条残留边不证明更远同源完全不存在。",
        fontsize=8.8,
        color=MUTED,
    )
    save(fig, "figure-2-cluster-aware-split")


def model_selection(data: dict) -> None:
    selection = data["model_selection"]
    post = data["post_freeze_comparison"]
    fig = plt.figure(figsize=(12.0, 11.0), facecolor=PAPER)
    ax_l = fig.add_axes([0.16, 0.56, 0.78, 0.29])
    ax_r = fig.add_axes([0.06, 0.08, 0.88, 0.39])

    fig.text(0.06, 0.958, "14 个模型，我最后为什么选了 ESM-C 6B", fontsize=23, fontweight="bold", color=INK)
    fig.text(
        0.06,
        0.923,
        "先检查每个 Head 的 Validation gate，再比较共享 folds 的不确定性、FPR、成本与发布状态。",
        fontsize=11.1,
        color=MUTED,
    )

    # Left: 14-model scores and gates.
    models = selection["models"]
    names = [row["name"] for row in models][::-1]
    scores = np.array([row["score"] for row in models][::-1])
    gates = [row["gate"] for row in models][::-1]
    selected = [row["selected"] for row in models][::-1]
    y = np.arange(len(models))
    colors = [GREEN if gate == "PASS" else "#a8aaa8" for gate in gates]
    ax_l.hlines(y, 0.98, scores, color=colors, linewidth=2.0, alpha=0.75)
    ax_l.scatter(scores, y, s=[88 if flag else 45 for flag in selected], color=[AMBER if flag else color for flag, color in zip(selected, colors)], edgecolor=[BROWN if flag else WHITE for flag in selected], linewidth=1.2, zorder=3)
    ax_l.set_yticks(y, labels=names, fontsize=9.6)
    ax_l.set_xlim(0.980, 0.9982)
    ax_l.set_xticks([0.982, 0.986, 0.990, 0.994, 0.998])
    ax_l.tick_params(axis="x", labelsize=9.2, colors=MUTED)
    ax_l.grid(axis="x", color=LINE, linewidth=0.8, alpha=0.65)
    ax_l.set_axisbelow(True)
    ax_l.set_xlabel("Train-only five-fold composite S（局部放大，横轴从 0.980 起）", fontsize=10.2, color=INK)
    ax_l.set_title("a  14-model shared component CV", loc="left", fontsize=15, fontweight="bold", pad=14)
    ax_l.text(0.9802, 13.0, "8 pass all headwise gates", fontsize=9.8, color=GREEN, fontweight="bold")
    ax_l.text(0.9802, 12.25, "1 remains inside paired one-SE", fontsize=9.8, color=AMBER, fontweight="bold")
    ax_l.annotate(
        "selected · ESM-C 6B\nS = 0.997145",
        xy=(selection["models"][0]["score"], len(models) - 1),
        xytext=(0.9930, len(models) - 2.35),
        fontsize=9.8,
        color=BROWN,
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=BROWN, lw=1.2),
    )

    # Bottom: post-freeze trade-off, separated from the development ranking.
    ax_r.set_xlim(0, 1)
    ax_r.set_ylim(0, 1)
    ax_r.axis("off")
    ax_r.text(0.0, 0.99, "b  冻结后又出现了一个更高分候选", fontsize=15, fontweight="bold", color=INK, va="top")
    release = post["released_all_esmc_6b"]
    nominee = post["mixed_nominee"]
    for x0, title, item, face, edge in [
        (0.0, "Frozen V0 · all ESM-C 6B", release, GREEN_LIGHT, GREEN),
        (0.515, "Post-freeze mixed nominee", nominee, AMBER_LIGHT, AMBER),
    ]:
        rounded_box(ax_r, (x0, 0.46), 0.485, 0.40, face=face, edge=edge, linewidth=1.5)
        ax_r.text(x0 + 0.025, 0.802, title, fontsize=11.2, color=edge, fontweight="bold")
        ax_r.text(x0 + 0.025, 0.718, f"Train-CV S  {item['score']:.6f}", fontsize=10.2, color=INK)
        ax_r.text(x0 + 0.025, 0.648, f"viral strict clusters  {item['viral_strict_clusters_correct']}/{item['viral_strict_clusters_total']}", fontsize=9.7, color=INK)
        ax_r.text(x0 + 0.025, 0.578, f"always-on  {item['always_on_seconds_per_sequence']:.4f} s/seq", fontsize=9.3, color=INK)
        ax_r.text(x0 + 0.255, 0.578, f"worst-case  {item['worst_case_seconds_per_sequence']:.4f} s/seq", fontsize=9.3, color=INK)
        ax_r.text(x0 + 0.025, 0.505, f"Test: {item['test_status']}", fontsize=9.3, color=RED, fontweight="bold")
        ax_r.text(x0 + 0.255, 0.505, item["release_status"], fontsize=9.3, color=edge, fontweight="bold")

    ax_r.text(0.0, 0.36, "为什么不替换 V0？", fontsize=11.2, color=INK, fontweight="bold")
    bullets = [
        "分数只高 0.000500；仍是 Train-CV evidence",
        "viral strict clusters 从 55/69 变为 52/69",
        "always-on 更快，但最坏路径反而更慢",
        "两者在该 Test cohort 上均为 not_evaluated",
    ]
    for idx, item in enumerate(bullets):
        column = idx % 2
        row = idx // 2
        x0 = 0.015 + column * 0.50
        y0 = 0.275 - row * 0.105
        ax_r.scatter(x0, y0 + 0.005, s=25, color=AMBER)
        ax_r.text(x0 + 0.025, y0, item, fontsize=9.5, color=MUTED, va="center")

    fig.text(
        0.06,
        0.025,
        "图 3｜开发期模型比较与冻结后候选。mixed nominee 分数略高，但在其他检查完成前不替换 V0。",
        fontsize=8.7,
        color=MUTED,
    )
    save(fig, "figure-3-model-selection")


def reproducible_workflow(data: dict) -> None:
    steps = data["reproducibility"]["steps"]
    fig, ax = canvas(12.0, 7.1)
    ax.text(0.055, 0.94, "V0 最后固定下来的开发流程", fontsize=23, fontweight="bold", color=INK)
    ax.text(
        0.055,
        0.892,
        "除了保存结果，我也保存数据、切分、模型和评估状态的机器可读身份。",
        fontsize=11.4,
        color=MUTED,
    )

    # Central spine with grouped stages.
    groups = [
        ("DEFINE", steps[0:2], BLUE_LIGHT, BLUE),
        ("SEPARATE", steps[2:5], GREEN_LIGHT, GREEN),
        ("SELECT", steps[5:8], AMBER_LIGHT, AMBER),
        ("FREEZE", steps[8:10], RED_LIGHT, RED),
        ("AUDIT", steps[10:12], "#ece8e3", BROWN),
    ]
    xs = [0.055, 0.245, 0.455, 0.665, 0.855]
    widths = [0.16, 0.18, 0.18, 0.16, 0.115]
    y, h = 0.46, 0.30
    for idx, ((label, items, face, edge), x, w) in enumerate(zip(groups, xs, widths)):
        rounded_box(ax, (x, y), w, h, face=face, edge=edge, linewidth=1.6)
        ax.text(x + 0.018, y + h - 0.055, label, fontsize=10.2, fontweight="bold", color=edge)
        for j, item in enumerate(items):
            display = {
                "versioned sources + SHA-256": "版本化来源\n+ SHA-256",
                "evidence-tiered conditional labels": "证据分层\n+ 条件标签",
                "global similarity/component graph": "全局关系图",
                "component-safe Train/Validation/Test": "component-safe\nTrain / Val / Test",
                "independent post-split leakage audit": "独立 post-split\n泄漏审计",
                "frozen shared Train-only CV folds": "冻结共享\nTrain-only folds",
                "fixed checkpoint and embedding contract": "固定 checkpoint\n与 embedding contract",
                "Validation calibration + headwise gates + paired one-SE": "Validation calibration\n+ gates + paired SE",
                "frozen model, thresholds and selection identity": "冻结模型、阈值\n与 selection identity",
                "content-addressed single-use Test ledger": "内容寻址的一次性\nTest ledger",
                "post-freeze diagnostics cannot feed back": "post-freeze\ndiagnostics\n只读、不可反馈",
                "compact evidence core + checksum-bound archive": "compact evidence\ncore + checksum\narchive",
            }[item]
            item_y = y + h - 0.105 - j * (0.07 if len(items) == 3 else 0.085)
            item_fontsize = 8.1 if label == "AUDIT" else 8.7
            ax.text(x + 0.018, item_y, display, fontsize=item_fontsize, color=INK, va="top", linespacing=1.18)
        if idx < len(groups) - 1:
            arrow(ax, (x + w + 0.005, y + h / 2), (xs[idx + 1] - 0.006, y + h / 2), color=MUTED, linewidth=1.4)

    # Test firewall and post-freeze feedback block.
    ax.plot([0.635, 0.825], [0.39, 0.39], color=RED, linewidth=4, solid_capstyle="round")
    ax.text(0.73, 0.415, "TEST FIREWALL", ha="center", fontsize=9.2, color=RED, fontweight="bold")
    arrow(ax, (0.915, 0.44), (0.75, 0.31), color=BROWN, linewidth=1.3, style="-|>")
    ax.text(0.83, 0.29, "挑战结论：允许", fontsize=9.2, color=BROWN, fontweight="bold", ha="center")
    ax.text(0.83, 0.252, "反馈选模：禁止", fontsize=9.2, color=RED, fontweight="bold", ha="center")

    # Audit badges.
    badges = [
        ("20/20", "schema 5 gates"),
        ("289", "endpoints replayed"),
        ("24/24", "materialization attestations"),
        ("0", "Test rows in post-freeze analyses"),
    ]
    for idx, (value, label) in enumerate(badges):
        x = 0.055 + idx * 0.228
        rounded_box(ax, (x, 0.10), 0.205, 0.105, face=WHITE, edge=LINE, linewidth=1.0)
        ax.text(x + 0.025, 0.157, value, fontsize=15, fontweight="bold", color=GREEN if value != "0" else RED, va="center")
        ax.text(x + 0.083, 0.157, wrap(label, 24), fontsize=8.4, color=MUTED, va="center")

    ax.text(
        0.055,
        0.045,
        "图 4｜可重复工作流。数字为冻结后 schema 5 compact evidence 的独立完整性检查；它们验证流程一致性，不等于独立外部泛化。",
        fontsize=8.7,
        color=MUTED,
    )
    save(fig, "figure-4-reproducible-workflow")


def main() -> int:
    configure_matplotlib()
    data = load_data()
    cover(data)
    labels_and_hardneg(data)
    cluster_split(data)
    model_selection(data)
    reproducible_workflow(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
