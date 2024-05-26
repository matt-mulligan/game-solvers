import re
from unittest.mock import Mock, call, patch

from game_solvers.cli import WordleCLI
from pytest import fixture, mark, raises


class TestWordleCLI:
    """Test class for WordleSolver CLI."""

    @fixture
    def wordle_cli(self):
        return WordleCLI

    @mark.parametrize(
        "input_value,expected",
        [
            (None, []),
            ("a1", [("A", 1)]),
            ("B4,i2", [("B", 4), ("I", 2)]),
            ("G2,H4,S1,d3", [("G", 2), ("H", 4), ("S", 1), ("D", 3)]),
        ],
    )
    def test_when_parse_green_then_correct_values_returned(self, wordle_cli, input_value, expected):
        actual = wordle_cli.parse_green(input_value)
        assert actual == expected

    def test_when_parse_green_and_value_too_long_then_raise_error(self, wordle_cli):
        err_msg = re.escape(
            "Each input for green letters must a letter followed by a number from 1-5. " "Input a12 is invalid"
        )

        with raises(ValueError, match=err_msg):
            wordle_cli.parse_green("a12")

    def test_when_parse_green_and_first_char_not_letter_then_raise_error(self, wordle_cli):
        err_msg = re.escape(
            "Each input for green letters must a letter followed by a number from 1-5. " "Input 4V is invalid"
        )

        with raises(ValueError, match=err_msg):
            wordle_cli.parse_green("4V")

    @mark.parametrize("input_value", ["AD", "r7", "D0", "t^"])
    def test_when_parse_green_and_second_char_not_valid_digit_then_raise_error(self, wordle_cli, input_value):
        err_msg = re.escape(
            "Each input for green letters must a letter followed by a number from 1-5. "
            f"Input {input_value} is invalid"
        )

        with raises(ValueError, match=err_msg):
            wordle_cli.parse_green(input_value)

    @mark.parametrize(
        "input_value,expected",
        [
            (None, []),
            ("s4", [("S", [4])]),
            ("H2351", [("H", [2, 3, 5, 1])]),
            ("n13,s5,g412", [("N", [1, 3]), ("S", [5]), ("G", [4, 1, 2])]),
        ],
    )
    def test_when_parse_yellow_then_correct_values_returned(self, wordle_cli, input_value, expected):
        actual = wordle_cli.parse_yellow(input_value)
        assert actual == expected

    @mark.parametrize("input_value", ["H", "D12345"])
    def test_when_parse_yellow_and_input_wrong_size_then_raise_error(self, wordle_cli, input_value):
        err_msg = re.escape(
            f"Each input for yellow letters must a letter followed by one to four numbers from 1-5. "
            f"Input {input_value} is invalid."
        )

        with raises(ValueError, match=err_msg):
            wordle_cli.parse_yellow(input_value)

    def test_when_parse_yellow_and_char_one_not_letter_then_raise_error(self, wordle_cli):
        err_msg = re.escape(
            "Each input for yellow letters must a letter followed by one to four numbers from 1-5. "
            "Input 4k is invalid."
        )

        with raises(ValueError, match=err_msg):
            wordle_cli.parse_yellow("4k")

    @mark.parametrize("input_value", ["d0", "s6", "j!", "v3*4", "Y3N4"])
    def test_when_parse_yellow_and_char_two_onwards_not_wordle_digit_then_raise_error(self, wordle_cli, input_value):
        err_msg = re.escape(
            f"Each input for yellow letters must a letter followed by one to four numbers from 1-5. "
            f"Input {input_value} is invalid."
        )

        with raises(ValueError, match=err_msg):
            wordle_cli.parse_yellow(input_value)

    @mark.parametrize(
        "input_value,expected",
        [
            (None, []),
            ("s", ["S"]),
            ("v,e", ["V", "E"]),
            (
                "f,t,w,c,s,q,g,e,b,u,i,o,p",
                ["F", "T", "W", "C", "S", "Q", "G", "E", "B", "U", "I", "O", "P"],
            ),
        ],
    )
    def test_when_parse_grey_then_correct_values_returned(self, wordle_cli, input_value, expected):
        actual = wordle_cli.parse_grey(input_value)
        assert actual == expected

    def test_when_parse_grey_and_too_long_then_raise_error(self, wordle_cli):
        err_msg = re.escape("Each input for grey letters must a single letter. Input ge is invalid.")

        with raises(ValueError, match=err_msg):
            wordle_cli.parse_grey("ge")

    def test_when_parse_grey_and_not_letter_then_raise_error(self, wordle_cli):
        err_msg = re.escape("Each input for grey letters must a single letter. Input 4 is invalid.")

        with raises(ValueError, match=err_msg):
            wordle_cli.parse_grey("4")

    def test_when_solutions_then_correct_calls_made(self, wordle_cli):
        opts = Mock(
            green_letters="a4",
            yellow_letters="b123",
            grey_letters="g,f,q",
        )

        wordle_cli.parse_green = Mock(return_value=[("A", 4)])
        wordle_cli.parse_yellow = Mock(return_value=[("B", [1, 2, 3])])
        wordle_cli.parse_grey = Mock(return_value=["G", "F", "Q"])

        with patch("game_solvers.cli.WordleSolver") as wordle_solver:
            wordle_cli.solutions(opts)

        wordle_cli.parse_green.assert_called_once_with("a4")
        wordle_cli.parse_yellow.assert_called_once_with("b123")
        wordle_cli.parse_grey.assert_called_once_with("g,f,q")

        wordle_solver.assert_has_calls(
            [
                call([("A", 4)], [("B", [1, 2, 3])], ["G", "F", "Q"]),
                call().solutions(),
            ]
        )
