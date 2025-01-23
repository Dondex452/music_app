from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QPushButton, QSlider,
                             QStyle, QVBoxLayout, QLabel)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from audio.player import AudioPlayer

class PlaybackControls(QWidget):
    def __init__(self):
        super().__init__()
        self.player = AudioPlayer()
        self.current_playlist = []  # List of track paths
        self.current_index = -1
        self.is_shuffle = False
        self.is_repeat = False
        
        # Setup timer for progress updates
        self.update_timer = QTimer()
        self.update_timer.setInterval(1000)  # Update every second
        self.update_timer.timeout.connect(self.update_progress)
        
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        
        # Progress bar and time labels
        progress_layout = QHBoxLayout()
        
        self.time_label = QLabel("0:00")
        self.time_label.setStyleSheet("color: #666;")
        progress_layout.addWidget(self.time_label)
        
        self.progress_bar = QSlider(Qt.Horizontal)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(1000)
        self.progress_bar.setStyleSheet("""
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
        progress_layout.addWidget(self.progress_bar)
        
        self.duration_label = QLabel("0:00")
        self.duration_label.setStyleSheet("color: #666;")
        progress_layout.addWidget(self.duration_label)
        
        main_layout.addLayout(progress_layout)
        
        # Playback controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(20)
        controls_layout.setContentsMargins(10, 0, 10, 0)
        
        # Create buttons with consistent size and styling
        button_style = """
            QPushButton {
                background-color: #2196F3;
                border-radius: 20px;
                padding: 10px;
                border: none;
                color: white;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
        """
        
        self.shuffle_button = QPushButton()
        self.shuffle_button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.shuffle_button.setFixedSize(40, 40)
        self.shuffle_button.setStyleSheet(button_style)
        
        self.prev_button = QPushButton()
        self.prev_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.prev_button.setFixedSize(40, 40)
        self.prev_button.setStyleSheet(button_style)
        
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.setFixedSize(50, 50)
        self.play_button.setStyleSheet(button_style)
        
        self.next_button = QPushButton()
        self.next_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.next_button.setFixedSize(40, 40)
        self.next_button.setStyleSheet(button_style)
        
        self.repeat_button = QPushButton()
        self.repeat_button.setIcon(self.style().standardIcon(QStyle.SP_BrowserStop))
        self.repeat_button.setFixedSize(40, 40)
        self.repeat_button.setStyleSheet(button_style)
        
        # Add buttons to layout with center alignment
        controls_layout.addStretch()
        controls_layout.addWidget(self.shuffle_button)
        controls_layout.addWidget(self.prev_button)
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.next_button)
        controls_layout.addWidget(self.repeat_button)
        controls_layout.addStretch()
        
        main_layout.addLayout(controls_layout)
        
        self.setLayout(main_layout)
        
        # Connect signals
        self.setup_connections()
    
    def setup_connections(self):
        self.play_button.clicked.connect(self.toggle_play)
        self.prev_button.clicked.connect(self.previous_track)
        self.next_button.clicked.connect(self.next_track)
        self.shuffle_button.clicked.connect(self.toggle_shuffle)
        self.repeat_button.clicked.connect(self.toggle_repeat)
        self.progress_bar.sliderMoved.connect(self.seek_position)
        self.progress_bar.sliderPressed.connect(self.on_slider_pressed)
        self.progress_bar.sliderReleased.connect(self.on_slider_released)
    
    def load_track(self, track_path: str):
        """Load a new track for playback."""
        if self.player.load_track(track_path):
            self.progress_bar.setMaximum(self.player.get_duration())
            self.duration_label.setText(self.format_time(self.player.get_duration()))
            self.play()
    
    def set_playlist(self, tracks: list, current_index: int = 0):
        """Set the current playlist and start playing from the specified index."""
        self.current_playlist = tracks
        self.current_index = current_index
        if tracks and 0 <= current_index < len(tracks):
            self.load_track(tracks[current_index])
    
    def toggle_play(self):
        if not self.player.current_track:
            return
        
        if self.player.is_playing:
            self.pause()
        else:
            self.play()
    
    def play(self):
        self.player.play()
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.update_timer.start()
    
    def pause(self):
        self.player.pause()
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.update_timer.stop()
    
    def previous_track(self):
        if not self.current_playlist:
            return
            
        if self.is_shuffle:
            # TODO: Implement shuffle previous
            pass
        else:
            self.current_index = (self.current_index - 1) % len(self.current_playlist)
            self.load_track(self.current_playlist[self.current_index])
    
    def next_track(self):
        if not self.current_playlist:
            return
            
        if self.is_shuffle:
            # TODO: Implement shuffle next
            pass
        else:
            self.current_index = (self.current_index + 1) % len(self.current_playlist)
            self.load_track(self.current_playlist[self.current_index])
    
    def toggle_shuffle(self):
        self.is_shuffle = not self.is_shuffle
        self.shuffle_button.setStyleSheet(
            self.shuffle_button.styleSheet() +
            f"background-color: {'#1565C0' if self.is_shuffle else '#2196F3'};"
        )
    
    def toggle_repeat(self):
        self.is_repeat = not self.is_repeat
        self.repeat_button.setStyleSheet(
            self.repeat_button.styleSheet() +
            f"background-color: {'#1565C0' if self.is_repeat else '#2196F3'};"
        )
    
    def seek_position(self, value):
        """Seek to position when user moves the slider."""
        if self.player.current_track:
            self.player.seek(value)
            self.time_label.setText(self.format_time(value))
    
    def on_slider_pressed(self):
        """Called when user starts dragging the progress slider."""
        self.update_timer.stop()
    
    def on_slider_released(self):
        """Called when user releases the progress slider."""
        if self.player.is_playing:
            self.update_timer.start()
    
    def update_progress(self):
        """Update progress bar position and time label."""
        if self.player.is_playing:
            position = self.player.get_position()
            self.progress_bar.setValue(position)
            self.time_label.setText(self.format_time(position))
    
    def set_volume(self, volume: float):
        """Set the playback volume."""
        self.player.set_volume(volume)
    
    @staticmethod
    def format_time(ms: int) -> str:
        """Convert milliseconds to MM:SS format."""
        total_seconds = ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"
