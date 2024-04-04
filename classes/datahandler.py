import os


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
