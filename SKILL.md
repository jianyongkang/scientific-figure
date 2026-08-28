---
name: scientific-figure
description: >-
  Create, revise, audit, and export publication-grade scientific figures in Python/Matplotlib under a strict physical-layout contract with exact 17 cm final width, height no more than 20 cm, Times New Roman typography, fixed role-based point sizes, readable panel density, editable vector text, and deterministic QA. Use for paper figures, manuscript plots, multi-panel scientific figures, data visualization for publication, Nature-style figure planning, figure redesign, SVG/PDF/PNG export, and figure readability/consistency checks. Do not use for Illustrator-first redraws, interactive dashboards, photo editing, or non-scientific illustration.
---

# Scientific Figure

Build publication figures as scientific arguments under one fixed physical-size system. Use Python only for drawing, previewing, exporting, and visual QA.

## Non-negotiable output contract

Apply these rules to every figure unless the user explicitly overrides a rule in the current request:

- Use Python + Matplotlib for all figure drawing and exports.
- Set final figure width to exactly **17.0 cm**.
- Keep final figure height **<= 20.0 cm**.
- Use **Times New Roman** for all ordinary text. Never bundle or redistribute font files.
- Use one fixed point-size system:
  - panel label `A/B/C`: **10 pt bold**
  - figure-level title, only when explicitly needed: **10 pt**
  - panel title: **9 pt**
  - axis label: **8 pt**
  - tick labels: **7 pt**
  - legend: **7 pt**
  - ordinary annotation/statistical text: **7 pt**
- Never shrink one panel, one axis, or one text group to make it fit. A given point size must have the same physical size everywhere in the final PDF/SVG.
- Do not use `bbox_inches="tight"` for final export because it changes the physical output box. Fix layout on the 17 cm canvas instead.
- Keep SVG text editable (`svg.fonttype = none`) and PDF text as TrueType (`pdf.fonttype = 42`).

Use [scripts/figure_style.py](scripts/figure_style.py) instead of recreating these constants in each plotting script.

## Workflow

### 1. Establish the scientific contract

Before writing plotting code, write a compact working contract:

```text
Core conclusion:
Results-level question:
Figure archetype:
Panel map:
  A:
  B:
Evidence hierarchy:
Statistics/uncertainty:
Source data:
Reviewer risk:
```

Use one figure = one major claim as the default. Each panel must add a distinct inferential step. If removing a panel does not weaken or qualify the claim, merge it, move it, or remove it.

Read [references/figure-contract.md](references/figure-contract.md) for panel roles and evidence-chain patterns.

### 2. Choose panel density from readability, not convenience

Default to **one or two panels per row**.

Allow **three panels per row only when every panel is simple**. Treat a panel as simple only when it has short labels, few ticks, no dense internal legend, no dense significance brackets, no heatmap-like text density, no long categorical names, and no crowded multi-series geometry.

Block 3+ panels per row when any panel is a dense scatter, heatmap, multi-group line plot, long-label bar chart, complex image + annotation panel, or otherwise requires reduced type to remain legible.

Never reduce the fixed font sizes to justify more columns. Reflow to two columns or one column instead.

Use [scripts/figure_style.py](scripts/figure_style.py) `recommend_columns()` when the layout is generated programmatically. See [references/layout-rules.md](references/layout-rules.md) for the complexity gate.

### 3. Build directly at final physical size

Create the canvas using `create_pub_figure(height_cm=...)`. Do not create an oversized figure and later scale it down.

Use a white background unless the scientific image itself requires a dark image plate. Prefer restrained color families and preserve the same condition/method color across panels.

Remove top and right spines by default. Keep legends frameless. Prefer direct labels or one shared legend when repeated legends waste panel area.

### 4. Preserve one typography system

Use the role constants from `figure_style.py`; do not pass arbitrary `fontsize` values throughout plotting code.

If text does not fit:

1. shorten or wrap wording;
2. reposition the text or legend;
3. change panel arrangement;
4. increase figure height while staying <= 20 cm;
5. move explanatory prose into the caption.

Do **not** solve crowding by shrinking a local font below its role size.

### 5. Render, audit, and revise

Before final delivery:

1. run `python scripts/doctor.py` once per environment;
2. run the plotting script at the final 17 cm width;
3. call `validate_figure(fig)` before export;
4. export with `export_pub_figure(fig, output_base)`;
5. run `python scripts/audit_pdf_text.py figure.pdf --strict` when PyMuPDF is available;
6. inspect the final PDF/PNG panel by panel at final physical size.

Fix any detected clipping, mixed font family, local font-size drift, unreadable 3-column layout, or text smaller than the fixed role contract.

Read [references/qa-rules.md](references/qa-rules.md) for the delivery gate.

## Figure design defaults

- Prefer one hero panel plus subordinate evidence when scientific importance is unequal.
- Use consistent axes and uncertainty definitions for panels that invite direct comparison.
- Avoid rainbow colormaps and red/green as the only differentiator.
- Keep statistical definitions (`n`, center, spread, test, correction) traceable.
- Do not silently drop observations, variables, replicates, or categories to simplify a plot.
- Preserve source-data traceability for every quantitative panel.

## Deliverables

Return the plotting source plus final **PDF + SVG + PNG** when the user asks for rendered outputs. Keep the PDF/SVG as authoritative publication outputs; PNG is the preview.

For a reusable starter, adapt [scripts/example_figure.py](scripts/example_figure.py). Do not copy the example's scientific content into real work.
