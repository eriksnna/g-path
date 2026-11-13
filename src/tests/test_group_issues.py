from core.lexer import ERROR, WARNING, Issue, group_issues


def test_identical_issues_are_grouped_in_first_seen_order():
    a = Issue(33, ERROR, "fora da área")
    b = Issue(16, ERROR, "fora da área")
    assert group_issues([a, b, a, a]) == [(a, 3), (b, 1)]


def test_different_message_or_severity_is_not_grouped():
    issues = [Issue(5, ERROR, "x"), Issue(5, WARNING, "x"), Issue(5, ERROR, "y")]
    assert [count for _, count in group_issues(issues)] == [1, 1, 1]


def test_empty_list():
    assert group_issues([]) == []