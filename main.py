import os
import shutil
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

def sanitize_name(name):
    """Sanitize folder names to avoid issues with invalid characters."""
    return "".join(c for c in name if c.isalnum() or c in " .-_()").strip()

def organize_mp3s():
    path_source_input = input("Please enter source path: ")
    path_destination_input = input("Please enter destination path: ")

    for filename in os.listdir(path_source_input):
        if not filename.lower().endswith(".mp3"):
            continue
        
        filepath = os.path.join(path_source_input, filename)

        try:
            audio = MP3(filepath, ID3=EasyID3)
            artist = audio.get('artist', ['Unknown Artist'])[0]
            album = audio.get('album', ['Unknown Album'])[0]

            artist_folder = sanitize_name(artist)
            album_folder = sanitize_name(album)

            target_dir = os.path.join(path_destination_input, artist_folder, album_folder)
            os.makedirs(target_dir, exist_ok=True)

            target_path = os.path.join(target_dir, filename)
            print(f"Moving '{filename}' to '{target_path}'")
            shutil.move(filepath, target_path)

        except Exception as e:
            print(f"Error processing '{filename}': {e}")

if __name__ == "__main__":
    organize_mp3s()


# TODO:
# can make this into an all-in-one with spotdl. This would allow me to implement custom code to prevent duplicates in the nested folders