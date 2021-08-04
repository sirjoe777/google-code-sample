"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, name) -> None:
        """"Playlist constructor"""
        self._name = name
        self._videos = []

    def __eq__(self, other) -> bool:
        return self.name.casefold() == other.name.casefold()

    def __lt__(self, other) -> bool:
        return self.name.casefold() < other.name.casefold()
    
    def __str__(self) -> str:
        return self._name

    @property
    def name(self) -> str:
        return self._name
    
    def addVideo(self, video):
        if video in self._videos: return False
        self._videos.append(video)
        return True
    
    def showVideos(self):
        if len(self._videos) == 0:
            print('No videos here yet')
            return
        for video in self._videos:
            print(f'{video}')

    def removeVideo(self, video):
        try:
            self._videos.remove(video)
        except:
            return False
        return True

    def removeAllVideos(self):
        for video in self._videos:
            self.removeVideo(video)
        
    
    