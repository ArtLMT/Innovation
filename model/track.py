class Track:
    def __init__(self, name, image, artist, rating, youtube_link):
        self.name = name
        self.image = image
        self.artist = artist
        self.rating = rating
        self.youtube_link = youtube_link
    
    def get_name(self):
        return self.name
    
    def get_artist(self):
        return self.artist
    
    def get_rating(self):
        return self.rating
    
    def getImgPath(self):
        return self.image
