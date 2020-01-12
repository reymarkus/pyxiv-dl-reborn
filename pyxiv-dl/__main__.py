"""pyxiv-dl main script

This is the main script that executes the main pyxiv-dl argument parser.
"""

import argparse, re as regex, sys
from webcrawler import PixivWebCrawler

# constants

"""Script version"""
PYXIVDL_VERSION = "0.1.0"

"""Main function for accepting download args"""
def main():
    # load argparse here
    argParser = argparse.ArgumentParser(
        description="pyxiv-dl: Downloads full-sized arts from Pixiv",
        usage="pyxiv-dl.py [options] <ids>>..."
    )

    # add NSFW confirmation bypass
    argParser.add_argument(
        "-n",
        "--nsfw",
        help="Always allow NSFW image download. If not set, you are asked to confirm the download",
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
    pxIdRegex = regex.compile("^[0-9]+$", regex.I)

    for ids in parsedArgs.ids[0]:
        pxIdCheck = pxIdRegex.match(ids)
        try:
            if pxIdCheck is not None:
                pass
            else:
                print("ERROR: one or more inputs is not a valid Pixiv Art ID. Aborting.")
                sys.exit(1)
        except IndexError:
            print("ERROR: something went wrong with checking the Pixiv Art IDs. Aborting")
            sys.exit(1)

        # initialize download
        PixivWebCrawler.downloadImages(
            PixivWebCrawler(ids, parsedArgs.verbose, parsedArgs.nsfw)
        )


# main call
if __name__ == "__main__":
    main()