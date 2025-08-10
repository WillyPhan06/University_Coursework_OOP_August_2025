import tkinter as tk                     # Import the base tkinter module for GUI
from tkinter import ttk, Canvas          # Import themed widgets and Canvas from tkinter
from PIL import Image, ImageTk           # Import PIL for image loading and resizing
import os                                # OS module for checking file paths
# Define the ViewTracksTab class which inherits from ttk.Frame
class ViewTracksTab(ttk.Frame):
    def __init__(self, master, lib):
        super().__init__(master)         # Call parent constructor
        self.lib = lib                   # Reference to the track library passed in
        self.last_displayed_keys = []    # Store last viewed track keys for filtering context
        self.build_view_tab()            # Build the GUI layout
        self.view_all()                  # Show all tracks initially

    def build_view_tab(self):
        # Create the top frame for input controls
        self.view_top = tk.Frame(self)
        self.view_top.pack(fill="x", padx=10, pady=5)

        # Track ID input and buttons
        tk.Label(self.view_top, text="Track Number:").pack(side="left")                     # Label for track number
        self.view_entry = tk.Entry(self.view_top, width=5)                                 # Entry field for track number
        self.view_entry.pack(side="left", padx=5)
        tk.Button(self.view_top, text="View", bg="#b3e5fc", command=self.view_clicked).pack(side="left")  # View one
        tk.Button(self.view_top, text="View All", bg="#d0e7ff", command=self.view_all).pack(side="left", padx=5)  # View all

        # Search field and button
        self.search_entry = tk.Entry(self.view_top, width=30)                              # Entry for search query
        self.search_entry.pack(side="left", padx=10)
        tk.Button(self.view_top, text="Search", bg="#d4fcd4", command=self.search_clicked).pack(side="left")  # Trigger search

        # Filter section
        tk.Label(self.view_top, text="Filter by:").pack(side="left", padx=(20, 5))         # Label for filter type
        self.filter_type = ttk.Combobox(self.view_top, width=12, state="readonly")         # Dropdown for filter types
        self.filter_type['values'] = ["Artist", "Rating", "Play Count"]                    # Set filter options
        self.filter_type.pack(side="left", padx=5)
        self.filter_type.bind("<<ComboboxSelected>>", self.update_filter_values)           # When selected, update values

        self.filter_value = ttk.Combobox(self.view_top, width=20, state="readonly")        # Dropdown for filter values
        self.filter_value.pack(side="left", padx=5)
        tk.Button(self.view_top, text="Apply Filter", bg="#fff9c4", command=self.apply_filter).pack(side="left")  # Apply button

        # Create a scrollable canvas area for track display
        self.canvas = Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Resize canvas when internal frame size changes
        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")       # Add scrollable frame to canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)                            # Expand canvas
        self.scrollbar.pack(side="right", fill="y")                                        # Pack scrollbar on right

        # Enable mousewheel scroll when hovering over canvas
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        # Linux-compatible scroll events
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))  # Scroll up
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))   # Scroll down

    def view_all(self):
        self.clear_scrollable_frame()                      # Clear current display
        keys = self.lib.get_keys()                         # Get all track keys
        for key in keys:
            self.display_track(key)                        # Display each track
        self.last_displayed_keys = keys                    # Store displayed keys for filtering

    def view_clicked(self):
        key = self.view_entry.get().strip().zfill(2)       # Get track ID, zero-padded
        if self.lib.get_name(key):                         # Check if track exists
            self.display_tracks_by_keys([key])             # Display single track
        else:
            self.display_tracks_by_keys([])                # Show "not found" message

    def search_clicked(self):
        query = self.search_entry.get().strip().lower()    # Get and lower search input
        result_keys = [
            key for key in self.lib.get_keys()
            if query in self.lib.get_name(key).lower() or query in self.lib.get_artist(key).lower()
        ]                                                  # Filter by name or artist
        self.display_tracks_by_keys(result_keys)           # Display matches

    def apply_filter(self):
        filter_type = self.filter_type.get()               # Get selected filter type
        filter_value = self.filter_value.get().strip()     # Get filter value

        base_keys = self.last_displayed_keys if self.last_displayed_keys else self.lib.get_keys()
        result_keys = []                                   # Track results

        for key in base_keys:  # Loop through each track key from previously displayed or all tracks
            if filter_type == "Artist" and self.lib.get_artist(key).lower() == filter_value.lower():
                # If filtering by Artist and artist name matches (case-insensitive), add to result
                result_keys.append(key)
            elif filter_type == "Rating" and str(self.lib.get_rating(key)) == filter_value:
                # If filtering by Rating and it matches the selected value, add to result
                result_keys.append(key)
            elif filter_type == "Play Count":  # If filtering by Play Count range
                count = self.lib.get_play_count(key)  # Get the track's play count
                if (filter_value == "0-10" and count <= 10 or
                        filter_value == "11-20" and 11 <= count <= 20 or
                        filter_value == "21-50" and 21 <= count <= 50 or
                        filter_value == "51+" and count >= 51):
                    # Check if count falls within selected range, then add to result
                    result_keys.append(key)

        self.display_tracks_by_keys(result_keys)  # Show all tracks that match the filter

    def update_filter_values(self, event=None):
        choice = self.filter_type.get()                    # Get filter type
        if choice == "Artist":
            values = sorted(set(self.lib.get_artist(k) for k in self.lib.get_keys()))  # Unique artist list
        elif choice == "Rating":
            values = [str(i) for i in range(6)]            # Ratings 0–5
        elif choice == "Play Count":
            values = ["0-10", "11-20", "21-50", "51+"]     # Play count ranges
        else:
            values = []
        self.filter_value['values'] = values               # Set filter value options
        self.filter_value.set("")                          # Clear previous selection

    def display_track(self, key):
        name = self.lib.get_name(key)                      # Get track name
        artist = self.lib.get_artist(key)                  # Get track artist
        rating = self.lib.get_rating(key)                  # Get track rating
        stars = '*' * rating                               # Visual stars
        plays = self.lib.get_play_count(key)               # Get track play count

        frame = ttk.Frame(self.scrollable_frame, relief="solid", borderwidth=1)
        # Create a bordered frame to hold the track's details inside the scrollable area

        frame.pack(fill="x", padx=10, pady=5)
        # Add the frame to the scrollable section with horizontal fill and padding

        # Display track info on the left
        info = f"Track {key}: {name}\nArtist: {artist}\nRating: {stars}\nPlays: {plays}"
        # Format a string with track info: ID, name, artist, rating as stars, and play count

        tk.Label(frame, text=info, justify="left").pack(side="left", padx=10)
        # Create and pack a label on the left side of the frame to show the text info

        try:
            img_path = f"track_images/{key}.jpg"  # Construct the path to the image file for this track

            if os.path.exists(img_path):
                img = Image.open(img_path).resize((100, 100))  # Open and resize image to 100x100 pixels
                photo = ImageTk.PhotoImage(img)  # Convert the image for tkinter
                img_label = tk.Label(frame, image=photo)  # Create a label to show the image
                img_label.image = photo  # Keep a reference to avoid garbage collection
                img_label.pack(side="right", padx=10)  # Pack the image to the right side of the frame

            else:
                fallback_img = Image.open("track_images/no_image.jpg").resize((100, 100))
                # If the track image doesn't exist, use a fallback image instead

                fallback_photo = ImageTk.PhotoImage(fallback_img)  # Convert fallback image for tkinter
                fallback_label = tk.Label(frame, image=fallback_photo)  # Create label with fallback image
                fallback_label.image = fallback_photo  # Keep a reference to avoid garbage collection
                fallback_label.pack(side="right", padx=10)  # Pack fallback image to right side

        except Exception as e:
            tk.Label(frame, text="Error loading image").pack(side="right", padx=10)
            # If loading image fails for any reason, show an error label instead

            print(e)  # Print the error to the console for debugging

    def display_tracks_by_keys(self, keys):
        self.clear_scrollable_frame()  # Clear the scrollable frame before displaying new content

        if not keys:
            tk.Label(self.scrollable_frame, text="No tracks found.").pack(pady=10)
            # If the list of keys is empty, show a message saying no results found
            return

        for key in keys:
            self.display_track(key)  # Display each track found in the list of keys

        self.last_displayed_keys = keys  # Save the currently displayed keys for future filter context

    def clear_scrollable_frame(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()  # Remove (destroy) every widget currently inside the scrollable frame

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        # Scroll the canvas vertically when the mouse wheel is used (Windows/macOS behavior)

    def refresh(self):
        self.view_all()  # A refresh method that re-displays all tracks, used externally to refresh the tab

