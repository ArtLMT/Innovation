import tkinter as tk
from view.main_menu import MainMenu
from view.LibraryViewer import LibraryUI
from view.PlaylistViewer import PlaylistUI
from view.CreatePlayList import PlaylistCreator
from view.CreateTrack import TrackCreator
# from view.main_menu import Test

class JukeBoxApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.gui()

    def gui(self):
        # Set height and width
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry(f"{width}x{height}")
        self.title("JukeBox")
        self.configure(bg="light sky blue")
        
        # Create container for frames
        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for Page in (MainMenu,LibraryUI,PlaylistUI,PlaylistCreator,TrackCreator):
            page_name = Page.__name__
            frame = Page(parent=container, controller = self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)
            
        #self.show_frame("PlaylistUI")
        #self.show_frame("LibraryUI")
        self.show_frame("MainMenu")

        
    def show_frame(self,page_name):
        frame = self.frames[page_name]

        if page_name == "PlaylistUI":
            frame.reload_playlist_view()
            
        if page_name == "PlaylistCreator":
            frame.reload_library()

        frame.tkraise()
        
    def get_frame(self, frame_name):
        return self.frames.get(frame_name)