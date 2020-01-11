import sys, re as regex, requests, json
from lxml import etree
from enum import Enum

# enum class for returning pixiv art post types
class PixivArtPostType(Enum):
    """ Enum class for determining the art post type of a Pixiv page"""

    IMAGE_SINGLE = 1
    IMAGE_MULTI = 2
    UGOIRA = 3

class PixivWebCrawler:
    """The main site ripper for Pixiv."""

    # class constants
    """Base Pixiv URL, which is also used as a referrer"""
    PIXIV_URL = "https://www.pixiv.net"

    """Request headers for use with requests library"""
    REQUEST_HEADERS = {
        "referer": PIXIV_URL,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0"
    }

    """Regex for the link that contains original images"""
    PIXIV_ORIGINAL_IMG_PREFIX_REGEX = "i.pximg.net\/img-original"

    def __init__(self, pxArtId : int, isVerbose :  bool, ignoreNsfw : bool):
        """Initialize the class and starts the download"""

        """The post art ID"""
        self.pixivArtId = pxArtId

        """Enable verbose output"""
        self.verboseOutput = isVerbose

        """Prompt download for NSFW-marked posts"""
        self.ignoreNsfw = ignoreNsfw

    # main downloader function
    def downloadImages(self):
        """Initialize image downloading"""
        # download page metadata
        pageMetaJson = self._getPreloadMetadata(self.pixivArtId)

        # check first if there is JSON output
        if pageMetaJson is None:
            # exit function
            return

        # get art post type
        artPostType = self._detectPostType(pageMetaJson, self.pixivArtId)


    ####################

    # private functions

    # THANK FUCK PIXIV FOR EASY ACCESS :POGU: :HyperPoggers:
    def _getPreloadMetadata(self, pxArtId):
        """Gets the art page's preload metadata"""

        # get the page first
        pageRequest = requests.get(
            self.PIXIV_URL + "/" + pxArtId,
            headers=self.REQUEST_HEADERS
        )

        # check first if response is != 200
        if pageRequest.status_code == 404:
            print("Art page not found. Skipping.")
            return None
        elif pageRequest.status_code == 403:
            print("Cannot load art page, access denied. Skipping.")
            return None

        # get JSON content from metadata
        elemTree = etree.HTML(pageRequest.content)
        pageMetaStr = elemTree.xpath("//meta[@name='preload-data']/@content")

        # get JSON from string
        return json.loads(pageMetaStr[0])

    def _detectPostType(self, metaJson : json, pxArtId : int) -> PixivArtPostType:
        """Detects the art post type by its preload metadata"""

        # get the main post metadata
        # post metadata is located at illust.<postId>
        metadataRoot = metaJson["illust"][pxArtId]

        # criteria for pixiv metadata check
        # single post: illust.<pxid>.pageCount == 1
        # multiple post: illust.<pxid>.pageCount > 1
        # ugoira: illust.<pxid>.illustType = 2
        # is marked NSFW: illust.<pxid>.sl >= 4 (wild guess!)

        # priority check: check first if image is an ugoira
        if int(metadataRoot["illustType"]) == 2:
            return PixivArtPostType.UGOIRA

        # check for amount of images in the post
        if int(metadataRoot["pageCount"]) == 1:
            return PixivArtPostType.IMAGE_SINGLE
        elif int(metadataRoot["pageCount"]) > 1:
            return PixivArtPostType.IMAGE_MULTI
