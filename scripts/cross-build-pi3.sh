#!/bin/sh
# Cross-compile NauticMixxx (Mixxx 2.5.6 + patches) on x86_64 for a Raspberry Pi 3B running 64-bit DietPi.
# Mirrors scripts/build-mixxx-rx3-linux.sh (same patches, flags, branding) but with an aarch64 toolchain.
#
#   ./scripts/cross-build-pi3.sh            # resumable: re-run after an interruption, ninja continues
#   RX3_BUILD_JOBS=4 RX3_BUILD_ROOT=/workspaces/build ./scripts/cross-build-pi3.sh
set -eu
project=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
version=$(cat "$project/VERSION")
work=${RX3_BUILD_ROOT:-"$project/build/pi3-aarch64"}
jobs=${RX3_BUILD_JOBS:-$(nproc)}
tune=${RX3_CPU_TUNE:-cortex-a53}            # Pi 3B; -mtune only, ISA stays portable ARMv8
tc="$project/scripts/cross/toolchain-pi3-aarch64.cmake"
mkdir -p "$work"; work=$(CDPATH= cd -- "$work" && pwd)

archive="$work/mixxx-2.5.6.tar.gz"
[ -f "$archive" ] || curl --fail --location --retry 3 \
  https://github.com/mixxxdj/mixxx/archive/refs/tags/2.5.6.tar.gz -o "$archive"
printf '%s  %s\n' 9cfc9025d50d2511767ee52a07b8854f75c581f0585197d043bc219fcf9f9050 "$archive" | sha256sum -c -

src="$work/mixxx-2.5.6"
digest=$(cat "$project"/patches/00[0-9][0-9]-*.patch | sha256sum | cut -d ' ' -f 1)
[ -d "$src" ] || tar -xzf "$archive" -C "$work"
if [ ! -f "$src/.rx3-patched" ]; then
  for p in "$project"/patches/00[0-9][0-9]-*.patch; do
    (cd "$src" && GIT_CEILING_DIRECTORIES="$work" git apply --no-index "$p")
  done
  printf '%s\n' "$digest" > "$src/.rx3-patched"
fi
[ "$(cat "$src/.rx3-patched")" = "$digest" ] || { echo 'Patches changed; use a fresh RX3_BUILD_ROOT.' >&2; exit 1; }
python3 "$project/packaging/linux/prepare-branding.py" "$src" "$project"

cmake -S "$src" -B "$work/cross" -G Ninja -DCMAKE_TOOLCHAIN_FILE="$tc" \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
  -DNAUTICMIX_VERSION="$version" -DCMAKE_INSTALL_PREFIX="$work/stage" -DCMAKE_INSTALL_LIBDIR=lib \
  -DQT6=ON -DQML=OFF -DOPTIMIZE=portable -DENGINEPRIME=OFF -DKEYFINDER=OFF \
  -DBUILD_LOW_MEMORY=ON -DCMAKE_DISABLE_PRECOMPILE_HEADERS=ON \
  -DCMAKE_C_FLAGS="-mtune=$tune" -DCMAKE_CXX_FLAGS="-mtune=$tune" \
  -DBUILD_TESTING=OFF -DBUILD_BENCH=OFF
cmake --build "$work/cross" --target mixxx --parallel "$jobs"
cmake --install "$work/cross"
python3 "$project/scripts/cross/stage-package-aarch64.py" "$project/packaging/linux/stage-package.py" \
  "$work/stage" "$src" "$project"

# --- sanity: the binary must be aarch64 -------------------------------------------------
bin=$(find "$work/stage" -type f \( -name mixxx -o -name nauticmixxx \) | head -n 1)
file "$bin" | tee "$work/elf-check.txt"
grep -q 'ARM aarch64' "$work/elf-check.txt" || { echo 'ERROR: binary is not aarch64' >&2; exit 1; }

# --- runtime packages the Pi needs (mapped from the binary's NEEDED libraries) ----------
{
  aarch64-linux-gnu-readelf -d "$bin" | sed -n 's/.*Shared library: \[\(.*\)\]/\1/p' | while read -r so; do
    f=$(find /usr/lib/aarch64-linux-gnu -maxdepth 1 -name "$so" 2>/dev/null | head -n 1)
    [ -n "$f" ] && dpkg -S "$f" 2>/dev/null | cut -d: -f1
  done
  printf '%s\n' qt6-qpa-plugins libqt6sql6-sqlite qt6-svg-plugins xserver-xorg xinit fonts-open-sans
} | sort -u | grep -v '^libc6$' > "$work/pi-runtime-packages.txt"

out="$work/NauticMixxx-$version-pi3-aarch64.tar.gz"
tar -czf "$out" -C "$work" stage pi-runtime-packages.txt
(cd "$work" && sha256sum "$(basename "$out")" > SHA256SUMS.txt)
printf '\nDONE: %s\nOn the Pi:  sudo apt install $(cat pi-runtime-packages.txt)   then run stage/bin/nauticmixxx\n' "$out"
