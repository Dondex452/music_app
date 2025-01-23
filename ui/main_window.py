from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QListWidget, QSlider,
                             QApplication, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
import os
from .playback_controls import PlaybackControls
from .library_view import LibraryView
from audio.metadata import MetadataReader
from .themes import ThemeManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Player")
        self.setMinimumSize(1000, 700)
        self.is_dark_theme = False
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create top bar with modern styling
        top_bar = QWidget()
        top_bar.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                border-bottom: 1px solid #ddd;
            }
        """)
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(15, 10, 15, 10)
        
        # Add logo
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'logo.webp')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        top_bar_layout.addWidget(logo_label)
        
        # Add app name
        app_name = QLabel("Music Player")
        app_name.setFont(QFont("Segoe UI", 14, QFont.Bold))
        app_name.setStyleSheet("color: #1976D2;")
        top_bar_layout.addWidget(app_name)
        top_bar_layout.addSpacing(20)
        
        # Add search bar with styling
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search music...")
        self.search_bar.setMinimumWidth(300)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background: white;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
            }
        """)
        top_bar_layout.addWidget(self.search_bar)
        
        # Add theme toggle button
        self.theme_button = QPushButton(" Dark Mode")
        self.theme_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.theme_button.clicked.connect(self.toggle_theme)
        top_bar_layout.addWidget(self.theme_button)
        
        main_layout.addWidget(top_bar)
        
        # Create content area
        content_area = QHBoxLayout()
        content_area.setSpacing(0)
        content_area.setContentsMargins(0, 0, 0, 0)
        
        # Left sidebar (library and playlists)
        self.library_view = LibraryView()
        content_area.addWidget(self.library_view, stretch=2)
        
        # Add vertical separator
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setStyleSheet("background-color: #ddd;")
        content_area.addWidget(separator)
        
        # Right area (currently playing + controls)
        right_widget = QWidget()
        right_widget.setMinimumWidth(400)
        right_area = QVBoxLayout(right_widget)
        right_area.setSpacing(20)
        right_area.setContentsMargins(20, 20, 20, 20)
        
        # Now playing section with styling
        now_playing_frame = QFrame()
        now_playing_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        now_playing_layout = QVBoxLayout(now_playing_frame)
        
        now_playing_header = QLabel("Now Playing")
        now_playing_header.setFont(QFont("Segoe UI", 12, QFont.Bold))
        now_playing_header.setAlignment(Qt.AlignCenter)
        now_playing_layout.addWidget(now_playing_header)
        
        self.now_playing_label = QLabel("Not Playing")
        self.now_playing_label.setFont(QFont("Segoe UI", 14))
        self.now_playing_label.setAlignment(Qt.AlignCenter)
        self.now_playing_label.setWordWrap(True)
        now_playing_layout.addWidget(self.now_playing_label)
        
        self.artist_label = QLabel("")
        self.artist_label.setFont(QFont("Segoe UI", 12))
        self.artist_label.setAlignment(Qt.AlignCenter)
        self.artist_label.setStyleSheet("color: #666;")
        now_playing_layout.addWidget(self.artist_label)
        
        self.album_label = QLabel("")
        self.album_label.setFont(QFont("Segoe UI", 11))
        self.album_label.setAlignment(Qt.AlignCenter)
        self.album_label.setStyleSheet("color: #666;")
        now_playing_layout.addWidget(self.album_label)
        
        right_area.addWidget(now_playing_frame)
        
        # Add playback controls
        self.playback_controls = PlaybackControls()
        right_area.addWidget(self.playback_controls)
        
        # Volume control with styling
        volume_frame = QFrame()
        volume_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        volume_layout = QHBoxLayout(volume_frame)
        
        volume_label = QLabel("Volume")
        volume_label.setFont(QFont("Segoe UI", 10))
        volume_layout.addWidget(volume_label)
        
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(100)
        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #cccccc;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #2196F3;
                border: 1px solid #1976D2;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
        """)
        volume_layout.addWidget(self.volume_slider)
        
        right_area.addWidget(volume_frame)
        
        # Add stretch to push everything up
        right_area.addStretch()
        
        # Add right area to content area
        content_area.addWidget(right_widget, stretch=1)
        
        # Add content area to main layout
        content_widget = QWidget()
        content_widget.setLayout(content_area)
        main_layout.addWidget(content_widget)
        
        self.setup_ui_connections()
    
    def setup_ui_connections(self):
        # Connect library selection to playback
        self.library_view.tree_view.doubleClicked.connect(self.play_selected_track)
        
        # Connect volume control
        self.volume_slider.valueChanged.connect(self.volume_changed)
        
        # Connect search
        self.search_bar.textChanged.connect(self.search_library)
    
    def toggle_theme(self):
        """Toggle between light and dark theme."""
        self.is_dark_theme = not self.is_dark_theme
        ThemeManager.apply_theme(QApplication.instance(), self.is_dark_theme)
        
        # Update button text
        if self.is_dark_theme:
            self.theme_button.setText(" Light Mode")
        else:
            self.theme_button.setText(" Dark Mode")
    
    def play_selected_track(self, index):
        track_path = self.library_view.get_selected_track()
        if track_path:
            # Get all tracks for playlist functionality
            all_tracks = self.library_view.get_all_tracks()
            current_index = all_tracks.index(track_path)
            
            # Set the playlist and start playing
            self.playback_controls.set_playlist(all_tracks, current_index)
            
            # Update now playing information
            metadata = MetadataReader.read_metadata(track_path)
            self.now_playing_label.setText(metadata.get('title', 'Unknown Title'))
            self.artist_label.setText(metadata.get('artist', 'Unknown Artist'))
            self.album_label.setText(metadata.get('album', 'Unknown Album'))
    
    def volume_changed(self, value):
        # Convert 0-100 range to 0-1 range
        volume = value / 100.0
        self.playback_controls.set_volume(volume)
    
    def search_library(self, text):
        # TODO: Implement library search
        pass
