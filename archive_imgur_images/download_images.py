#!/usr/bin/env python3


import argparse
import json
from pathlib import Path

import requests

DESCRIPTION = """
Download imgur images that have not yet been downloaded.
"""


def log(image_ids, n, image_id, msg):
    print(f"{image_id} ({n+1:_}/{len(image_ids):_}): {msg}")


def main():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--info",
        "-i",
        type=Path,
        default=Path("imgur_images.json"),
        help="the json file with the links",
    )
    parser.add_argument(
        "--dir",
        "-d",
        type=Path,
        default=Path("imgur_images"),
        help="the directory to save the images in",
    )
    args = parser.parse_args()

    print("Loading image ids")
    with open(args.info) as f:
        image_ids = json.load(f)["image_ids"]

    args.dir.mkdir(parents=True, exist_ok=True)

    for n, image_id in enumerate(image_ids):
        # Yes, I know not all images are pngs. Use file(1) or any other tool of
        # your choice to fix the extensions after downloading the files.
        image_path = args.dir / f"{image_id}.png"
        # Yes, imgur ignores the file extension and doesn't even redirect. It
        # just serves the file.
        image_link = f"https://i.imgur.com/{image_id}.png"

        if image_path.exists():
            continue

        try:
            r = requests.get(image_link)
            if r.status_code == 404:
                log(image_ids, n, image_id, "Not found (404)")
                continue
            elif r.status_code != 200:
                log(image_ids, n, image_id, f"Weird status code: {r.status_code}")
                continue
            with open(image_path, "wb") as f:
                f.write(r.content)
            log(image_ids, n, image_id, "Downloaded")
        except Exception as e:
            log(image_ids, n, image_id, f"Error fetching {image_link}: {e}")


if __name__ == "__main__":
    main()
