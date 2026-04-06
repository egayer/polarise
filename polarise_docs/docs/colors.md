# Colors & Colormaps

polarise ships with a curated set of built-in colors and colormaps that work with no additional dependencies. Built-in colormaps cover sequential and divergent use cases and are sourced directly from authoritative [cpt-city](https://phillips.shef.ac.uk/pub/cpt-city/) files for pixel-accurate color reproduction.

When popular visualization packages are installed, polarise seamlessly extends its colormap support to their full collections — including [matplotlib](https://matplotlib.org/), [cmcrameri](https://www.fabiocrameri.ch/colourmaps/) (Fabio Crameri's Scientific Colour Maps), [colorcet](https://colorcet.com/) (Peter Kovesi's ColorCET), and [colorspace](https://python-colorspace.readthedocs.io/) (HCL-based perceptually uniform palettes).

Any colormap — whether built-in or from an optional package — can be reversed by appending `_r` to its name. For example, `nuuk_r` reverses the `nuuk` colormap from cmcrameri, and `CET_L19_r` reverses the built-in `CET_L19`.

Colors are available as named strings in any `fill=` or `color=` parameter. Colormaps are available in any `cmap=` parameter.

## Fixed Colors

{{ read_html('snippets/color_fixed.html') }}

## Colormaps

{{ read_html('snippets/color_cmaps.html') }}

## Sources & References

| Source | Type | Colormaps |
|--------|------|-----------|
| [Fabio Crameri (v8.0.1)](https://www.fabiocrameri.ch/colourmaps/) | Sequential | hawaii, acton, nuuk, lipari, davos, buda |
| [Fabio Crameri (v8.0.1)](https://www.fabiocrameri.ch/colourmaps/) | Divergent | vik, managua |
| [Peter Kovesi / ColorCET](https://colorcet.com/) | Sequential | CET_L17, CET_L19, CET_L20 |
| [Peter Kovesi / ColorCET](https://colorcet.com/) | Divergent | CET_D11, CET_D12, CET_I3 |
| [matplotlib](https://matplotlib.org/stable/gallery/color/colormap_reference.html) | Sequential | viridis, plasma |
| Custom single-hue | Sequential | grays, reds, blues, greens |
| Diane Simoni | Sequential | orange-to-purple |

**Scientific colour maps** by Fabio Crameri — MIT license  
<https://www.fabiocrameri.ch/colourmaps/>  
Perceptually uniform sequential and diverging colormaps, sourced from cpt-city.

**ColorCET** by Peter Kovesi — CC BY 4.0  
<https://colorcet.com/>  
Perceptually uniform colormaps, sourced from cpt-city.

**matplotlib** — Hunter, J. D. (2007). Matplotlib: A 2D graphics environment.  
Perceptually uniform sequential colormaps: viridis, plasma.

**IBM Carbon Design System** — Alert/status colors  
<https://carbondesignsystem.com/>
