# mkv2mp3-converter
Script for automatically converting the an audio track from an MKV file into a MP3 file with the desired tags.

## Requires FFMPEG
You need to have FFMPEG installed on your system. You can download it from [here](https://ffmpeg.org/download.html).
Preferably add the bin folder to your PATH

## Requires Python and Mutagen
You need to have Python installed on your system. You can download it from [here](https://www.python.org/downloads/).
You also need to have the Mutagen library installed. You can install it by running `pip install mutagen` or `pip install -r requirements.txt`

## Usage
Drag and drop the MKV file onto the **drag-n-drop.bat** file (or the main.py file, if your system supports it). The script will look at the MKV and list the available audio tracks along with their *Title* tag and ask you to select one, then read the default information from the **defaults.txt** file, followed by asking you if you'd like to change any of the information. When the script asks for Cover Art, you can either drag and drop an image file onto the console (to automatically enter the path to the image) or leave it empty to use the default cover art included.

## Output
Unless altered, the script will output the 320Kbps MP3 file in the users Music directory, with the Artist, Album, Title, Track Number, Year, Album Artist, Composer, and Cover Art as specified.

## Purpose
I got tired of manually converting the 2nd audio track from MKV files into MP3 files, by loading the MKV into Audacity, running my macros for eliminating intro- and outro-silence, updating the ID3 information and cover art manually with MP3tag, and then renaming the file to a URL-friendly format. So I made this script to automate the process.