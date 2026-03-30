"""Colormap system with built-in colormaps and matplotlib integration.

Provides color interpolation for gradients. Built-in colormaps work
without dependencies. Additional colormaps available if matplotlib is installed.

Attribution
-----------
This module includes colormaps from the following sources:

1. **Scientific colour maps** by Fabio Crameri
   - Website: https://www.fabiocrameri.ch/colourmaps/
   - Perceptually uniform sequential and diverging colormaps
   - Included: bamako, lapaz, bilbao, lipari, vik, roma, bam, managua

2. **colorspace package** - HCL-based colormaps
   - GitHub: https://github.com/retostauffer/python-colorspace
   - Perceptually-based color palettes using HCL (Hue-Chroma-Luminance) space
   - Included: blues_2, purple_blue, red_purple, light_grays, heat_2,
     mint, peach, pinkyl, sunset, oryel, blue_red_2

3. **matplotlib** - plasma colormap
   - The plasma colormap is from matplotlib (Hunter, J. D. (2007))
   - Perceptually uniform sequential colormap
"""

from typing import Callable, Union, Any
from .colors import rgb_to_hex


# Built-in colormaps (no dependencies required)
# Simplified versions with key color stops for interpolation

BUILTIN_CMAPS = {

    # ========================================================================
    # CRAMERI SEQUENTIAL COLORMAPS (perceptually uniform)
    # ========================================================================

    # Bamako: dark blue → yellow (sequential)
    'bamako': [
        (0.004, 0.153, 0.282),
        (0.051, 0.231, 0.427),
        (0.094, 0.310, 0.545),
        (0.157, 0.384, 0.616),
        (0.239, 0.459, 0.663),
        (0.341, 0.533, 0.690),
        (0.459, 0.608, 0.698),
        (0.584, 0.682, 0.690),
        (0.710, 0.757, 0.667),
        (0.831, 0.831, 0.631),
        (0.945, 0.906, 0.584),
        (1.000, 0.984, 0.557),
    ],

    # Lapaz: dark blue → white → orange (sequential with light middle)
    'lapaz': [
        (0.035, 0.063, 0.220),
        (0.118, 0.165, 0.376),
        (0.212, 0.282, 0.502),
        (0.314, 0.408, 0.596),
        (0.424, 0.537, 0.663),
        (0.545, 0.659, 0.714),
        (0.671, 0.773, 0.757),
        (0.800, 0.875, 0.792),
        (0.925, 0.957, 0.820),
        (0.969, 0.910, 0.718),
        (0.953, 0.804, 0.549),
        (0.918, 0.659, 0.329),
    ],

    # Bilbao: white → dark red (sequential)
    'bilbao': [
        (1.000, 1.000, 1.000),
        (0.984, 0.941, 0.910),
        (0.965, 0.882, 0.820),
        (0.941, 0.820, 0.729),
        (0.914, 0.757, 0.639),
        (0.882, 0.690, 0.549),
        (0.847, 0.620, 0.459),
        (0.808, 0.549, 0.369),
        (0.765, 0.475, 0.278),
        (0.718, 0.400, 0.188),
        (0.667, 0.322, 0.098),
        (0.612, 0.243, 0.012),
    ],

    # Lipari: black → yellow → white (sequential through yellow)
    'lipari': [
        (0.012, 0.012, 0.012),
        (0.102, 0.051, 0.071),
        (0.192, 0.090, 0.129),
        (0.282, 0.129, 0.188),
        (0.373, 0.169, 0.247),
        (0.463, 0.208, 0.306),
        (0.553, 0.247, 0.365),
        (0.643, 0.286, 0.424),
        (0.733, 0.486, 0.486),
        (0.824, 0.686, 0.549),
        (0.914, 0.886, 0.612),
        (1.000, 1.000, 0.800),
    ],

    # ========================================================================
    # CRAMERI DIVERGENT COLORMAPS
    # ========================================================================

    # Vik: blue ← white → red (divergent)
    'vik': [
        (0.016, 0.153, 0.267),
        (0.129, 0.263, 0.416),
        (0.255, 0.380, 0.557),
        (0.388, 0.502, 0.678),
        (0.529, 0.627, 0.780),
        (0.675, 0.753, 0.863),
        (0.820, 0.871, 0.933),
        (0.953, 0.957, 0.973),
        (0.973, 0.914, 0.871),
        (0.957, 0.808, 0.718),
        (0.925, 0.675, 0.537),
        (0.875, 0.518, 0.341),
        (0.808, 0.341, 0.145),
        (0.722, 0.157, 0.016),
        (0.616, 0.012, 0.000),
    ],

    # Roma: cyan ← white → brown (divergent)
    'roma': [
        (0.498, 0.051, 0.031),
        (0.600, 0.157, 0.075),
        (0.694, 0.271, 0.129),
        (0.780, 0.392, 0.196),
        (0.855, 0.518, 0.278),
        (0.918, 0.647, 0.376),
        (0.969, 0.776, 0.494),
        (0.992, 0.898, 0.631),
        (0.980, 0.996, 0.796),
        (0.824, 0.949, 0.847),
        (0.631, 0.871, 0.871),
        (0.424, 0.773, 0.871),
        (0.220, 0.659, 0.847),
        (0.035, 0.529, 0.800),
        (0.000, 0.392, 0.729),
    ],

    # Bam: blue ← white → red (divergent, alternative to Vik)
    'bam': [
        (0.012, 0.243, 0.400),
        (0.133, 0.345, 0.502),
        (0.267, 0.455, 0.596),
        (0.408, 0.565, 0.682),
        (0.553, 0.675, 0.757),
        (0.698, 0.784, 0.824),
        (0.839, 0.890, 0.886),
        (0.969, 0.980, 0.945),
        (0.980, 0.933, 0.871),
        (0.957, 0.820, 0.741),
        (0.918, 0.682, 0.580),
        (0.863, 0.522, 0.396),
        (0.792, 0.345, 0.204),
        (0.706, 0.157, 0.027),
        (0.600, 0.000, 0.000),
    ],

    # Managua: purple ← white → green (divergent)
    'managua': [
        (0.310, 0.000, 0.294),
        (0.424, 0.098, 0.384),
        (0.533, 0.212, 0.471),
        (0.635, 0.337, 0.549),
        (0.729, 0.471, 0.620),
        (0.816, 0.608, 0.686),
        (0.894, 0.745, 0.749),
        (0.961, 0.882, 0.812),
        (0.984, 0.992, 0.875),
        (0.878, 0.949, 0.773),
        (0.733, 0.882, 0.651),
        (0.569, 0.800, 0.514),
        (0.388, 0.706, 0.373),
        (0.200, 0.604, 0.231),
        (0.000, 0.486, 0.094),
    ],

    # ========================================================================
    # MATPLOTLIB COLORMAPS
    # ========================================================================

    # Viridis: perceptually uniform sequential (purple → green → yellow)
    'viridis': [
        (0.267004, 0.004874, 0.329415),
        (0.282623, 0.140926, 0.457517),
        (0.253935, 0.265254, 0.529983),
        (0.206756, 0.371758, 0.553117),
        (0.163625, 0.471133, 0.558148),
        (0.127568, 0.566949, 0.550556),
        (0.134692, 0.658636, 0.517649),
        (0.266941, 0.748751, 0.440573),
        (0.477504, 0.821444, 0.318195),
        (0.741388, 0.873449, 0.149561),
        (0.993248, 0.906157, 0.143936),
    ],

    # Plasma: dark blue → purple → yellow (perceptually uniform sequential)
    'plasma': [
        (0.05, 0.03, 0.528),
        (0.241, 0.015, 0.61),
        (0.387, 0.001, 0.654),
        (0.524, 0.025, 0.653),
        (0.651, 0.125, 0.596),
        (0.752, 0.227, 0.513),
        (0.837, 0.329, 0.431),
        (0.907, 0.435, 0.353),
        (0.963, 0.554, 0.272),
        (0.992, 0.681, 0.195),
        (0.987, 0.822, 0.144),
        (0.94, 0.975, 0.131),
    ],

    # Greys: white → black (grayscale sequential)
    'greys': [
        (1.000000, 1.000000, 1.000000),
        (0.941176, 0.941176, 0.941176),
        (0.850980, 0.850980, 0.850980),
        (0.741176, 0.741176, 0.741176),
        (0.588235, 0.588235, 0.588235),
        (0.450980, 0.450980, 0.450980),
        (0.321569, 0.321569, 0.321569),
        (0.145098, 0.145098, 0.145098),
        (0.000000, 0.000000, 0.000000),
    ],

    # ========================================================================
    # HCL COLORMAPS (from colorspace package)
    # ========================================================================

    # Blues 2: dark blue → light gray (HCL sequential)
    'blues_2': [
        (0.008, 0.247, 0.647),
        (0.235, 0.329, 0.651),
        (0.345, 0.408, 0.675),
        (0.435, 0.482, 0.706),
        (0.518, 0.553, 0.737),
        (0.592, 0.62, 0.769),
        (0.663, 0.682, 0.796),
        (0.725, 0.741, 0.824),
        (0.784, 0.792, 0.847),
        (0.831, 0.835, 0.867),
        (0.867, 0.871, 0.878),
        (0.886, 0.886, 0.886),
    ],

    # Purple-Blue: purple → blue → light gray (HCL sequential)
    'purple_blue': [
        (0.42, 0.0, 0.467),
        (0.431, 0.208, 0.529),
        (0.447, 0.322, 0.596),
        (0.471, 0.42, 0.659),
        (0.498, 0.514, 0.714),
        (0.533, 0.596, 0.769),
        (0.58, 0.678, 0.812),
        (0.635, 0.753, 0.851),
        (0.698, 0.82, 0.886),
        (0.773, 0.875, 0.918),
        (0.851, 0.922, 0.937),
        (0.945, 0.945, 0.945),
    ],

    # Red-Purple: dark red → purple → light gray (HCL sequential)
    'red_purple': [
        (0.49, 0.004, 0.071),
        (0.576, 0.125, 0.251),
        (0.651, 0.224, 0.384),
        (0.718, 0.314, 0.498),
        (0.773, 0.404, 0.604),
        (0.82, 0.494, 0.702),
        (0.855, 0.584, 0.788),
        (0.886, 0.671, 0.863),
        (0.906, 0.749, 0.922),
        (0.925, 0.824, 0.965),
        (0.941, 0.89, 0.988),
        (0.949, 0.941, 0.965),
    ],

    # Light Grays: dark gray → light gray (HCL sequential)
    'light_grays': [
        (0.278, 0.278, 0.278),
        (0.349, 0.349, 0.349),
        (0.424, 0.424, 0.424),
        (0.494, 0.494, 0.494),
        (0.561, 0.561, 0.561),
        (0.627, 0.627, 0.627),
        (0.686, 0.686, 0.686),
        (0.745, 0.745, 0.745),
        (0.792, 0.792, 0.792),
        (0.835, 0.835, 0.835),
        (0.871, 0.871, 0.871),
        (0.886, 0.886, 0.886),
    ],

    # Heat 2: red → orange → yellow-green (HCL sequential)
    'heat_2': [
        (0.827, 0.247, 0.416),
        (0.851, 0.322, 0.376),
        (0.871, 0.388, 0.333),
        (0.886, 0.455, 0.286),
        (0.902, 0.514, 0.239),
        (0.91, 0.576, 0.192),
        (0.914, 0.635, 0.161),
        (0.918, 0.694, 0.165),
        (0.914, 0.753, 0.216),
        (0.906, 0.808, 0.298),
        (0.894, 0.863, 0.408),
        (0.886, 0.902, 0.741),
    ],

    # Mint: dark teal → mint green (HCL sequential)
    'mint': [
        (0.0, 0.365, 0.404),
        (0.0, 0.416, 0.435),
        (0.0, 0.467, 0.471),
        (0.145, 0.522, 0.506),
        (0.255, 0.576, 0.545),
        (0.349, 0.627, 0.584),
        (0.435, 0.682, 0.624),
        (0.518, 0.737, 0.671),
        (0.6, 0.792, 0.718),
        (0.686, 0.847, 0.769),
        (0.773, 0.902, 0.827),
        (0.878, 0.949, 0.902),
    ],

    # Peach: coral → peach (HCL sequential)
    'peach': [
        (0.918, 0.298, 0.231),
        (0.929, 0.373, 0.255),
        (0.937, 0.435, 0.286),
        (0.949, 0.494, 0.329),
        (0.957, 0.553, 0.373),
        (0.961, 0.604, 0.424),
        (0.969, 0.655, 0.478),
        (0.973, 0.702, 0.537),
        (0.976, 0.749, 0.596),
        (0.976, 0.792, 0.655),
        (0.98, 0.835, 0.714),
        (0.98, 0.867, 0.765),
    ],

    # PinkYl: pink → yellow (HCL sequential)
    'pinkyl': [
        (0.886, 0.298, 0.502),
        (0.906, 0.376, 0.475),
        (0.925, 0.443, 0.455),
        (0.937, 0.51, 0.439),
        (0.949, 0.573, 0.435),
        (0.961, 0.631, 0.439),
        (0.969, 0.69, 0.459),
        (0.973, 0.749, 0.486),
        (0.976, 0.804, 0.529),
        (0.98, 0.859, 0.584),
        (0.988, 0.91, 0.643),
        (0.992, 0.965, 0.71),
    ],

    # Sunset: purple → orange → yellow (HCL sequential)
    'sunset': [
        (0.439, 0.302, 0.62),
        (0.561, 0.314, 0.647),
        (0.667, 0.329, 0.663),
        (0.761, 0.361, 0.659),
        (0.839, 0.404, 0.643),
        (0.902, 0.455, 0.612),
        (0.945, 0.525, 0.573),
        (0.965, 0.6, 0.537),
        (0.976, 0.678, 0.51),
        (0.976, 0.757, 0.51),
        (0.969, 0.831, 0.537),
        (0.953, 0.906, 0.604),
    ],

    # OrYel: orange → yellow (HCL sequential)
    'oryel': [
        (0.937, 0.282, 0.408),
        (0.961, 0.337, 0.357),
        (0.961, 0.408, 0.322),
        (0.961, 0.471, 0.294),
        (0.961, 0.525, 0.282),
        (0.957, 0.58, 0.286),
        (0.949, 0.631, 0.314),
        (0.945, 0.678, 0.353),
        (0.937, 0.725, 0.404),
        (0.933, 0.769, 0.467),
        (0.929, 0.812, 0.533),
        (0.925, 0.851, 0.6),
    ],

    # Blue-Red 2: blue ← light gray → red (HCL diverging)
    'blue_red_2': [
        (0.29, 0.435, 0.89),
        (0.427, 0.518, 0.882),
        (0.537, 0.6, 0.882),
        (0.643, 0.678, 0.886),
        (0.741, 0.761, 0.89),
        (0.839, 0.847, 0.89),
        (0.894, 0.831, 0.843),
        (0.902, 0.722, 0.753),
        (0.894, 0.612, 0.667),
        (0.882, 0.502, 0.584),
        (0.859, 0.384, 0.498),
        (0.827, 0.247, 0.416),
    ],

    # ========================================================================
    # CUSTOM SINGLE-HUE GRADIENTS
    # ========================================================================

    # Reds: white → #ff3300 (orange-red)
    'reds': [
        (1.000, 1.000, 1.000),  # white
        (1.000, 0.933, 0.933),
        (1.000, 0.867, 0.867),
        (1.000, 0.800, 0.800),
        (1.000, 0.733, 0.733),
        (1.000, 0.667, 0.667),
        (1.000, 0.600, 0.600),
        (1.000, 0.533, 0.533),
        (1.000, 0.467, 0.467),
        (1.000, 0.400, 0.400),
        (1.000, 0.333, 0.267),
        (1.000, 0.200, 0.000),  # #ff3300
    ],

    # Blues: white → #0099ff (bright blue)
    'blues': [
        (1.000, 1.000, 1.000),  # white
        (0.933, 0.967, 1.000),
        (0.867, 0.933, 1.000),
        (0.800, 0.900, 1.000),
        (0.733, 0.867, 1.000),
        (0.667, 0.833, 1.000),
        (0.600, 0.800, 1.000),
        (0.533, 0.767, 1.000),
        (0.467, 0.733, 1.000),
        (0.400, 0.700, 1.000),
        (0.200, 0.650, 1.000),
        (0.000, 0.600, 1.000),  # #0099ff
    ],

    # Greens: white → #669900 (olive green)
    'greens': [
        (1.000, 1.000, 1.000),  # white
        (0.933, 0.967, 0.933),
        (0.867, 0.933, 0.867),
        (0.800, 0.900, 0.800),
        (0.733, 0.867, 0.733),
        (0.667, 0.833, 0.667),
        (0.600, 0.800, 0.600),
        (0.533, 0.767, 0.533),
        (0.500, 0.733, 0.400),
        (0.467, 0.700, 0.267),
        (0.433, 0.650, 0.133),
        (0.400, 0.600, 0.000),  # #669900
    ],
}

# Generate reversed versions of all colormaps (like matplotlib's _r suffix)
_base_cmaps = dict(BUILTIN_CMAPS)  # Copy the original colormaps
for name, stops in _base_cmaps.items():
    # Add reversed version with _r suffix
    BUILTIN_CMAPS[f"{name}_r"] = list(reversed(stops))


def interpolate_color(stops: list[tuple[float, float, float]], value: float) -> str:
    """Linearly interpolate color from stops.

    Parameters:
        stops: List of RGB tuples (each value 0-1)
        value: Position to interpolate (0-1)

    Returns:
        Hex color string

    Examples:
        >>> interpolate_color([(1, 0, 0), (0, 0, 1)], 0.5)
        '#7F007F'
    """
    # Clamp value to [0, 1]
    value = max(0.0, min(1.0, value))

    # Handle edge cases
    if value == 0.0:
        r, g, b = stops[0]
        return rgb_to_hex(int(r * 255), int(g * 255), int(b * 255))
    if value == 1.0:
        r, g, b = stops[-1]
        return rgb_to_hex(int(r * 255), int(g * 255), int(b * 255))

    # Find surrounding stops
    n_stops = len(stops)
    segment_size = 1.0 / (n_stops - 1)
    segment_idx = int(value / segment_size)

    # Clamp segment index
    segment_idx = min(segment_idx, n_stops - 2)

    # Get surrounding stops
    stop1 = stops[segment_idx]
    stop2 = stops[segment_idx + 1]

    # Local interpolation within segment
    local_value = (value - segment_idx * segment_size) / segment_size

    # Interpolate RGB
    r = stop1[0] + (stop2[0] - stop1[0]) * local_value
    g = stop1[1] + (stop2[1] - stop1[1]) * local_value
    b = stop1[2] + (stop2[2] - stop1[2]) * local_value

    return rgb_to_hex(int(r * 255), int(g * 255), int(b * 255))


def get_colormap(cmap: Union[str, Any]) -> Callable[[float], str]:
    """Get colormap function from name or matplotlib-like colormap object.

    Parameters:
        cmap: Colormap name (str) or matplotlib-like colormap object
              (e.g., 'viridis', 'RdBu', cm.jet, cmocean.cm.thermal)

    Returns:
        Function that maps value in [0, 1] to hex color

    Raises:
        ValueError: If colormap not found or invalid type

    Examples:
        >>> # Using string name
        >>> cmap = get_colormap('viridis')
        >>> cmap(0.5)
        '#21908C'

        >>> # Using matplotlib colormap object
        >>> from matplotlib import cm
        >>> cmap = get_colormap(cm.jet)
        >>> cmap(0.5)
        '#00FFFF'
    """
    # Check if it's a colormap object (duck typing)
    # Matplotlib colormaps (and cmocean, colorcet, etc.) are callable
    if hasattr(cmap, '__call__') and not isinstance(cmap, str):
        # It's a matplotlib-like colormap object
        def mapper(value: float) -> str:
            """Wrapper for matplotlib-like colormap object."""
            rgba = cmap(float(value))
            # Handle RGBA tuple (r, g, b, a) or (r, g, b)
            r, g, b = rgba[0], rgba[1], rgba[2]
            return rgb_to_hex(int(r * 255), int(g * 255), int(b * 255))
        return mapper

    # Otherwise, treat as string name
    if isinstance(cmap, str):
        # Check built-in colormaps first
        if cmap in BUILTIN_CMAPS:
            stops = BUILTIN_CMAPS[cmap]
            return lambda v: interpolate_color(stops, v)

        # Try matplotlib if available
        try:
            import matplotlib.pyplot as plt
            import matplotlib.colors as mcolors

            mpl_cmap = plt.cm.get_cmap(cmap)

            def mpl_wrapper(value: float) -> str:
                """Wrapper for matplotlib colormap."""
                rgba = mpl_cmap(value)
                r, g, b = rgba[0], rgba[1], rgba[2]
                return rgb_to_hex(int(r * 255), int(g * 255), int(b * 255))

            return mpl_wrapper

        except ImportError:
            raise ValueError(
                f"Colormap '{cmap}' not found. Built-in colormaps: {list(BUILTIN_CMAPS.keys())}. "
                f"Install matplotlib for additional colormaps."
            )
        except Exception as e:
            raise ValueError(f"Error loading colormap '{cmap}': {e}")

    # Invalid type
    raise TypeError(
        f"cmap must be a string name or a callable colormap object, got {type(cmap).__name__}"
    )
