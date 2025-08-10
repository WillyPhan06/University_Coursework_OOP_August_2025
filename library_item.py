#library_item.py
class LibraryItem:
    def __init__(self, name, artist, rating=0):
        self.name = name
        self.artist = artist
        self.rating = rating
        self.play_count = 0

    def info(self):
        return f"{self.name} - {self.artist} {self.stars()}"

    def stars(self):
        stars = ""
        for i in range(self.rating):
            stars += "*"
        return stars

class LibraryItemAlbum(LibraryItem):
    def __init__(self, name, artist, rating=0, album="", year=None):
        super().__init__(name, artist, rating)
        self.album = album
        self.year = year

    def info(self):
        base_info = super().info()
        return f"{self.name} - {self.artist} ({self.album}, {self.year}) {self.stars()}"

