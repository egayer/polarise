"""Dev-only tool: extract color stops from crameri / HCL / matplotlib sources.

Usage — single colormap:
    python tools/extract_colormap.py --source crameri --name oslo --stops 12
    python tools/extract_colormap.py --source hcl --name ag_sunset --stops 12
    python tools/extract_colormap.py --source matplotlib --name cividis --stops 12

Usage — batch from file:
    python tools/extract_colormap.py --file tools/new_colormaps.md

Output is printed to stdout. Review it, then paste the entries into the
appropriate section of BUILTIN_CMAPS in polarise/utils/colormaps.py.

Section headers used in the output (and in colormaps.py):
    # ── CRAMERI SEQUENTIAL ──────────────────────────────────────────────────
    # ── CRAMERI DIVERGENT ───────────────────────────────────────────────────
    # ── HCL SEQUENTIAL ──────────────────────────────────────────────────────
    # ── HCL DIVERGENT ───────────────────────────────────────────────────────
    # ── MATPLOTLIB ──────────────────────────────────────────────────────────
    # ── CUSTOM ──────────────────────────────────────────────────────────────
"""

import argparse
import re
import sys

import numpy as np


# ── helpers ───────────────────────────────────────────────────────────────────

def _crameri_version():
    try:
        from importlib.metadata import version
        return version("cmcrameri")
    except Exception:
        return "unknown"


def _format_entry(name, label, source_tag, stops):
    """Format one colormap entry as ready-to-paste Python source (4-space indent)."""
    lines = [
        f"    # {name.capitalize()}: {label} ({source_tag})",
        f"    '{name}': [",
    ]
    for r, g, b in stops:
        lines.append(f"        ({r:.3f}, {g:.3f}, {b:.3f}),")
    lines.append("    ],")
    lines.append("")
    return "\n".join(lines)


def _hex_to_rgb(h):
    """Convert '#RRGGBB' to (r, g, b) floats in [0, 1]."""
    h = h.lstrip("#")
    return tuple(round(int(h[i:i+2], 16) / 255, 3) for i in (0, 2, 4))


# ── source extractors ─────────────────────────────────────────────────────────

def extract_crameri(name, n_stops):
    """Extract n_stops RGB tuples from a cmcrameri colormap."""
    try:
        import cmcrameri.cm as cmc
    except ImportError:
        print(
            "ERROR: cmcrameri is not installed.\n"
            "Install it with:  pip install cmcrameri",
            file=sys.stderr,
        )
        return None

    cmap_obj = getattr(cmc, name, None)
    if cmap_obj is None:
        print(f"ERROR: cmcrameri has no colormap named '{name}'.", file=sys.stderr)
        return None

    positions = np.linspace(0, 1, n_stops)
    stops = []
    for t in positions:
        r, g, b, _a = cmap_obj(float(t))
        stops.append((round(r, 3), round(g, 3), round(b, 3)))
    return stops


def extract_hcl(name, n_stops, kind="sequential"):
    """Extract n_stops RGB tuples from a colorspace HCL palette."""
    try:
        import colorspace
    except ImportError:
        print(
            "ERROR: colorspace is not installed.\n"
            "Install it with:  pip install colorspace",
            file=sys.stderr,
        )
        return None

    # Build name variants to try (the colorspace package is case-sensitive)
    variants = [
        name,
        name.lower(),
        name.replace(" ", "_"),
        name.lower().replace(" ", "_"),
        name.replace("-", "_"),
        name.lower().replace("-", "_"),
        name.replace("_", " "),
        name.lower().replace("_", " "),
    ]
    # Remove duplicates while preserving order
    seen = set()
    variants = [v for v in variants if not (v in seen or seen.add(v))]

    constructor = colorspace.sequential_hcl if kind == "sequential" else colorspace.diverging_hcl

    # Try constructor(name)(N) first
    for v in variants:
        try:
            hex_colors = constructor(v)(n_stops)
            return [_hex_to_rgb(h) for h in hex_colors]
        except Exception:
            pass

    # Try hcl_palettes().get_palette(name)(N)
    try:
        palettes = colorspace.hcl_palettes()
        for v in variants:
            try:
                hex_colors = palettes.get_palette(v)(n_stops)
                return [_hex_to_rgb(h) for h in hex_colors]
            except Exception:
                pass
    except Exception:
        pass

    print(
        f"ERROR: HCL colormap '{name}' not found in colorspace.\n"
        f"  Tried variants: {variants}",
        file=sys.stderr,
    )
    return None


def extract_matplotlib(name, n_stops):
    """Extract n_stops RGB tuples from a matplotlib colormap."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print(
            "ERROR: matplotlib is not installed.\n"
            "Install it with:  pip install matplotlib",
            file=sys.stderr,
        )
        return None

    try:
        cmap_obj = plt.cm.get_cmap(name)
    except Exception:
        print(f"ERROR: matplotlib has no colormap named '{name}'.", file=sys.stderr)
        return None

    positions = np.linspace(0, 1, n_stops)
    stops = []
    for t in positions:
        r, g, b, _a = cmap_obj(float(t))
        stops.append((round(r, 3), round(g, 3), round(b, 3)))
    return stops


# ── batch file parser ─────────────────────────────────────────────────────────

# Maps markdown section header → (source, kind, default_stops)
SECTION_MAP = {
    "crameri sequential": ("crameri",    "sequential", 12),
    "crameri divergent":  ("crameri",    "divergent",  15),
    "hcl sequential":     ("hcl",        "sequential", 12),
    "hcl divergent":      ("hcl",        "divergent",  15),
    "matplotlib":         ("matplotlib", "sequential", 12),
    "custom":             ("custom",     "sequential", 12),
}

SECTION_HEADERS = {
    "crameri sequential": "    # ── CRAMERI SEQUENTIAL ──────────────────────────────────────────────────",
    "crameri divergent":  "    # ── CRAMERI DIVERGENT ───────────────────────────────────────────────────",
    "hcl sequential":     "    # ── HCL SEQUENTIAL ──────────────────────────────────────────────────────",
    "hcl divergent":      "    # ── HCL DIVERGENT ───────────────────────────────────────────────────────",
    "matplotlib":         "    # ── MATPLOTLIB ──────────────────────────────────────────────────────────",
    "custom":             "    # ── CUSTOM ──────────────────────────────────────────────────────────────",
}


def parse_batch_file(filepath):
    """Parse new_colormaps.md → list of (name, source, kind, n_stops)."""
    entries = []
    current_source = None
    current_kind = None
    current_stops = 12

    with open(filepath, encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            # Section header: ## Crameri Sequential
            if line.startswith("#"):
                header_text = re.sub(r"^#+\s*", "", line).strip().lower()
                if header_text in SECTION_MAP:
                    current_source, current_kind, current_stops = SECTION_MAP[header_text]
            # Colormap entry: - name
            elif line.startswith("-"):
                name = line.lstrip("- ").strip()
                if name and current_source is not None:
                    entries.append((name, current_source, current_kind, current_stops))

    return entries


# ── source-tag builder ────────────────────────────────────────────────────────

def _source_tag(source, kind):
    ver = _crameri_version() if source == "crameri" else None
    if source == "crameri":
        return f"Crameri v{ver}, {kind}"
    if source == "hcl":
        return f"HCL colorspace, {kind}"
    if source == "matplotlib":
        return "matplotlib"
    return "custom"


# ── single-map mode ───────────────────────────────────────────────────────────

def run_single(source, name, n_stops, kind):
    extractor = {
        "crameri":    lambda: extract_crameri(name, n_stops),
        "hcl":        lambda: extract_hcl(name, n_stops, kind),
        "matplotlib": lambda: extract_matplotlib(name, n_stops),
    }.get(source)

    if extractor is None:
        print(f"ERROR: unknown --source '{source}'. Choose: crameri, hcl, matplotlib", file=sys.stderr)
        sys.exit(1)

    stops = extractor()
    if stops is None:
        sys.exit(1)

    tag = _source_tag(source, kind)
    label = "(add description)"
    print(_format_entry(name, label, tag, stops))


# ── batch mode ────────────────────────────────────────────────────────────────

def run_batch(filepath):
    entries = parse_batch_file(filepath)
    if not entries:
        print("No colormaps found in the batch file.", file=sys.stderr)
        sys.exit(1)

    SEP = "    # ────────────────────────────────────────────────────────────────────────"

    # Group by section key to print section headers once
    current_section_key = None

    for i, (name, source, kind, n_stops) in enumerate(entries):
        section_key = f"{source} {kind}" if source != "matplotlib" else "matplotlib"

        if section_key != current_section_key:
            if current_section_key is not None:
                print()
            if section_key in SECTION_HEADERS:
                print(SECTION_HEADERS[section_key])
                print()
            current_section_key = section_key

        if source == "crameri":
            stops = extract_crameri(name, n_stops)
        elif source == "hcl":
            stops = extract_hcl(name, n_stops, kind)
        elif source == "matplotlib":
            stops = extract_matplotlib(name, n_stops)
        else:
            print(f"ERROR: unknown source '{source}' for '{name}'", file=sys.stderr)
            continue

        if stops is None:
            print(f"    # SKIPPED: {name} (extraction failed)", "")
            continue

        tag = _source_tag(source, kind)
        label = "(add description)"
        print(_format_entry(name, label, tag, stops))

        # Separator between entries within the same section
        next_same_section = (
            i + 1 < len(entries) and
            (f"{entries[i+1][1]} {entries[i+1][2]}" if entries[i+1][1] != "matplotlib"
             else "matplotlib") == section_key
        )
        if next_same_section:
            print(SEP)
            print()


# ── entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Extract colormap stops for polarise/utils/colormaps.py."
    )
    parser.add_argument("--source", choices=["crameri", "hcl", "matplotlib"],
                        help="Colormap source (single-map mode)")
    parser.add_argument("--name",   help="Colormap name (single-map mode)")
    parser.add_argument("--stops",  type=int, default=None,
                        help="Number of stops (default: 12 sequential, 15 divergent)")
    parser.add_argument("--type",   dest="kind", choices=["sequential", "divergent"],
                        default="sequential",
                        help="Colormap type (default: sequential)")
    parser.add_argument("--file",   help="Batch markdown file (batch mode)")
    args = parser.parse_args()

    if args.file:
        run_batch(args.file)
    elif args.source and args.name:
        n = args.stops if args.stops else (15 if args.kind == "divergent" else 12)
        run_single(args.source, args.name, n, args.kind)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
