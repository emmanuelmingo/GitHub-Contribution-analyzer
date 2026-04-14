import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from analyzers.repo import analyze_repo
from tests.conftest import SAMPLE_REPOS


def test_counts_originals_and_forks():
    result = analyze_repo(SAMPLE_REPOS)
    assert result["original_count"] == 3
    assert result["fork_count"] == 1
    assert result["total_repos"] == 4


def test_fork_ratio():
    result = analyze_repo(SAMPLE_REPOS)
    assert result["fork_ratio"] == 25.0


def test_most_starred_order():
    result = analyze_repo(SAMPLE_REPOS)
    stars = [s for _, s in result["most_starred"]]
    assert stars == sorted(stars, reverse=True)


def test_most_starred_top_5():
    repos = [
        {"name": f"repo-{i}", "fork": False, "stargazers_count": i, "pushed_at": "2024-01-01T00:00:00Z"}
        for i in range(10)
    ]
    result = analyze_repo(repos)
    assert len(result["most_starred"]) == 5
    assert result["most_starred"][0] == ("repo-9", 9)


def test_most_active_order():
    result = analyze_repo(SAMPLE_REPOS)
    dates = [d for _, d in result["most_active"]]
    assert dates == sorted(dates, reverse=True)


def test_empty_repos():
    result = analyze_repo([])
    assert result["total_repos"] == 0
    assert result["original_count"] == 0
    assert result["fork_count"] == 0
    assert result["fork_ratio"] == 0
    assert result["most_starred"] == []
    assert result["most_active"] == []


def test_all_forks():
    repos = [
        {"name": "a", "fork": True, "stargazers_count": 0, "pushed_at": "2024-01-01T00:00:00Z"},
        {"name": "b", "fork": True, "stargazers_count": 0, "pushed_at": "2024-01-01T00:00:00Z"},
    ]
    result = analyze_repo(repos)
    assert result["fork_ratio"] == 100.0
    assert result["original_count"] == 0


def test_no_forks():
    repos = [
        {"name": "a", "fork": False, "stargazers_count": 10, "pushed_at": "2024-01-01T00:00:00Z"},
    ]
    result = analyze_repo(repos)
    assert result["fork_ratio"] == 0.0
    assert result["fork_count"] == 0
