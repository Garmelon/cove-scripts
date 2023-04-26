#!/usr/bin/env python3


import argparse
import json
from pathlib import Path

import requests

DESCRIPTION = """
Download imgur images that have not yet been downloaded.
"""


def log(ids, n, id, msg):
    print(f"{id} ({n+1:_}/{len(ids):_}): {msg}")


def download(ids, n, id, path, link):
    tmppath = path.parent / (path.name + ".tmp")
    try:
        r = requests.get(link)
        if r.status_code == 404:
            log(ids, n, id, "Not found (404)")
            return
        elif r.status_code != 200:
            log(ids, n, id, f"Weird status code: {r.status_code}")
            return
        with open(tmppath, "wb") as f:
            f.write(r.content)
        tmppath.rename(path)
        log(ids, n, id, "Downloaded")
    except Exception as e:
        log(ids, n, id, f"Error fetching {link}: {e}")


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

    print("Loading image and album ids")
    with open(args.info) as f:
        data = json.load(f)
    image_ids = data["image_ids"]
    album_ids = data["album_ids"]

    args.dir.mkdir(parents=True, exist_ok=True)

    print("Downloading images")
    for n, image_id in enumerate(image_ids):
        # Yes, I know not all images are pngs. Use file(1) or any other tool of
        # your choice to fix the extensions after downloading the files.
        image_path = args.dir / f"{image_id}.png"
        # Yes, imgur ignores the file extension and doesn't even redirect. It
        # just serves the file.
        image_link = f"https://i.imgur.com/{image_id}.png"

        if image_path.exists():
            continue

        download(image_ids, n, image_id, image_path, image_link)

    print("Downloading albums")
    for n, album_id in enumerate(album_ids):
        album_path = args.dir / f"{album_id}.png"
        album_link = f"https://imgur.com/a/{album_id}/zip"

        if album_path.exists():
            continue

        download(album_ids, n, album_id, album_path, album_link)


if __name__ == "__main__":
    main()
