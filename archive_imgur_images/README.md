# Archive imgur images

A set of scripts for finding and downloading imgur images linked in messages.

Since imgur announced to remove anonymously posted content soon, I decided to
write some scripts to download and preserve all imgur images ever posted to
euphoria. Run at your own risk :P

## Usage

First, install [requests](https://pypi.org/project/requests/) or use the flake
with `nix develop`. Then execute the following commands:

```
$ cove export -o - -f json-stream -a | ./find_images.py
$ ./download_images.py
```

For more info and available arguments, consult `cove export --help`,
`./find_images.py --help`, and `./download_images.py --help`.
