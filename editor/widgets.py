from PyQt6.QtWidgets import QTextEdit, QCompleter
from PyQt6.QtGui import QFont, QTextCursor
from PyQt6.QtCore import Qt, QStringListModel

from .syntax_highlighter import Sn2SyntaxHighlighter

class CodeEditor(QTextEdit):
    """
    Custom QTextEdit with syntax highlighting and code completion.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighter = Sn2SyntaxHighlighter(self.document())

        # Basic styling
        font = QFont("Courier New", 11)
        self.setFont(font)

        # Setup completer
        self.completer = QCompleter(self)
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        
        keywords = [
            "let", "show", "if", "else", "loop", "in", "while", "func", "class",
            "try", "catch", "return", "this", "super", "import", "as", "match", "case",
            "true", "false", "null", "input", "len", "iter", "next", "toInt", "toFloat", "toString"
        ]
        model = QStringListModel(keywords, self.completer)
        self.completer.setModel(model)
        self.completer.activated.connect(self.insert_completion)

    def set_theme(self, theme):
        palette = self.palette()
        palette.setColor(palette.ColorRole.Base, theme["base"])
        palette.setColor(palette.ColorRole.Text, theme["text"])
        self.setPalette(palette)
        self.highlighter.set_theme(theme)

    def text_under_cursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.SelectionType.WordUnderCursor)
        return tc.selectedText()

    def insert_completion(self, completion):
        tc = self.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        tc.movePosition(QTextCursor.MoveOperation.Left)
        tc.movePosition(QTextCursor.MoveOperation.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    def keyPressEvent(self, event):
        """
        Overrides the key press event to handle auto-completion.
        """
        if self.completer.popup().isVisible():
            if event.key() in [Qt.Key.Key_Enter, Qt.Key.Key_Return, Qt.Key.Key_Escape, Qt.Key.Key_Tab, Qt.Key.Key_Backtab]:
                event.ignore()
                return

        super().keyPressEvent(event)

        completion_prefix = self.text_under_cursor()

        is_modifier = event.modifiers() in [Qt.KeyboardModifier.ControlModifier, Qt.KeyboardModifier.ShiftModifier, Qt.KeyboardModifier.AltModifier]
        word_separators = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="

        if (
            len(completion_prefix) < 1 or
            (is_modifier and not event.text()) or
            (event.text() and event.text()[-1] in word_separators)
        ):
            self.completer.popup().hide()
            return

        if completion_prefix != self.completer.completionPrefix():
            self.completer.setCompletionPrefix(completion_prefix)
            self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0))

        cursor_rect = self.cursorRect()
        cursor_rect.setWidth(self.completer.popup().sizeHintForColumn(0) + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cursor_rect)

class TerminalWidget(QTextEdit):
    """
    A custom QTextEdit that acts as a writable terminal, sending input
    to a running QProcess.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.process = None
        self.prompt_pos = 0

        self.setFont(QFont("Consolas", 10))

    def set_theme(self, theme):
        palette = self.palette()
        palette.setColor(palette.ColorRole.Base, theme["base"])
        palette.setColor(palette.ColorRole.Text, theme["text"])
        self.setPalette(palette)

    def set_process(self, process):
        self.process = process

    def keyPressEvent(self, event):
        cursor = self.textCursor()

        if cursor.position() < self.prompt_pos:
            cursor.setPosition(self.prompt_pos)
            self.setTextCursor(cursor)

        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.setTextCursor(cursor)
            text = self.toPlainText()[self.prompt_pos:]
            
            if self.process:
                self.process.write(f"{text}\n".encode())

            self.append("")
            self.prompt_pos = self.textCursor().position()
            return

        super().keyPressEvent(event)

    def append_output(self, text):
        self.insertPlainText(text)
        self.moveCursor(QTextCursor.MoveOperation.End)
        self.prompt_pos = self.textCursor().position()