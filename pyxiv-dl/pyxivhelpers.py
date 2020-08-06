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

    # type cast and compare
    try:
        # get range indices
        ranges = rangeStr.split(",", 1)

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

    except (ValueError, IndexError, AttributeError):
        return False

    return True

### scraper helpers

def promptNsfwDownload(postSafetyLevel : int) -> bool:
    """Prompts the user if the download should continue on sensitive/NSFW posts"""
    # prompt for NSFW download:
    while True:

        #prompt response
        nsfwPrompt = ""

        # verify post safetly level
        # newly-discovered criteria:
        # SL = 4: potentially sensitive post, not necessarily NSFW
        # SL = 6: NSFW (R18+) post

        if postSafetyLevel == 4:
            nsfwPrompt = input("WARNING: This post may contain sensitive media. Proceed with download? [y/N] ")
        elif postSafetyLevel == 6:
            nsfwPrompt = input("WARNING: This post contains explicit (e.g. sexual) content. Proceed with download? [y/N] ")

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
    uploadedOn = dateutil.parser.parse(pageMetadata["uploadDate"]).astimezone(tz=None)\
        .strftime("%b %-d %Y, %H:%M:%S %Z")
    postLikes = pageMetadata["likeCount"]
    postBookmarks = pageMetadata["bookmarkCount"]
    postViews = pageMetadata["viewCount"]
    postImageCount = pageMetadata["pageCount"]
    postTags = parsePostTags(pageMetadata["tags"])

    # post rating display (safe, potentially sensitive, NSFW)
    postRating = ""
    if int(pageMetadata["sl"]) < 4:
        postRating = "Safe"
    elif int(pageMetadata["sl"]) == 4:
        postRating = "Potentially sensitive"
    elif int(pageMetadata["sl"]) == 6:
        postRating = "NSFW"

    # print post metadata
    print("====================\nPost information:\n")
    print("Artist: {}".format(artistInfo))
    print("Title: {}".format(artTitle))
    print("Upload date: {}".format(uploadedOn))
    print("Likes: {:,}".format(postLikes))
    print("Bookmarks: {:,}".format(postBookmarks))
    print("Views: {:,}".format(postViews))
    print("Images in post: {}".format(postImageCount))
    print("Post tags: {}".format(postTags))
    print("Pixiv URL: https://www.pixiv.net/artworks/{}".format(illustId))
    print("Post rating: {}".format(postRating))
    print("====================")

def parsePostTags(tagsMetadataRoot : list):
    """Parses the list of tags the art has"""

    # parsed tags array storage
    postTags = ""

    # loop in tags
    for idx, tags in enumerate(tagsMetadataRoot["tags"]):
        postTags += tags["tag"]

        # compare index and length
        # append a comma if loop index < length
        if idx + 1 < len(tags):
            postTags += ", "

    return postTags

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

def downloadRangesHelper(imageCount : int, downloadRange, downloadIndex):
    """Helper function for calculating download ranges and/or download index"""
    # expected output should be [x,y], where x = zero-based image index start,
    # and y = the amount of images in a post.

    # check if downloadRange and downloadIndex are set
    # then return an error message
    if downloadRange is not None and downloadIndex is not None:
        print("Range and index parameters cannot be combined at the same time.")
        return None

    # check if there is only one image in a post
    if imageCount == 1:
        return [0, 1]
    elif imageCount > 1 and (downloadRange is None and downloadIndex is None):
        return [0, imageCount]

    # checks when download range is set
    if downloadRange is not None:
        return _calculateRange(imageCount, downloadRange)
    elif downloadIndex is not None:
        return _calculateIndex(imageCount, downloadIndex)


def _calculateRange(imageCount : int, downloadRange):
    """Calculates the download index ranges"""

    rangeMin = 0
    rangeMax = imageCount

    # do checks per index
    # 0 = index start
    # 1 = index end
    if downloadRange[0] is not None:
        # check if range start < 1
        if downloadRange[0] < 1:
            print("Range input values can not be less than 1. Aborting.")
            return None

        # check first if indexStart > imageTotal
        # then return error if it is
        if downloadRange[0] > imageCount:
            print("Entered start index exceeds the total images in the post. Aborting.")
            return None

        rangeMin = downloadRange[0] -1

    if downloadRange[1] is not None:
        # check if range end < 1:
        if downloadRange[1] < 1:
            print("Range input values can not be less than 1. Aborting.")
            return None

        # if entered max image index does not go
        # above the max image count, override
        if downloadRange[1] < imageCount:
            rangeMax = downloadRange[1]

    return [rangeMin, rangeMax]

def _calculateIndex(imageCount : int, downloadIndex : int):
    """Calculates the download index"""

    # check if downloadIndex <= 0
    if downloadIndex < 0:
        print("Entered image index must not be less than 1.")
        return None

    # check if downloadIndex > imageCount
    if downloadIndex > imageCount:
        print("Entered image index must not exceed the post's total image count.")
        return None

    return [downloadIndex - 1, downloadIndex]