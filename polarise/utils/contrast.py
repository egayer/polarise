"""WCAG-based automatic text color contrast calculation.

Implements the WCAG (Web Content Accessibility Guidelines) algorithm
to automatically choose black or white text based on background luminance.
"""

from .colors import hex_to_rgb


def auto_text_color(bg_color: str) -> str:
    """Calculate optimal text color for accessibility.

    Uses WCAG relative luminance formula to determine whether
    black or white text provides better contrast on the given background.

    Parameters:
        bg_color: Background color (hex or named color)

    Returns:
        '#000000' (black) or '#FFFFFF' (white)

    Examples:
        >>> auto_text_color('yellow')
        '#000000'
        >>> auto_text_color('navy')
        '#FFFFFF'
        >>> auto_text_color('#FF0000')
        '#FFFFFF'
    """
    r, g, b = hex_to_rgb(bg_color)

    def linearize(c: int) -> float:
        """Convert 8-bit color to linear RGB."""
        c_norm = c / 255.0
        if c_norm <= 0.03928:
            return c_norm / 12.92
        else:
            return ((c_norm + 0.055) / 1.055) ** 2.4

    # WCAG relative luminance formula
    luminance = (
        0.2126 * linearize(r) +
        0.7152 * linearize(g) +
        0.0722 * linearize(b)
    )

    # Return white for dark backgrounds, black for light backgrounds
    return '#FFFFFF' if luminance < 0.5 else '#000000'
