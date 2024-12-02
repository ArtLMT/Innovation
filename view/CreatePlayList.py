import tkinter as tk
from model.library import Library
from model.playlistManager import PlaylistManagement
from utils.utils import Utils
from PIL import Image, ImageTk

class PlaylistCreator(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller


        self.current_track = None
        self.library = Library()  # Access library for tracks
        self.playlist_manager = PlaylistManagement(self.library)  # Use PlaylistManager methods
        self.selected_tracks = []  # Store tracks selected for the playlist
        
        self.create_ui()

    def create_ui(self):
        width = self.winfo_screenwidth()
        self.configure(bg="light sky blue")

        # Input box for playlist name
        self.playlist_name_entry = tk.Entry(self, font=("Arial", 16))
        self.playlist_name_entry.place(x=250, y=100, width=300, height=30)

        # Label for playlist name
        playlist_name_lbl = tk.Label(self, text="Playlist Name:", font=("Arial", 16), bg="light sky blue")
        playlist_name_lbl.place(x=100, y=100)

        self.create_playlist_btn = tk.Button(self,text="Create Playlist",font=("Arial", 16), command=self.create_playlist)
        self.create_playlist_btn.place(x = 200 + 850 - 200 ,y = 575, width = 500, height = 50)

        self.to_playlist_display_btn = tk.Button(self, text = "View playlists", font=("Arial", 16), command= self.to_playlist_clicked)
        self.to_playlist_display_btn.place(x = 200 + 850 - 200 ,y = 650, width = 500, height = 50)

        self.display_available_track()
        self.display_selected_track()
        # Display tracks from the library
        self.display_tracks(self.library.get_tracks())

    def display_available_track(self):
        
        # Scrollable Track Selection Area
        self.track_area = tk.Canvas(self, bg="gray", borderwidth=1, relief="solid")  # Canvas with border
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.track_area.yview, borderwidth=1, relief="solid")  # Scrollbar with border
        
        # Frame to hold track content (inside the canvas)
        self.track_frame = tk.Frame(self.track_area, bg="lightgray")

        # Add `track_frame` to the canvas
        self.track_area.create_window((0, 0), window=self.track_frame, anchor="nw")
        self.track_area.configure(yscrollcommand=scrollbar.set)

        # Place the canvas and scrollbar
        self.track_area.place(x=100, y=150, width=700, height=600)
        scrollbar.place(x=800, y=150, height=600)

        # Dynamically update the scrollregion
        self.track_frame.bind("<Configure>", lambda e: self.track_area.configure(scrollregion=self.track_area.bbox("all")))

    def display_selected_track(self):
        # Scrollable Track Selection Area
        self.selected_track_area = tk.Canvas(self, bg="gray", borderwidth=1, relief="solid")  # Canvas with border
        selected_track_scrollbar = tk.Scrollbar(self, orient="vertical", command=self.selected_track_area.yview, borderwidth=1, relief="solid")  # Scrollbar with border
        
        # Frame to hold track content (inside the canvas)
        self.selected_track_frame = tk.Frame(self.selected_track_area, bg="lightgray")

        # Add `track_frame` to the canvas
        self.selected_track_area.create_window((0, 0), window=self.selected_track_frame, anchor="nw")
        self.selected_track_area.configure(yscrollcommand=selected_track_scrollbar.set)

        # Place the canvas and scrollbar
        self.selected_track_area.place(x=850, y=150, width=500, height=400)
        selected_track_scrollbar.place(x=(500+850), y=150, height=400)

        # Dynamically update the scrollregion
        self.selected_track_frame.bind("<Configure>", lambda e: self.selected_track_area.configure(scrollregion=self.selected_track_area.bbox("all")))
        
        self.update_selected_area()

    def display_tracks(self, tracks):
        # Reload the library's tracks from the CSV
        self.library.tracks = Utils.load_tracks_from_csv()
        tracks = tracks or self.library.get_tracks()  # Default to library's tracks if none provided
        
        # Clear previous content
        Utils.clear_frame(self.track_frame)

        # Add tracks to the track frame
        for track in tracks:
            # Create a frame for each track
            frame = tk.Frame(self.track_frame, bg="white", bd=1, relief="solid")
            frame.pack(pady=5, fill="x")

            # Load track image
            img = Image.open(track.getImgPath()).resize((100, 100))
            track_img = ImageTk.PhotoImage(img)
            img_label = tk.Label(frame, image=track_img, bg="white")
            img_label.image = track_img  # Prevent garbage collection
            img_label.grid(row=0, column=0, padx=10, pady=10)

            # Track name label
            name_label = tk.Label(frame, text=track.get_name().strip(), font=("Arial", 18), bg="white", anchor="w")
            name_label.grid(row=0, column=1, padx=10, sticky="w")

            # Configure column width
            frame.grid_columnconfigure(1, weight=1)
            name_label.configure(width=int(39))

            # Bind click event to the frame to add into selected track
            frame.bind("<Button-1>", lambda e, t=track: self.add_track_to_preview(t))
            name_label.bind("<Button-1>", lambda e, t=track: self.add_track_to_preview(t))
            img_label.bind("<Button-1>", lambda e, t=track: self.add_track_to_preview(t))

    def add_track_to_preview(self, track):
        if track not in self.selected_tracks:
            self.selected_tracks.append(track)
            self.update_selected_area()  # Refresh the selected track area
        else:
            tk.messagebox.showinfo("Info", f"Track '{track.get_name()}' is already selected.")

    def on_track_click(self,track):
        self.current_track = track

    def update_selected_area(self):
        # Clear previous content in selected track area
        Utils.clear_frame(self.selected_track_frame)

        # Add selected tracks to the selected_track_frame
        if not self.selected_tracks:
            # Display placeholder message when no tracks are selected
            message = tk.Label(self.selected_track_frame, text="No tracks selected", 
                                font=("Arial", 16), bg="lightgray", fg="black")
            message.pack(pady=20)
            message.configure(width=int(41))
        else:
            # Add selected tracks to the selected_track_frame
            for track in self.selected_tracks:
                # Create a frame for each selected track
                frame = tk.Frame(self.selected_track_frame, bg="white", bd=1, relief="solid")
                frame.pack(pady=5, fill="x")

                # Load track image
                img = Image.open(track.getImgPath()).resize((100, 100))
                track_img = ImageTk.PhotoImage(img)
                img_label = tk.Label(frame, image=track_img, bg="white")
                img_label.image = track_img  # Prevent garbage collection
                img_label.grid(row=0, column=0, padx=10, pady=10)

                # Track name label
                name_label = tk.Label(frame, text=track.get_name().strip(), font=("Arial", 18), bg="white", anchor="w")
                name_label.grid(row=0, column=1, padx=10, sticky="w")

                # Configure column width
                frame.grid_columnconfigure(1, weight=1)
                name_label.configure(width=int(39))
                
                # Bind double click event to remove track from selected tracks
                frame.bind("<Double-1>", lambda e, t=track: self.remove_track_from_selected(t))
                name_label.bind("<Double-1>", lambda e, t=track: self.remove_track_from_selected(t))
                img_label.bind("<Double-1>", lambda e, t=track: self.remove_track_from_selected(t))

    def create_playlist(self):
        playlist_name = self.playlist_name_entry.get().strip()
        # self.cur
        if not playlist_name:
            tk.messagebox.showerror("Error", "Playlist name cannot be empty!")
            return

        if not self.selected_tracks:
            tk.messagebox.showerror("Error", "No tracks selected!")
            return

        if self.playlist_manager.create_playlist(playlist_name, self.selected_tracks):
            tk.messagebox.showinfo("Success", f"Playlist '{playlist_name}' created successfully!")
            Utils.save_playlists_to_csv(self.playlist_manager.get_playlists())
            self.controller.get_frame("PlaylistUI").reload_playlist_view()
        else:
            tk.messagebox.showinfo("Failed", f"Playlist '{playlist_name}' already exits!")
        
        self.selected_tracks = []
        self.playlist_name_entry.delete(0, tk.END)
        self.update_selected_area()

    def remove_track_from_selected(self, track):
        #track in self.selected_tracks:
        self.selected_tracks.remove(track)
        self.update_selected_area()

    def to_playlist_clicked(self):
        self.controller.show_frame("PlaylistUI")
        
    def reload_library(self):
        self.library.tracks = Utils.load_tracks_from_csv()
        self.display_tracks(self.library.get_tracks())
