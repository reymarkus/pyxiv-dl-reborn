# pyxiv-dl Reborn

A  hobby project of a (hopefully) improved script of my previous `pyxiv-dl` personal script which rips original size Pixiv arts.

[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-black.svg)](https://sonarcloud.io/dashboard?id=reymarkus_pyxiv-dl-reborn)

**Note**: This script is still WIP, and it will be updated in the future!

### Usage
```
python pyxiv-dl -h
usage: pyxiv-dl.py [options] <id>

pyxiv-dl: Downloads full-sized arts from Pixiv

positional arguments:
  id                    your Pixiv medium ID to get original-sized images or
                        ugoira from

optional arguments:
  -h, --help            show this help message and exit
  -i INDEX, --index INDEX
                        Download a specific image on a multi image post based
                        on its index. Cannot be combined with -r/--range
  -r RANGE, --range RANGE
                        Download images from a specified range using a from,to
                        format. Cannot be combined with -i/--index. See help for
                        more info
  -n, --nsfw            Always allow NSFW image download. If not set, you are
                        asked to confirm the download first
  -v, --verbose         Show verbose output
  -V, --version         Show the application's version and exit
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
* `ugoira` >= 0.6.0
* `python-dateutil`

### System dependencies
* `libxml2-dev`
* `libxslt1.1`
* `imagemagick` (for ugoira posts)

### Download and Install

Clone this repository and install dependencies
```
https://gitlab.com/reymarkus/pyxiv-dl-reborn.git
cd pyxiv-dl-reborn
pip install -r requirements.txt
```

### Branching Information

This repository uses Git Flow as its branching model. Thus, the specified branches contains different states of the project

* On `master`, tagged commits are considered stable releases, with can sometimes have hotfixes
* The `develop` branch contains the "bleeding-edge" build which may contain new features, and may be unstable for general use
* `feature/*` branches contains features or fixes that are in-development, and will likely break when used. 

### Third-party Libraries used

* [ugoira](https://github.com/item4/ugoira/) by item4, licensed under the [MIT License](https://github.com/item4/ugoira/blob/master/LICENSE)

### License
MIT. See license.txt for more information.
