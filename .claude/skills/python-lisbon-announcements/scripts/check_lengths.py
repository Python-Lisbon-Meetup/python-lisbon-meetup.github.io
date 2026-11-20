#!/usr/bin/env python3
"""Check post lengths against X (280) and Mastodon (500) limits.

Usage:
    python3 check_lengths.py x post_x.txt
    python3 check_lengths.py mastodon post_mastodon.txt

Both platforms count every URL as 23 characters. X also counts emoji and most
other non-Latin characters as 2. Mastodon counts them as 1.
"""
import re
import sys

URL = re.compile(r"https?://\S+")
LIMITS = {"x": 280, "mastodon": 500}


def x_len(text: str) -> int:
    text = URL.sub("x" * 23, text)
    return sum(2 if ord(c) > 0x10FF else 1 for c in text)


def mastodon_len(text: str) -> int:
    return len(URL.sub("x" * 23, text))


if __name__ == "__main__":
    platform, path = sys.argv[1].lower(), sys.argv[2]
    text = open(path, encoding="utf-8").read().strip()
    n = x_len(text) if platform == "x" else mastodon_len(text)
    limit = LIMITS[platform]
    print(f"{platform}: {n}/{limit} {'OK' if n <= limit else 'TOO LONG by ' + str(n - limit)}")
    sys.exit(0 if n <= limit else 1)
