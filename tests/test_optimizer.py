from documark.optimizer import optimize


def test_optimizer_strips_trailing_spaces():
    result = optimize("# Title   \n\nBody   ")
    assert "   \n" not in result


def test_optimizer_collapses_blank_lines():
    result = optimize("Para 1\n\n\n\nPara 2")
    assert "\n\n\n" not in result


def test_optimizer_fixes_heading_spacing():
    result = optimize("##Bad heading")
    assert "## Bad heading" in result


def test_optimizer_ends_with_newline():
    result = optimize("Some text")
    assert result.endswith("\n")
