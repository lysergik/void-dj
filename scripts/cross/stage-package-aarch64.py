#!/usr/bin/env python3
# Runs packaging/linux/stage-package.py but reports the TARGET architecture (aarch64) instead of the build host's.
import platform, runpy, sys
platform.machine = lambda: 'aarch64'
sys.argv = sys.argv[1:]
runpy.run_path(sys.argv[0], run_name='__main__')
