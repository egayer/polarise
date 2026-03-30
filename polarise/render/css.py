"""CSS utilities for table rendering."""

from pathlib import Path
from ..utils.colors import normalize_color
from ..fashion.zebra import ZEBRA_DEFAULT_FILL1, ZEBRA_DEFAULT_FILL2


def _load_css_file(filename: str) -> str:
    """Load CSS file from the fashion/css directory.

    Parameters:
        filename: Name of CSS file (e.g., 'grid.css')

    Returns:
        CSS content as string
    """
    css_dir = Path(__file__).parent.parent / "fashion" / "css"
    css_file = css_dir / filename

    if not css_file.exists():
        raise FileNotFoundError(f"CSS file not found: {css_file}")

    return css_file.read_text(encoding='utf-8')


def get_fashion_css(fashion: str | dict) -> str:
    """Get CSS for the specified fashion.

    CSS is loaded from files at runtime, so changes to CSS files
    take effect immediately without restarting Python.

    Parameters:
        fashion: Fashion name ('grid', 'zebra', 'raw', 'scientific')
                 or dict with name and params for zebra

    Returns:
        CSS string

    Raises:
        ValueError: If fashion name not recognized
    """
    # Handle dict format (for parameterized fashions like zebra)
    if isinstance(fashion, dict):
        name = fashion.get('name')
        params = fashion.get('params', {})

        if name == "zebra":
            # Load zebra template and substitute colors
            # Use defaults from zebra.py if not specified
            fill1 = params.get('fill1') or ZEBRA_DEFAULT_FILL1
            fill2 = params.get('fill2') or ZEBRA_DEFAULT_FILL2

            # Normalize color names to hex
            color1 = normalize_color(fill1) if not fill1.startswith('#') else fill1
            color2 = normalize_color(fill2) if not fill2.startswith('#') else fill2

            # Load template and substitute
            template = _load_css_file('zebra.css')
            return template.replace('{COLOR1}', color1).replace('{COLOR2}', color2)
        else:
            # For non-parameterized fashions, fall through
            fashion = name

    # Handle string format - load from files
    if fashion == "grid":
        return _load_css_file('grid.css')
    elif fashion == "zebra":
        # Use default zebra colors from zebra.py
        color1 = normalize_color(ZEBRA_DEFAULT_FILL1) if not ZEBRA_DEFAULT_FILL1.startswith('#') else ZEBRA_DEFAULT_FILL1
        color2 = normalize_color(ZEBRA_DEFAULT_FILL2) if not ZEBRA_DEFAULT_FILL2.startswith('#') else ZEBRA_DEFAULT_FILL2
        template = _load_css_file('zebra.css')
        return template.replace('{COLOR1}', color1).replace('{COLOR2}', color2)
    elif fashion == "raw":
        return _load_css_file('raw.css')
    elif fashion == "scientific":
        return _load_css_file('scientific.css')
    elif fashion == "minimal":
        return _load_css_file('minimal.css')
    elif fashion == "compact":
        return _load_css_file('compact.css')
    elif fashion == "presentation":
        return _load_css_file('presentation.css')
    else:
        raise ValueError(f"Unknown fashion: {fashion}")
