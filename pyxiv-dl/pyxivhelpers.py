import re as regex, dateutil

"""Helper functions for pyxiv-dl"""

### CLI helpers

def validatePostIdRegex(pxId : str) -> bool:
    """Validates the given Pixiv post ID"""
    postIdRegex = regex.compile(r"^[0-9]+$", regex.I)
    try:
        if postIdRegex.match(pxId) is not None:
            return True
    except IndexError:
        return False

def validateRange(rangeStr : str) -> bool:
    """Validates the range argument"""

    # get range indices
    ranges = rangeStr.split(",", 1)

    # type cast and compare
    try:
        rangeFrom = 0 if ranges[0] == "" else int(ranges[0])
        rangeTo = 0 if ranges[1] == "" else int(ranges[1])

        # check first if both ranges are not set
        # using the -r , hack
        if ranges == ["", ""]:
            return False

        # check if any of the range param is set
        # and do testing per side

        # if either range start/end is set and is <= 0:
        if (ranges[0] != "" and rangeFrom < 0) or\
            (ranges[1] != "" and rangeTo < 0):
            return False
        elif (ranges[0] != "") and (ranges[1] != ""):
            # if both are set, do conditions here
            # if from == to or from > to or from,to <=0, fail
            if (rangeFrom == rangeTo) or\
                (rangeFrom > rangeTo) or\
                ((rangeFrom <= 0) or (rangeTo <= 0)):
                return False

    except (ValueError, IndexError):
        return False

    return True

### scraper helpers

def promptNsfwDownload() -> bool:
    """If the NSFW download flag is not set, prompt the user first"""
    # prompt for NSFW download:
    while True:
        nsfwPrompt = input("WARNING: This post may contain sensitive media. Proceed with download? [y/N] ")

        if (str(nsfwPrompt).lower() == "n") or (nsfwPrompt == ""):
            # if N or no answer is entered, abort
            print("Aborting download for this post.")
            return False
        elif str(nsfwPrompt).lower() == "y":
            # download
            return True

def printVerboseMetadata(pageMetadata : list):
    """Prints detailed information about the art post from the post metadata"""

    illustId = pageMetadata["illustId"]
    artistInfo = "{} ({})".format(
        pageMetadata["userName"],
        pageMetadata["userAccount"]
    )
    artTitle = pageMetadata["illustTitle"]
    uploadedOn = dateutil.parser.parse(pageMetadata["uploadDate"])\
        .strftime("%b %-d %Y, %H:%M:%S %Z")
    postLikes = pageMetadata["likeCount"]
    postBookmarks = pageMetadata["bookmarkCount"]
    postViews = pageMetadata["viewCount"]
    postImageCount = pageMetadata["pageCount"]

    # print post metadata
    print("====================\nPost information:\n")
    print("Artist: {}".format(artistInfo))
    print("Title: {}".format(artTitle))
    print("Upload date: {}".format(uploadedOn))
    print("Likes: {:,}".format(postLikes))
    print("Bookmarks: {:,}".format(postBookmarks))
    print("Views: {:,}".format(postViews))
    print("Images in post: {}".format(postImageCount))
    print("Pixiv URL: https://www.pixiv.net/artworks/{}".format(illustId))
    print("====================")

def parseDownloadRange(rangeStr : str):
    """Parse and get the download range indices"""

    # validate first if it is a valid range format
    if not validateRange(rangeStr):
        return None

    # get range specifiers
    ranges = rangeStr.split(",")

    try:
        rangeFrom = None if ranges[0] == "" else int(ranges[0])
        rangeTo = None if ranges[1] == "" else int(ranges[1])
        return  [rangeFrom, rangeTo]
    except ValueError:
        return None