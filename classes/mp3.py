from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3


class mp3:

    @staticmethod
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

        # Edit ID3 tags
        mp3 = EasyID3(mp3_filename)
        mp3["title"] = title
        mp3["artist"] = artist
        mp3["albumartist"] = artist
        mp3["composer"] = artist
        mp3["album"] = album
        mp3["tracknumber"] = track
        mp3["date"] = year
        mp3["genre"] = genre
        mp3.save()

        # Embed cover image
        mp3 = MP3(mp3_filename, ID3=ID3)
        try:
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
        except Exception as e:
            print(f"An error occurred while embedding the cover image: {e}")

        try:
            mp3.save()
        except Exception as e:
            print(f"An error occurred while saving the MP3 file: {e}")
            return False
