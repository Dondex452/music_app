import pygame
import threading
import time
from typing import Optional, Callable

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_track: Optional[str] = None
        self.is_playing = False
        self.is_paused = False
        self.volume = 1.0  # Range: 0.0 to 1.0
        self.position = 0  # Current position in milliseconds
        self.duration = 0  # Track duration in milliseconds
        self.update_thread: Optional[threading.Thread] = None
        self.should_stop = False
        
        # Callbacks
        self.on_track_finished: Optional[Callable] = None
        self.on_position_changed: Optional[Callable] = None
    
    def load_track(self, track_path: str) -> bool:
        """Load a track from file."""
        try:
            self.stop()
            pygame.mixer.music.load(track_path)
            self.current_track = track_path
            # Get audio length (this is approximate as pygame doesn't provide exact duration)
            sound = pygame.mixer.Sound(track_path)
            self.duration = int(sound.get_length() * 1000)  # Convert to milliseconds
            self.position = 0
            return True
        except Exception as e:
            print(f"Error loading track: {e}")
            return False
    
    def play(self):
        """Start or resume playback."""
        if not self.current_track or self.is_playing:
            return
        
        if self.is_paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.play(start=self.position / 1000.0)  # Convert ms to seconds
            
            # Start position tracking thread
            self.should_stop = False
            self.update_thread = threading.Thread(target=self._track_position)
            self.update_thread.daemon = True
            self.update_thread.start()
        
        self.is_playing = True
        self.is_paused = False
    
    def _track_position(self):
        """Track the current playback position."""
        while not self.should_stop and self.is_playing:
            if not pygame.mixer.music.get_busy() and not self.is_paused:
                # Track finished
                self.stop()
                if self.on_track_finished:
                    self.on_track_finished()
                break
            
            # Update position (this is approximate)
            if not self.is_paused:
                self.position = int(pygame.mixer.music.get_pos())
                if self.on_position_changed:
                    self.on_position_changed(self.position)
            
            time.sleep(0.1)  # Update every 100ms
    
    def pause(self):
        """Pause playback."""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.is_playing = False
    
    def stop(self):
        """Stop playback."""
        self.should_stop = True
        if self.update_thread:
            self.update_thread.join(timeout=1.0)
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.position = 0
    
    def set_volume(self, volume: float):
        """Set playback volume (0.0 to 1.0)."""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
    
    def seek(self, position_ms: int):
        """Seek to position in milliseconds."""
        if not self.current_track:
            return
        
        was_playing = self.is_playing
        self.stop()
        self.position = max(0, min(position_ms, self.duration))
        
        if was_playing:
            self.play()
    
    def get_position(self) -> int:
        """Get current playback position in milliseconds."""
        if self.is_playing:
            pos = pygame.mixer.music.get_pos()
            return pos if pos >= 0 else self.position
        return self.position
    
    def get_duration(self) -> int:
        """Get track duration in milliseconds."""
        return self.duration
