import tkinter as tk
from PIL import Image, ImageTk
from view.PlaylistViewer import PlaylistUI
from view.LibraryViewer import LibraryUI
from view.CreatePlayList import PlaylistCreator
from view.CreateTrack import TrackCreator

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.gui()

    def gui(self):
        self.configure(bg="light sky blue")
        # Create a logo which can be used as a return home button
        self.logo_icon = tk.Label(text="Jukebox", font=("Helvetica", 48, "bold italic"), bg="light sky blue", fg="Black")
        self.logo_icon.place(x=40,y=0)
        self.logo_icon.bind("<Button-1>", lambda e: self.controller.show_frame("MainMenu"))
        
        # Button to navigate to Library interface
        self.library_btn = tk.Button(self,text="Library", font=("Helvetica", 24, "bold italic"), command = lambda : self.controller.show_frame("LibraryUI"))
        self.library_btn.place(x=300, y =137 + 69, height= 60, width= 400)
        
        # Button to navigate to Playlist interface
        self.playlist_btn = tk.Button(self, text="Playlist",font=("Helvetica", 24, "bold italic"),command = lambda : self.controller.show_frame("PlaylistUI"))
        self.playlist_btn.place(x=300, y = 137+137+69, height= 60, width= 400)
        #self.playlist_btn.bind("<Button-1>", lambda e: self.controller.show_frame("PlaylistUI"))
        
        self.create_playlist_btn = tk.Button(self, text="Add Playlist!",font=("Helvetica", 24, "bold italic"),command=lambda: self.controller.show_frame("PlaylistCreator"))
        self.create_playlist_btn.place(x=300, y = 136 * 3 + 69, height= 60, width= 400)
        
        self.add_track_btn = tk.Button(self, text = "Add more track!",font=("Helvetica", 24, "bold italic"),command=lambda: self.controller.show_frame("TrackCreator"))
        self.add_track_btn.place(x = 300, y = 137 * 4 + 69, height= 60, width= 400)
        
        img = Image.open("Image/logo.png").resize((550, 550))  # Resize image
        self.logo_image = ImageTk.PhotoImage(img)  # Convert to PhotoImage
        logo_label = tk.Label(self, image=self.logo_image, bg="light sky blue")
        logo_label.place(x=800, y=157)  # Position the logo on the right
