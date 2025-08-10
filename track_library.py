#track_library.py
import csv
import os
import shutil
from library_item import LibraryItem, LibraryItemAlbum

class TrackLibrary:
    def __init__(self, track_csv="tracks.csv", img_folder="track_images", sound_folder="track_sounds"):
        self.track_csv = track_csv
        self.img_folder = img_folder
        self.sound_folder = sound_folder
        self.library = {}
        self.load_library_from_csv()

    def load_library_from_csv(self):
        self.library = {}
        if not os.path.exists(self.track_csv):
            return
        with open(self.track_csv, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                track_id = row["track_id"]
                name = row["name"]
                artist = row["artist"]
                rating = int(row["rating"])
                plays = int(row["plays"])
                album = row.get("album", "").strip()
                year_raw = row.get("year", "").strip()
                year = int(year_raw) if year_raw.isdigit() else None

                if album and year:
                    item = LibraryItemAlbum(name, artist, rating, album, year)
                else:
                    item = LibraryItem(name, artist, rating)

                item.play_count = plays
                self.library[track_id] = item
    def save_library_to_csv(self):
        with open(self.track_csv, mode="w", encoding="utf-8", newline="") as file:
            fieldnames = ["track_id", "name", "artist", "rating", "plays", "album", "year"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for key, item in self.library.items():
                writer.writerow({
                    "track_id": key,
                    "name": item.name,
                    "artist": item.artist,
                    "rating": item.rating,
                    "plays": item.play_count,
                    "album": getattr(item, "album", ""),
                    "year": getattr(item, "year", "")
                })
    def add_track(self, track_id, name, artist, rating, album="", year=None, image_path=None, audio_path=None):
        if track_id in self.library:
            return False, "Track ID already exists."

        if album and year:
            item = LibraryItemAlbum(name, artist, rating, album, year)
        else:
            item = LibraryItem(name, artist, rating)

        self.library[track_id] = item
        self.save_library_to_csv()

        # Copy image
        if image_path:
            dest_img = os.path.join(self.img_folder, f"{track_id}.jpg")
            try:
                shutil.copy(image_path, dest_img)
            except Exception as e:
                print(f"Image copy failed: {e}")

        # Copy audio
        if audio_path:
            dest_audio = os.path.join(self.sound_folder, f"{track_id}.mp3")
            try:
                shutil.copy(audio_path, dest_audio)
            except Exception as e:
                print(f"Audio copy failed: {e}")

        return True, "Track added successfully."
    def remove_track(self, track_id):
        if track_id not in self.library:
            return False, "Track ID not found."
        del self.library[track_id]
        self.save_library_to_csv()

        # Remove files
        img = os.path.join(self.img_folder, f"{track_id}.jpg")
        aud = os.path.join(self.sound_folder, f"{track_id}.mp3")
        if os.path.exists(img): os.remove(img)
        if os.path.exists(aud): os.remove(aud)
        return True, "Track removed."

    # --- Accessor Methods ---

    def get_keys(self):
        return list(self.library.keys())
    def get_item(self, key):
        return self.library.get(key)
    def get_name(self, key):
        item = self.get_item(key)
        return item.name if item else None
    def get_artist(self, key):
        item = self.get_item(key)
        return item.artist if item else None
    def get_rating(self, key):
        item = self.get_item(key)
        return item.rating if item else -1
    def get_play_count(self, key):
        item = self.get_item(key)
        return item.play_count if item else -1
    def increment_play_count(self, key):
        item = self.get_item(key)
        if item:
            item.play_count += 1
            self.save_library_to_csv()
    def set_rating(self, key, rating):
        item = self.get_item(key)
        if item:
            item.rating = rating
            self.save_library_to_csv()



