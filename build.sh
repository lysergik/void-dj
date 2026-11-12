#!/bin/sh
# NauticMixxx native Linux build wrapper (Mixxx 2.5.6 + patches 0001-0062).
#
#   ./build.sh --root "$PWD/build" [--jobs N] [--tests] [--no-build]
#
# --root   build folder (source tree, cmake dir, stage). It may be on any drive
#          that allows executable files. An existing tree from an earlier
#          archive is brought up to date in place: only the patches it is
#          missing are applied, and only the changed files are recompiled.
set -eu
project=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root=""; jobs=2; tests=OFF; nobuild=0
while [ $# -gt 0 ]; do
  case "$1" in
    --root) root=$2; shift 2 ;;
    --root=*) root=${1#--root=}; shift ;;
    --jobs) jobs=$2; shift 2 ;;
    --tests) tests=ON; shift ;;
    --no-build) nobuild=1; shift ;;
    -h|--help) sed -n 2,11p "$0"; exit 0 ;;
    *) printf 'Unknown option: %s\n' "$1" >&2; exit 1 ;;
  esac
done
[ -n "$root" ] || root="$project/build"
mkdir -p "$root"; root=$(CDPATH= cd -- "$root" && pwd)
tree="$root/mixxx-2.5.6"
total=$(ls "$project"/patches/00[0-9][0-9]-*.patch | wc -l | tr -d ' ')
[ "$total" = 62 ] && [ -f "$project/patches/0062-rx3-usb-eject-and-automount.patch" ] || {
  printf 'Expected 62 patches including 0062-rx3-usb-eject-and-automount.patch, found %s.\n' "$total" >&2; exit 1; }

# sha256 of the concatenation of the first $1 patches (same digest the build
# script stores in .rx3-patched).
digest_upto() {
  ls "$project"/patches/00[0-9][0-9]-*.patch | head -n "$1" | xargs cat | sha256sum | cut -d ' ' -f 1
}

refresh_tree() {
  [ -d "$tree" ] || return 0
  marker="$tree/.rx3-patched"
  new=$(digest_upto "$total")
  [ -f "$marker" ] || return 0
  [ "$(cat "$marker")" != "$new" ] || return 0
  applied=0
  if [ -f "$tree/.rx3-applied" ]; then
    applied=$(cat "$tree/.rx3-applied")
  else
    old=$(cat "$marker")
    n=1
    while [ "$n" -le "$total" ]; do
      if [ "$(digest_upto "$n")" = "$old" ]; then applied=$n; break; fi
      n=$((n + 1))
    done
    # Fallback for trees built from an archive whose patch 0030 differed.
    if [ "$applied" = 0 ] && grep -q 'kStorageRoot' "$tree/src/widget/wrx3browser.h" 2>/dev/null; then
      applied=49
    fi
  fi
  if [ "$applied" = 0 ]; then
    echo 'Cannot tell which patches this tree contains; use a fresh --root.' >&2; exit 1
  fi
  n=$((applied + 1))
  for patch in $(ls "$project"/patches/00[0-9][0-9]-*.patch | tail -n +"$n"); do
    printf 'Applying %s to the existing tree\n' "$(basename "$patch")"
    (cd "$tree" && GIT_CEILING_DIRECTORIES="$root" git apply --no-index "$patch") \
      || { echo "Could not apply $(basename "$patch"); use a fresh --root." >&2; exit 1; }
  done
  printf '%s\n' "$total" > "$tree/.rx3-applied"
  printf '%s\n' "$new" > "$marker"
}

refresh_tree
[ "$nobuild" = 0 ] || exit 0
RX3_BUILD_ROOT="$root" RX3_BUILD_JOBS="$jobs" RX3_BUILD_TESTING="$tests" \
  exec sh "$project/scripts/build-mixxx-rx3-linux.sh"
