#!/usr/bin/env python3
"""Extract colormap stops from .cpt files into BUILTIN_CMAPS-ready Python dict entries.

Usage:
    # Single file
    python tools/extract_cpt.py tools/cpt_files/bamako.cpt

    # Batch — all .cpt files listed in tools/cpt_colormaps.md
    python tools/extract_cpt.py --file tools/cpt_colormaps.md
"""

import sys
import re
from pathlib import Path


CPT_FILES_DIR = Path(__file__).parent / "cpt_files"
SECTION_WIDTH = 76  # total width of section separator line (4-space indent + # + text)


def parse_cpt(path: Path) -> tuple[list[tuple[float, float, float]], dict[str, str]]:
    """Parse a .cpt file and return (stops, metadata).

    stops: list of (R, G, B) tuples, values in [0, 1], rounded to 3 decimal places.
    metadata: dict with keys from .cpt header comments.
    """
    stops = []
    meta = {}
    last_rgb2 = None

    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Collect metadata from comment lines
        if line.startswith("#"):
            if line.startswith("# cpt-city:"):
                meta["source"] = line.split("# cpt-city:")[1].strip()
            elif line.startswith("# author:"):
                meta["author"] = line.split("# author:")[1].strip()
            elif line.startswith("# copyright:"):
                meta["copyright"] = line.split("# copyright:")[1].strip()
            continue

        # Skip B/F/N special lines
        if re.match(r"^[BFN](\s|$)", line):
            continue

        parts = line.split()
        if not parts:
            continue

        if "/" in line:
            # Slash format: pos1 R/G/B pos2 R/G/B
            # e.g. "0.000000   140/2/115  0.003922   141/4/114"
            if len(parts) < 4:
                continue
            try:
                r1, g1, b1 = (int(x) for x in parts[1].split("/"))
                r2, g2, b2 = (int(x) for x in parts[3].split("/"))
            except ValueError:
                continue
        else:
            # Space format: pos1 R G B pos2 R G B
            # e.g. "0 236 122 36  50 206 93 128"
            if len(parts) < 8:
                continue
            try:
                r1, g1, b1 = int(parts[1]), int(parts[2]), int(parts[3])
                r2, g2, b2 = int(parts[5]), int(parts[6]), int(parts[7])
            except ValueError:
                continue

        stops.append((round(r1 / 255, 3), round(g1 / 255, 3), round(b1 / 255, 3)))
        last_rgb2 = (round(r2 / 255, 3), round(g2 / 255, 3), round(b2 / 255, 3))

    if last_rgb2 is not None:
        stops.append(last_rgb2)

    return stops, meta


def format_entry(name: str, stops: list, meta: dict) -> str:
    """Format a single colormap entry as a ready-to-paste Python dict block."""
    source = meta.get("source", "")
    author = meta.get("author", "")
    copyright_ = meta.get("copyright", "")

    header = f"# {name}: cpt-city {source} | {author} | {copyright_}"
    lines = [f"    {header}"]
    lines.append(f"    '{name}': [")
    for r, g, b in stops:
        lines.append(f"        ({r}, {g}, {b}),")
    lines.append("    ],")
    lines.append("")
    return "\n".join(lines)


def section_header(section_name: str) -> str:
    """Format a BUILTIN_CMAPS section separator comment."""
    label = section_name.upper()
    # "    # ── LABEL ──...──" padded to SECTION_WIDTH chars total
    prefix = f"    # ── {label} "
    dashes = "─" * max(4, SECTION_WIDTH - len(prefix))
    return f"\n{prefix}{dashes}\n"


def resolve_path(entry: str) -> Path:
    """Resolve a cpt_colormaps.md entry to an absolute Path.

    Accepts:
    - Bare name:  "hawaii"  → tools/cpt_files/hawaii.cpt
    - With ext:   "hawaii.cpt" → tools/cpt_files/hawaii.cpt
    - With path:  "tools/cpt_files/hawaii.cpt" → resolved relative to repo root
    """
    entry = entry.strip()
    if "/" in entry:
        p = Path(entry)
        if not p.is_absolute():
            p = Path(__file__).parent.parent / p
        return p
    # bare name
    stem = entry if not entry.endswith(".cpt") else entry[:-4]
    return CPT_FILES_DIR / f"{stem}.cpt"


def parse_colormaps_md(md_path: Path) -> list[tuple[str, list[str]]]:
    """Parse cpt_colormaps.md → list of (section_name, [entries])."""
    sections: list[tuple[str, list[str]]] = []
    current_section: str | None = None
    current_entries: list[str] = []

    with open(md_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("##"):
                if current_section is not None:
                    sections.append((current_section, current_entries))
                current_section = line.lstrip("#").strip()
                current_entries = []
            elif line.startswith("-"):
                entry = line.lstrip("-").strip()
                if entry:
                    current_entries.append(entry)

    if current_section is not None:
        sections.append((current_section, current_entries))

    return sections


def process_single(cpt_path: Path) -> None:
    """Process one .cpt file and print the dict entry."""
    name = cpt_path.stem.lower()
    stops, meta = parse_cpt(cpt_path)
    print(format_entry(name, stops, meta))
    print(f"# → {len(stops)} stops", file=sys.stderr)


def process_batch(md_path: Path) -> None:
    """Process all .cpt files listed in cpt_colormaps.md."""
    sections = parse_colormaps_md(md_path)
    parts = []

    for section_name, entries in sections:
        if not entries:
            continue
        parts.append(section_header(section_name))
        for entry in entries:
            cpt_path = resolve_path(entry)
            if not cpt_path.exists():
                print(f"WARNING: {cpt_path} not found — skipping.", file=sys.stderr)
                continue
            name = cpt_path.stem.lower()
            stops, meta = parse_cpt(cpt_path)
            parts.append(format_entry(name, stops, meta))
            print(f"  {name}: {len(stops)} stops", file=sys.stderr)

    print("".join(parts))


def main() -> None:
    args = sys.argv[1:]

    if "--file" in args:
        idx = args.index("--file")
        if idx + 1 >= len(args):
            print("Error: --file requires a path argument", file=sys.stderr)
            sys.exit(1)
        md_path = Path(args[idx + 1])
        if not md_path.exists():
            print(f"Error: {md_path} not found", file=sys.stderr)
            sys.exit(1)
        process_batch(md_path)
    elif args:
        cpt_path = Path(args[0])
        if not cpt_path.exists():
            print(f"Error: {cpt_path} not found", file=sys.stderr)
            sys.exit(1)
        process_single(cpt_path)
    else:
        print(__doc__, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
