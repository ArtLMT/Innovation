import tkinter as tk
from PIL import Image, ImageTk
import webbrowser
from tkinter import messagebox
from model.library import Library
from utils.utils import Utils

class LibraryUI(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Initialize Library
        self.library = Library()
        self.listOfTrack = self.library.get_tracks()
        self.current_track = self.listOfTrack[0] if self.listOfTrack else None  # Default to first track or None
        self.track_info_frame = None  # Frame to display selected track's info

        self.create_ui()

        if self.current_track:  # Only call if there's a valid track
            self.on_track_click(self.current_track)
        else:
            self.display_no_results_message()

    def create_ui(self):
        width = self.winfo_screenwidth()
        self.configure(bg="light sky blue")

        # Search bar
        search_bar = tk.Entry(self, font=("Arial", 24))
        search_bar.place(x=((width / 2) - 300), y=20, width=600, height=32)
        search_bar.bind("<Return>", self.search_tracks)  # Bind Enter key to search function

        # Scrollable area for tracks
        self.list_track_area = tk.Canvas(self, bg="gray")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.list_track_area.yview)
        self.track_frame = tk.Frame(self.list_track_area, bg="lightgray")

        # Configure `list_track_area` and link it to `scrollbar`
        self.list_track_area.create_window((0, 0), window=self.track_frame, anchor="nw")
        self.list_track_area.configure(yscrollcommand=scrollbar.set)

        # Update scrollregion dynamically when the content changes
        self.track_frame.bind("<Configure>", lambda e: self.list_track_area.configure(scrollregion=self.list_track_area.bbox("all")))

        self.list_track_area.place(x=40, y=80, width=1020, height=700)
        scrollbar.place(x=1050, y=80, height=700)

        # Frame to display track information
        self.track_info_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        self.track_info_frame.place(x=1090, y=80, width=400, height=450)

        # Play button below the track_info_frame
        play_button = tk.Button(self, text="Play", font=("Arial", 18) ,bg="white", fg="black", command=self.play_track)
        play_button.place(x=1090, y=550, width=400, height=50)
        
        # Play button below the track_info_frame
        create_track_btn = tk.Button(self, text="Add track", font=("Arial", 18), bg="green", fg="white", command= self.add_track_clicked)
        create_track_btn.place(x=1090, y=625, width=400, height=50)
        
        remove_track_btn = tk.Button(self, text="Remove track", font=("Arial", 18), bg="red", fg="white", command= self.remove_track_clicked)
        remove_track_btn.place(x=1090, y=700, width=400, height=50)

        # Display all tracks in the library
        self.display_tracks(self.library.get_tracks())
        
    def on_track_click(self, track):      
        if track is None:  # Guard clause for None track
            self.display_no_results_message()
            return
        self.current_track = track
        
        self.reload_current_track_selected()

    def display_tracks(self,tracks):
        # Clear previous content
        Utils.clear_frame(self.track_frame)
        if self.listOfTrack is None:
            self.display_no_results_message()
            return
        
        for index, track in enumerate(tracks):
            # Create a frame for each track
            frame = tk.Frame(self.track_frame, bg="white", bd=1, relief="solid" )
            frame.pack(pady=5, fill="x")

            img = Image.open(track.getImgPath()).resize((100, 100))
            track_img = ImageTk.PhotoImage(img)
            img_label = tk.Label(frame, image=track_img, bg="white")
            img_label.image = track_img  # Prevent garbage collection
            img_label.grid(row=0, column=0, padx=10, pady=10)

            # Create the track name label
            name_label = tk.Label(frame, text=track.get_name().strip(), font=("Arial", 18), bg="white", anchor="w")
            name_label.grid(row=0, column=1, padx=10, sticky="w")
            
            # Ensure the name_label has a fixed pixel width
            frame.grid_columnconfigure(1, weight=1)  # Let column 1 (name label) expand
            name_label.configure(width=int(61))  # Approx. 15 pixels per character

            # Bind click events to frame and its children
            frame.bind("<Button-1>", lambda e, t=track: self.on_track_click(t))
            name_label.bind("<Button-1>", lambda e, t=track: self.on_track_click(t))
            img_label.bind("<Button-1>", lambda e, t=track: self.on_track_click(t))
            
            frame.bind("<Double-Button-1>", lambda e, t=track: self.play_track())
            name_label.bind("<Double-Button-1>", lambda e, t=track: self.play_track())
            img_label.bind("<Double-Button-1>", lambda e, t=track: self.play_track())

    def play_track(self):
        if not self.current_track:
            messagebox.showinfo("Info", "No track selected to play.")
            return
        webbrowser.open(self.current_track.youtube_link)

    def search_tracks(self, event):
        search_query = event.widget.get().strip()
        if search_query:
            filtered_tracks = Utils.search_tracks(search_query)
            if filtered_tracks:
                self.display_tracks(filtered_tracks)  # Display matching tracks
            else:
                self.display_no_results_message()  # Display "No Results Found" message
        else:
            # If the query is empty, show all tracks
            self.display_tracks(self.library.get_tracks())

    def display_no_results_message(self):
        # Clear previous content
        Utils.clear_frame(self.track_frame)

        # Create a "No Tracks Found" label
        no_results_label = tk.Label(
            self.track_frame, 
            text="No Tracks Found", 
            font=("Arial", 18), 
            bg="lightgray", 
            fg="red", 
            wraplength=800, 
            justify="center"
        )
        no_results_label.pack(pady=50)

        # Clear the track info frame
        Utils.clear_frame(self.track_info_frame)

    def reload_current_track_selected(self):
        # Update the track_info_frame to display the selected track's details
        Utils.clear_frame(self.track_info_frame)
        track = self.current_track

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

    def remove_track_clicked(self):
        if not self.listOfTrack:
            messagebox.showinfo("Info", "No tracks available to remove.")
            return

        if not self.current_track:
            messagebox.showinfo("Info", "No track selected to remove.")
            return

        # Find the track in the list by name
        track_to_remove = next((track for track in self.listOfTrack if track.get_name() == self.current_track.get_name()), None)

        if track_to_remove:
            self.listOfTrack.remove(track_to_remove)
            Utils.save_tracks_to_csv(self.listOfTrack)
            self.display_tracks(self.listOfTrack)

            # Update selection or clear if no tracks remain
            self.current_track = self.listOfTrack[0] if self.listOfTrack else None
            self.reload_current_track_selected()
        else:
            messagebox.showinfo("Info", "Selected track not found in the list.")


    def add_track_clicked(self):
        self.controller.show_frame("TrackCreator")
        
    def reload_library_view(self):
        self.listOfTrack = Utils.load_tracks_from_csv()

        if not self.listOfTrack:
            self.display_no_results_message()
            self.current_track = None
        else:
            self.display_tracks(self.listOfTrack)
            self.current_track = self.listOfTrack[0]  # Default to the first track
