"""Name the Robot Band — make.fun entry.

Writes one line: a funny robot band name plus a few words on its hit song.
The band is a boy band that never finishes loading; the joke lands twice —
once on the name, once on the song that never arrives.
"""

import os
import sys

ENTRY_TEXT = (
    "The Buffering Boys \u2014 their hit single \u2018Loading\u2026\u2019 "
    "has been stuck at 99% since 2019, and fans are still waiting for the drop."
)


def _env_path(name):
    """Return the raw value of an env var, or None when unset/blank."""
    value = os.environ.get(name)
    if value is None:
        return None
    value = value.strip()
    return value or None


def _as_entry_file(candidate):
    """Normalise a candidate output location to a file path.

    ENTRY_OUT may point at a file or at a directory; a directory means
    ``entry.txt`` inside it. Returns None when the candidate is unusable.
    """
    if not candidate:
        return None
    if os.path.isdir(candidate):
        return os.path.join(candidate, "entry.txt")
    parent = os.path.dirname(os.path.abspath(candidate))
    if parent and not os.path.isdir(parent):
        return None
    return candidate


def resolve_output_path():
    """Pick where entry.txt goes, in grader order.

    1. ENTRY_OUT (file or directory)
    2. MAKEFUN_OUTPUT_DIR (a directory)
    3. /output/entry.txt
    4. ./entry.txt in the current working directory (last resort)
    """
    entry_out = _env_path("ENTRY_OUT")
    if entry_out:
        resolved = _as_entry_file(entry_out)
        if resolved:
            return resolved

    out_dir = _env_path("MAKEFUN_OUTPUT_DIR")
    if out_dir and os.path.isdir(out_dir):
        return os.path.join(out_dir, "entry.txt")

    if os.path.isdir("/output"):
        return "/output/entry.txt"

    return os.path.join(os.getcwd(), "entry.txt")


def write_entry(path, text):
    """Write the entry text with no trailing newline, creating dirs as needed."""
    directory = os.path.dirname(os.path.abspath(path))
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    return path


def main(argv=None):
    """Resolve the output path, write the entry, and report back."""
    del argv  # no CLI arguments are used
    target = resolve_output_path()
    written = write_entry(target, ENTRY_TEXT)
    chars = len(ENTRY_TEXT)
    nbytes = len(ENTRY_TEXT.encode("utf-8"))
    print("wrote %d chars (%d bytes) to %s" % (chars, nbytes, written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
