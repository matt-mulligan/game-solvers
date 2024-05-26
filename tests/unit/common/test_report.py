from unittest.mock import Mock, call, patch

from game_solvers.common.report import report_wordle_solutions


@patch("game_solvers.common.report.Group")
@patch("game_solvers.common.report.Panel")
@patch("game_solvers.common.report.Console")
def test_when_report_wordle_solutions_and_no_info_then_correct_calls_made(console_class, panel_class, group_class):
    console = Mock()
    console_class.return_value = console

    panel_green = Mock()
    panel_yellow = Mock()
    panel_grey = Mock()
    panel_answers = Mock()
    panel_non_repeated = Mock()
    panel_new_char = Mock()
    panel_wordle = Mock()
    panel_class.side_effect = [
        panel_green,
        panel_yellow,
        panel_grey,
        panel_answers,
        panel_non_repeated,
        panel_new_char,
        panel_wordle,
    ]

    group_answers = Mock()
    group_non_repeated = Mock()
    group_new_char = Mock()
    group_wordle = Mock()
    group_class.side_effect = [group_answers, group_non_repeated, group_new_char, group_wordle]

    report_wordle_solutions([], [], [], [], [], [])

    console.assert_has_calls([call.print(panel_wordle)])

    panel_class.assert_has_calls(
        [
            call(
                "",
                title="[white]Green Letters[/white]",
                title_align="left",
                border_style="green",
            ),
            call("", title="[white]Yellow Letters[/white]", title_align="left", border_style="yellow"),
            call("", title="[white]Grey Letters[/white]", title_align="left", border_style="bright_black"),
            call(group_answers, title="[white]Top 10 Answers[/white]", title_align="left", border_style="dodger_blue2"),
            call(
                group_non_repeated,
                title="[white]Top 10 [bold]Non-Repeating Letter[/bold] Answers[/white]",
                title_align="left",
                border_style="dodger_blue2",
            ),
            call(
                group_new_char,
                title="[white]Top 10 [bold]New Letter[/bold] Answers[/white]",
                title_align="left",
                border_style="dodger_blue2",
            ),
            call(group_wordle, title="[blue]Wordle: Possible Solutions[/blue]", border_style="white"),
        ]
    )

    group_class.assert_has_calls(
        [
            call(
                "Words that:",
                " * Fit the given criteria",
                " * Scored the highest based on letter distributions of all five-letter words",
                "",
                "These are our best guesses based on statistics",
                "",
            ),
            call(
                "Words that:",
                " * Fit the given criteria",
                " * Scored the highest based on letter distributions of all five-letter words",
                " * [bold]Do not contain any repeated letters[/bold]" "",
                "These are still valid guesses but also allow you to rule out/in more options if they are wrong",
                "",
            ),
            call(
                "Words that:",
                " * [bold]Do not[/bold] Fit the given criteria",
                " * Use only [bold]totally new letters[/bold]"
                " * Scored the highest based on letter distributions of all five-letter words",
                "",
                "These words can be great if you're trying to get as much information as possible from the next turn",
                "",
            ),
            call(panel_green, panel_yellow, panel_grey, "", panel_answers, "", panel_non_repeated, "", panel_new_char),
        ]
    )


@patch("game_solvers.common.report.Group")
@patch("game_solvers.common.report.Panel")
@patch("game_solvers.common.report.Console")
def test_when_report_wordle_solutions_and_all_info_then_correct_calls_made(console_class, panel_class, group_class):
    console = Mock()
    console_class.return_value = console

    panel_green = Mock()
    panel_yellow = Mock()
    panel_grey = Mock()
    panel_answers = Mock()
    panel_non_repeated = Mock()
    panel_new_char = Mock()
    panel_wordle = Mock()
    panel_class.side_effect = [
        panel_green,
        panel_yellow,
        panel_grey,
        panel_answers,
        panel_non_repeated,
        panel_new_char,
        panel_wordle,
    ]

    group_answers = Mock()
    group_non_repeated = Mock()
    group_new_char = Mock()
    group_wordle = Mock()
    group_class.side_effect = [group_answers, group_non_repeated, group_new_char, group_wordle]

    report_wordle_solutions(
        [("B", 1), ("R", 3)],
        [("D", [2, 5]), ("S", [1])],
        ["Z", "V", "Q", "N"],
        [("BARDS", 24977), ("BIRDS", 21651)],
        [("BARDS", 24977), ("BIRDS", 21651)],
        [("ATELO", 29850), ("LAETI", 29698)],
    )

    console.assert_has_calls([call.print(panel_wordle)])

    panel_class.assert_has_calls(
        [
            call(
                "[green]B = 1[/green]\t[green]R = 3[/green]",
                title="[white]Green Letters[/white]",
                title_align="left",
                border_style="green",
            ),
            call(
                "[yellow]D != [2, 5][/yellow]\t[yellow]S != [1][/yellow]",
                title="[white]Yellow Letters[/white]",
                title_align="left",
                border_style="yellow",
            ),
            call(
                "[bright_black]Z[/bright_black], [bright_black]V[/bright_black], [bright_black]Q[/bright_black], [bright_black]N[/bright_black]",
                title="[white]Grey Letters[/white]",
                title_align="left",
                border_style="bright_black",
            ),
            call(group_answers, title="[white]Top 10 Answers[/white]", title_align="left", border_style="dodger_blue2"),
            call(
                group_non_repeated,
                title="[white]Top 10 [bold]Non-Repeating Letter[/bold] Answers[/white]",
                title_align="left",
                border_style="dodger_blue2",
            ),
            call(
                group_new_char,
                title="[white]Top 10 [bold]New Letter[/bold] Answers[/white]",
                title_align="left",
                border_style="dodger_blue2",
            ),
            call(group_wordle, title="[blue]Wordle: Possible Solutions[/blue]", border_style="white"),
        ]
    )

    group_class.assert_has_calls(
        [
            call(
                "Words that:",
                " * Fit the given criteria",
                " * Scored the highest based on letter distributions of all five-letter words",
                "",
                "These are our best guesses based on statistics",
                "",
                "BARDS - 24977",
                "BIRDS - 21651",
            ),
            call(
                "Words that:",
                " * Fit the given criteria",
                " * Scored the highest based on letter distributions of all five-letter words",
                " * [bold]Do not contain any repeated letters[/bold]" "",
                "These are still valid guesses but also allow you to rule out/in more options if they are wrong",
                "",
                "BARDS - 24977",
                "BIRDS - 21651",
            ),
            call(
                "Words that:",
                " * [bold]Do not[/bold] Fit the given criteria",
                " * Use only [bold]totally new letters[/bold]"
                " * Scored the highest based on letter distributions of all five-letter words",
                "",
                "These words can be great if you're trying to get as much information as possible from the next turn",
                "",
                "ATELO - 29850",
                "LAETI - 29698",
            ),
            call(panel_green, panel_yellow, panel_grey, "", panel_answers, "", panel_non_repeated, "", panel_new_char),
        ]
    )
