import pandas as pd
from model.track import Track
from model.playlist import Playlist
import requests

CSV_FILE_PATH = "utils/library.csv" 
PLAYLIST_CSV_FILE = "utils/playlists.csv"

class Utils:
    @staticmethod
    def save_tracks_to_csv(tracks):
        data = {
            "name": [track.name for track in tracks],
            "image": [track.image for track in tracks],
            "artist": [track.artist for track in tracks],
            "rating": [track.rating for track in tracks],
            "youtube_link": [track.youtube_link for track in tracks],
        }
        df = pd.DataFrame(data)
        df.to_csv(CSV_FILE_PATH, index=False)

    @staticmethod
    def load_tracks_from_csv():
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(CSV_FILE_PATH)
            # Convert the DataFrame to a list of Track objects
            tracks = [
                Track(
                    name=row["name"],
                    image=row["image"],
                    artist=row["artist"],
                    rating=row["rating"],
                    youtube_link=row["youtube_link"],
                )
                for _, row in df.iterrows()
            ]
            return tracks 
        except FileNotFoundError:
            return []

    @staticmethod
    def search_tracks(query):
        try:
            df = pd.read_csv(CSV_FILE_PATH)
            # Filter tracks by query in the 'name' or 'artist' columns
            filtered_df = df[
                df["name"].str.contains(query, case=False, na=False) |
                df["artist"].str.contains(query, case=False, na=False)
            ]
            if filtered_df.empty:
                return []  # Return an empty list if no matches are found
            
            # Convert matching rows into Track objects
            tracks = [
                Track(
                    name=row["name"],
                    image=row["image"],
                    artist=row["artist"],
                    rating=row["rating"],
                    youtube_link=row["youtube_link"],
                )
                for _, row in filtered_df.iterrows()
            ]
            return tracks
        except FileNotFoundError:
            print(f"CSV file not found at {CSV_FILE_PATH}. Cannot perform search.")
            return []

    @staticmethod
    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()

    # Play list 
    @staticmethod
    def save_playlists_to_csv(playlists):
        if not playlists:  # If no playlists exist
            # Create an empty DataFrame with the correct headers
            df = pd.DataFrame(columns=["name", "tracks"])
            df.to_csv(PLAYLIST_CSV_FILE, index=False)
        else:
            data = []
            for playlist in playlists:
                # Validate tracks against the current library
                valid_tracks = [track.get_name() for track in playlist.tracks if isinstance(track, Track)]
                data.append({
                    "name": playlist.name,
                    "tracks": "|".join(valid_tracks)
                })

            # Write to CSV
            df = pd.DataFrame(data)
            df.to_csv(PLAYLIST_CSV_FILE, index=False)


    @staticmethod
    def load_playlists_from_csv():
        try:
            # Load the library tracks into a dictionary
            library_tracks = {track.name: track for track in Utils.load_tracks_from_csv()}
            
            # Read playlists CSV
            df = pd.read_csv(PLAYLIST_CSV_FILE)
            playlists = []
            
            for _, row in df.iterrows():
                if pd.notna(row["tracks"]) and isinstance(row["tracks"], str):
                    # Filter out invalid tracks
                    tracks = []
                    for track_name in row["tracks"].split("|"):
                        if track_name in library_tracks:
                            tracks.append(library_tracks[track_name])
                        else:
                            print(f"Warning: Track '{track_name}' not found in library.")
                else:
                    tracks = []

                # Create Playlist object
                playlists.append(Playlist(name=row["name"], tracks=tracks))
            return playlists
        except FileNotFoundError:
            print(f"CSV file not found at {PLAYLIST_CSV_FILE}. Starting with no playlists.")
            return []  # Return an empty list if no file exists
    
    @staticmethod
    def test():
        test_playlist = Utils.load_playlists_from_csv()
        return test_playlist
    

    @staticmethod
    def is_youtube_link_valid(link):
        try:
            response = requests.get(link, timeout=5)  # Set a timeout for responsiveness
            # Check if the response is successful (status code 200)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException:
            # Handle errors (e.g., timeout, connection error)
            return False