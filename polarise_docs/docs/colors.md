# Colors & Colormaps

polarise ships with a carefully curated set of colors and colormaps — no matplotlib required.
Colors are available as named strings in any `fill=` or `color=` parameter.
Colormaps are available in any `cmap=` parameter.

## Sources & Attribution

polarise's built-in colormaps come from four sources:

| Source | Type | Colormaps |
|--------|------|-----------|
| [Fabio Crameri (v8.0)](https://www.fabiocrameri.ch/colourmaps/) | Sequential & Divergent | bamako, lapaz, bilbao, lipari, vik, roma, bam, managua |
| [colorspace (HCL)](https://python-colorspace.readthedocs.io/) | Sequential & Divergent | blues_2, purple_blue, red_purple, heat_2, mint, peach, pinkyl, sunset, oryel, blue_red_2 |
| [matplotlib](https://matplotlib.org/stable/gallery/color/colormap_reference.html) | Sequential | viridis, plasma |
| [IBM Carbon Design](https://carbondesignsystem.com/) | Alert colors | alert_red, alert_orange, alert_yellow, alert_green |

Crameri colormaps are perceptually uniform and optimized for scientific use.
HCL colormaps are generated using the `colorspace` package's hue-chroma-luminance model.

## Reference

{{ read_html('snippets/color_reference_body.html') }}
