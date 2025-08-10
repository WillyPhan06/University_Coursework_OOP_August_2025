#update_tracks_tab.py
import tkinter as tk
from tkinter import filedialog, ttk, Canvas
import shutil
from library_item import LibraryItemAlbum

class UpdateTracksTab(ttk.Frame):
    def __init__(self, master, lib):
        super().__init__(master)
        self.lib = lib
        self.selected_image_path = None
        self.selected_audio_path = None

        self.build_update_tab()
        self.view_all()

    def build_update_tab(self):
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # === LEFT: Track Editor ===
        editor_frame = tk.Frame(main_frame)
        editor_frame.pack(side="left", fill="y", padx=(0, 20), anchor="n")

        self.editor_entries = {}
        for idx, label in enumerate(["Track ID", "Name", "Artist", "Rating", "Album", "Year"]):
            tk.Label(editor_frame, text=f"{label}:").grid(row=idx, column=0, sticky="e")
            entry = tk.Entry(editor_frame, width=30)
            entry.grid(row=idx, column=1, padx=5, pady=2)
            self.editor_entries[label.lower()] = entry

        tk.Button(editor_frame, text="Select Image",bg="#ffe0b2" ,command=self.select_image).grid(row=0, column=2, padx=10)
        tk.Button(editor_frame, text="Select Audio",bg="#f0f4c3" ,command=self.select_audio).grid(row=1, column=2, padx=10)

        btn_frame = tk.Frame(editor_frame)
        btn_frame.grid(row=7, column=0, columnspan=3, pady=10)
        tk.Button(btn_frame, text="Add Track",bg="#c8e6c9" ,command=self.add_track).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Update Track Info",bg="#bbdefb" ,command=self.update_track_info).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="Delete Track by ID",bg="#ffcdd2" ,command=self.delete_track).grid(row=0, column=2, padx=10)

        self.status_label = tk.Label(editor_frame, text="", font=("Helvetica", 10))
        self.status_label.grid(row=8, column=0, columnspan=3, pady=5)

        # === RIGHT: Search, Filter, and Track List ===
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="left", fill="both", expand=True)

        # Top: Search and Filter
        top_controls = tk.Frame(right_frame)
        top_controls.pack(fill="x", pady=(0, 10))

        tk.Label(top_controls, text="Search:").pack(side="left")
        self.search_entry = tk.Entry(top_controls, width=30)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(top_controls, text="Go",bg="#c8e6c9" ,command=self.search_clicked).pack(side="left")

        tk.Label(top_controls, text="Filter by:").pack(side="left", padx=(20, 5))
        self.filter_type = ttk.Combobox(top_controls, width=12, state="readonly")
        self.filter_type['values'] = ["Artist", "Rating", "Play Count"]
        self.filter_type.pack(side="left")
        self.filter_type.bind("<<ComboboxSelected>>", self.update_filter_values)

        self.filter_value = ttk.Combobox(top_controls, width=20, state="readonly")
        self.filter_value.pack(side="left", padx=5)
        tk.Button(top_controls, text="Apply",bg="#e1bee7" ,command=self.apply_filter).pack(side="left")

        # Bottom: Scrollable track list
        self.canvas = Canvas(right_frame)
        self.scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    def select_image(self):
        self.selected_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg")])
        if self.selected_image_path:
            self.status_label.configure(text="Image selected.")
    def select_audio(self):
        self.selected_audio_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3")])
        if self.selected_audio_path:
            self.status_label.configure(text="Audio selected.")
    def clear_editor_fields(self):
        for entry in self.editor_entries.values():
            entry.delete(0, tk.END)
        self.selected_image_path = None
        self.selected_audio_path = None
    def delete_track(self):
        track_id = self.editor_entries["track id"].get().strip().zfill(2)
        if track_id not in self.lib.get_keys():
            self.status_label.configure(text="Track ID not found.")
            return

        self.lib.remove_track(track_id)
        self.status_label.configure(text=f"Track {track_id} deleted.")
        self.clear_editor_fields()
        self.view_all()
    def update_track_info(self):
        track_id = self.editor_entries["track id"].get().strip().zfill(2)
        if track_id not in self.lib.get_keys():
            self.status_label.configure(text="Track ID not found.")
            return

        name = self.editor_entries["name"].get().strip()
        artist = self.editor_entries["artist"].get().strip()
        rating = self.editor_entries["rating"].get().strip()
        album = self.editor_entries["album"].get().strip()
        year = self.editor_entries["year"].get().strip()

        item = self.lib.get_item(track_id)
        if name:
            item.name = name
        if artist:
            item.artist = artist
        if rating.isdigit():
            rating_val = int(rating)
            if 0 <= rating_val <= 5:
                item.rating = rating_val
            else:
                self.status_label.configure(text="Rating must be between 0 and 5.")
                return
        elif rating:
            self.status_label.configure(text="Invalid rating input.")
            return

        needs_album = bool(album)
        needs_year = year.isdigit()
        if not isinstance(item, LibraryItemAlbum) and (needs_album or needs_year):
            new_album = album if needs_album else ""
            new_year = int(year) if needs_year else 0
            new_item = LibraryItemAlbum(item.name, item.artist, item.rating, new_album, new_year)
            new_item.play_count = item.play_count
            self.lib.library[track_id] = new_item
            item = new_item

        if album:
            item.album = album
        if year.isdigit():
            item.year = int(year)

        self.lib.save_library_to_csv()

        if self.selected_image_path:
            shutil.copy(self.selected_image_path, f"track_images/{track_id}.jpg")
        if self.selected_audio_path:
            shutil.copy(self.selected_audio_path, f"track_sounds/{track_id}.mp3")

        self.status_label.configure(text="Track updated successfully.")
        self.clear_editor_fields()
        self.view_all()
    def add_track(self):
        track_id = self.editor_entries["track id"].get().strip().zfill(2)
        name = self.editor_entries["name"].get().strip()
        artist = self.editor_entries["artist"].get().strip()
        rating = self.editor_entries["rating"].get().strip()
        album = self.editor_entries["album"].get().strip()
        year = self.editor_entries["year"].get().strip()

        if not (track_id and name and artist and rating.isdigit()):
            self.status_label.configure(text="Missing or invalid input.")
            return

        if track_id in self.lib.get_keys():
            self.status_label.configure(text="Track ID already exists.")
            return

        if not self.selected_audio_path:
            self.status_label.configure(text="Audio file required for new track.")
            return

        year_val = int(year) if year.isdigit() else None
        success, msg = self.lib.add_track(
            track_id, name, artist, int(rating), album, year_val,
            self.selected_image_path, self.selected_audio_path
        )
        self.status_label.configure(text=msg)
        self.clear_editor_fields()
        self.view_all()
    def search_clicked(self):
        query = self.search_entry.get().strip().lower()
        result_keys = [
            key for key in self.lib.get_keys()
            if query in self.lib.get_name(key).lower() or query in self.lib.get_artist(key).lower()
        ]
        self.display_tracks_by_keys(result_keys)
    def update_filter_values(self, event=None):
        choice = self.filter_type.get()
        if choice == "Artist":
            values = sorted(set(self.lib.get_artist(k) for k in self.lib.get_keys()))
        elif choice == "Rating":
            values = [str(i) for i in range(6)]
        elif choice == "Play Count":
            values = ["0-10", "11-20", "21-50", "51+"]
        else:
            values = []
        self.filter_value['values'] = values
        self.filter_value.set("")
    def apply_filter(self):
        filter_type = self.filter_type.get()
        filter_value = self.filter_value.get().strip()
        base_keys = self.lib.get_keys()
        result_keys = []

        for key in base_keys:
            if filter_type == "Artist" and self.lib.get_artist(key).lower() == filter_value.lower():
                result_keys.append(key)
            elif filter_type == "Rating" and str(self.lib.get_rating(key)) == filter_value:
                result_keys.append(key)
            elif filter_type == "Play Count":
                count = self.lib.get_play_count(key)
                if (filter_value == "0-10" and count <= 10 or
                        filter_value == "11-20" and 11 <= count <= 20 or
                        filter_value == "21-50" and 21 <= count <= 50 or
                        filter_value == "51+" and count >= 51):
                    result_keys.append(key)

        self.display_tracks_by_keys(result_keys)
    def view_all(self):
        self.display_tracks_by_keys(self.lib.get_keys())
    def display_tracks_by_keys(self, keys):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for key in keys:
            name = self.lib.get_name(key)
            artist = self.lib.get_artist(key)
            rating = self.lib.get_rating(key)
            stars = '*' * rating
            plays = self.lib.get_play_count(key)

            frame = ttk.Frame(self.scrollable_frame, relief="solid", borderwidth=1)
            frame.pack(fill="x", padx=5, pady=3)

            info = f"Track {key}: {name}\nArtist: {artist}\nRating: {stars}\nPlays: {plays}"
            tk.Label(frame, text=info, justify="left").pack(side="left", padx=10)
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    def refresh(self):
        self.view_all()