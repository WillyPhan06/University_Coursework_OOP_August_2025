#create_track_list_tab.py
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import pygame
import os
import threading
import time

class CreateTrackListTab(ttk.Frame):
    def __init__(self, master, lib):
        super().__init__(master)
        self.lib = lib
        self.playlist = []
        self.is_playing = False
        self.is_paused = False
        self.current_track_index = 0

        pygame.mixer.init()
        self._load_icons()
        self.build_create_tab()

    def _load_icons(self):
        self.icons = {}
        try:
            self.icons['add'] = ImageTk.PhotoImage(Image.open("icons/add.png").resize((18, 18)))
            self.icons['reset'] = ImageTk.PhotoImage(Image.open("icons/reset.png").resize((18, 18)))
            self.icons['play'] = ImageTk.PhotoImage(Image.open("icons/play.png").resize((18, 18)))
            self.icons['pause'] = ImageTk.PhotoImage(Image.open("icons/pause.png").resize((18, 18)))
            self.icons['save'] = ImageTk.PhotoImage(Image.open("icons/save.png").resize((18, 18)))
            self.icons['load'] = ImageTk.PhotoImage(Image.open("icons/load.png").resize((18, 18)))
            self.icons['remove'] = ImageTk.PhotoImage(Image.open("icons/remove.png").resize((18, 18)))
        except:
            print("[Warning] Could not load icons. Make sure the 'icons/' folder exists with proper PNG files.")
    def build_create_tab(self):
        tk.Label(self, text="Enter track numbers (comma-separated):").grid(row=0, column=0, padx=10, pady=10)
        self.create_entry = tk.Entry(self, width=30)
        self.create_entry.grid(row=0, column=1, padx=10, pady=10)

        self.create_status = tk.Label(self, text="", font=("Helvetica", 10))
        self.create_status.grid(row=1, column=0, columnspan=2)

        self.create_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE, width=80, height=12)
        self.create_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text=" Add", image=self.icons.get('add'), compound="left",bg="#c8e6c9" ,command=self.create_add).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Remove", image=self.icons.get('remove'), compound="left",bg="#ffcdd2" ,command=self.remove_entered).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text=" Reset", image=self.icons.get('reset'), compound="left",bg="#ffe0b2" ,command=self.create_reset).grid(row=0, column=2, padx=10)
        self.play_button = tk.Button(btn_frame, text=" Play", image=self.icons.get('play'), compound="left",bg="#f0f4c3" ,command=self.play_playlist)
        self.play_button.grid(row=0, column=3, padx=10)
        self.pause_button = tk.Button(btn_frame, text=" Pause", image=self.icons.get('pause'), compound="left",bg="#f5f5dc" ,command=self.pause_audio)
        self.pause_button.grid(row=0, column=4, padx=10)
        tk.Button(btn_frame, text=" Save", image=self.icons.get('save'), compound="left",bg="#bbdefb" ,command=self.save_playlist).grid(row=0, column=5, padx=10)
        tk.Button(btn_frame, text=" Load", image=self.icons.get('load'), compound="left",bg="#e1bee7" ,command=self.load_playlist).grid(row=0, column=6, padx=10)
    def create_add(self):
        raw = self.create_entry.get().strip()
        if not raw:
            self.create_status.config(text="Please enter at least one track number.")
            return

        input_keys = [x.strip().zfill(2) for x in raw.split(',')]
        new_keys = []
        invalid = []

        for key in input_keys:
            if not key.isdigit() or self.lib.get_name(key) is None:
                invalid.append(key)
            elif key not in self.playlist and key not in new_keys:
                new_keys.append(key)

        self.playlist.extend(new_keys)
        self.refresh_listbox()

        if invalid:
            self.create_status.config(text=f"Invalid: {', '.join(invalid)}")
        elif not new_keys:
            self.create_status.config(text="No new valid tracks to add.")
        else:
            self.create_status.config(text="Tracks added.")

        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.current_track_index = 0
        self.play_button.config(state=tk.NORMAL)
    def refresh_listbox(self):
        self.create_listbox.delete(0, tk.END)
        for key in self.playlist:
            name = self.lib.get_name(key)
            artist = self.lib.get_artist(key)
            rating = "*" * self.lib.get_rating(key)
            plays = self.lib.get_play_count(key)
            self.create_listbox.insert(tk.END, f"{key}: {name} - {artist} | Rating: {rating} | Plays: {plays}")
    def create_reset(self):
        self.playlist.clear()
        self.create_listbox.delete(0, tk.END)
        self.create_status.config(text="Playlist reset.")
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.current_track_index = 0
        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(text="Pause")
    def remove_entered(self):
        raw = self.create_entry.get().strip()
        if not raw:
            self.create_status.config(text="Please enter track IDs to remove.")
            return

        input_keys = [x.strip().zfill(2) for x in raw.split(',')]
        removed = []
        invalid = []

        for key in input_keys:
            if not key.isdigit():
                invalid.append(key)
            elif key in self.playlist and key not in removed:
                self.playlist.remove(key)
                removed.append(key)
            elif key not in self.playlist:
                invalid.append(key)

        self.refresh_listbox()
        self.is_playing = False
        self.is_paused = False
        pygame.mixer.music.stop()
        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(text="Pause")

        if removed and invalid:
            self.create_status.config(text=f"Removed: {', '.join(removed)} | Invalid: {', '.join(invalid)}")
        elif removed:
            self.create_status.config(text=f"Removed: {', '.join(removed)}")
        elif invalid:
            self.create_status.config(text=f"No valid tracks found. Invalid: {', '.join(invalid)}")
    def monitor_playback(self):
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        if not self.is_paused:
            self.current_track_index += 1
            self.play_next_track()
    def play_playlist(self):
        if not self.playlist:
            self.create_status.config(text="No tracks in playlist.")
            self.play_button.config(state=tk.NORMAL)
            return

        if self.is_paused:
            pygame.mixer.music.unpause()
            self.create_status.config(text="Playback resumed.")
            self.is_paused = False
            return

        if self.is_playing:
            return

        self.play_button.config(state=tk.DISABLED)
        self.current_track_index = 0
        self.play_next_track()
    def play_next_track(self):
        if self.current_track_index >= len(self.playlist):
            self.create_status.config(text="All tracks played.")
            self.is_playing = False
            self.play_button.config(state=tk.NORMAL)
            return

        key = self.playlist[self.current_track_index]
        audio_path = f"track_sounds/{key}.mp3"

        if os.path.exists(audio_path):
            try:
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()
                self.pause_button.config(text="Pause")
                self.lib.increment_play_count(key)
                self.refresh_listbox()
                self.create_status.config(text=f"Now playing: {key}")
                self.is_playing = True
                self.is_paused = False
                threading.Thread(target=self.monitor_playback, daemon=True).start()
            except Exception as e:
                self.create_status.config(text=f"Error playing track {key}")
                print("Audio error:", e)
                self.current_track_index += 1
                self.play_next_track()
        else:
            self.create_status.config(text=f"Skipped: {key} (no audio)")
            self.current_track_index += 1
            self.play_next_track()
    def pause_audio(self):
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.create_status.config(text="Paused.")
            self.is_paused = True
            self.pause_button.config(text="Resume")
        elif self.is_playing and self.is_paused:
            pygame.mixer.music.unpause()
            self.create_status.config(text="Resumed.")
            self.is_paused = False
            self.pause_button.config(text="Pause")
            self.play_button.config(state=tk.DISABLED)
    def save_playlist(self):
        if not self.playlist:
            self.create_status.config(text="No tracks to save.")
            return

        try:
            with open("playlist.csv", "w") as f:
                for track_id in self.playlist:
                    f.write(track_id + "\n")
            self.create_status.config(text="Playlist saved.")
        except Exception as e:
            print("Save error:", e)
            self.create_status.config(text="Error saving playlist.")
    def load_playlist(self):
        try:
            with open("playlist.csv", "r") as f:
                lines = f.readlines()
                self.playlist = [line.strip().zfill(2) for line in lines if self.lib.get_name(line.strip().zfill(2))]
            self.refresh_listbox()
            self.create_status.config(text="Playlist loaded.")
        except FileNotFoundError:
            self.create_status.config(text="playlist.csv not found.")
        except Exception as e:
            print("Load error:", e)
            self.create_status.config(text="Error loading playlist.")
    def refresh(self):
        self.refresh_listbox()