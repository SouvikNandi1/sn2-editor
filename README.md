# Sn2 Code Editor

A dedicated, cross-platform code editor for the [Sn2 scripting language](https://disunic.vercel.app/documentation/sn2), built with Python and PyQt6.

![Sn2 Editor Screenshot](https://raw.githubusercontent.com/SouvikNandi1/sn2-editor/main/assets/screenshot.png)

## Features

*   **Sn2 Syntax Highlighting**: Clear and colorful syntax highlighting specifically for the Sn2 language.
*   **Smart Code Completion**: Autocompletes keywords and built-in functions as you type.
*   **Extensive Theming**: Comes with over 20 pre-built themes (both dark and light) to customize your coding environment. Includes popular themes like Monokai, Dracula, Nord, Solarized, and more.
*   **Integrated Terminal**: Run your Sn2 scripts directly within the editor and see the output immediately.
*   **File Explorer**: A dockable file explorer to easily navigate your project folders and files.
*   **Tabbed Interface**: Work on multiple files simultaneously with a familiar tabbed layout.
*   **Automatic Update Checker**: Notifies you when a new version of the editor is available.
*   **Cross-Platform**: Built with Python and PyQt6, it runs on Windows, macOS, and Linux.

## Getting Started

To run the editor from the source code, follow these steps.

### Prerequisites

*   Python 3.6+
*   Git

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/SouvikNandi1/sn2-editor.git
    cd sn2-editor
    ```

2.  **Install the required dependencies:**
    The editor relies on PyQt6. You can install it using pip.
    ```sh
    pip install PyQt6
    ```

3.  **Run the editor:**
    Execute the `main.py` script to launch the application.
    ```sh
    python main.py
    ```

## How to Use

*   **Opening Files/Folders**: Use the `Open File` or `Open Folder` buttons on the toolbar or the welcome page to start working on your projects. You can also double-click files in the File Explorer.
*   **Running Sn2 Code**:
    1.  Open a `.sn2` file.
    2.  Click the **Run** button (▶️) on the top-right of the toolbar.
    3.  The output of your script will be displayed in the integrated terminal at the bottom.
    > **Note**: You must save your file before you can run it.
*   **Changing Themes**:
    1.  Click the **View** button on the toolbar.
    2.  Navigate to the **Themes** submenu.
    3.  Select your desired theme from the list. The editor's appearance will update instantly.

## Project Structure

The project is organized as follows:

```
sn2-editor/
├── editor/
│   ├── __init__.py
│   ├── main_window.py      # Main application window, UI, and logic
│   ├── syntax_highlighter.py # Logic for Sn2 syntax highlighting
│   ├── themes.py           # Color definitions for all themes
│   ├── update_worker.py    # Background worker for checking updates
│   ├── version.py          # Editor version constant
│   └── widgets.py          # Custom widgets like CodeEditor and Terminal
├── main.py                 # Main entry point to run the application

```

## Contributing

Contributions are welcome! If you have ideas for new features, find a bug, or want to improve the code, feel free to open an issue or submit a pull request.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Commit your changes (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/YourFeature`).
5.  Open a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


This `README.md` provides a great starting point for your project. I've included a placeholder for a screenshot which is highly recommended to showcase your editor. You can take a screenshot and add it to your repository, then update the link.

<!--
[PROMPT_SUGGESTION]The update checker is simple. Can you improve it to handle pre-releases or more complex version strings like '1.2.3-beta'?[/PROMPT_SUGGESTION]
[PROMPT_SUGGESTION]How can I package this PyQt6 application into a standalone executable for Windows, macOS, and Linux using PyInstaller?[/PROMPT_SUGGESTION]
