# pyxiv-dl-reborn

A  hobby project of a (hopefully) improved script of my previous `pyxiv-dl` script which rips original size Pixiv arts.

**Note**: This script is still WIP, and it will be updated in the future!

### Usage
```
python pyxiv-dl -h
usage: pyxiv-dl.py [options] <ids>...

pyxiv-dl: Downloads full-sized arts from Pixiv

positional arguments:
  ids            your Pixiv medium IDs to get original images

optional arguments:
  -h, --help     show this help message and exit
  -n, --nsfw     Always allow NSFW image download. If not set, you are asked
                 to confirm the download
  -v, --verbose  Show verbose output
  -V, --version  Show the application's version and exit
```

Example usage:
```bash
# Example page: https://www.pixiv.net/en/artworks/66445862
python pyxiv-dl 66445862
Downloading 66445862...
Downloading 1/1...
File written to ./pyxiv-dl-images/66445862_p0.jpg
```

### Requirements:
* Python >= 3.6
* `requests`
* `lxml`

### Download and Install

Clone this repository and install dependencies
```
https://gitlab.com/reymarkus/pyxiv-dl-reborn.git
cd pyxiv-dl-reborn
pip3 install -r requirements.txt
```

### Limitations:
These are the features that are not yet implemented and will be added soon.

* Verbose output is not yet fully implemented
* Ugoira support (animated image post) coming soon!

### License
TBD, will decide on the first stable release.
