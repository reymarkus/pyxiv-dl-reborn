# pyxiv-dl Changelog

### 0.4.0
* Changed behavior of downloading images from downloading all images then saving them all at once to downloading the images and saving them one by one.
* Added file size output when an image is downloaded (not available on ugoira downloads due to limitations of `ugoira` library)
* `webcrawler.py`
    * Changed `saveImagesFromPost(list, list)` to `saveImageFromPost(str, bytes)`
        * To change the way the image downloads work, the above function needs to be modified in order to cater one-off downloads instead of aggregating data to lists and saving them to disk one by one.

### 0.3.3
* Fixed bug when attempting to download a non-existent post will throw an exception after the art not found message

### 0.3.2
* Fixed bug on range input where entering a range value less than 1 will still run the script, but will not get any output.

### 0.3.1
* Fixed bug on multi-image downloading without passing either `-i` or `-r`

### 0.3.0

* Added download range option (`-r`/`--range`) for multiple image posts
    * This enables you to download only a specific range of images based from the given starting and ending ranges.
* Added download index option (`-i`/`--index`) for multiple image posts
    * If you want to download only the specific image based on its image position (index) in the post, you can use this option.
* Necessary regression: multiple post download (e.g. `post1 post2 postn ...` is no longer possible due to the implementation of download range and download index options)
* Some bugfixes here and there, including some code smells reported by SonarCloud

### 0.2.0

* Added ugoira support
* Added a proper open-source license (yay, ready for initial use!)

### 0.1.1

* Added proper NSFW post checks. In this way, the `-n`/`--nsfw` flag is now working.

### 0.1.0

* Initial downloader support for single and multi-image posts. Ugoira support coming soon