from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont
from PyQt6.QtCore import QRegularExpression

class Sn2SyntaxHighlighter(QSyntaxHighlighter):
    """
    A syntax highlighter for the Sn2 language.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.highlighting_rules = []

        # Keywords
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setFontWeight(QFont.Weight.Bold)
        keywords = [
            "let", "show", "if", "else", "loop", "in", "while", "func", "class",
            "try", "catch", "return", "this", "super", "import", "as", "match", "case"
        ]
        self.highlighting_rules.extend([(QRegularExpression(f"\\b{keyword}\\b"), self.keyword_format) for keyword in keywords])

        # Literals (true, false, null)
        self.literal_format = QTextCharFormat()
        literals = ["true", "false", "null"]
        self.highlighting_rules.extend([(QRegularExpression(f"\\b{literal}\\b"), self.literal_format) for literal in literals])

        # Strings (double-quoted)
        self.string_format = QTextCharFormat()
        self.highlighting_rules.append((QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), self.string_format))

        # Numbers
        self.number_format = QTextCharFormat()
        self.highlighting_rules.append((QRegularExpression(r'\b[0-9]+\.?[0-9]*\b'), self.number_format))

        # Single-line comments
        self.single_line_comment_format = QTextCharFormat()
        self.highlighting_rules.append((QRegularExpression(r'//[^\n]*'), self.single_line_comment_format))

        # Multi-line comments
        self.multi_line_comment_format = QTextCharFormat()
        self.comment_start_expression = QRegularExpression(r"/\*")
        self.comment_end_expression = QRegularExpression(r"\*/")

    def set_theme(self, theme):
        self.keyword_format.setForeground(theme["keyword"])
        self.literal_format.setForeground(theme["literal"])
        self.string_format.setForeground(theme["string"])
        self.number_format.setForeground(theme["number"])
        self.single_line_comment_format.setForeground(theme["comment"])
        self.multi_line_comment_format.setForeground(theme["comment"])
        self.rehighlight()

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

        # Multi-line comment highlighting
        self.setCurrentBlockState(0)
        start_index = 0
        if self.previousBlockState() != 1:
            start_index = self.comment_start_expression.match(text).capturedStart()

        while start_index >= 0:
            end_index = self.comment_end_expression.match(text, start_index).capturedStart()
            comment_length = 0
            if end_index == -1:
                self.setCurrentBlockState(1)
                comment_length = len(text) - start_index
            else:
                comment_length = end_index - start_index + 2

            self.setFormat(start_index, comment_length, self.multi_line_comment_format)
            start_index = self.comment_start_expression.match(text, start_index + comment_length).capturedStart()