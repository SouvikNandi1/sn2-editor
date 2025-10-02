import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFileDialog,
    QMessageBox, QTabWidget, QToolBar, QDockWidget, QTreeView, QSizePolicy, QMenu, QToolButton,
    QLabel
)
from PyQt6.QtGui import (
    QFont, QIcon, QAction, QPalette, QFileSystemModel, QActionGroup, QDesktopServices
)
from PyQt6.QtCore import (
    Qt, QDir, QSettings, QProcess, QUrl, QThread
)

from .themes import THEMES, DEFAULT_THEME
from .widgets import CodeEditor, TerminalWidget
from .update_worker import UpdateWorker

# Add project root to sys.path to allow finding the sn2_interpreter
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("Sn2Lang", "Sn2Editor")
        self.current_folder_path = None
        self.interpreter_path = os.path.join(project_root, "bin", "sn2_interpreter.py")
        self.init_ui()
        self.restore_settings()
        self.check_for_updates()

    def init_ui(self):
        self.setWindowTitle("Sn2 Code Editor")
        self.setWindowIcon(QIcon(os.path.join(project_root, "bin", "sn2.ico")))
        self.resize(1200, 800)

        # --- Central Widget: Tabbed Editor ---
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tab_widget)

        # --- Welcome Page ---
        self.show_welcome_page()

        # --- Actions and Toolbar ---
        # Docks must be created before the toolbar that references them.
        self.create_actions()
        self.create_docks()
        self.create_toolbar()

    def show_welcome_page(self):
        self.welcome_widget = QWidget()
        main_layout = QVBoxLayout(self.welcome_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(20)

        # --- Title ---
        title = QLabel("Welcome to the Sn2 Code Editor")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        main_layout.addSpacing(30)

        # --- Action Links ---
        link_font = QFont("Segoe UI", 12)
        link_style = "text-decoration: none; color: {color};"

        open_file_btn = QLabel(f'<a href="open_file" style="{link_style}">Open File...</a>')
        open_file_btn.setFont(link_font)
        open_file_btn.linkActivated.connect(self.open_file)
        open_file_btn.setAlignment(Qt.AlignmentFlag.AlignCenter)

        open_folder_btn = QLabel(f'<a href="open_folder" style="{link_style}">Open Folder...</a>')
        open_folder_btn.setFont(link_font)
        open_folder_btn.linkActivated.connect(self.open_folder)
        open_folder_btn.setAlignment(Qt.AlignmentFlag.AlignCenter)

        doc_link = QLabel(f'<a href="doc" style="{link_style}">View Documentation</a>')
        doc_link.setFont(link_font)
        doc_link.linkActivated.connect(lambda: QDesktopServices.openUrl(QUrl("https://disunic.vercel.app/documentation/sn2")))
        doc_link.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(open_file_btn)
        main_layout.addWidget(open_folder_btn)
        main_layout.addWidget(doc_link)

        self.tab_widget.addTab(self.welcome_widget, "Welcome")
        self.tab_widget.setTabsClosable(False) # Can't close welcome tab

    def create_actions(self):
        self.new_action = QAction(QIcon.fromTheme("document-new"), "&New", self)
        self.new_action.triggered.connect(self.new_file)
        self.open_action = QAction(QIcon.fromTheme("document-open"), "&Open File...", self)
        self.open_action.triggered.connect(self.open_file)
        self.open_folder_action = QAction(QIcon.fromTheme("folder-open"), "Open &Folder...", self)
        self.open_folder_action.triggered.connect(self.open_folder)
        self.save_action = QAction(QIcon.fromTheme("document-save"), "&Save", self)
        self.save_action.triggered.connect(self.save_file)
        self.save_as_action = QAction(QIcon.fromTheme("document-save-as"), "Save &As...", self)
        self.save_as_action.triggered.connect(self.save_file_as)
        self.run_action = QAction(QIcon.fromTheme("system-run"), "&Run Sn2 Code", self)
        self.run_action.triggered.connect(self.run_code)
        self.about_action = QAction(QIcon.fromTheme("help-about"), "&About", self)
        self.about_action.triggered.connect(self.show_about_dialog)


    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        toolbar.setMovable(False)

        # Prevent the toolbar from being hidden by the user via context menus
        toolbar.toggleViewAction().setVisible(False)

        toolbar.addAction(self.new_action)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.open_folder_action)
        toolbar.addAction(self.save_action)
        toolbar.addSeparator()

        # Create a "View" menu button on the toolbar
        view_button = QToolButton(self)
        view_icon = QIcon.fromTheme("preferences-system")
        if view_icon.isNull():
            # Fallback to text if icon theme is not available (e.g., on some Windows setups)
            view_button.setText("View")
        else:
            view_button.setIcon(view_icon)
        view_button.setAutoRaise(True) # Makes the button flat
        view_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        view_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        view_menu = QMenu(view_button)
        view_button.setMenu(view_menu)
        toolbar.addWidget(view_button)

        # --- Populate the View Menu ---
        theme_menu = view_menu.addMenu("Themes")
        self.theme_group = QActionGroup(self)
        self.theme_group.setExclusive(True)
        for theme_name in THEMES:
            action = QAction(theme_name, self, checkable=True)
            action.triggered.connect(lambda checked, name=theme_name: self.apply_theme(name))
            theme_menu.addAction(action)
            self.theme_group.addAction(action)

        view_menu.addSeparator()
        view_menu.addAction(self.explorer_dock.toggleViewAction())
        view_menu.addAction(self.terminal_dock.toggleViewAction())

        view_menu.addSeparator()
        view_menu.addAction(self.about_action)

        # Add a spacer widget to push the run button to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        toolbar.addWidget(spacer)

        toolbar.addAction(self.run_action)

    def create_docks(self):
        # --- File Explorer Dock ---
        self.explorer_dock = QDockWidget("File Explorer", self)
        self.file_system_model = QFileSystemModel()
        self.file_system_model.setFilter(QDir.Filter.NoDotAndDotDot | QDir.Filter.AllDirs | QDir.Filter.Files)
        self.file_system_model.setNameFilters(["*.sn2", "*.txt"])
        self.file_system_model.setNameFilterDisables(False)

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_system_model)
        self.tree_view.doubleClicked.connect(self.explorer_file_opened)
        
        # Hide unnecessary columns
        for i in range(1, self.file_system_model.columnCount()):
            self.tree_view.hideColumn(i)

        self.explorer_dock.setWidget(self.tree_view)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.explorer_dock)

        # --- Terminal Dock ---
        self.terminal_dock = QDockWidget("Terminal", self)
        self.terminal = TerminalWidget()
        self.terminal_dock.setWidget(self.terminal)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.terminal_dock)

        # --- Splitter ---
        self.setCorner(Qt.Corner.BottomLeftCorner, Qt.DockWidgetArea.LeftDockWidgetArea)

    def restore_settings(self):
        theme_name = self.settings.value("theme", DEFAULT_THEME, type=str)
        self.apply_theme(theme_name)

        last_folder = self.settings.value("last_folder", QDir.homePath())
        self.set_folder_view(last_folder)
        
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        state = self.settings.value("windowState")
        if state:
            self.restoreState(state)

    def apply_theme(self, name):
        if name not in THEMES:
            name = DEFAULT_THEME

        theme = THEMES[name]
        app = QApplication.instance()

        # Set application-wide palette
        palette = QPalette()
        text_color = theme.get("app_text", theme["text"])
        palette.setColor(QPalette.ColorRole.Window, theme["app_window"])
        palette.setColor(QPalette.ColorRole.WindowText, text_color)
        palette.setColor(QPalette.ColorRole.Base, theme["app_base"])
        palette.setColor(QPalette.ColorRole.AlternateBase, theme["app_window"])
        palette.setColor(QPalette.ColorRole.ToolTipBase, text_color)
        palette.setColor(QPalette.ColorRole.ToolTipText, theme["app_window"])
        palette.setColor(QPalette.ColorRole.Text, text_color)
        palette.setColor(QPalette.ColorRole.Button, theme["app_window"])
        palette.setColor(QPalette.ColorRole.ButtonText, text_color)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, theme["app_highlight"])
        palette.setColor(QPalette.ColorRole.Highlight, theme["app_highlight"])
        palette.setColor(QPalette.ColorRole.HighlightedText, theme.get("app_highlighted_text", Qt.GlobalColor.white))
        app.setPalette(palette) # type: ignore

        # Update editor widgets
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if isinstance(widget, CodeEditor):
                widget.set_theme(theme)

        # Update terminal theme
        self.terminal.set_theme(theme)

        self.settings.setValue("theme", name)
        self.update_theme_menu_selection(name)

    def set_folder_view(self, path):
        if os.path.isdir(path):
            self.current_folder_path = path
            self.file_system_model.setRootPath(path)
            self.tree_view.setRootIndex(self.file_system_model.index(path))
            self.settings.setValue("last_folder", path)

    def update_theme_menu_selection(self, theme_name):
        for action in self.theme_group.actions():
            if action.text() == theme_name:
                action.setChecked(True)

    def explorer_file_opened(self, index):
        path = self.file_system_model.filePath(index)
        if os.path.isfile(path):
            self.open_file(path)

    def check_for_updates(self):
        """Starts the update check in a background thread."""
        self.update_thread = QThread()
        self.update_worker = UpdateWorker()
        self.update_worker.moveToThread(self.update_thread)

        self.update_thread.started.connect(self.update_worker.run)
        self.update_worker.update_found.connect(self.show_update_dialog)

        # Clean up the thread when it's finished
        self.update_worker.finished.connect(self.update_thread.quit)
        self.update_thread.finished.connect(self.update_thread.deleteLater)
        self.update_worker.finished.connect(self.update_worker.deleteLater)

        self.update_thread.start()

    def show_update_dialog(self, new_version, download_url):
        """Shows a dialog notifying the user about a new version."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Update Available")
        msg_box.setText(f"A new version ({new_version}) of the Sn2 Code Editor is available!\n\nWould you like to visit the download page?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if msg_box.exec() == QMessageBox.StandardButton.Yes:
            QDesktopServices.openUrl(QUrl(download_url))

    def show_about_dialog(self):
        """Displays the About dialog box for the editor."""
        from .version import __version__ as editor_version
        title = "About Sn2 Code Editor"
        text = (
            f"<h2>Sn2 Code Editor v{editor_version}</h2>"
            "<p>A dedicated code editor for the <b>Sn2</b> scripting language.</p>"
            "<p>Developed by Souvik Nandi.</p>"
            "<p>This editor provides syntax highlighting, code completion, "
            "a file explorer, and an integrated terminal to write and run Sn2 code seamlessly.</p>"
            "<p>For more information about the Sn2 language, visit the "
            "<a href='https://disunic.vercel.app/documentation/sn2'>official documentation</a>.</p>"
        )
        QMessageBox.about(self, title, text)

    def new_file(self):
        self.add_editor_tab(None, "Untitled")

    def open_file(self, path=None):
        if not path:
            path, _ = QFileDialog.getOpenFileName(
                self, "Open File", self.current_folder_path or QDir.homePath(), "Sn2 Files (*.sn2);;Text Files (*.txt);;All Files (*)"
            )
        if path:
            # Check if file is already open
            for i in range(self.tab_widget.count()):
                if self.tab_widget.tabToolTip(i) == path:
                    self.tab_widget.setCurrentIndex(i)
                    return
            self.add_editor_tab(path, os.path.basename(path))

    def open_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Open Folder", self.current_folder_path or QDir.homePath())
        if path:
            self.set_folder_view(path)

    def save_file(self):
        current_widget = self.tab_widget.currentWidget()
        if not isinstance(current_widget, CodeEditor):
            return

        path = self.tab_widget.tabToolTip(self.tab_widget.currentIndex())
        if path and path != "Unsaved":
            self._write_to_file(path, current_widget.toPlainText())
        else:
            self.save_file_as()

    def save_file_as(self):
        current_widget = self.tab_widget.currentWidget()
        if not isinstance(current_widget, CodeEditor):
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Save File As", self.current_folder_path or QDir.homePath(), "Sn2 Files (*.sn2);;Text Files (*.txt)"
        )
        if path:
            self._write_to_file(path, current_widget.toPlainText())
            self.tab_widget.setTabText(self.tab_widget.currentIndex(), os.path.basename(path))
            self.tab_widget.setTabToolTip(self.tab_widget.currentIndex(), path)

    def _write_to_file(self, path, content):
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.statusBar().showMessage(f"Saved to {path}", 2000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file:\n{e}")

    def add_editor_tab(self, path, name):
        # If this is the first file opened, remove the welcome tab
        if self.tab_widget.count() == 1 and self.tab_widget.widget(0) == self.welcome_widget:
            self.tab_widget.removeTab(0)
            self.tab_widget.setTabsClosable(True)

        editor = CodeEditor()
        # Apply the current theme to the new editor instance
        current_theme_name = self.settings.value("theme", DEFAULT_THEME)
        self.terminal.set_theme(THEMES[current_theme_name])
        editor.set_theme(THEMES[current_theme_name])

        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    editor.setPlainText(f.read())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file:\n{e}")
                return

        index = self.tab_widget.addTab(editor, name)
        self.tab_widget.setTabToolTip(index, path if path else "Unsaved")
        self.tab_widget.setCurrentIndex(index)

    def close_tab(self, index):
        editor = self.tab_widget.widget(index)
        if editor.document().isModified():
            reply = QMessageBox.question(
                self, 'Save Changes?',
                f"'{self.tab_widget.tabText(index)}' has been modified. Save changes?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.save_file()
            elif reply == QMessageBox.StandardButton.Cancel:
                return

        self.tab_widget.removeTab(index)

        # If no tabs are left, show the welcome page
        if self.tab_widget.count() == 0:
            self.show_welcome_page()

    def run_code(self):
        # If the terminal is hidden, show it before running code.
        if not self.terminal_dock.isVisible():
            self.terminal_dock.show()

        current_widget = self.tab_widget.currentWidget()
        if not isinstance(current_widget, CodeEditor):
            self.terminal.append(">>> No Sn2 file is active to run.")
            return

        path = self.tab_widget.tabToolTip(self.tab_widget.currentIndex())
        if not path or path == "Unsaved":
            self.terminal.append(">>> Please save the file before running.")
            return

        if not path.endswith(".sn2"):
            self.terminal.append(f">>> Cannot run '{os.path.basename(path)}'. Only .sn2 files are executable.")
            return

        self.terminal.clear()
        self.terminal.append(f">>> Running {path}...\n")

        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.handle_process_output)
        self.process.finished.connect(self.handle_process_finished)

        self.terminal.set_process(self.process) # Give the terminal a reference to the process

        # Call the python interpreter directly for more reliable output capturing
        # by QProcess, bypassing the .bat script.
        python_executable = sys.executable
        self.process.start(python_executable, [self.interpreter_path, path])

    def handle_process_output(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.terminal.append_output(data)

    def handle_process_finished(self):
        self.terminal.append("\n>>> Process finished.")
        self.terminal.set_process(None) # Clear the process reference
        self.process = None

    def closeEvent(self, event):
        # Save settings on close
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        self.settings.setValue("theme", self.settings.value("theme", DEFAULT_THEME))
        
        # Check for unsaved changes before closing all tabs
        for i in range(self.tab_widget.count()):
            if isinstance(self.tab_widget.widget(i), CodeEditor) and self.tab_widget.widget(i).document().isModified():
                self.tab_widget.setCurrentIndex(i)
                reply = QMessageBox.question(
                    self, 'Save Changes?',
                    f"You have unsaved changes. Save before exiting?",
                    QMessageBox.StandardButton.SaveAll | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel
                )
                if reply == QMessageBox.StandardButton.SaveAll:
                    for j in range(self.tab_widget.count()):
                        self.tab_widget.setCurrentIndex(j)
                        self.save_file()
                    break
                elif reply == QMessageBox.StandardButton.Cancel:
                    event.ignore()
                    return
                elif reply == QMessageBox.StandardButton.Discard:
                    break # Exit the loop and allow closing

        super().closeEvent(event)