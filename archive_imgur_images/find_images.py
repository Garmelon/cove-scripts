#!/usr/bin/env python3

import argparse
import json
import re
import sys
from pathlib import Path

DESCRIPTION = """
Find imgur images and albums linked in message contents and store them in a json
file.
"""

EPILOG = """
This program expects the output of `cove export -o - -f json-stream <room>` on
stdin. To run the script on all messages in your vault, pass `-a` to cove
instead of specifying one or more rooms directly.
"""

IMAGE_RE = re.compile(r"imgur.com/([a-zA-Z0-9]+)")
ALBUM_RE = re.compile(r"imgur.com/a/([a-zA-Z0-9]+)")


def main():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--info",
        "-i",
        type=Path,
        default=Path("imgur_images.json"),
        help="the json file to save the links in",
    )
    args = parser.parse_args()

    image_ids = set()
    album_ids = set()

    sifted = 0
    for line in sys.stdin:
        msg = json.loads(line)
        for match in IMAGE_RE.finditer(msg["content"]):
            image_ids.add(match.group(1))
        for match in ALBUM_RE.finditer(msg["content"]):
            album_ids.add(match.group(1))

        sifted += 1
        if sifted % 100_000 == 0:
            print(
                f"Sifted through {sifted:_} messages, "
                f"found {len(image_ids):_} image ids, "
                f"{len(album_ids):_} album ids so far"
            )

    print(f"Sifted through {sifted:_} messages in total")
    print(f"Found {len(image_ids):_} unique image ids")
    print(f"Found {len(album_ids):_} unique album ids")

    print("Saving image and album ids")
    data = {
        "image_ids": list(sorted(image_ids)),
        "album_ids": list(sorted(album_ids)),
    }
    with open(args.info, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()
