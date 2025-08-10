#single_gui.py
import tkinter as tk
from tkinter import ttk
from font_manager import FontManager
from view_tracks_tab import ViewTracksTab
from create_track_list_tab import CreateTrackListTab
from update_tracks_tab import UpdateTracksTab
from track_library import TrackLibrary

lib = TrackLibrary()

class JukeBoxApp(tk.Tk):
    def __init__(self):
        super().__init__()
        FontManager().configure()
        self.title("JukeBox App")
        self.state('zoomed')
        self.resizable(True, True)

        # Notebook for tabs
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")
        notebook.bind("<<NotebookTabChanged>>",self.on_tab_change)

        # View Tracks Tab
        self.view_tab = ViewTracksTab(notebook, lib)
        notebook.add(self.view_tab, text="👀 View Tracks")

        # Create Playlist Tab
        self.create_tab = CreateTrackListTab(notebook, lib)
        notebook.add(self.create_tab, text="🎵 Create Playlist")

        # Update Tracks Tab
        self.update_tab = UpdateTracksTab(notebook, lib)
        notebook.add(self.update_tab, text="✏️ Update Tracks")

    def on_tab_change(self, event):
        selected_tab = event.widget.select()
        selected_frame = event.widget.nametowidget(selected_tab)
        if hasattr(selected_frame, "refresh"):
            selected_frame.refresh()


if __name__ == "__main__":
    app = JukeBoxApp()
    app.mainloop()