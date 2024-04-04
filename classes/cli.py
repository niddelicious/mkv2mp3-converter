class cli:

    @staticmethod
    def select_audio_track(audio_tracks: dict):
        while True:
            track_number = input(
                "Enter the track number to select (or 'exit' to quit): "
            )
            if track_number.lower() == "exit":
                return None
            if track_number.isdigit() and any(
                track
                for track in audio_tracks
                if str(track.get("index")) == track_number
            ):
                return track_number
            print("Invalid track number. Please try again.")

    @staticmethod
    def request_new_value(key, current_value):
        new_value = input(
            f"Enter new value for {key} (or press Enter to keep '{current_value}'): "
        )
        new_value = new_value.strip()
        return new_value if new_value else current_value
