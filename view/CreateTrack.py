import tkinter as tk 
from tkinter import messagebox
from model.library import Library
from utils.utils import Utils

class TrackCreator(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        
        self.controller = controller
        self.library = Library()
        self.create_ui()

    def create_ui(self):
        self.config(bg = "light sky blue")
        
        input_name_lbl = tk.Label(self,bg = "light sky blue", text="Track's name",font=("Arial", 28))
        input_name_lbl.place(x = 200 , y = 200)
        
        self.input_name_bar = tk.Entry(self,font=("Arial", 28), width=40)
        self.input_name_bar.place(x = 450, y = 200)
        
        input_artist_lbl = tk.Label(self,bg = "light sky blue", text="Track's artist",font=("Arial", 28))
        input_artist_lbl.place(x=200, y = 300)
        
        self.input_artist_bar = tk.Entry(self,font=("Arial", 28), width=40)
        self.input_artist_bar.place(x = 450, y = 300)
        
        input_rating_lbl = tk.Label(self,bg = "light sky blue",font=("Arial", 28),text="Track's rating")
        input_rating_lbl.place(x = 200, y = 400)
        
        self.input_rating_bar = tk.Entry(self,font=("Arial", 28), width=40)
        self.input_rating_bar.place(x = 450, y = 400)
        
        input_youtube_lbl = tk.Label(self,bg = "light sky blue",font=("Arial", 28),text="Youtube link")
        input_youtube_lbl.place(x=200, y = 500)
        
        self.input_youtube_bar = tk.Entry(self,font=("Arial", 28), width=40)
        self.input_youtube_bar.place(x = 450 , y = 500)
        
        width = self.winfo_screenwidth()
        
        self.create_btn = tk.Button(self,text="Create",font=("Arial", 28),command= self.create_track)
        self.create_btn.place(x= (width / 2 - 200), y = 600, height= 50, width= 400)
        
    def create_track(self):
        # Get user input
        name = self.input_name_bar.get().strip()
        artist = self.input_artist_bar.get().strip()
        rating = self.input_rating_bar.get().strip()
        youtube_link = self.input_youtube_bar.get().strip()

        # Validate input
        if not name or not artist or not rating or not youtube_link:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            rating = int(rating)
            if rating < 0 or rating > 5:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Rating must be a number between 0 and 5.")
            return

        # Validate YouTube link
        if not Utils.is_youtube_link_valid(youtube_link):
            messagebox.showerror("Error", "Invalid YouTube link!")
            return

        # Create the track using the Library class
        success = self.library.create_track(name, artist, rating, youtube_link)

        if success:
            messagebox.showinfo("Success", f"Track '{name}' by '{artist}' created successfully!")
            self.clear_inputs()
            self.reload_libraryUI()
        else:
            messagebox.showerror("Error", f"Track '{name}' already exists!")

    def clear_inputs(self):
        self.input_name_bar.delete(0, tk.END)
        self.input_artist_bar.delete(0, tk.END)
        self.input_rating_bar.delete(0, tk.END)
        self.input_youtube_bar.delete(0, tk.END)
        
    def reload_libraryUI(self):
        self.controller.get_frame("LibraryUI").reload_library_view()