"""Consistency checks that need no ESPHome: effect names and indices, YAML effect
lists, and the version in packages/base.yaml."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# The names Home Assistant, the XIAO / NanoC6 firmware and the Spooky Sound
# integration all use (Effects.cpp EFFECT_NAMES).
EXPECTED = ("Solid", "Candle Flicker", "Ghost Breath", "Lightning Storm", "Witch's Cauldron", "Tell-Tale Heart",
            "Haunted Chase", "Poltergeist", "Possessed Pumpkin", "Blood Moon")


def main() -> int:
    errors = []
    comp = (ROOT / "components" / "spooky_show" / "__init__.py").read_text()
    pairs = re.findall(r'"(\w+)": \((\d+), "([^"]+)"\)', comp)
    if tuple(n for _, _, n in pairs) != EXPECTED or [int(i) for _, i, _ in pairs] != list(range(10)):
        errors.append(f"component EFFECTS {pairs} != {EXPECTED}")
    fx = (ROOT / "components" / "spooky_show" / "Effects.cpp").read_text()
    for name in EXPECTED:
        if f'"{name}"' not in fx:
            errors.append(f"Effects.cpp lacks {name!r}")
    keys = {k for k, _, _ in pairs}
    for strip in ("rgb", "rgbw", "rgbcct"):
        used = set(re.findall(r"spooky: \{effect: (\w+)\}", (ROOT / "packages" / f"strip-{strip}.yaml").read_text()))
        if used != keys:
            errors.append(f"strip-{strip}.yaml effects {sorted(used)} != {sorted(keys)}")
    if not re.search(r'version: "\d+\.\d+\.\d+"', (ROOT / "packages" / "base.yaml").read_text()):
        errors.append("packages/base.yaml has no project version")
    for e in errors:
        print("FAIL", e)
    print("ok" if not errors else f"{len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
