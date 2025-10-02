import sys
import os
from PyQt6.QtWidgets import QApplication

# Add project root to sys.path to allow finding the sn2_interpreter
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = script_dir # The editor script is at the root of the project
sys.path.insert(0, project_root) # Add project root to the path

from editor.main_window import MainWindow

if __name__ == '__main__':
    # Ensure you have PyQt6 installed: pip install PyQt6
    app = QApplication(sys.argv)
    
    # Set a modern style
    app.setStyle("Fusion")

    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())