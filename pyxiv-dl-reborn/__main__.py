"""pyxiv-dl-reborn main script

This is the main script that executes the main pyxiv-dl-reborn argument parser.
"""

import argparse
from imagerip import PixivImageRipper

# constants

"""Script version"""
PYXIVDL_VERSION = "0.1.0"

"""Main function for accepting download args"""
def main():
    # load argparse here
    argParser = argparse.ArgumentParser(
        description="pyxiv-dl: Downloads full-sized arts from Pixiv",
        usage="pyxiv-dl.py [options] urls..."
    )
    
    # add verbose argument
    argParser.add_argument(
        "-v",
        "--verbose",
        help="show verbose output",
        action="store_true"
    )
    
    # add NSFW confirmation bypass
    argParser.add_argument(
        "-n",
        "--nsfw",
        help="Always allow NSFW image download. If not set, you are asked to confirm the download",
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
    PixivImageRipper(parsedArgs.ids[0], parsedArgs.verbose, parsedArgs.nsfw)

# main call
if __name__ == "__main__":
    main()