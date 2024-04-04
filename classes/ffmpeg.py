import subprocess
import json


class ffmpeg:

    @staticmethod
    def list_audio_tracks(mkv_file):
        command = [
            "ffprobe",
            "-loglevel",
            "error",
            "-select_streams",
            "a",
            "-show_entries",
            "stream=index:stream_tags=title",
            "-of",
            "json",
            mkv_file,
        ]

        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode != 0:
            print("An error occurred while trying to list audio tracks.")
            return []

        streams_info = json.loads(result.stdout)
        audio_tracks = streams_info.get("streams", [])

        if not audio_tracks:
            print("No audio tracks found.")
            return []

        for track in audio_tracks:
            index = track.get("index", "Unknown")
            title = track.get("tags", {}).get("title", "Unknown")
            print(f"{index}: {title}")

        return audio_tracks

    @staticmethod
    def adjust_audio_track(selected_track):
        if int(selected_track) > 0:
            return int(selected_track) - 1
        else:
            return 0

    @staticmethod
    def extract_convert_trim_to_mp3(mkv_file, mp3_filename, audio_track=0):
        audio_track = f"0:a:{ffmpeg.adjust_audio_track(audio_track)}"

        command = [
            "ffmpeg",  # Change to full path if ffmpeg is not in PATH
            "-i",
            mkv_file,  # Input file
            "-map",
            audio_track,  # Select the second audio track. Change to 0:a:0 for the first.
            "-af",
            "silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:stop_periods=1:stop_duration=1:stop_threshold=-60dB",  # Silence removal filter
            "-b:a",
            "320k",  # Bitrate 320kbps
            "-ac",
            "2",  # Stereo
            mp3_filename,  # Output file
        ]
        subprocess.run(command, check=True)
