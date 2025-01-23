import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.themes import ThemeManager

def main():
    app = QApplication(sys.argv)
    
    # Apply initial light theme
    ThemeManager.apply_theme(app, is_dark=False)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
