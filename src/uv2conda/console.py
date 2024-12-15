from rich.console import Console
from rich.syntax import Syntax


def print_syntax(text: str, language: str = "yaml"):
    console = Console()
    syntax = Syntax(text, language, background_color="default")
    console.print(syntax)
