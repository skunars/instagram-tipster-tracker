from src.parser import parse_odds, parse_prediction_line


def test_parse_odds():
    assert parse_odds("Team A 2.15") == 2.15
    assert parse_odds("2,40") == 2.4


def test_prediction_line():
    parsed = parse_prediction_line("Team A - Team B")
    assert parsed is not None
    assert parsed.event == "Team A"
    assert parsed.selection == "Team B"
