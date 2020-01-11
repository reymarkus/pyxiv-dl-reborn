import sys, re as regex

class PixivImageRipper:
    """Main image ripper class"""

    """Initialize downloader"""
    def __init__(self, pixivIds=[], verbose=False, bypassNsfw=False):
        # set class-level variables
        self.isVerbose = verbose
        self.bypassNsfw = bypassNsfw

        # check for pixiv IDs first
        # note that it will self-exit if there
        # is an error in the input
        self._checkPixivIds(pixivIds)

    """Checks the input if they are a valid Pixiv ID"""
    def _checkPixivIds(self, pixivIds):
        # pixiv IDs are numeric

        #compile the regex for checking numbers
        pxIdRegex = regex.compile("^[0-9]+$", regex.I)

        for ids in pixivIds:
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
