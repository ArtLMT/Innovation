from utils.utils import Utils
from model.track import Track

class Library:
    def __init__(self):
        self.tracks = Utils.load_tracks_from_csv()

    def get_tracks(self):
        self.tracks = Utils.load_tracks_from_csv()
        return self.tracks

    def get_track_by_index(self, index):
        if 0 <= index < len(self.tracks):
            return self.tracks[index]
        return None
    
    def get_track_by_name(self, name):
        for track in self.tracks:
            if track.getName() == name:
                return track
        return None

    def create_track(self, name, artist, rating, youtube_link):
        image_src = "Image/logo.png"
        
        if any(track.get_name() == name for track in self.tracks):
            print(f"Track '{name}' already exists.")
            return False
        # Create a new Track object
        new_track = Track(name=name, image=image_src, artist=artist, rating=rating, youtube_link=youtube_link)
        
        self.tracks = Utils.load_tracks_from_csv()
        
        self.tracks.append(new_track)
        
        Utils.save_tracks_to_csv(self.tracks)
        return True