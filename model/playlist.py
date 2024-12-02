class Playlist:
    def __init__(self, name, tracks=None):
        self.name = name
        self.tracks = tracks or []  # Default to an empty list if no tracks are provided

    def add_track(self, track_name):
            self.tracks.append(track_name)

    def remove_track(self, track_name):
        if track_name in self.tracks:
            self.tracks.remove(track_name)

    def to_dict(self):
        return {"name": self.name, "tracks": ",".join(self.tracks)}
    
    def get_name(self):
        return self.name
    
    def get_tracks_in_playlist(self):
        return self.tracks
    
    def get_playlist(self, name):
        # Find and return the playlist with the given name
        for playlist in self.playlists:
            if playlist.name == name:
                return playlist
        return None  # Return None if not found

