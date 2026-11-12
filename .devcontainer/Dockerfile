# x86_64 build host + Debian arm64 multiarch sysroot -> real cross-compile (no QEMU, fast).
# DEBIAN_RELEASE must match the Debian base of your DietPi image (current DietPi = trixie / Debian 13;
# use bookworm for a DietPi that is still on Debian 12).
ARG DEBIAN_RELEASE=trixie
FROM debian:${DEBIAN_RELEASE}
ENV DEBIAN_FRONTEND=noninteractive

RUN dpkg --add-architecture arm64 && apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential crossbuild-essential-arm64 cmake ninja-build pkgconf git curl ca-certificates \
      python3 python3-pil fonts-open-sans protobuf-compiler file xz-utils sudo less ccache \
      qt6-base-dev qt6-base-private-dev qt6-base-dev-tools qt6-declarative-dev \
      qt6-shadertools-dev qt6-tools-dev-tools qt6-l10n-tools \
 && rm -rf /var/lib/apt/lists/*

# Target (arm64) development libraries: same list as scripts/install-linux-build-deps.sh
RUN apt-get update && apt-get install -y --no-install-recommends \
      libavcodec-dev:arm64 libavformat-dev:arm64 libavutil-dev:arm64 libswresample-dev:arm64 \
      libchromaprint-dev:arm64 libebur128-dev:arm64 libfftw3-dev:arm64 libflac-dev:arm64 \
      libgmock-dev:arm64 libgtest-dev:arm64 libgl1-mesa-dev:arm64 libhidapi-dev:arm64 \
      libid3tag0-dev:arm64 liblilv-dev:arm64 libmad0-dev:arm64 libmodplug-dev:arm64 \
      libmp3lame-dev:arm64 libmsgsl-dev libogg-dev:arm64 libopus-dev:arm64 libopusfile-dev:arm64 \
      libportmidi-dev:arm64 libprotobuf-dev:arm64 libqt6core5compat6-dev:arm64 \
      libqt6opengl6-dev:arm64 libqt6sql6-sqlite:arm64 libqt6svg6-dev:arm64 \
      librubberband-dev:arm64 libshout-idjc-dev:arm64 libsndfile1-dev:arm64 libsoundtouch-dev:arm64 \
      libsqlite3-dev:arm64 libssl-dev:arm64 libtag1-dev:arm64 libudev-dev:arm64 \
      libupower-glib-dev:arm64 libusb-1.0-0-dev:arm64 libvorbis-dev:arm64 libwavpack-dev:arm64 \
      libx11-dev:arm64 lv2-dev portaudio19-dev:arm64 \
      qt6-base-dev:arm64 qt6-base-private-dev:arm64 qt6-declarative-dev:arm64 \
      qt6-shadertools-dev:arm64 qtkeychain-qt6-dev:arm64 libjack-jackd2-dev:arm64 \
 && rm -rf /var/lib/apt/lists/*
