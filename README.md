# Music Player App

A Windows-based music player application built with Python and PyQt5.

## Features
- Modern, clean UI design
- Play local music files
- Manage playlists
- Search music library
- Light/Dark theme support
- Basic playback controls (play, pause, skip, shuffle, repeat)
- Metadata display (title, artist, album)
- Volume control
- Progress bar with time display

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Dondex452/music_app.git
cd music_app
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

## Requirements
- Python 3.8+
- Windows OS
- PyQt5
- Pygame (for audio playback)
- Mutagen (for metadata reading)

## Project Structure
```
music_app/
├── main.py                     # Entry point
├── ui/                         # UI components
│   ├── main_window.py         # Main application window
│   ├── playback_controls.py   # Audio playback controls
│   ├── library_view.py        # Music library view
│   └── themes.py              # Theme management
├── audio/                      # Audio handling
│   ├── player.py              # Audio playback
│   └── metadata.py            # Metadata reading
├── database/                   # Playlist management
├── utils/                      # Utilities
│   └── file_utils.py          # File operations
└── assets/                    # Static assets
    └── logo.webp              # Application logo
