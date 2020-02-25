"""pyxiv-dl main script

This is the main script that executes the main pyxiv-dl argument parser.
"""

import argparse, sys, textwrap
from webcrawler import PixivWebCrawler
from pyxivhelpers import *

# constants

"""Script version"""
PYXIVDL_VERSION = "0.3.3"

"""Main function for accepting download args"""
def main():
    # load argparse here
    argParser = argparse.ArgumentParser(
        description="pyxiv-dl: Downloads full-sized arts from Pixiv",
        usage="pyxiv-dl.py [options] <id>",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        ADDITIONAL NOTES
        
        The -r/--range option lets you to download images in a multi-image post on a
        specified range. This is silently ignored for single and ugoira posts. For the
        -r/--range option, the format it accepts is the following:
        
        \tx,y
        
        where 0 > x > y. x denotes the start of the image index to download and y denotes the
        end of the image index. If y exceeds the total number of posts, it will be silently
        ignored and will download up to the last image index.
        
        These are the valid formats accepted by the -r/--range option:
        \t1,4\tDownloads images from index 1 to 4
        \t4,6\tDownloads images from index 4 to 6
        \t4,\tDownloads images from index 4 up to the last
        \t,5\tDownloads images from the start up to index 5
        
        Anything not in the valid formats are considered invalid.
        """)
    )

    argParser.add_argument(
        "-i",
        "--index",
        help="Download a specific image on a multi image post based on its index. Cannot be combined with -r/--range",
        action="store",
        type=int
    )

    argParser.add_argument(
        "-r",
        "--range",
        help="Download images from a specified range using a from,to format. Cannot be combined with -i/--index. "
             "See help for more info",
        action="store"
    )

    # add NSFW confirmation bypass
    argParser.add_argument(
        "-n",
        "--nsfw",
        help="Always allow NSFW image download. If not set, you are asked to confirm the download first",
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
        "id",
        help="your Pixiv medium ID to get original-sized images or ugoira from",
        action="store"
    )

    # set parsed args variable
    parsedArgs = argParser.parse_args()

    # validate inputs first

    # check first for valid pixiv IDs
    if not validatePostIdRegex(parsedArgs.id):
        print("One or more inputs is not a valid Pixiv post ID. Aborting.")
        sys.exit(1)

    if parsedArgs.range is not None and not validateRange(parsedArgs.range):
        print("Range parameter is incorrect. See help for more info.")
        sys.exit(1)

    # run scraper
    pxCrawl = PixivWebCrawler(
        parsedArgs.id,
        parsedArgs.verbose,
        parsedArgs.nsfw,
        parsedArgs.range,
        parsedArgs.index
    )
    PixivWebCrawler.downloadImages(pxCrawl)

# main call
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Aborting.")