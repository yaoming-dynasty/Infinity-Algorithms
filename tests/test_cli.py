import pytest

from infinity_algorithms_cli import main


def test_reason_command_reports_success(capsys):
    assert main(["reason"]) == 0
    output = capsys.readouterr().out
    assert "Success: True" in output
    assert "cleave_bond_3_4" in output


def test_reason_command_fails_when_depth_is_too_small(capsys):
    assert main(["reason", "--max-depth", "0"]) == 1
    assert "Success: False" in capsys.readouterr().out


def test_negative_depth_is_rejected():
    with pytest.raises(SystemExit, match="non-negative"):
        main(["reason", "--max-depth", "-1"])
