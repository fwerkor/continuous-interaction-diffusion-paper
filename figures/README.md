# CID vector figures

The six figures share a point-based design system: blue for external facts,
purple for thought, green for display, and ochre for runtime operations.
Labels and layout remain intelligible without color.

## Rebuild

Install `matplotlib==3.10.9`, then run `make figures`.
The generator writes matching PDF and SVG files plus temporary PNG previews
under `build/figure-preview/`. Edit `scripts/draw_figures.py` to keep both
formats synchronized. SVG glyphs are outlines; PDF fonts are embedded TrueType.
Fixed metadata and SVG identifiers make regeneration deterministic.

The paper includes the checked-in PDFs directly. Normal LaTeX compilation needs
no Matplotlib, SVG converter, shell escape, or system font installation.
The small TeX wrappers set the intended publication width.
Do not crop with a tight bounding box: the explicit artboards reserve space
for arrowheads, math extents, and labels.

## Visual verification

After editing, regenerate all figures and compile the full paper. Inspect both
the individual PDF/SVG renderings and every page containing a figure at actual
placement size and high resolution. Check label collisions, math subscripts,
arrow endpoints, glyphs, clipping, and figure/caption placement. The generator
rejects text outside the artboard; this complements visual inspection.

The selective-revision figure is an illustrative running example, not an empirical
model trace. Overview TCT rows show example dominant soft roles; roles may
overlap within a cell. The anatomy figure expands one aligned row into a single bounded cell; internal
positions and visual values are schematic, not a neural architecture or a measured state.
