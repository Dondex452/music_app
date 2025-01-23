from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                             QTreeView, QFileDialog, QMessageBox, QLabel,
                             QHBoxLayout, QFrame, QSplitter)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont, QIcon

from utils.file_utils import MusicLibrary
from audio.metadata import MetadataReader

class LibraryView(QWidget):
    def __init__(self):
        super().__init__()
        self.library = MusicLibrary()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Title', 'Artist', 'Album', 'Duration'])
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create a splitter for library and playlists
        splitter = QSplitter(Qt.Vertical)
        
        # Library section
        library_widget = QWidget()
        library_layout = QVBoxLayout(library_widget)
        library_layout.setContentsMargins(10, 10, 10, 10)
        
        # Library header
        library_header = QHBoxLayout()
        library_label = QLabel("Music Library")
        library_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        library_header.addWidget(library_label)
        
        self.add_folder_button = QPushButton("Add Folder")
        self.add_folder_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.add_folder_button.clicked.connect(self.add_music_folder)
        library_header.addWidget(self.add_folder_button)
        
        library_layout.addLayout(library_header)
        
        # Library tree view
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.setSortingEnabled(True)
        self.tree_view.setStyleSheet("""
            QTreeView {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QTreeView::item {
                padding: 4px;
            }
            QTreeView::item:hover {
                background-color: #e3f2fd;
            }
            QTreeView::item:selected {
                background-color: #bbdefb;
            }
        """)
        
        # Set column widths
        self.tree_view.setColumnWidth(0, 300)  # Title
        self.tree_view.setColumnWidth(1, 200)  # Artist
        self.tree_view.setColumnWidth(2, 200)  # Album
        self.tree_view.setColumnWidth(3, 100)  # Duration
        
        library_layout.addWidget(self.tree_view)
        
        # Add library widget to splitter
        splitter.addWidget(library_widget)
        
        # Playlists section
        playlists_widget = QWidget()
        playlists_layout = QVBoxLayout(playlists_widget)
        playlists_layout.setContentsMargins(10, 10, 10, 10)
        
        # Playlists header
        playlists_header = QHBoxLayout()
        playlists_label = QLabel("Playlists")
        playlists_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        playlists_header.addWidget(playlists_label)
        
        self.create_playlist_button = QPushButton("New Playlist")
        self.create_playlist_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.create_playlist_button.clicked.connect(self.create_playlist)
        playlists_header.addWidget(self.create_playlist_button)
        
        playlists_layout.addLayout(playlists_header)
        
        # Add playlists widget to splitter
        splitter.addWidget(playlists_widget)
        
        # Set initial sizes
        splitter.setSizes([300, 100])
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
    
    def add_music_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Music Folder",
            "",
            QFileDialog.ShowDirsOnly
        )
        if folder:
            try:
                # Scan folder for music files
                new_files = self.library.add_folder(folder)
                self.update_library_view(new_files)
                QMessageBox.information(
                    self,
                    "Success",
                    f"Added {len(new_files)} tracks to library"
                )
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Error adding folder: {str(e)}"
                )
    
    def update_library_view(self, files):
        """Update the tree view with new music files."""
        for file_path in files:
            metadata = MetadataReader.read_metadata(file_path)
            
            # Create items for the tree view
            title_item = QStandardItem(metadata.get('title', 'Unknown Title'))
            artist_item = QStandardItem(metadata.get('artist', 'Unknown Artist'))
            album_item = QStandardItem(metadata.get('album', 'Unknown Album'))
            duration = self.format_duration(metadata.get('length', 0))
            duration_item = QStandardItem(duration)
            
            # Store the file path in the item's data
            title_item.setData(file_path, Qt.UserRole)
            
            # Add the row to the model
            self.model.appendRow([title_item, artist_item, album_item, duration_item])
    
    def create_playlist(self):
        # TODO: Implement playlist creation dialog
        pass
    
    def get_selected_track(self):
        """Get the file path of the selected track."""
        indexes = self.tree_view.selectedIndexes()
        if indexes:
            # Get the first column (title) of the selected row
            title_index = indexes[0]
            return self.model.itemFromIndex(title_index).data(Qt.UserRole)
        return None
    
    def get_all_tracks(self):
        """Get a list of all tracks in the library."""
        tracks = []
        for row in range(self.model.rowCount()):
            title_item = self.model.item(row, 0)
            track_path = title_item.data(Qt.UserRole)
            if track_path:
                tracks.append(track_path)
        return tracks
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration in seconds to MM:SS format."""
        minutes = int(seconds) // 60
        seconds = int(seconds) % 60
        return f"{minutes}:{seconds:02d}"
