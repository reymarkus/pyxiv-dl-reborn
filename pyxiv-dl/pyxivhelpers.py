import re as regex, dateutil

"""Helper functions for pyxiv-dl"""

### CLI helpers

def validatePostIdRegex(pxId : list) -> bool:
    """Validates the list of Pixiv post IDs"""
    postIdRegex = regex.compile(r"^[0-9]+$", regex.I)
    for postId in pxId:
        try:
            if postIdRegex.match(postId) is not None:
                pass
        except IndexError:
            return False

    return True

def validateRange(rangeStr : str) -> bool:
    """Validates the range argument"""

    # validate if the format is correct
    # rangeRgx = regex.compile(r"^[0-9]+,[0-9]+$")
    # try:
    #     if rangeRgx.match(rangeStr) is None:
    #         return False
    # except IndexError:
    #     return False

    # get range indices
    ranges = rangeStr.split(",")

    # type cast and compare
    try:
        print("{}, {}".format(ranges[0], ranges[1]))
        rangeFrom =  0 if ranges[0] == "" else int(ranges[0])
        rangeTo = 0 if ranges[1] == "" else int(ranges[1])

        # compare ranges
        # list of bad conditions:
        # * x = y
        # * x > y
        # * x,y < 0

        if rangeFrom == rangeTo:
            return False

        if rangeFrom > rangeTo:
            return False

        if (rangeFrom <= 0) or (rangeTo <= 0):
            return False

    except ValueError:
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
        else:
            pass
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
    return  [
        int(ranges[0]),
        int(ranges[1])
    ]