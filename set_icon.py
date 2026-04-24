#!/usr/bin/env python3
"""Attach a custom icon to a file on macOS.

Usage:
    python3 set_icon.py <icon_image> <target_file>

Requires pyobjc-framework-Cocoa (pip install pyobjc-framework-Cocoa).
Uses NSWorkspace.setIcon_forFile_options_ under the hood.
"""
import os
import sys


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)

    icon_path = os.path.abspath(sys.argv[1])
    target_path = os.path.abspath(sys.argv[2])

    if not os.path.isfile(icon_path):
        print(f"ERROR: icon file not found: {icon_path}")
        sys.exit(1)
    if not os.path.exists(target_path):
        print(f"ERROR: target file not found: {target_path}")
        sys.exit(1)

    try:
        from Cocoa import NSImage, NSWorkspace
    except ImportError:
        print(
            "ERROR: pyobjc-framework-Cocoa is not installed.\n"
            "Install it with:  pip install pyobjc-framework-Cocoa"
        )
        sys.exit(1)

    image = NSImage.alloc().initWithContentsOfFile_(icon_path)
    if image is None:
        print(f"ERROR: could not load image: {icon_path}")
        sys.exit(1)

    ok = NSWorkspace.sharedWorkspace().setIcon_forFile_options_(
        image, target_path, 0
    )
    if not ok:
        print(f"ERROR: setIcon_forFile_options_ returned False for {target_path}")
        sys.exit(1)

    print(f"Custom icon attached to {target_path}")


if __name__ == "__main__":
    main()
