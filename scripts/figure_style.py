#!/usr/bin/env python3
"""Strict final-size style helpers for the scientific-figure skill."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt

CM_PER_INCH = 2.54
FIGURE_WIDTH_CM = 17.0
FIGURE_MAX_HEIGHT_CM = 20.0

FONT_PANEL_LABEL_PT = 10.0
FONT_SUPTITLE_PT = 10.0
FONT_PANEL_TITLE_PT = 9.0
FONT_AXIS_LABEL_PT = 8.0
FONT_TICK_PT = 7.0
FONT_LEGEND_PT = 7.0
FONT_ANNOTATION_PT = 7.0

ALLOWED_FONT_SIZES_PT = {
    FONT_PANEL_LABEL_PT,
    FONT_SUPTITLE_PT,
    FONT_PANEL_TITLE_PT,
    FONT_AXIS_LABEL_PT,
    FONT_TICK_PT,
    FONT_LEGEND_PT,
    FONT_ANNOTATION_PT,
}


@dataclass(frozen=True)
class PanelComplexity:
    series: int = 1
    x_major_ticks: int = 5
    y_major_ticks: int = 5
    long_labels: bool = False
    rotated_category_labels: bool = False
    dense_internal_legend: bool = False
    significance_stacks: int = 0
    point_labels: bool = False
    dense_heatmap_labels: bool = False
    complex_image_annotations: bool = False

    @property
    def simple(self) -> bool:
        return (
            self.series <= 3
            and self.x_major_ticks <= 6
            and self.y_major_ticks <= 6
            and not self.long_labels
            and not self.rotated_category_labels
            and not self.dense_internal_legend
            and self.significance_stacks <= 1
            and not self.point_labels
            and not self.dense_heatmap_labels
            and not self.complex_image_annotations
        )


def cm_to_inch(cm: float) -> float:
    return cm / CM_PER_INCH


def configure_publication_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman"],
            "mathtext.fontset": "stix",
            "font.size": FONT_TICK_PT,
            "axes.titlesize": FONT_PANEL_TITLE_PT,
            "axes.labelsize": FONT_AXIS_LABEL_PT,
            "xtick.labelsize": FONT_TICK_PT,
            "ytick.labelsize": FONT_TICK_PT,
            "legend.fontsize": FONT_LEGEND_PT,
            "figure.titlesize": FONT_SUPTITLE_PT,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 0.8,
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            "legend.frameon": False,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "savefig.bbox": None,
        }
    )


def create_pub_figure(height_cm: float, **kwargs):
    if not (0 < height_cm <= FIGURE_MAX_HEIGHT_CM):
        raise ValueError(f"height_cm must be > 0 and <= {FIGURE_MAX_HEIGHT_CM}")
    configure_publication_style()
    return plt.figure(
        figsize=(cm_to_inch(FIGURE_WIDTH_CM), cm_to_inch(height_cm)),
        **kwargs,
    )


def recommend_columns(panels: Sequence[PanelComplexity], requested: int | None = None) -> int:
    """Return a readable column count under the 17 cm contract."""
    if not panels:
        raise ValueError("panels must not be empty")
    if requested is None:
        requested = 2 if len(panels) > 1 else 1
    if requested <= 0:
        raise ValueError("requested columns must be positive")
    if requested <= 2:
        return requested
    if requested == 3 and all(panel.simple for panel in panels):
        return 3
    return 2


def apply_panel_label(ax, label: str, x: float = -0.12, y: float = 1.04):
    return ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=FONT_PANEL_LABEL_PT,
        fontweight="bold",
        fontfamily="Times New Roman",
    )


def style_axis_text(ax) -> None:
    ax.title.set_fontsize(FONT_PANEL_TITLE_PT)
    ax.title.set_fontfamily("Times New Roman")
    ax.xaxis.label.set_fontsize(FONT_AXIS_LABEL_PT)
    ax.xaxis.label.set_fontfamily("Times New Roman")
    ax.yaxis.label.set_fontsize(FONT_AXIS_LABEL_PT)
    ax.yaxis.label.set_fontfamily("Times New Roman")
    for tick in list(ax.get_xticklabels()) + list(ax.get_yticklabels()):
        tick.set_fontsize(FONT_TICK_PT)
        tick.set_fontfamily("Times New Roman")
    legend = ax.get_legend()
    if legend is not None:
        for text in legend.get_texts():
            text.set_fontsize(FONT_LEGEND_PT)
            text.set_fontfamily("Times New Roman")


def _size_cm(fig) -> tuple[float, float]:
    width_in, height_in = fig.get_size_inches()
    return width_in * CM_PER_INCH, height_in * CM_PER_INCH


def validate_figure(fig, tolerance_cm: float = 0.01) -> None:
    width_cm, height_cm = _size_cm(fig)
    if abs(width_cm - FIGURE_WIDTH_CM) > tolerance_cm:
        raise ValueError(
            f"figure width must be {FIGURE_WIDTH_CM:.1f} cm; got {width_cm:.3f} cm"
        )
    if not (0 < height_cm <= FIGURE_MAX_HEIGHT_CM + tolerance_cm):
        raise ValueError(
            f"figure height must be <= {FIGURE_MAX_HEIGHT_CM:.1f} cm; got {height_cm:.3f} cm"
        )

    for text in fig.findobj(mpl.text.Text):
        if not text.get_visible() or not text.get_text().strip():
            continue
        size = round(float(text.get_fontsize()), 6)
        if size not in ALLOWED_FONT_SIZES_PT:
            raise ValueError(
                f"unexpected font size {size} pt for text {text.get_text()!r}; "
                f"allowed sizes are {sorted(ALLOWED_FONT_SIZES_PT)}"
            )


def export_pub_figure(fig, output_base: str | Path, dpi: int = 600) -> list[Path]:
    """Validate and export PDF, SVG and PNG without changing the physical canvas."""
    validate_figure(fig)
    base = Path(output_base)
    base.parent.mkdir(parents=True, exist_ok=True)
    outputs = [base.with_suffix(".pdf"), base.with_suffix(".svg"), base.with_suffix(".png")]
    fig.savefig(outputs[0], bbox_inches=None)
    fig.savefig(outputs[1], bbox_inches=None)
    fig.savefig(outputs[2], dpi=dpi, bbox_inches=None)
    return outputs
