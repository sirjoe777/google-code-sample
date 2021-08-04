"""A video class."""

from typing import Sequence


class Video:
    """A class used to represent a Video."""

    def __init__(self, video_title: str, video_id: str, video_tags: Sequence[str]):
        """Video constructor."""
        self._title = video_title
        self._video_id = video_id

        # Turn the tags into a tuple here so it's unmodifiable,
        # in case the caller changes the 'video_tags' they passed to us
        self._tags = tuple(video_tags)

        #Booleans to check if video is playing or paused
        self._playing = False
        self._paused = False
        self._flagged = [False, '']

    @property
    def title(self) -> str:
        """Returns the title of a video."""
        return self._title

    @property
    def video_id(self) -> str:
        """Returns the video id of a video."""
        return self._video_id

    @property
    def tags(self) -> Sequence[str]:
        """Returns the list of tags of a video."""
        return self._tags

    @property
    def playing(self) -> bool:
        """Returns boolean representing if video is playing"""
        return self._playing
    
    @property
    def paused(self) -> bool:
        """Returns voolean representing if video is paused"""
        return self._paused
    
    @property
    def flagged(self) -> list:
        """Returns list representing if video is flagged and eventual reason for flagging"""
        return self._flagged


    #For sorting
    def __eq__(self, other):
        return self.video_id == other.video_id
    
    def __lt__(self,other):
        return self.title<other.title
    
    #For printing tags separately
    def tags_str(self):
        tags_str = ''
        for i in range(len(self.tags)):
            tags_str += self.tags[i]
            if i != len(self.tags)-1: 
                tags_str += ' '
        return tags_str

    #Manipulate status of the video
    def play(self):
        self._playing = True
        self._paused = False
    def pause(self):
        self._paused = True
        self._playing = False

    #String representation
    def __str__(self):
        video = f'{self.title} ({self.video_id}) [{self.tags_str()}]'
        if self.flagged[0]:
            return video + f' - FLAGGED (reason: {self.flagged[1]})'
        return video
    
    #Flag a video
    def flag(self, message):
        if message == '' or message == "":
            self._flagged = [True,'Not supplied']
        else:
            self._flagged = [True, message]
    
    #Un-flag a video
    def unflag(self):
        self._flagged = [False, '']

