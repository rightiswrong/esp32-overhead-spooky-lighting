#!/usr/bin/env bash
# Compile the show (effects + sound analyser + mixer) for the PC and run the tests:
# synthetic thunder / fire through the real analyser, and Music Assistant cues.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
comp="$here/../../components/spooky_show"
out="${TMPDIR:-/tmp}/spooky-overhead-hosttest"
mkdir -p "$out"
g++ -std=gnu++17 -O1 -g -Wall -Wextra -Wno-unused-parameter -Werror -I"$here/stubs" -I"$comp" -I"$here" \
    -fsanitize=address,undefined -x c++ "$here/test_strip.cpp" "$comp/show_core.cpp" "$comp/Effects.cpp" \
    "$comp/SoundAnalyzer.cpp" "$comp/SoundBus.cpp" "$comp/mic_stream.cpp" -o "$out/test_strip" -lm
"$out/test_strip"
