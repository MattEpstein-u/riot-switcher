import sys
import os
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Riot Account Switcher")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("RiotSwitcher")
    
    # Create main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()