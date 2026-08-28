# Layout rules

## Fixed physical canvas

- final width: exactly 17.0 cm
- final height: > 0 and <= 20.0 cm
- build directly at final size
- final export must not crop the figure box with `bbox_inches="tight"`

## Panels per row

Default: 1 or 2.

Three panels per row are allowed only when every panel is simple. A simple panel normally satisfies all of the following:

- <= 3 primary series/groups
- <= 6 major x ticks and <= 6 major y ticks
- short axis/tick labels
- no long rotated categorical labels
- no dense internal legend
- <= 1 compact significance bracket/annotation stack
- no per-point labels
- no dense heatmap matrix labels
- no complex image annotations
- no need to shrink any fixed role font

If any condition is violated, use <= 2 panels per row.

Four or more panels per row are blocked by default. Use them only when the user explicitly requests a micro-panel layout and the final-size QA proves every label and tick is readable without changing the fixed font sizes.

## Reflow priority

When a layout is crowded, fix it in this order:

1. reduce columns per row;
2. increase height while staying <= 20 cm;
3. shorten/wrap labels;
4. use a shared legend or direct labels;
5. move explanatory prose to the caption.

Never shrink local type to rescue a crowded layout.
