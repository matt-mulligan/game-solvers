"""Module to provide rich reporting for application."""

from rich.console import Console, Group
from rich.panel import Panel


def report_wordle_solutions(
    greens: list[tuple[str, int]],
    yellows: list[tuple[str, list[int]]],
    greys: list[str],
    scored_words: list[tuple[str, int]],
    non_repeating_words: list[tuple[str, int]],
    new_char_words: list[tuple[str, int]],
) -> None:
    """Report wordle solutions to user using rich reporting.

    :param greens:
    :param yellows:
    :param greys:
    :param scored_words:
    :param non_repeating_words:
    :param new_char_words:
    :return:
    """
    console = Console()

    panel_green = Panel(
        "\t".join([f"[green]{letter} = {pos}[/green]" for letter, pos in greens]),
        title="[white]Green Letters[/white]",
        title_align="left",
        border_style="green",
    )
    panel_yellow = Panel(
        "\t".join([f"[yellow]{letter} != {pos}[/yellow]" for letter, pos in yellows]),
        title="[white]Yellow Letters[/white]",
        title_align="left",
        border_style="yellow",
    )
    panel_grey = Panel(
        ", ".join([f"[bright_black]{letter}[/bright_black]" for letter in greys]),
        title="[white]Grey Letters[/white]",
        title_align="left",
        border_style="bright_black",
    )

    panel_answers = Panel(
        Group(
            "Words that:",
            " * Fit the given criteria",
            " * Scored the highest based on letter distributions of all five-letter words",
            "",
            "These are our best guesses based on statistics",
            "",
            *[f"{word} - {score}" for word, score in scored_words],
        ),
        title="[white]Top 10 Answers[/white]",
        title_align="left",
        border_style="dodger_blue2",
    )
    panel_non_repeated = Panel(
        Group(
            "Words that:",
            " * Fit the given criteria",
            " * Scored the highest based on letter distributions of all five-letter words",
            " * [bold]Do not contain any repeated letters[/bold]" "",
            "These are still valid guesses but also allow you to rule out/in more options if they are wrong",
            "",
            *[f"{word} - {score}" for word, score in non_repeating_words],
        ),
        title="[white]Top 10 [bold]Non-Repeating Letter[/bold] Answers[/white]",
        title_align="left",
        border_style="dodger_blue2",
    )
    panel_new_char = Panel(
        Group(
            "Words that:",
            " * [bold]Do not[/bold] Fit the given criteria",
            " * Use only [bold]totally new letters[/bold]"
            " * Scored the highest based on letter distributions of all five-letter words",
            "",
            "These words can be great if you're trying to get as much information as possible from the next turn",
            "",
            *[f"{word} - {score}" for word, score in new_char_words],
        ),
        title="[white]Top 10 [bold]New Letter[/bold] Answers[/white]",
        title_align="left",
        border_style="dodger_blue2",
    )

    panel_wordle = Panel(
        Group(panel_green, panel_yellow, panel_grey, "", panel_answers, "", panel_non_repeated, "", panel_new_char),
        title="[blue]Wordle: Possible Solutions[/blue]",
        border_style="white",
    )

    console.print(panel_wordle)
