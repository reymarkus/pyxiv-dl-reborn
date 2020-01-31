import sys, requests, json, re as regex, os, dateutil.parser
from lxml import etree
from enum import Enum
from pyxivhelpers import *

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

    """Regex for full image filenames"""
    DOWNLOAD_FILENAME_REGEX = "[0-9]+_p[0-9]+.[a-z]{3}$"

    """The downloads folder"""
    DOWNLOADS_FOLDER = "pyxiv-dl-images"

    def __init__(self, pxArtId : int, isVerbose = False, ignoreNsfw = False, downloadRange = None):
        """Initialize the class and starts the download"""

        """The post art ID"""
        self.pixivArtId = pxArtId

        """Enable verbose output"""
        self.verboseOutput = isVerbose

        """Prompt download for NSFW-marked posts"""
        self.ignoreNsfw = ignoreNsfw

        """The download range"""
        self.downloadRange = downloadRange

        # check first if downloads folder exist
        if not os.path.exists(self._getFolderPath()):
            os.makedirs(self._getFolderPath())


    # main downloader function
    def downloadImages(self):
        """Initialize image downloading"""
        # download page metadata
        pageMetaJson = self._getPreloadMetadata(self.pixivArtId)
        pageMetadata = pageMetaJson["illust"][self.pixivArtId]

        # check first if there is JSON output
        if pageMetaJson is None:
            # exit function
            return

        # check if image is marked as NSFW before downloading anything
        # NSFW criteria: illust.{PIXIV_ID}.sl >= 4
        # also, prompt for NSFW download. if declined, stop
        if int(pageMetadata["sl"]) >= 4 \
            and self.ignoreNsfw == False and\
            not promptNsfwDownload():
                return

        # directly download if it's a single or multi image post
        print("Downloading {}...".format(self.pixivArtId))
        
        # verbose: print post metadata
        if self.verboseOutput:
            printVerboseMetadata(pageMetadata)

        # get art post type
        artPostType = self._detectPostType(pageMetaJson, self.pixivArtId)
        if artPostType == PixivArtPostType.IMAGE_SINGLE \
            or artPostType == PixivArtPostType.IMAGE_MULTI:
            self._downloadImagePost(pageMetaJson, self.pixivArtId)
        elif artPostType == PixivArtPostType.UGOIRA:
            self._downloadUgoiraPost(self.pixivArtId)

    ####################

    # private functions

    # THANK FUCK PIXIV FOR EASY ACCESS :POGU: :HyperPoggers:
    def _getPreloadMetadata(self, pxArtId):
        """Gets the art page's preload metadata"""

        # get the page first
        pageRequest = requests.get(
            self.PIXIV_URL + "/artworks/" + pxArtId,
            headers=self.REQUEST_HEADERS
        )

        # check first if response is != 200
        if pageRequest.status_code == 404:
            print("Art page not found. Skipping.")
            return None
        elif pageRequest.status_code == 403:
            print("Cannot load art page, access denied. Skipping.")
            return None
        elif pageRequest.status_code in range(500, 599):
            # for HTTP 5xx errors
            print("Cannot load art page. Server error.")
            return None

        # get JSON content from metadata
        elemTree = etree.HTML(pageRequest.content.decode("utf-8"))
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

    # download methods
    def _downloadImagePost(self, metaJson : json, pxArtId : int):
        """Downloads the original images from an image post and returns a stream array"""
        # main post metadata
        metadataRoot = metaJson["illust"][pxArtId]

        # get amount of arts in a post
        imageCount =  int(metadataRoot["pageCount"])

        # download images in an index
        imgStreamList = []
        dlFilenames = []
        for imgIndex in range (0, imageCount):
            # set current image index
            currentImgIndex = imgIndex + 1
            print("Downloading {}/{}...".format(currentImgIndex, imageCount))

            # get base image URL
            baseImageUrl = str(metadataRoot["urls"]["original"])

            # set image URL to download
            imageUrl = baseImageUrl.replace("_p0", "_p" + str(imgIndex))

            # download image stream
            imageStream = requests.get(
                imageUrl,
                headers=self.REQUEST_HEADERS,
                stream=True
            )

            # append stream to list
            imgStreamList.append(imageStream.content)
            # append download filenames to list
            dlFilenames.append(regex.search(
                self.DOWNLOAD_FILENAME_REGEX, imageUrl
            ).group(0))

        # download images to folder
        self._saveImagesFromPost(dlFilenames, imgStreamList)

    def _downloadUgoiraPost(self, illustId):
        """Downloads an ugoira post"""

        import ugoira.lib as Ugoira
        # this incorporates some functions from the ugoira library
        # found at https://github.com/item4/ugoira

        # get ugoira file
        print("Downloading ugoira and saving to GIF format")
        ugoiraData, frames = Ugoira.download_ugoira_zip(int(illustId))

        # convert to GIF and save to path
        Ugoira.make_gif(
            self._getFolderPath() + "{}.gif".format(str(illustId)),
            ugoiraData,
            frames
        )

        print("File written to {}.gif".format(self._getFolderPath() + illustId))

    def _saveImagesFromPost(self, dlFilenames : list, imgStreams : list):
        """Downloads the full arts and saves it in the folder"""
        # write files recursively
        for i, fileNames in enumerate(dlFilenames):
            with open(self._getFolderPath() + fileNames, "wb") as imgs:
                # write file
                imgs.write(imgStreams[i])
                print("File written to {}".format(self._getFolderPath() + fileNames))

    def _getFolderPath(self):
        """Get the folder path based on the system's OS."""
        if any(sys.platform == h for h in {"linux", "linux2", "cygwin", "darwin"}):
            # linux 2.6/linux/cygwin/osx
            return r"./{}/".format(self.DOWNLOADS_FOLDER)
        elif sys.platform == "win32":
            # windows
            return r".\\{}\\".format(self.DOWNLOADS_FOLDER)
