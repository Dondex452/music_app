from typing import Dict, Optional
from mutagen import File
from mutagen.easyid3 import EasyID3
import os

class MetadataReader:
    @staticmethod
    def read_metadata(file_path: str) -> Dict:
        """Read metadata from an audio file."""
        if not os.path.exists(file_path):
            return {}
        
        try:
            # Try to read ID3 tags first
            audio = File(file_path, easy=True)
            if audio is None:
                # Fallback to basic file info
                return MetadataReader._get_basic_info(file_path)
            
            metadata = {
                'title': MetadataReader._get_first(audio, 'title'),
                'artist': MetadataReader._get_first(audio, 'artist'),
                'album': MetadataReader._get_first(audio, 'album'),
                'genre': MetadataReader._get_first(audio, 'genre'),
                'date': MetadataReader._get_first(audio, 'date'),
                'track_number': MetadataReader._get_first(audio, 'tracknumber'),
            }
            
            # Add basic file info
            metadata.update(MetadataReader._get_basic_info(file_path))
            
            return metadata
            
        except Exception as e:
            print(f"Error reading metadata for {file_path}: {e}")
            return MetadataReader._get_basic_info(file_path)
    
    @staticmethod
    def _get_first(audio: EasyID3, key: str) -> Optional[str]:
        """Get first value from a metadata field."""
        try:
            return audio[key][0] if key in audio else None
        except:
            return None
    
    @staticmethod
    def _get_basic_info(file_path: str) -> Dict:
        """Get basic file information when metadata is unavailable."""
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        
        return {
            'filename': filename,
            'title': name,  # Use filename as title
            'extension': ext.lower(),
            'path': file_path,
            'size': os.path.getsize(file_path),
            'modified': os.path.getmtime(file_path)
        }
