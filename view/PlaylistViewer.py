import tkinter as tk
import time
import webbrowser
from tkinter import messagebox
from PIL import Image, ImageTk
from model.library import Library
from utils.utils import Utils
from model.playlistManager import PlaylistManagement
from functools import partial

class PlaylistUI(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.library = Library()
        self.playlist_controller = PlaylistManagement(self.library)
        self.playlists = Utils.load_playlists_from_csv()  # List of playlists
        
        self.current_track = None  # Currently selected track, initialize to None
        self.current_playlist = None
        self.track_info_frame = None
        
        self.create_ui()

        if not self.playlists:
            self.display_no_playlists_message()
        else:
            self.display_playlist(self.playlists)
            self.current_playlist = self.playlists[0]
            
    def create_ui(self):
        self.configure(bg="light sky blue")
        self.playlist_area = tk.Canvas(self, bg="gray", borderwidth=1, relief="solid")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.playlist_area.yview)
        self.track_frame = tk.Frame(self.playlist_area, bg="lightgray",bd=1, relief="solid")

        # Configure `playlist_area` and link it to `scrollbar`
        self.playlist_area.create_window((0, 0), window=self.track_frame, anchor="nw")
        self.playlist_area.configure(yscrollcommand=scrollbar.set)

        # Update scrollregion dynamically when the content changes
        self.track_frame.bind("<Configure>", lambda e: self.playlist_area.configure(scrollregion=self.playlist_area.bbox("all")))

        # Place `playlist_area` and `scrollbar`
        self.playlist_area.place(x=40, y=80, width=1020, height=600)
        scrollbar.place(x=1050, y=80, height=600)

        # Display all playlists in the library
        self.display_playlist(self.playlists)
        # Frame to display track information
        self.track_info_frame = tk.Frame(self, bg="white",bd=1, relief="solid")
        self.track_info_frame.place(x=1090, y=80, width=400, height=450)

        # Play button below the track_info_frame
        play_button = tk.Button(self, text="Play", font=("Arial", 18), bg="white", fg="black", command= self.play_all_tracks)
        play_button.place(x=1090, y=550, width=400, height=50)
        
        remove_track_button = tk.Button(self, text="Remove", font=("Arial", 18), bg="red", fg="black", command= self.on_remove_track_click)
        remove_track_button.place(x=1090, y=625, width=400, height=50)
        
        # Create playlist button
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        create_playlist_btn = tk.Button(self,text="Create Playlist",font=("Arial", 18), command=lambda: self.controller.show_frame("PlaylistCreator"))
        create_playlist_btn.place(x=(width/2)-200,y=700, width=400,height=50)


    def display_tracks_in_playlist(self, playlist):
        # Clear previous content in track_info_frame
        Utils.clear_frame(self.track_info_frame)
        self.playlists = Utils.load_playlists_from_csv()


        # Create a scrollable area for tracks
        canvas = tk.Canvas(self.track_info_frame, bg="white")
        scrollbar = tk.Scrollbar(self.track_info_frame, orient="vertical", command=canvas.yview)
        track_list_frame = tk.Frame(canvas, bg="white")

        # Configure the canvas and scrollbar
        canvas.create_window((0, 0), window=track_list_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Update scrollregion dynamically
        track_list_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        frame = tk.Frame(track_list_frame, bg="white")
        frame.pack(pady=10, fill="x", padx=2)
        frame.grid_columnconfigure(1, weight=0)
        
        playlist_name = playlist.get_name().strip()
        playlist_name_lbl = tk.Label(frame, text=playlist_name,font=("Arial", 18, "bold"),bg="white",anchor="center")
        
        playlist_name_lbl.pack(side="left", padx=(10,0))
        
        # Display tracks in the selected playlist
        for track in playlist.get_tracks_in_playlist():

            # Create a frame for each track
            frame = tk.Frame(track_list_frame, bg="white")
            frame.pack(pady=5, fill="x", padx=2)

            # Display track image
            img = Image.open(track.getImgPath()).resize((75, 75))
            track_img = ImageTk.PhotoImage(img)
            img_label = tk.Label(frame, image=track_img, bg="white")
            img_label.image = track_img  # Prevent garbage collection
            img_label.pack(side="left", padx=10)

            # Display track details
            name_label = tk.Label(frame, text=track.get_name(), font=("Arial", 18), bg="white", anchor="w")
            name_label.pack(side="left", fill="x", expand=True)
            
            frame.grid_columnconfigure(1, weight=1)  # Let column 1 (name label) expand
            name_label.configure(width=int(27))

            # Add a click event for each track
            frame.bind("<Button-1>", lambda e, t=track: self.select_track(t))
            name_label.bind("<Button-1>", lambda e, t=track: self.select_track(t))
            img_label.bind("<Button-1>", lambda e, t=track: self.select_track(t))

        def on_playlist_click(self, playlist):
            self.current_playlist = playlist
            self.reload_playlist_and_tracks_display()

    def display_playlist(self, items):
        # Clear previous content in track_frame
        Utils.clear_frame(self.track_frame)
        
        self.playlists = Utils.load_playlists_from_csv()
        
        for item in items:  # Ensure `items` is a list
            # Create a frame for each playlist
            frame = tk.Frame(self.track_frame, bg="white", bd=1, relief="solid")
            frame.pack(pady=5, fill="x")

            # Check if item is a playlist
            img_path = "Image/ping_music_icon.jpg"  # Default playlist image
            name = item.get_name()  # Assuming playlists have a `name` attribute

            # Load and display the image
            img = Image.open(img_path).resize((100, 100))
            item_img = ImageTk.PhotoImage(img)
            img_label = tk.Label(frame, image=item_img, bg="white")
            img_label.image = item_img  # Prevent garbage collection
            img_label.grid(row=0, column=0, padx=10, pady=10)

            # Display the playlist name
            name_label = tk.Label(frame, text=name.strip(), font=("Arial", 18), bg="white", anchor="w")
            name_label.grid(row=0, column=1, padx=10, sticky="w")

            frame.grid_columnconfigure(1, weight=1)
            name_label.configure(width=int(61))  

            def on_click_with_parameter(playlist):
                self.current_playlist = playlist
                self.current_track = None
                self.reload_playlist_and_tracks_display()
                
            # Bind click events -> Showing tracks inside the playlist when clicked
            frame.bind("<Button-1>", lambda e, p=item: on_click_with_parameter(p))
            name_label.bind("<Button-1>", lambda e, p=item: on_click_with_parameter(p))
            img_label.bind("<Button-1>", lambda e, p=item: on_click_with_parameter(p))
            

    def on_item_click(self, track):
        self.current_track = None  # Reset current track
        # Clear previous content
        Utils.clear_frame(self.track_info_frame)

        if hasattr(track, 'image'):  # It's a track
            self.current_track = track  # Set the current track

            # Display track details
            img = Image.open(track.getImgPath()).resize((200, 200))
            track_img = ImageTk.PhotoImage(img)
            img_label = tk.Label(self.track_info_frame, image=track_img, bg="white")
            img_label.image = track_img  # Prevent garbage collection
            img_label.pack(pady=10)

            name_label = tk.Label(self.track_info_frame, text=f"Name: {track.get_name()}", font=("Arial", 18), bg="white")
            name_label.pack(pady=10)

            artist_label = tk.Label(self.track_info_frame, text=f"Artist: {track.get_artist()}", font=("Arial", 14), bg="white")
            artist_label.pack(pady=10)

            rating_label = tk.Label(self.track_info_frame, text=f"Rating: {track.get_rating()}", font=("Arial", 14), bg="white")
            rating_label.pack(pady=10)

        else:  # It's a playlist
            img = Image.open("Image/ping_music_icon.jpg").resize((200, 200))
            playlist_img = ImageTk.PhotoImage(img)
            img_label = tk.Label(self.track_info_frame, image=playlist_img, bg="white")
            img_label.image = playlist_img
            img_label.pack(pady=10)

            name_label = tk.Label(self.track_info_frame, text=f"Playlist: {item.get_name()}", font=("Arial", 18), bg="white")
            name_label.pack(pady=10)

    def on_remove_track_click(self):
        if not self.current_playlist:
            messagebox.showwarning("Warning", "No playlist selected to remove.")
            return

        if self.current_track:  # Remove a track from the playlist
            success = self.playlist_controller.remove_track_from_playlist(
                self.current_playlist.get_name(), self.current_track.get_name()
            )
            if success:
                messagebox.showinfo(
                    "Success", f"Track '{self.current_track.get_name()}' removed from playlist."
                )
                self.current_track = None  # Reset current track selection
                self.reload_playlist_and_tracks_display()
            else:
                messagebox.showerror("Error", "Failed to remove track.")
        else:  # Remove the entire playlist
            current_playlist_name = self.current_playlist.get_name()
            self.playlist_controller.delete_playlist(current_playlist_name)
            messagebox.showinfo("Success", f"Playlist '{current_playlist_name}' has been deleted.")
            self.current_playlist = None  # Reset current playlist selection
            self.reload_playlist_view()

    def reload_playlist_and_tracks_display(self):
        # Set the updated playlists
        self.playlists = Utils.load_playlists_from_csv()

        if not self.playlists:  # No playlists available
            self.display_no_playlists_message()
            self.current_playlist = None
            return

        old_playlist_name = self.current_playlist.get_name() if self.current_playlist else None
        new_playlist = self.playlist_controller.get_playlist_by_name(old_playlist_name)

        if new_playlist:
            self.current_playlist = new_playlist
            self.display_tracks_in_playlist(new_playlist)
        else:
            # Default to the first playlist, or clear selection if none exist
            self.current_playlist = self.playlists[0] if self.playlists else None
            if self.current_playlist:
                self.display_tracks_in_playlist(self.current_playlist)
            else:
                self.display_no_playlists_message()

    def reload_playlist_view(self):
        self.playlists = Utils.load_playlists_from_csv()

        if not self.playlists:  # If no playlists exist
            self.display_no_playlists_message()
            self.current_playlist = None
        else:
            self.display_playlist(self.playlists)
            # Automatically select the first playlist
            self.current_playlist = self.playlists[0]
            self.display_tracks_in_playlist(self.current_playlist)
        
    def clear_track_frame(self,track_frame):
        Utils.clear_frame(track_frame)

    def select_track(self, track):
        self.current_track = track
        self.on_item_click(track)

    def play_all_tracks(self):
        if not self.current_playlist:
            messagebox.showinfo("Info", "No playlist selected.")
            return

        tracks = self.current_playlist.get_tracks_in_playlist()

        if not tracks:
            messagebox.showinfo("Info", "No tracks available in the playlist.")
            return

        for track in tracks:
            if track.youtube_link:
                webbrowser.open(track.youtube_link)
                time.sleep(15)  # Wait 15 seconds before playing the next track
            else:
                print(f"Track '{track.get_name()}' has no YouTube link.")

    def display_no_playlists_message(self):
        # Clear previous content
        Utils.clear_frame(self.track_frame)

        # Add "No Playlists Found" message
        no_playlists_label = tk.Label(
            self.track_frame, 
            text="No Playlists Found", 
            font=("Arial", 18), 
            bg="lightgray", 
            fg="red", 
            wraplength=1020, 
            justify="center"
        )
        no_playlists_label.pack(pady=50)
        no_playlists_label.configure(width=int(71))