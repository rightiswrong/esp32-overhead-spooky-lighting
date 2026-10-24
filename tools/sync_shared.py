"""Refresh the shared effects / sound code from Spooky Sound.

The effects engine and the sound analyser live in the XIAO sketch of
https://github.com/rightiswrong/esp32c6-spooky-sound (firmware/XIAO_SpookySound):
an Arduino sketch must contain its own sources. This component carries
identical copies, so the overhead strip hears exactly like the XIAO.

    python3 tools/sync_shared.py [PATH_TO_XIAO_SpookySound]          # copy
    python3 tools/sync_shared.py [PATH_TO_XIAO_SpookySound] --check  # exit 1 if different

PATH defaults to ../esp32c6-spooky-sound/firmware/XIAO_SpookySound.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DST = ROOT / "components" / "spooky_show"
SHARED = ("Effects.h", "Effects.cpp", "SoundAnalyzer.h", "SoundAnalyzer.cpp", "SoundBus.h", "SoundBus.cpp",
          "P9813Chain.h")


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    src_dir = Path(args[0]) if args else ROOT.parent / "esp32c6-spooky-sound" / "firmware" / "XIAO_SpookySound"
    check = "--check" in sys.argv
    stale = []
    for name in SHARED:
        src, dst = (src_dir / name).read_bytes(), DST / name
        if dst.exists() and dst.read_bytes() == src:
            continue
        stale.append(name)
        if not check:
            dst.write_bytes(src)
    if check and stale:
        print("out of date:", *stale, "— run python3 tools/sync_shared.py")
        return 1
    print("copied:" if stale else "in sync", *stale)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
