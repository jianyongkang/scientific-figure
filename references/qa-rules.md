# QA rules

A figure is not ready because the plotting code ran successfully. Audit the final render.

## Blocking checks

- width is exactly 17.0 cm within floating-point tolerance
- height does not exceed 20.0 cm
- Times New Roman is configured for ordinary text
- all standard text uses the fixed role sizes: 10/9/8/7 pt as defined by the skill
- no panel was scaled independently after plotting
- no final export uses `bbox_inches="tight"`
- no clipped titles, labels, legends, annotations, or panel letters
- 3-column rows are used only for genuinely simple plots
- source data and uncertainty definitions remain traceable

## Final visual inspection

Inspect each panel separately, then the assembled figure. Ask:

- Are tick labels readable at 17 cm final width?
- Does any text collide with data, error bars, or another text item?
- Are comparable axes/units/uncertainty definitions consistent?
- Is the important evidence more visually salient than baselines?
- Would removing a panel leave the scientific claim unchanged?
- Did any workaround make one panel use smaller text than the others?

If the answer to the last question is yes, reflow the layout rather than accepting the figure.
