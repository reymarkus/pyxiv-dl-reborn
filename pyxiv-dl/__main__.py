"""pyxiv-dl main script

This is the main script that executes the main pyxiv-dl argument parser.
"""

import argparse, re as regex, sys
from webcrawler import PixivWebCrawler
from pyxivhelpers import *

# constants

"""Script version"""
PYXIVDL_VERSION = "0.2.0"

"""Main function for accepting download args"""
def main():
    # load argparse here
    argParser = argparse.ArgumentParser(
        description="pyxiv-dl: Downloads full-sized arts from Pixiv",
        usage="pyxiv-dl.py [options] <ids>..."
    )

    # add NSFW confirmation bypass
    argParser.add_argument(
        "-n",
        "--nsfw",
        help="Always allow NSFW image download. If not set, you are asked to confirm the download per post",
        action="store_true"
    )

    # add verbose argument
    argParser.add_argument(
        "-v",
        "--verbose",
        help="Show verbose output",
        action="store_true"
    )

    # show script version
    argParser.add_argument(
        "-V",
        "--version",
        help="Show the application's version and exit",
        action="version",
        version="%(prog)s v{}".format(PYXIVDL_VERSION)
    )

    # main argument: pixiv art IDs
    argParser.add_argument(
        "ids",
        help="your Pixiv medium IDs to get original images",
        type=str,
        action="append",
        nargs="+"
    )

    # set parsed args variable
    parsedArgs = argParser.parse_args()

    ###########
    # runner
    ##########

    # check first for valid pixiv IDs
    if not validatePostIdRegex(parsedArgs.ids[0]):
        print("One or more inputs is not a valid Pixiv post ID. Aborting.")
        sys.exit(1)

    for ids in parsedArgs.ids[0]:
        # initialize download
        pxCrawl = PixivWebCrawler(ids, parsedArgs.verbose, parsedArgs.nsfw)
        PixivWebCrawler.downloadImages(pxCrawl)

# main call
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Aborting.")