import os
import re


class datahandler:

    @staticmethod
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

    @staticmethod
    def update_default(key, value, defaults_file="defaults.txt"):
        defaults = datahandler.read_defaults(defaults_file)
        defaults[key] = value
        with open(defaults_file, "w") as f:
            for key, value in defaults.items():
                f.write(f"{key}={value}\n")

    @staticmethod
    def clean_path(path: str):
        try:
            file_path = path.strip("'\"")
            return file_path

        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def parse_path(path, filename):
        user_dir = os.path.expanduser("~")
        output_dir = os.path.join(user_dir, path)
        full_path = os.path.join(output_dir, filename)
        return full_path

    @staticmethod
    def parse_filename_element(element: str):
        return element.replace(" ", "-").lower()

    @staticmethod
    def parse_filename(artist, album, track, genre):
        filename_artist = datahandler.parse_filename_element(artist)
        filename_album = datahandler.parse_filename_element(album)
        filename_track = datahandler.parse_filename_element(track)
        filename_genre = datahandler.parse_filename_element(genre)
        filename = (
            f"{filename_artist}-{filename_album}-{filename_track}-{filename_genre}.mp3"
        )
        return filename

    @staticmethod
    def parse_track_title(track, genre):
        if track and genre:
            title = f"Episode {track} - {genre}"
        return title

    @staticmethod
    def parse_playlist(playlist_file):
        with open(playlist_file, "r") as file:
            lines = file.readlines()
            chapters, chapters_list = datahandler.parse_chapters(lines)
        return chapters, chapters_list

    @staticmethod
    def parse_playlist_line(timestamp):
        pattern = re.compile(r"\[(\d{2}):(\d{2}):?(\d{2})?\] (.+)")
        match = pattern.match(timestamp)
        if match:
            hours, minutes, seconds = match.group(1), match.group(2), match.group(3)
            if seconds is None:  # Format [MM:SS]
                seconds = minutes
                minutes = hours
                hours = 0
            else:  # Format [HH:MM:SS]
                hours = int(hours)
            hours = int(hours)
            minutes = int(minutes)
            seconds = int(seconds)
            timestamp = hours * 3600 + minutes * 60 + seconds
            timestamp = timestamp * 1000  # Convert to milliseconds
            artist_title = match.group(4)
            artist, title = artist_title.split(" - ", 1)
        return timestamp, artist, title

    @staticmethod
    def parse_chapters(lines):
        chapters = []
        chapters_list = []
        for i, line in enumerate(lines):
            start_timestamp, artist, title = datahandler.parse_playlist_line(line)

            # Look ahead for the next track's start timestamp to use as the current track's end timestamp
            if i + 1 < len(lines):
                end_timestamp, next_artist, next_title = (
                    datahandler.parse_playlist_line(lines[i + 1])
                )
            else:
                end_timestamp = None
            chapters.append(
                {
                    "start_timestamp": start_timestamp,
                    "end_timestamp": end_timestamp,
                    "artist": artist,
                    "title": title,
                    "id": f"trk{i + 1}",
                }
            )
            chapters_list.append(f"trk{i + 1}")

        return chapters, chapters_list
