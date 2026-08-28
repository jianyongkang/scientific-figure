# Scientific Figure

A strict Python publication-figure Skill built around one physical output system:

- exact 17 cm final width
- maximum 20 cm height
- Times New Roman
- fixed role-based type sizes (10/9/8/7 pt)
- same point size = same physical size across every panel
- one or two panels per row by default
- three panels per row only for simple, low-density plots
- PDF + SVG + PNG output with editable vector text

The workflow is claim-first: define the scientific conclusion and evidence roles before plotting, then render directly at final size and audit the final output.

Use `scripts/figure_style.py` as the style/runtime contract instead of redefining figure size and font settings in every plotting script.
