#!/usr/bin/env python

""" Command Line Interface functions """

from enum import Enum, IntEnum
from pathlib import Path
from sys import argv, exit, stdout
from typing import Any, Callable, Optional

import click
import typer
import icecream


def bell():
    """TODO"""
    stdout.write("\a")
    stdout.flush()


def rub_out(n=1):
    """TODO"""
    spaces = " " * n
    backspaces = "\b" * n
    click.echo(backspaces + spaces + backspaces, nl=False)


def typer_run(
    function: Callable[..., Any],
    use_stem: bool = False,  # use the stem of argv[0] for help
) -> None:
    """
    Call a typer.command without add_completion.
    This will remove the install-completion and show-completion flags
    """
    prog_name = Path(argv[0]).stem if use_stem else None

    app = typer.Typer(add_completion=False)
    command = app.command()
    command(function)
    app(prog_name=prog_name)


def arguments() -> bool:
    """Returns whether there are any command line arguments"""
    return len(argv) > 1


def show_help(function: Callable[..., Any]) -> Any:
    """
     Display help message

    run(f"{argv[0]} --help", confirm=False)
    """
    from typer.testing import CliRunner

    app = typer.Typer(add_completion=False)
    command = app.command()
    command(function)

    result = CliRunner().invoke(app, ["--help"])
    print(result.stdout)


class Color(str, Enum):  # StrEnum
    """TODO"""

    BLACK = "black"
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    MAGENTA = "magenta"
    CYAN = "cyan"
    WHITE = "white"


class Style:
    """TODO"""

    def __init__(
        self,
        fg=None,
        bg=None,
        bold=None,
        dim=None,
        underline=None,
        blink=None,
        reverse=None,
        reset=True,
    ):
        self._style = dict(
            fg=fg,
            bg=bg,
            bold=bold,
            dim=dim,
            underline=underline,
            blink=blink,
            reverse=reverse,
            reset=reset,
        )

    def __call__(self, text, **kw):
        """Convenience shortcut for echo"""
        self.echo(text, **kw)

    def style(self, text: str):
        """TODO"""
        return click.style(text, **self._style)

    def echo(self, text: str = "", **kw) -> None:
        """TODO"""
        click.echo(self.style(text), **kw)

    def prompt(self, text: str = "", **kw) -> Any:
        """TODO"""
        return click.prompt(self.style(text), **kw)

    def confirm(self, text: str = "", **kw) -> str:
        """TODO"""
        return click.confirm(self.style(text), **kw)

    def pause(self, text: str = "", **kw) -> str:
        """TODO"""
        return click.pause(self.style(text), **kw)

    def keystroke(self, text: str, options, default=None) -> str:
        """TODO"""
        return keystroke(self, text, options, default)

    def error(self, text: str = "", exit_code=1, **kw) -> None:
        """TODO"""
        click.echo(self.style(text), **kw)
        exit(exit_code)


class Styles:
    """Default Styles"""

    prompt = Style(fg=Color.CYAN, bg=Color.BLACK, bold=True)
    error = Style(fg=Color.RED, bg=Color.BLACK, bold=True)
    output = Style(fg=Color.WHITE)
    option = Style(fg=Color.WHITE)


class Key(IntEnum):
    """TODO"""

    # vi
    BACKSPACE_2 = 8
    ENTER_2 = 10
    # TAB_2 = 9
    # ESCAPE_2 = 27

    # bash
    BACKSPACE = 127
    ENTER = 13
    CTRL_C = 3
    ESC = 27  # 10
    TAB = 9

    U_ARROW = 97  # (72, 117, 65)
    D_ARROW = 98  # (80, 100, 66)
    R_ARROW = 99  # (77, 114, 67)
    L_ARROW = 100  # (75, 108, 68)


def keystroke(style, text, options, default=None):
    """TODO"""
    while True:
        style(f"{text}: ", nl=False)
        c = click.getchar().lower()
        style("")

        if c in options:
            return c
        if default and ord(c) in (Key.ENTER, Key.ENTER_2):
            return default


def select(
    options,  # TODO: :stringable?
    title: str = "",
    prompt: str = "Select",
    prompt_style: Style = None,
    output_style: Style = None,
) -> Optional[int]:
    """CLI Select from a list of options - similar to bullet"""

    if not options:
        return None

    prompt_style = prompt_style or Styles.prompt
    output_style = output_style or Styles.output

    if title:
        output_style(title)

    for index, option in enumerate(options):
        prompt_style(f"{index+1:3}: ", nl=False)
        output_style(str(option))

    while True:
        selected = prompt_style.prompt(prompt, type=int)

        if selected == 0:
            return None
        if 0 < selected <= len(options):
            return selected - 1
        output_style(f"Error: {selected} is out of range")


def select_demo():
    """Demonstrate select"""

    options = (
        "First shalt thou take out the Holy Pin.",
        "Then, shalt thou count to three. No more.  No less."
        "Three shalt be the number thou shalt count, and the number of the counting shall be three.",
        "Four shalt thou not count, nor either count thou two, excepting that thou then proceed to three.",
        "Five is right out.",
        "Once the number three, being the third number, be reached,",
        "then, lobbest thou thy Holy Hand Grenade of Antioch towards thy foe,",
        "who, being naughty in My sight, shall snuff it.",
    )

    index = select(options)
    if index is not None:
        print(options[index])


def demo():
    """
    Demonstrate command line interface provided by click
    """
    click.clear()

    # Automatically remove all ANSI styles if data is piped into a file.
    for color in Color:
        bcolor = f"bright_{color}"
        click.secho(f"{color:7} ", fg=color, nl=False)
        click.secho(f"{color:7} ", fg=bcolor, nl=False)
        click.secho("reverse", fg=color, reverse=True, nl=False)
        click.secho("reverse", fg=bcolor, reverse=True, nl=False)
        click.secho("")
    click.secho("")

    click.secho("Bold", bold=True)
    click.secho("Blinking", blink=True)
    click.secho("Underlined", underline=True)
    click.secho("Printed to stderr", err=True)
    Style(fg=Color.RED, bg=Color.YELLOW).echo("Styled\n")

    prompt_style = Styles.prompt
    output_style = Styles.output

    text = "Press any key to continue."
    prompt_style.pause(text)
    bell()
    click.clear()

    text = "Please enter a valid integer"
    value = prompt_style.prompt(text, type=int)
    output_style(f"{value}\n")

    text = "Value for pi"
    value = prompt_style.prompt(text, default=3.14)
    output_style(f"{value}\n")

    text = "Tap a number from 1 to 7"
    c = prompt_style.keystroke(text, "1234567")
    output_style(f"{c}\n")

    text = "Do you want to stop?"
    c = prompt_style.confirm(text)
    output_style("I will stop!" if c else "I will not stop!\n")

    select_demo()


if __name__ == "__main__":
    typer_run(demo)
