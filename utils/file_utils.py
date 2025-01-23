import os
from typing import List, Dict
from pathlib import Path

SUPPORTED_FORMATS = {'.mp3', '.wav', '.flac', '.m4a', '.ogg'}

class MusicLibrary:
    def __init__(self):
        self.music_folders: List[str] = []
        self.tracks: Dict[str, Dict] = {}  # path -> track info
    
    def add_folder(self, folder_path: str) -> List[str]:
        """Add a folder to the music library and scan for music files."""
        if not os.path.exists(folder_path):
            raise ValueError(f"Folder does not exist: {folder_path}")
        
        self.music_folders.append(folder_path)
        return self.scan_folder(folder_path)
    
    def scan_folder(self, folder_path: str) -> List[str]:
        """Scan a folder for music files and return list of found files."""
        music_files = []
        
        for root, _, files in os.walk(folder_path):
            for file in files:
                if Path(file).suffix.lower() in SUPPORTED_FORMATS:
                    full_path = os.path.join(root, file)
                    self.tracks[full_path] = {
                        'path': full_path,
                        'filename': file,
                        'folder': root
                    }
                    music_files.append(full_path)
        
        return music_files
    
    def remove_folder(self, folder_path: str):
        """Remove a folder and its tracks from the library."""
        if folder_path in self.music_folders:
            self.music_folders.remove(folder_path)
            # Remove tracks from this folder
            self.tracks = {
                path: info for path, info in self.tracks.items()
                if not path.startswith(folder_path)
            }
    
    def get_all_tracks(self) -> List[Dict]:
        """Return all tracks in the library."""
        return list(self.tracks.values())
    
    def get_track_info(self, track_path: str) -> Dict:
        """Get information about a specific track."""
        return self.tracks.get(track_path, {})
