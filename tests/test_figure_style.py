from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import matplotlib
matplotlib.use("Agg")

from figure_style import (
    FIGURE_WIDTH_CM,
    PanelComplexity,
    create_pub_figure,
    recommend_columns,
    validate_figure,
)


def test_fixed_width_and_height_contract():
    fig = create_pub_figure(10.0)
    validate_figure(fig)
    width_cm, height_cm = fig.get_size_inches() * 2.54
    assert abs(width_cm - FIGURE_WIDTH_CM) < 0.01
    assert abs(height_cm - 10.0) < 0.01


def test_three_columns_require_simple_panels():
    simple = [PanelComplexity() for _ in range(3)]
    assert recommend_columns(simple, requested=3) == 3

    dense = [PanelComplexity(), PanelComplexity(long_labels=True), PanelComplexity()]
    assert recommend_columns(dense, requested=3) == 2
