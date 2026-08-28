#!/usr/bin/env python3
"""Minimal two-column example using the strict publication style."""

from pathlib import Path
import numpy as np

from figure_style import (
    FONT_ANNOTATION_PT,
    apply_panel_label,
    create_pub_figure,
    export_pub_figure,
    style_axis_text,
)


def main() -> None:
    fig = create_pub_figure(height_cm=8.5, constrained_layout=True)
    axs = fig.subplots(1, 2)

    x = np.arange(5)
    axs[0].plot(x, [1.0, 1.8, 2.3, 2.7, 3.0], marker="o", label="Control")
    axs[0].plot(x, [1.0, 2.1, 2.9, 3.5, 4.0], marker="o", label="Treatment")
    axs[0].set_title("Time course")
    axs[0].set_xlabel("Time")
    axs[0].set_ylabel("Response")
    axs[0].legend()

    axs[1].bar([0, 1], [2.9, 4.0])
    axs[1].set_title("Endpoint")
    axs[1].set_xticks([0, 1], ["Control", "Treatment"])
    axs[1].set_ylabel("Response")
    axs[1].text(0.5, 4.2, "*", ha="center", va="bottom", fontsize=FONT_ANNOTATION_PT)

    for label, ax in zip(("A", "B"), axs):
        apply_panel_label(ax, label)
        style_axis_text(ax)

    export_pub_figure(fig, Path(__file__).resolve().parent / "example_output")


if __name__ == "__main__":
    main()
