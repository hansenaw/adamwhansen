"""Wraps a small PNG (e.g. 32x32) in an .ico container. Modern browsers accept PNG-in-ICO.

Usage: python3 tools/png2ico.py input.png favicon.ico
"""
import struct
import sys

png = open(sys.argv[1], "rb").read()
width, height = struct.unpack(">II", png[16:24])
header = struct.pack("<HHH", 0, 1, 1)
entry = struct.pack("<BBBBHHII", width % 256, height % 256, 0, 0, 1, 32, len(png), 6 + 16)
with open(sys.argv[2], "wb") as out:
    out.write(header + entry + png)
