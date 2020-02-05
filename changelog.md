# pyxiv-dl Changelog


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