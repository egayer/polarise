"""Dev-only tool: extract Crameri colormap color stops from cmcrameri.

Usage:
    python tools/extract_crameri.py

Output is printed to stdout. Review it, then paste the entries directly
into the BUILTIN_CMAPS dict in polarise/utils/colormaps.py, replacing
the existing Crameri entries.
"""

import sys

import numpy as np

try:
    import cmcrameri.cm as cmc
except ImportError:
    print(
        "ERROR: cmcrameri is not installed.\n"
        "Install it with:  pip install cmcrameri",
        file=sys.stderr,
    )
    sys.exit(1)

try:
    from importlib.metadata import version
    crameri_version = version("cmcrameri")
except Exception:
    crameri_version = "unknown"


# ── map definitions ──────────────────────────────────────────────────────────

SEQUENTIAL_MAPS = [
    ("bamako",  12, "dark green → yellow",        "sequential"),
    ("lapaz",   12, "dark blue → white → orange", "sequential"),
    ("bilbao",  12, "white → dark red",           "sequential"),
    ("lipari",  12, "black → yellow → white",     "sequential"),
]

DIVERGENT_MAPS = [
    ("vik",     15, "blue ← white → red",           "divergent"),
    ("roma",    15, "blue ← white → red-brown",     "divergent"),
    ("bam",     15, "blue ← green → red",           "divergent"),
    ("managua", 15, "purple ← white → green",       "divergent"),
]


def extract_stops(cmap_name: str, n_stops: int) -> list[tuple[float, float, float]]:
    """Return n_stops evenly-spaced RGB tuples from a cmcrameri colormap."""
    cmap = getattr(cmc, cmap_name)
    positions = np.linspace(0, 1, n_stops)
    stops = []
    for t in positions:
        r, g, b, _a = cmap(float(t))
        stops.append((round(r, 3), round(g, 3), round(b, 3)))
    return stops


def format_entry(
    name: str,
    label: str,
    kind: str,
    stops: list[tuple[float, float, float]],
    ver: str,
) -> str:
    """Format one colormap entry as ready-to-paste Python source."""
    lines = []
    display = name.capitalize()
    lines.append(f"    # {display}: {label} (Crameri v{ver}, {kind})")
    lines.append(f"    '{name}': [")
    for r, g, b in stops:
        lines.append(f"        ({r:.3f}, {g:.3f}, {b:.3f}),")
    lines.append("    ],")
    lines.append("")
    return "\n".join(lines)


SEP     = "    # ────────────────────────────────────────────────────────────────────────"
HDR_SEQ = "    # ── CRAMERI SEQUENTIAL ──────────────────────────────────────────────────"
HDR_DIV = "    # ── CRAMERI DIVERGENT ───────────────────────────────────────────────────"


def main() -> None:
    print(
        "# ============================================================================\n"
        "# Paste the following entries into BUILTIN_CMAPS in polarise/utils/colormaps.py\n"
        "# replacing the existing Crameri entries.\n"
        f"# Generated from cmcrameri v{crameri_version}\n"
        "# ============================================================================\n"
    )

    print(HDR_SEQ)
    print()
    for i, (name, n, label, kind) in enumerate(SEQUENTIAL_MAPS):
        stops = extract_stops(name, n)
        print(format_entry(name, label, kind, stops, crameri_version))
        if i < len(SEQUENTIAL_MAPS) - 1:
            print(SEP)
            print()

    print(SEP)
    print()
    print(HDR_DIV)
    print()
    for i, (name, n, label, kind) in enumerate(DIVERGENT_MAPS):
        stops = extract_stops(name, n)
        print(format_entry(name, label, kind, stops, crameri_version))
        if i < len(DIVERGENT_MAPS) - 1:
            print(SEP)
            print()


if __name__ == "__main__":
    main()
