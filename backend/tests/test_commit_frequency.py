import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from unittest.mock import patch
from analyzers.commit_frequency import analyze_commit_frequency
from tests.conftest import SAMPLE_REPOS, SAMPLE_COMMITS, mock_response

BASE_URL = "https://api.github.com"
HEADERS = {"Accept": "application/vnd.github.v3+json"}


def test_counts_total_commits():
    with patch("analyzers.commit_frequency.requests.get") as mock_get:
        mock_get.return_value = mock_response(SAMPLE_COMMITS)
        result = analyze_commit_frequency("user", SAMPLE_REPOS, BASE_URL, HEADERS)
    original_repos = [r for r in SAMPLE_REPOS if not r.get("fork")]
    assert result["total_commits"] == len(SAMPLE_COMMITS) * len(original_repos)


def test_forks_are_skipped():
    fork_only = [{"name": "forked", "fork": True}]
    with patch("analyzers.commit_frequency.requests.get") as mock_get:
        result = analyze_commit_frequency("user", fork_only, BASE_URL, HEADERS)
    mock_get.assert_not_called()
    assert result["total_commits"] == 0


def test_non_200_response_is_skipped():
    repos = [{"name": "project-alpha", "fork": False}]
    with patch("analyzers.commit_frequency.requests.get") as mock_get:
        mock_get.return_value = mock_response([], status=403)
        result = analyze_commit_frequency("user", repos, BASE_URL, HEADERS)
    assert result["total_commits"] == 0


def test_by_day_contains_correct_days():
    commits = [
        {"commit": {"author": {"date": "2024-03-11T10:00:00Z"}}},
        {"commit": {"author": {"date": "2024-03-12T10:00:00Z"}}},
    ]
    repos = [{"name": "repo", "fork": False}]
    with patch("analyzers.commit_frequency.requests.get") as mock_get:
        mock_get.return_value = mock_response(commits)
        result = analyze_commit_frequency("user", repos, BASE_URL, HEADERS)
    assert "Monday" in result["by_day"]
    assert "Tuesday" in result["by_day"]


def test_by_date_keys_are_iso_format():
    repos = [{"name": "repo", "fork": False}]
    with patch("analyzers.commit_frequency.requests.get") as mock_get:
        mock_get.return_value = mock_response(SAMPLE_COMMITS)
        result = analyze_commit_frequency("user", repos, BASE_URL, HEADERS)
    for key in result["by_date"].keys():
        assert len(key) == 10
        assert key[4] == "-" and key[7] == "-"


def test_most_active_day_is_highest_count():
    commits = [
        {"commit": {"author": {"date": "2024-03-11T10:00:00Z"}}},
        {"commit": {"author": {"date": "2024-03-11T14:00:00Z"}}},
        {"commit": {"author": {"date": "2024-03-12T10:00:00Z"}}},
    ]
    repos = [{"name": "repo", "fork": False}]
    with patch("analyzers.commit_frequency.requests.get") as mock_get:
        mock_get.return_value = mock_response(commits)
        result = analyze_commit_frequency("user", repos, BASE_URL, HEADERS)
    assert result["most_active_day"] == "Monday"


def test_empty_repos_returns_zeroes():
    result = analyze_commit_frequency("user", [], BASE_URL, HEADERS)
    assert result["total_commits"] == 0
    assert result["by_day"] == {}
    assert result["most_active_day"] is None
    assert result["most_active_hour"] is None


def test_commits_with_missing_date_are_skipped():
    commits = [
        {"commit": {"author": {"date": ""}}},
        {"commit": {"author": {}}},
        {"commit": {}},
    ]
    repos = [{"name": "repo", "fork": False}]
    with patch("analyzers.commit_frequency.requests.get") as mock_get:
        mock_get.return_value = mock_response(commits)
        result = analyze_commit_frequency("user", repos, BASE_URL, HEADERS)
    assert result["total_commits"] == 0
