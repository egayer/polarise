"""Zebra fashion - Alternating row colors, no grid.

CSS has been moved to: polarise/fashion/css/zebra.css

The CSS file contains a template with {COLOR1} and {COLOR2} placeholders
that are substituted at runtime with the actual colors specified in
fashion_zebra(fill1=..., fill2=...).

This allows for runtime loading - changes to CSS take effect immediately
without restarting Python or reinstalling the package.
"""

# DEFAULT COLORS - Single source of truth
# Change these values to modify the default zebra stripe colors
ZEBRA_DEFAULT_FILL1 = "white"
ZEBRA_DEFAULT_FILL2 = "#f2f2f2"
