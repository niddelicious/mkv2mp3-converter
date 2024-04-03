import os
import sys
import subprocess
from datetime import date
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3


def request_new_value(key, current_value):
    new_value = input(
        f"Enter new value for {key} (or press Enter to keep '{current_value}'): "
    )
    new_value = new_value.strip()
    return new_value if new_value else current_value


def parse_track_title(track, genre):
    if track and genre:
        title = f"Episode {track} - {genre}"
    return title


def read_defaults(defaults_file="defaults.txt"):
    defaults = {}
    try:
        with open(defaults_file, "r") as f:
            for line in f:
                key, value = line.strip().split("=", 1)
                defaults[key] = value
    except FileNotFoundError:
        print(
            f"Warning: Default file '{defaults_file}' not found. Using hardcoded defaults."
        )
    return defaults


defaults = read_defaults()


def update_default(key, value, defaults_file="defaults.txt"):
    defaults = read_defaults(defaults_file)
    defaults[key] = value
    with open(defaults_file, "w") as f:
        for key, value in defaults.items():
            f.write(f"{key}={value}\n")


def clean_path(path: str):
    try:
        file_path = path.strip("'\"")
        return file_path

    except Exception as e:
        print(f"An error occurred: {e}")


if len(sys.argv) < 2:
    mkv_file = request_new_value("mkv_file", None)
    mkv_file = clean_path(mkv_file)
else:
    mkv_file = sys.argv[1]
mp3_file = "output.mp3"
mp3_path = defaults.get("output_dir", "Music")
mp3_path = request_new_value("output_dir", mp3_path)


def parse_path(path, filename):
    user_dir = os.path.expanduser("~")
    output_dir = os.path.join(user_dir, path)
    full_path = os.path.join(output_dir, filename)
    return full_path


artist = defaults.get("artist", "Unknown Artist")
album = defaults.get("album", "Unknown Album")

title = defaults.get("title", "Unknown Title")
track = defaults.get("track", "1")
genre = defaults.get("genre", "Unknown Genre")

year = defaults.get("year", str(date.today().year))

cover_image = defaults.get("cover_image", "default-cover.png")


artist = request_new_value("artist", artist)
album = request_new_value("album", album)
track = request_new_value("track", track)
year = request_new_value("year", year)
genre = request_new_value("genre", genre)
title = parse_track_title(track, genre)
title = request_new_value("title", title)

cover_image = request_new_value("cover_image", cover_image)


cover_image = clean_path(cover_image)


def parse_filename_element(element: str):
    return element.replace(" ", "-").lower()


def parse_filename(artist, album, track, genre):
    filename_artist = parse_filename_element(artist)
    filename_album = parse_filename_element(album)
    filename_track = parse_filename_element(track)
    filename_genre = parse_filename_element(genre)
    filename = (
        f"{filename_artist}-{filename_album}-{filename_track}-{filename_genre}.mp3"
    )
    return filename


mp3_file = parse_filename(artist, album, track, genre)
mp3_filename = parse_path(mp3_path, mp3_file)


def extract_convert_trim_to_mp3(mkv_file, mp3_filename):
    command = [
        "ffmpeg",  # Change to full path if ffmpeg is not in PATH
        "-i",
        mkv_file,  # Input file
        "-map",
        "0:a:1",  # Select the second audio track. Change to 0:a:0 for the first.
        "-af",
        "silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:stop_periods=1:stop_duration=1:stop_threshold=-60dB",  # Silence removal filter
        "-b:a",
        "320k",  # Bitrate 320kbps
        "-ac",
        "2",  # Stereo
        mp3_filename,  # Output file
    ]
    subprocess.run(command, check=True)


def edit_id3_tags(
    mp3_filename: str,
    title: str,
    artist: str,
    album: str,
    track: str,
    year: str,
    genre: str,
    cover_image: str,
):

    mp3 = EasyID3(mp3_filename)

    mp3["title"] = title
    mp3["artist"] = artist
    mp3["album"] = album
    mp3["tracknumber"] = track
    mp3["date"] = year
    mp3["genre"] = genre
    mp3["albumartist"] = artist
    mp3["composer"] = artist
    mp3.save()

    # Embed cover image

    mp3 = MP3(mp3_filename, ID3=ID3)
    with open(cover_image, "rb") as albumart:
        if cover_image.endswith("jpg"):
            mime_type = "image/jpeg"
        elif cover_image.endswith("png"):
            mime_type = "image/png"
        else:
            raise ValueError("Cover image must be either a JPEG or PNG file.")
        mp3.tags.add(
            APIC(
                encoding=3,
                mime=mime_type,
                type=3,  # Cover image (front)
                desc="Cover",
                data=albumart.read(),
            )
        )
    mp3.save()


extract_convert_trim_to_mp3(mkv_file, mp3_filename)
edit_id3_tags(mp3_filename, title, artist, album, track, year, genre, cover_image)

track = int(track) + 1

update_default("title", title)
update_default("artist", artist)
update_default("album", album)
update_default("year", year)
update_default("track", str(track))
update_default("genre", genre)
