# CMake toolchain: x86_64 Debian host -> Debian arm64 (Raspberry Pi 3B, Cortex-A53), multiarch sysroot.
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)
set(CMAKE_C_COMPILER aarch64-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER aarch64-linux-gnu-g++)
set(CMAKE_LIBRARY_ARCHITECTURE aarch64-linux-gnu)
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)   # host tools: moc, rcc, protoc, qsb, lrelease...
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY BOTH)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE BOTH)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE BOTH)
set(ENV{PKG_CONFIG_PATH} "")
set(ENV{PKG_CONFIG_LIBDIR} "/usr/lib/aarch64-linux-gnu/pkgconfig:/usr/lib/pkgconfig:/usr/share/pkgconfig")
# Qt6 cross: host tools come from the amd64 Qt packages.
set(QT_HOST_PATH /usr CACHE PATH "")
set(QT_HOST_PATH_CMAKE_DIR /usr/lib/x86_64-linux-gnu/cmake CACHE PATH "")
