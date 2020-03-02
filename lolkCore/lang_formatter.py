from lolkCore.lang_settings import LangSettings


class LangFormatter():
    """Format code and check for stuff."""

    def __init__(self):
        """Initiate all variables."""
        self.settings = LangSettings()
    
    def indented(self, code_line):
        """Check if given line is indented."""
        # Return True if the specified tabs are there.
        count_tabspaces = len(code_line) - len(code_line.lstrip())
        if count_tabspaces >= self.settings.tabspaces:
            return (True, count_tabspaces)
        
        # Else; return False.
        return (False, count_tabspaces)

    def format_code(self, code_line):
        """Format all code."""
        # Add ignore sign to indented function code.
        if self.indented(code_line)[0]:
            code_line = self.settings.in_function + code_line
        
        return code_line