# 🎥✨ Timeliner for DaVinci Resolve

Timeliner automatically creates a DaVinci Resolve timeline with the contents of an ordered directory of video files.

It adds blanks between the videos to allow time for crowd reactions.

## Installation

### Requirements

- Python
- Pyenv
- DaVinci Resolve (tested with version 18.1.16)

## Usage

> **Note:** The script will only work if the DaVinci Resolve project is already open.

```bash
python timeliner.py <path_to_directory>
```

The directory must contain video files without special characters in their names (spaced are allowed). The files will be sorted alphabetically and added to the timeline in the same order.

Example:

```bash
MyMovie/
|- 00 Intro.MP4
|- 01 First video.MP4
|- 02 Second video.MP4
...
|- 99 Outro.MP4
``` 