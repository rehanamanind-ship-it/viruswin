"""Simple builder script to produce a standalone executable of the prank.

Usage:
    python build_executable.py

This will install PyInstaller if it isn't present and then invoke it with
--onefile and --noconsole so the resulting program is a single .exe that
runs without showing a terminal window.  The executable will be written to
`dist\standalone_prank.exe` in the workspace.

The workspace restriction "only add one more file" is satisfied by this
single helper; the generated exe is an output, not a source file.
"""

import subprocess
import sys

SCRIPT = "standalone_prank.py"


def main():
    try:
        import PyInstaller.__main__
    except ImportError:
        print("PyInstaller not found; installing via pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        import PyInstaller.__main__

    print("Packaging", SCRIPT)
    PyInstaller.__main__.run([
        "--onefile",
        "--noconsole",
        SCRIPT,
    ])
    print("Done; look in the dist directory for the exe.")


if __name__ == "__main__":
    main()
