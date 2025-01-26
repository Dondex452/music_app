from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTreeView, 
                            QFileDialog, QMessageBox, QLabel, QHBoxLayout, 
                            QFrame, QSplitter, QInputDialog, QListWidget,
                            QMenu, QAction)
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
        self.playlists = {}  # Dictionary to store playlists
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
        
        # Add playlist list widget
        self.playlist_list = QListWidget()
        self.playlist_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QListWidget::item {
                padding: 8px;
            }
            QListWidget::item:hover {
                background-color: #e3f2fd;
            }
            QListWidget::item:selected {
                background-color: #bbdefb;
            }
        """)
        playlists_layout.addWidget(self.playlist_list)
        
        # Context menu for playlist items
        self.playlist_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.playlist_list.customContextMenuRequested.connect(self.show_playlist_menu)
        
        # Double click to play playlist
        self.playlist_list.itemDoubleClicked.connect(self.play_playlist)
        
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
        """Create a new playlist."""
        name, ok = QInputDialog.getText(self, 'Create Playlist', 'Enter playlist name:')
        if ok and name:
            if name not in self.playlists:
                self.playlists[name] = []
                self.playlist_list.addItem(name)
                return name
        return None

    def add_to_playlist(self, playlist_name):
        """Add selected tracks to playlist."""
        selected_track = self.get_selected_track()
        if selected_track and playlist_name in self.playlists:
            if selected_track not in self.playlists[playlist_name]:
                self.playlists[playlist_name].append(selected_track)

    def show_playlist_menu(self, position):
        """Show context menu for playlists."""
        menu = QMenu()
        delete_action = QAction("Delete Playlist", self)
        play_action = QAction("Play Playlist", self)
        
        menu.addAction(play_action)
        menu.addAction(delete_action)
        
        item = self.playlist_list.itemAt(position)
        if item:
            action = menu.exec_(self.playlist_list.mapToGlobal(position))
            if action == delete_action:
                self.delete_playlist(item.text())
            elif action == play_action:
                self.play_playlist(item)

    def delete_playlist(self, name):
        """Delete a playlist."""
        if name in self.playlists:
            del self.playlists[name]
            items = self.playlist_list.findItems(name, Qt.MatchExactly)
            for item in items:
                self.playlist_list.takeItem(self.playlist_list.row(item))

    def play_playlist(self, item):
        """Play the selected playlist."""
        playlist_name = item.text()
        if playlist_name in self.playlists and self.playlists[playlist_name]:
            from .main_window import MainWindow
            main_window = self.window()
            if isinstance(main_window, MainWindow):
                tracks = self.playlists[playlist_name]
                main_window.playback_controls.set_playlist(tracks, 0)

    def filter_library(self, search_text):
        """Filter library based on search text."""
        search_text = search_text.lower()
        for row in range(self.model.rowCount()):
            show_row = False
            for col in range(self.model.columnCount()):
                item = self.model.item(row, col)
                if search_text in item.text().lower():
                    show_row = True
                    break
            self.tree_view.setRowHidden(row, self.tree_view.rootIndex(), not show_row)

    # Add context menu for library items
    def setup_tree_view_context_menu(self):
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.show_library_context_menu)

    def show_library_context_menu(self, position):
        """Show context menu for library items."""
        menu = QMenu()
        add_to_playlist_menu = QMenu("Add to Playlist", self)
        
        # Add existing playlists
        for playlist_name in self.playlists.keys():
            action = QAction(playlist_name, self)
            action.triggered.connect(lambda x, name=playlist_name: self.add_to_playlist(name))
            add_to_playlist_menu.addAction(action)
        
        # Add "New Playlist" option
        new_playlist_action = QAction("New Playlist...", self)
        new_playlist_action.triggered.connect(self.create_and_add_to_playlist)
        add_to_playlist_menu.addAction(new_playlist_action)
        
        menu.addMenu(add_to_playlist_menu)
        menu.exec_(self.tree_view.mapToGlobal(position))

    def create_and_add_to_playlist(self):
        """Create a new playlist and add selected track."""
        playlist_name = self.create_playlist()
        if playlist_name:
            self.add_to_playlist(playlist_name)
    
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
    
    def highlight_playing_track(self, file_path: str):
        """Highlight the currently playing track in the tree view."""
        for row in range(self.model.rowCount()):
            item = self.model.item(row, 0)
            if item.data(Qt.UserRole) == file_path:
                self.tree_view.setCurrentIndex(item.index())
                self.tree_view.scrollTo(item.index())
                break
    
    def get_track_at_index(self, index: int) -> str:
        """Get track path at specific index."""
        if 0 <= index < self.model.rowCount():
            return self.model.item(index, 0).data(Qt.UserRole)
        return None
    
    def get_track_index(self, file_path: str) -> int:
        """Get the index of a track in the library."""
        for row in range(self.model.rowCount()):
            if self.model.item(row, 0).data(Qt.UserRole) == file_path:
                return row
        return -1
