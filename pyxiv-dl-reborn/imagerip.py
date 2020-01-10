import sys, requests, re as regex
from urllib.parse import urlparse

class PixivImageRipper():
    """Main image ripper class"""

    # class constants
    """Base Pixiv URL, which is also used as a referrer"""
    PIXIV_URL = "https://www.pixiv.net"

    """Request headers for use with requests library"""
    REQUEST_HEADERS = {
        "referer": PIXIV_URL,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0"
    }

    """Initialize downloader"""
    def __init__(self, pixivIds=[], verbose=False, bypassNsfw=False):
        # check for pixiv IDs first
        self._checkPixivIds(pixivIds)

    """Checks the input if they are a valid Pixiv ID"""
    def _checkPixivIds(self, pixivIds=[]):
        # pixiv IDs are 6-digits long and currently at 700,000 arts and
        # counting. Let's assume first that it will grow to 1M+ arts
        # throughout the year

        #compile the regex for checking numbers
        pxIdRegex = regex.compile("^[0-9]{6,7}$", regex.I)

        for ids in pixivIds:
            pxIdCheck = pxIdRegex.match(ids)
            try:
                if pxIdCheck is not None:
                    pass
                else:
                    print("ERROR: one or more inputs is not a valid Pixiv ID. Aborting.")
                    sys.exit(1)
            except IndexError:
                print("ERROR: something went wrong with checking the Pixiv IDs. Aborting")
