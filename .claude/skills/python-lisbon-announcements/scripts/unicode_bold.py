#!/usr/bin/env python3
"""Convert text to Unicode sans-serif bold for LinkedIn, which has no Markdown.

Usage:
    python3 unicode_bold.py "Gapstars, Edifício Atrium Saldanha"   # bold the whole argument
    python3 unicode_bold.py --markdown < details.md                  # convert **bold** spans, - bullets → •, strip []() links

Letters A–Z, a–z and digits 0–9 have bold versions. Accented letters (í, º, ç…)
do not, so they stay regular weight. That's expected.
"""
import re
import sys


def bold(text: str) -> str:
    out = []
    for c in text:
        if "A" <= c <= "Z":
            out.append(chr(0x1D5D4 + ord(c) - 65))
        elif "a" <= c <= "z":
            out.append(chr(0x1D5EE + ord(c) - 97))
        elif "0" <= c <= "9":
            out.append(chr(0x1D7EC + ord(c) - 48))
        else:
            out.append(c)
    return "".join(out)


def from_markdown(md: str) -> str:
    md = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", md)          # [text](url) -> text
    md = re.sub(r"\*\*(.+?)\*\*", lambda m: bold(m.group(1)), md)
    md = re.sub(r"^(\s*)- ", r"\1• ", md, flags=re.M)
    md = re.sub(r"^#+\s*", "", md, flags=re.M)
    return md


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--markdown":
        sys.stdout.write(from_markdown(sys.stdin.read()))
    else:
        print(bold(" ".join(sys.argv[1:])))
