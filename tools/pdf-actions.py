#!/usr/bin/env python3
"""Report PDF action markers in the files named on the command line.

The CV PDFs are served as they are, so a reader opens them with whatever
those files ask it to run. This scans the raw file and every stream it can
decompress, and prints one line per file with the number of markers found.
Zero is the expected result; anything else is a finding.

    python3 tools/pdf-actions.py src/assets/cv/*.pdf

Standard library only: the publish machine is a shell, not a Python project.
"""

import re
import sys
import zlib

MARKERS = re.compile(rb"/(OpenAction|JavaScript|Launch|SubmitForm)")
STREAM_START = re.compile(rb"stream\r?\n")


def markers_in(path):
    """Return the marker count and the number of streams decompressed."""
    data = open(path, "rb").read()
    found = len(MARKERS.findall(data))
    decompressed = 0

    for match in STREAM_START.finditer(data):
        end = data.find(b"endstream", match.end())
        if end == -1:
            continue
        try:
            body = zlib.decompress(data[match.end():end])
        except zlib.error:
            # Images and already-uncompressed streams: nothing to read here.
            continue
        decompressed += 1
        found += len(MARKERS.findall(body))

    return found, decompressed


def main(paths):
    if not paths:
        print("usage: pdf-actions.py FILE [FILE ...]", file=sys.stderr)
        return 2

    failed = False
    for path in paths:
        try:
            found, decompressed = markers_in(path)
        except OSError as error:
            print("%s: unreadable (%s)" % (path, error), file=sys.stderr)
            failed = True
            continue
        print("%s: %d marker(s), %d stream(s) decompressed" % (path, found, decompressed))
        failed = failed or found > 0

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
