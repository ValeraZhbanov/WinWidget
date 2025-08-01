import sqlparse
from sqlparse.tokens import Keyword, Name, Punctuation, Wildcard, Comment
from sqlparse.sql import Identifier, IdentifierList, Parenthesis
from PyQt6.QtCore import QThread, pyqtSignal

class CustomSQLFormatter:
    def __init__(self):
        self.indent = "    "
        self.current_indent = 0
        self.formatted = []
        self.last_token = None
        self.need_newline = False
        self.after_keyword = False

    def format(self, sql):
        parsed = sqlparse.parse(sql)[0]
        self._format_statement(parsed)
        return "\n".join(self.formatted)

    def _format_statement(self, statement):
        for token in statement.tokens:
            self._process_token(token)

    def _process_token(self, token):
        if token.is_whitespace:
            return

        if token.ttype in Comment:
            self._add_comment(token)
            return

        if token.ttype in Keyword:
            self._add_keyword(token)
            return

        if isinstance(token, Parenthesis):
            self._add_parenthesis(token)
            return

        if isinstance(token, IdentifierList):
            self._add_identifier_list(token)
            return

        if isinstance(token, Identifier):
            self._add_identifier(token)
            return

        self._add_other_token(token)

    def _add_keyword(self, token):
        keyword = token.value.upper()
        
        if keyword in ("WITH", "SELECT", "FROM", "WHERE", "JOIN", "GROUP BY", "HAVING", "UNION"):
            if not (self.last_token and self.last_token.value.upper() in ("WITH", "UNION")):
                self._add_newline()
            
        
        self.formatted.append(f"{self.indent * self.current_indent}{keyword}")

        if keyword in ("WITH", "SELECT", "FROM"):
            self.current_indent += 1

        self.last_token = token
        self.after_keyword = True

    def _add_parenthesis(self, token):
        self.formatted.append(f"{self.indent * self.current_indent}(")
        self.current_indent += 1
        self._format_statement(token)
        self.current_indent -= 1
        self.formatted.append(f"{self.indent * self.current_indent})")
        self.last_token = token

    def _add_identifier_list(self, token):
        identifiers = [t for t in token.tokens if not t.is_whitespace]
        for i, ident in enumerate(identifiers):
            if i > 0 and ident.value == ",":
                self.formatted[-1] += ","
                self._add_newline()
            else:
                self._process_token(ident)
        self.last_token = token

    def _add_identifier(self, token):
        ident = token.value
        if self.after_keyword:
            self.formatted[-1] += f" {ident}"
        else:
            self.formatted.append(f"{self.indent * self.current_indent}{ident}")
        self.last_token = token
        self.after_keyword = False

    def _add_comment(self, token):
        comment = token.value.strip()
        if comment.startswith("/*"):
            self._add_newline()
            self.formatted.append(f"{self.indent * self.current_indent}{comment}")
            self._add_newline()
        else:
            self.formatted[-1] += f" {comment}"
        self.last_token = token

    def _add_other_token(self, token):
        if token.value == ",":
            self.formatted[-1] += ","
        else:
            if self.after_keyword:
                self.formatted[-1] += f" {token.value}"
            else:
                self.formatted.append(f"{self.indent * self.current_indent}{token.value}")
        self.last_token = token
        self.after_keyword = False

    def _add_newline(self):
        if self.formatted and self.formatted[-1].strip():
            self.formatted.append("")


class SqlFormatThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        try:
            formatted_sql = CustomSQLFormatter().format(self.text)
            
            self.finished.emit(formatted_sql)
        
        except Exception as e:
            self.error.emit(f"Ошибка при форматировании SQL: {str(e)}")