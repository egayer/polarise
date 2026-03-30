"""Color utilities for Polarise.

Provides named color definitions and color format conversion utilities.

Attribution
-----------
This module includes colors from the following sources:

1. **CSS standard colors** - Common web colors
   - Basic colors: red, blue, green, yellow, orange, purple, pink
   - Grays: black, white, gray, lightgray, darkgray, silver
   - Additional: navy, steelblue, lightblue, darkgreen, darkred, gold, brown,
     lightgreen, olivegreen

2. **IBM Carbon Design System** - Alert/status colors
   - Website: https://carbondesignsystem.com/
   - Alert colors for consistent status indication
   - Included: alert_red, alert_orange, alert_yellow, alert_green
"""

# Named colors
CSS_COLORS = {
    # Basic CSS colors
    'red': '#FF0000',
    'yellow': '#FFFF00',
    'blue': '#0000FF',
    'green': '#008000',
    'navy': '#000080',
    'steelblue': '#4682B4',
    'lightblue': '#ADD8E6',
    'orange': '#FFA500',
    'purple': '#800080',
    'pink': '#FFC0CB',
    'gray': '#808080',
    'lightgray': '#D3D3D3',
    'darkgray': '#A9A9A9',
    'black': '#000000',
    'white': '#FFFFFF',
    'darkgreen': '#006400',
    'darkred': '#8B0000',
    'gold': '#FFD700',
    'silver': '#C0C0C0',
    'brown': '#A52A2A',
    'lightgreen': '#90EE90',
    'olivegreen': '#6B8E23',

    # IBM Carbon Design System alert colors
    'alert_red': '#DA1E28',      # rgb(218, 30, 40) - Error/danger
    'alert_orange': '#FF832B',   # rgb(255, 131, 43) - Serious warning
    'alert_yellow': '#FDDC69',   # rgb(253, 220, 105) - Warning
    'alert_green': '#24A148',    # rgb(36, 161, 72) - Success/normal
}


def normalize_color(color: str) -> str:
    """Convert named color to hex format.

    Parameters:
        color: Color name (e.g., 'red') or hex (e.g., '#FF0000')

    Returns:
        Hex color code (e.g., '#FF0000')

    Examples:
        >>> normalize_color('red')
        '#FF0000'
        >>> normalize_color('#FF0000')
        '#FF0000'
    """
    if color.startswith('#'):
        return color
    return CSS_COLORS.get(color.lower(), color)


def hex_to_rgb(color: str) -> tuple[int, int, int]:
    """Parse hex color to RGB tuple.

    Parameters:
        color: Hex color (e.g., '#FF0000') or named color (e.g., 'red')

    Returns:
        RGB tuple (each value 0-255)

    Examples:
        >>> hex_to_rgb('#FF0000')
        (255, 0, 0)
        >>> hex_to_rgb('red')
        (255, 0, 0)
    """
    color = normalize_color(color).lstrip('#')
    return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB values to hex color.

    Parameters:
        r: Red value (0-255)
        g: Green value (0-255)
        b: Blue value (0-255)

    Returns:
        Hex color code

    Examples:
        >>> rgb_to_hex(255, 0, 0)
        '#FF0000'
    """
    return f'#{r:02X}{g:02X}{b:02X}'
