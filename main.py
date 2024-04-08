import sys
from datetime import date
from classes import mp3, datahandler, ffmpeg, cli


# Gather MKV file and audio track information
if len(sys.argv) < 2:
    mkv_file = cli.request_new_value("mkv_file", None)
    mkv_file = datahandler.clean_path(mkv_file)
else:
    mkv_file = sys.argv[1]
audio_tracks = ffmpeg.list_audio_tracks(mkv_file)
if audio_tracks:
    selected_track = cli.select_audio_track(audio_tracks)
    if selected_track is not None:
        print(f"You've selected track {selected_track}.")
    else:
        print("Exiting without selection.")
else:
    print("Could not list audio tracks or no audio tracks available.")
    exit(1)

# Gather default ID3 tag information and output directory
defaults = datahandler.read_defaults()
mp3_path = defaults.get("output_dir", "Music")
mp3_path = cli.request_new_value("output_dir", mp3_path)

artist = defaults.get("artist", "Unknown Artist")
album = defaults.get("album", "Unknown Album")
title = defaults.get("title", "Unknown Title")
track = defaults.get("track", "1")
genre = defaults.get("genre", "Unknown Genre")
year = defaults.get("year", str(date.today().year))
cover_image = defaults.get("cover_image", "default-cover.png")


# Ask user for new ID3 tag information
artist = cli.request_new_value("artist", artist)
album = cli.request_new_value("album", album)
track = cli.request_new_value("track", track)
year = cli.request_new_value("year", year)
genre = cli.request_new_value("genre", genre)
title = datahandler.parse_track_title(track, genre)
title = cli.request_new_value("title", title)
cover_image = cli.request_new_value("cover_image", cover_image)
cover_image = datahandler.clean_path(cover_image)
playlist_file = cli.request_new_value("playlist_file", None)
playlist_file = datahandler.clean_path(playlist_file)
mp3_file = datahandler.parse_filename(artist, album, track, genre)
mp3_filename = datahandler.parse_path(mp3_path, mp3_file)


# Convert selected audio track to MP3 and update ID3 tags
ffmpeg.extract_convert_trim_to_mp3(mkv_file, mp3_filename, selected_track)
mp3.edit_id3_tags(mp3_filename, title, artist, album, track, year, genre)
mp3.embed_cover_image(mp3_filename, cover_image)
if playlist_file is not None:
    chapters, chapters_list = datahandler.parse_playlist(playlist_file)
    mp3.embed_chapters(mp3_filename, chapters, chapters_list)

# Update defaults with new ID3 tag information
track = int(track) + 1
datahandler.update_default("title", title)
datahandler.update_default("artist", artist)
datahandler.update_default("album", album)
datahandler.update_default("year", year)
datahandler.update_default("track", str(track))
datahandler.update_default("genre", genre)
