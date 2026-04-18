import pygame
import os

class MusicPlayer:
    def __init__(self, music_dir):
        pygame.mixer.init()
        self.music_dir = music_dir
        self.playlist = []
        self.current_index = 0
        self.is_playing = False
        self.is_paused = False
        
        self.load_playlist()

    def load_playlist(self):
        if os.path.exists(self.music_dir):
            for file in sorted(os.listdir(self.music_dir)):
                if file.endswith(('.mp3', '.wav', '.MP3', '.WAV')):
                    self.playlist.append(file)
        else:
            print(f"Warning: Directory '{self.music_dir}' not found.")

    def play(self):
        if not self.playlist:
            return

        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.is_playing = True
        elif not self.is_playing:
            track_path = os.path.join(self.music_dir, self.playlist[self.current_index])
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False

    def pause(self):
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True

    def next_track(self):
        if not self.playlist: return
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def prev_track(self):
        if not self.playlist: return
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    def get_current_track_name(self):
        if not self.playlist:
            return "No tracks available"
        return self.playlist[self.current_index]

    def get_status(self):
        if self.is_paused:
            return "Paused"
        elif self.is_playing:
            return "Playing"
        return "Stopped"
        
    def get_progress(self):
        if self.is_playing and not self.is_paused:
            return pygame.mixer.music.get_pos() / 1000.0
        return 0.0