#test_library_item.py
import pytest
from library_item import LibraryItem
from library_item import LibraryItemAlbum

def test_album_inheritance():
    album_item = LibraryItemAlbum("Numb", "Linkin Park", 5, "Meteora", 2003)
    assert album_item.album == "Meteora"
    assert album_item.year == 2003
    assert album_item.info() == "Numb - Linkin Park (Meteora, 2003) *****"

def test_initial_values():
    item = LibraryItem("Bohemian Rhapsody", "Queen", 5)
    assert item.name == "Bohemian Rhapsody"
    assert item.artist == "Queen"
    assert item.rating == 5
    assert item.play_count == 0

def test_info_output():
    item = LibraryItem("Imagine", "John Lennon", 4)
    expected = "Imagine - John Lennon ****"
    assert item.info() == expected

@pytest.mark.parametrize("rating, expected", [
    (0, ""),
    (1, "*"),
    (2, "**"),
    (3, "***"),
    (4, "****"),
    (5, "*****")
])

def test_stars_output(rating, expected):
    item = LibraryItem("Test", "Artist", rating)
    assert item.stars() == expected
