from model.playlist import Playlist
from utils.utils import Utils
from model.library import Library

class PlaylistManagement:
    def __init__(self, library):
        self.library = Library() # Reference to the Library for managing tracks
        self.tracks = []
        self.get_tracks()
        self.playlists = Utils.load_playlists_from_csv()  # Load existing playlists from CSV

    def get_playlists(self):
        return self.playlists

    def get_tracks(self):
        self.tracks = self.library.get_tracks()
        return self.tracks

    def create_playlist(self, name, track_list):
        self.playlists = Utils.load_playlists_from_csv()
        
        # Prevent duplicate playlist names
        if any(playlist.get_name() == name for playlist in self.playlists):
            return False

        # Create the new playlist
        new_playlist = Playlist(name)
        for track in track_list:
            new_playlist.add_track(track)

        # Append to current memory state
        self.playlists.append(new_playlist)

        # Save the updated list to the CSV
        Utils.save_playlists_to_csv(self.playlists)
        return True


    def delete_playlist(self, name):
        # Remove playlist from memory
        self.playlists = [p for p in self.playlists if p.get_name() != name]

        # Save updated playlists to CSV
        Utils.save_playlists_to_csv(self.playlists)
        return True

    def add_track_to_playlist(self, playlist_name, track_name):
        playlist = self.get_playlist_by_name(playlist_name)
        if not playlist:
            return False

        track = self.library.get_track_by_name(track_name)
        if not track:
            return False

        playlist.add_track(track)
        self.save_playlists()
        return True

    def remove_track_from_playlist(self, playlist_name, track_name):
        playlist = self.get_playlist_by_name(playlist_name)
        if not playlist:
            return False

        # Find the track directly within the playlist
        track_to_remove = None
        for track in playlist.get_tracks_in_playlist():
            if track.get_name() == track_name:
                track_to_remove = track
                break

        if not track_to_remove:
            return False

        playlist.remove_track(track_to_remove)
        self.save_playlists()
        return True

    def save_playlists(self):
        Utils.save_playlists_to_csv(self.playlists)

    def get_playlist_by_name(self, name):
        self.playlists = Utils.load_playlists_from_csv()
        for playlist in self.playlists:
            if playlist.get_name() == name:
                return playlist
        return None
