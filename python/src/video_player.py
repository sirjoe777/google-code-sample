"""A video player class."""

from .video_library import VideoLibrary
from random import randint
from .video_playlist import Playlist

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()

        #Store boolean to check if a video is playing and the playing video
        self.playing_video = None

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""

        videos = self._video_library.get_all_videos()
        videos.sort()
        print("Here's a list of all available videos:")
        for video in videos:
            print(f"{video}")

    def play_video(self, video_id):
        video = self._video_library.get_video(video_id)
        if video is None: 
            print('Cannot play video: Video does not exist')
            return
        elif video.flagged[0]:
            print(f'Cannot play video: Video is currently flagged (reason: {video.flagged[1]})')
            return
        elif self.playing_video is not None and (self.playing_video.playing or self.playing_video.paused):
            print(f'Stopping video: {self.playing_video.title}')
        print(f'Playing video: {video.title}')
        self.playing_video = video
        self.playing_video.play()


    def stop_video(self):
        """Stops the current video."""
        if self.playing_video is not None and (self.playing_video.playing or self.playing_video.paused):
            print(f'Stopping video: {self.playing_video.title}')
            self.playing_video = None
        else:
            print('Cannot stop video: No video is currently playing')

    def play_random_video(self):
        """Plays a random video from the video library."""
        available_videos = []
        for video in self._video_library.get_all_videos():
            if not video.flagged[0]: available_videos.append(video)
        if len(available_videos)==0: 
            print("No videos available")
            return
        index = randint(0,len(available_videos)-1)
        self.play_video(available_videos[index].video_id)

    def pause_video(self):
        """Pauses the current video."""
        if self.playing_video is None:
            print('Cannot pause video: No video is currently playing')
        elif self.playing_video.playing:
            print(f'Pausing video: {self.playing_video.title}')
            self.playing_video.pause()
        else:
            print(f'Video already paused: {self.playing_video.title}')
            

    def continue_video(self):
        """Resumes playing the current video."""
        if self.playing_video is None:
            print('Cannot continue video: No video is currently playing')
            return
        elif self.playing_video.playing:
            print('Cannot continue video: Video is not paused')
            return
        else:
            print(f'Continuing video: {self.playing_video.title}')
            self.playing_video.play()

    def show_playing(self):
        """Displays video currently playing."""
        if self.playing_video is None:
            print('No video is currently playing')
            return
        paused = ''
        if self.playing_video.paused:
            paused = ' - PAUSED'
        print(f'Currently playing: {self.playing_video}'+paused)

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name."""
        playlist = self._video_library.get_playlist(playlist_name)
        if playlist is None:
            playlist_to_add = Playlist(playlist_name)
            self._video_library.add_playlist(playlist_to_add)
            print(f'Successfully created new playlist: {playlist_name}')
        else: print('Cannot create playlist: A playlist with the same name already exists')
            

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name."""
        playlist = self._video_library.get_playlist(playlist_name)
        video = self._video_library.get_video(video_id)
        if playlist is None:
            print(f'Cannot add video to {playlist_name}: Playlist does not exist')
        elif video is None:
            print(f'Cannot add video to {playlist_name}: Video does not exist')
        elif video.flagged[0]:
            print(f'Cannot add video to {playlist_name}: Video is currently flagged (reason: {video.flagged[1]})')
        elif not playlist.addVideo(video):
            print(f'Cannot add video to {playlist_name}: Video already added')
        else:
            print(f'Added video to {playlist_name}: {video.title}')

        

    def show_all_playlists(self):
        """Display all playlists."""
        if len(self._video_library._playlists) == 0:
            print('No playlists exist yet')
            return
        print('Showing all playlists:')
        self._video_library._playlists.sort()
        for playlist in self._video_library._playlists:
            print(playlist)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name."""
        playlist = self._video_library.get_playlist(playlist_name)
        if playlist is None:
            print(f'Cannot show playlist {playlist_name}: Playlist does not exist')
            return
        print(f'Showing playlist: {playlist_name}')
        playlist.showVideos()

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name."""
        playlist = self._video_library.get_playlist(playlist_name)
        video = self._video_library.get_video(video_id)
        if playlist is None: print(f'Cannot remove video from {playlist_name}: Playlist does not exist')
        elif video is None: print(f'Cannot remove video from {playlist_name}: Video does not exist')
        elif not playlist.removeVideo(video): print(f'Cannot remove video from {playlist_name}: Video is not in playlist')
        else: print(f'Removed video from {playlist_name}: {video.title}')
            

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name."""
        playlist = self._video_library.get_playlist(playlist_name)
        if playlist is None: 
            print(f'Cannot clear playlist {playlist_name}: Playlist does not exist')
            return
        playlist.removeAllVideos()
        print(f'Successfully removed all videos from {playlist_name}')

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name."""
        playlist = self._video_library.get_playlist(playlist_name)
        if playlist is None:
            print(f'Cannot delete playlist {playlist_name}: Playlist does not exist')
        else: self._video_library.remove_playlist(playlist)


    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term."""

        #Collect search results
        videos = []
        for video in self._video_library.get_all_videos():
            if video.flagged[0]: continue
            if search_term.casefold() in video.title.casefold():
                videos.append(video)

        #If there are no results show warning and return
        if len(videos) == 0:
            print(f'No search results for {search_term}')
            return

        #Otherwise sort the results and display them
        videos.sort()
        print(f'Here are the results for {search_term}:')
        for i in range(len(videos)):
            print(f'{str(i+1)}) {videos[i].title} ({videos[i].video_id}) [{videos[i].tags_str()}]')

        #Ask the user if they want to play a video from the results
        print('Would you like to play any of the above? If yes, specify the number of the video.')
        print('If your answer is not a valid number, we will assume it\'s a no.')
        ans_str = input()
        try:
            ans_int = int(ans_str)
            if 1 <= ans_int <= len(videos):
                self.play_video(videos[ans_int-1].video_id)
        except ValueError:
            return

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag."""

        #If user forgot hashtag display message and return
        if video_tag[0] != '#':
            print(f'No search results for {video_tag}')
            return
        
        #Otherwise collect search results
        videos = []
        for video in self._video_library.get_all_videos():
            if video.flagged[0]: continue
            if video_tag.casefold() in video.tags_str().casefold():
                videos.append(video)

        #If there are no results show warning and return
        if len(videos) == 0:
            print(f'No search results for {video_tag}')
            return

        #Otherwise sort the results and display them
        videos.sort()
        print(f'Here are the results for {video_tag}:')
        for i in range(len(videos)):
            print(f'{str(i+1)}) {videos[i].title} ({videos[i].video_id}) [{videos[i].tags_str()}]')

        #Ask the user if they want to play a video from the results
        print('Would you like to play any of the above? If yes, specify the number of the video.')
        print('If your answer is not a valid number, we will assume it\'s a no.')
        ans_str = input()
        try:
            ans_int = int(ans_str)
            if 1 <= ans_int <= len(videos):
                self.play_video(videos[ans_int-1].video_id)
        except ValueError:
            return
        

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged."""
        video = self._video_library.get_video(video_id)
        if video is None:
            print('Cannot flag video: Video does not exist')
            return
        elif video.flagged[0]:
            print('Cannot flag video: Video is already flagged')
            return
        video.flag(flag_reason)
        if self.playing_video is not None and video == self.playing_video:
            self.stop_video()
        print(f'Successfully flagged video: {video.title} (reason: {video.flagged[1]})')

    def allow_video(self, video_id):
        """Removes a flag from a video."""
        video = self._video_library.get_video(video_id)
        if video is None:
            print('Cannot remove flag from video: Video does not exist')
            return
        elif not video.flagged[0]:
            print('Cannot remove flag from video: Video is not flagged')
            return
        video.unflag()
        print(f'Successfully removed flag from video: {video.title}')
