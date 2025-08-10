

# 🎵 Jukebox Simulation – University OOP Coursework

This repository contains my **Object-Oriented Programming coursework** for the University of Greenwich (August 2025).  
It’s a **Tkinter-based Jukebox Simulation** built in Python, allowing users to **view, search, filter, create playlists, update tracks, and play music** with cover images and audio.

---

## 📦 Features

- **View Tracks** – Browse the music library with dynamic cover images, star ratings, and play counts.
- **Search & Filter** – Search by name or artist, filter by artist, rating, or play count range.
- **Playlist Creation** – Add multiple tracks at once, save/load playlists, and play/pause music.
- **Track Management** – Add, update, or delete tracks with media uploads (image/audio).
- **Media Integration** – Organized local storage for cover images (`track_images/`) and audio files (`track_sounds/`).
- **OOP Design** – Encapsulation, inheritance, and modularity for maintainability and scalability.

---

## 🖥️ Technology Stack

- **Language:** Python 3.12  
- **GUI Framework:** Tkinter & ttk  
- **Audio Playback:** Pygame  
- **Image Handling:** Pillow (PIL)  
- **Data Storage:** CSV files (`tracks.csv`, `playlist.csv`)  
- **Testing:** unittest / pytest

---

## 📂 Project Structure

```bash
University\_Coursework\_OOP\_August\_2025/
├── single\_gui.py             # Main entry point (launch from here)
├── view\_tracks\_tab.py        # View/Search/Filter tab
├── create\_track\_list\_tab.py  # Playlist creation tab
├── update\_tracks\_tab.py      # Track management tab
├── track\_library.py          # Backend logic & data handling
├── library\_item.py           # Track model classes
├── font\_manager.py           # Global font settings
├── tracks.csv                # Track metadata
├── playlist.csv              # Example playlist
├── track\_images/             # Cover images
├── track\_sounds/             # Audio files
├── test\_library\_item.py      # Unit tests for model classes
├── requirements.txt          # Project dependencies
└── OOP\_CW\_GCS240359\_Phan\_Tuan\_Bao.pdf  # Full coursework report
````

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/WillyPhan06/University_Coursework_OOP_August_2025.git
cd University_Coursework_OOP_August_2025
````

### 2. Install dependencies

Make sure you have **Python 3.12+** installed, then run:

```bash
pip install -r requirements.txt
```

> `tkinter` comes pre-installed with most Python distributions.

### 3. Run the application

From the project root:

```bash
python single_gui.py
```

---

## 📝 Usage

1. **View Tracks Tab**

   * Browse the library with images, ratings, and play counts.
   * Search or filter to find tracks quickly.
2. **Create Playlist Tab**

   * Add multiple tracks by ID, save/load playlists, and play/pause songs.
3. **Update Tracks Tab**

   * Add new tracks with image/audio, update ratings or metadata, delete tracks by ID.
4. **Data Persistence**

   * All updates are saved to `tracks.csv`, images to `track_images/`, and audio to `track_sounds/`.

---

## 🧪 Testing

Run the included unit tests:

```bash
python test_library_item.py
```


---

## 📄 License

This project was developed for academic purposes as part of my university coursework.
You’re welcome to explore, but please **do not plagiarize** for academic submissions.


