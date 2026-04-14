import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from analyzers.language import analyze_language


def test_percentage_distribution():
    repos = [
        {"language": "Python"},
        {"language": "Python"},
        {"language": "JavaScript"},
    ]
    result = analyze_language(repos)
    langs = dict(result)
    assert langs["Python"] == round(200 / 3, 2)
    assert langs["JavaScript"] == round(100 / 3, 2)


def test_sorted_descending():
    repos = [
        {"language": "Go"},
        {"language": "Python"},
        {"language": "Python"},
    ]
    result = analyze_language(repos)
    percentages = [pct for _, pct in result]
    assert percentages == sorted(percentages, reverse=True)


def test_percentages_sum_to_100():
    repos = [
        {"language": "Python"},
        {"language": "JavaScript"},
        {"language": "Go"},
        {"language": "Rust"},
    ]
    result = analyze_language(repos)
    total = sum(pct for _, pct in result)
    assert abs(total - 100.0) < 0.1


def test_repos_without_language_are_ignored():
    repos = [
        {"language": "Python"},
        {"language": None},
        {},
    ]
    result = analyze_language(repos)
    langs = [name for name, _ in result]
    assert langs == ["Python"]


def test_empty_repos_returns_empty():
    assert analyze_language([]) == []


def test_all_none_language_returns_empty():
    repos = [{"language": None}, {"language": None}]
    assert analyze_language(repos) == []


def test_single_language_is_100_percent():
    repos = [{"language": "Python"}, {"language": "Python"}]
    result = analyze_language(repos)
    assert result == [("Python", 100.0)]
