import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from unittest.mock import patch
from datetime import datetime, date
from analyzers.streaks import analyze_streaks
from tests.conftest import mock_response

BASE_URL = "https://api.github.com"
HEADERS = {"Accept": "application/vnd.github.v3+json"}


def make_commit(date_str):
    return {"commit": {"author": {"date": date_str}}}


def run_streaks(commits, today=date(2024, 3, 20)):
    repos = [{"name": "repo", "fork": False}]
    with patch("analyzers.streaks.requests.get") as mock_get, \
         patch("analyzers.streaks.datetime") as mock_dt:
        mock_get.return_value = mock_response(commits)
        mock_dt.utcnow.return_value.date.return_value = today
        mock_dt.fromisoformat.side_effect = datetime.fromisoformat
        return analyze_streaks("user", repos, BASE_URL, HEADERS)


def test_no_commits_returns_zeros():
    repos = [{"name": "repo", "fork": False}]
    with patch("analyzers.streaks.requests.get") as mock_get:
        mock_get.return_value = mock_response([])
        result = analyze_streaks("user", repos, BASE_URL, HEADERS)
    assert result == {"longest_streak": 0, "current_streak": 0, "total_active_days": 0}


def test_consecutive_days_longest_streak():
    commits = [
        make_commit("2024-03-10T10:00:00Z"),
        make_commit("2024-03-11T10:00:00Z"),
        make_commit("2024-03-12T10:00:00Z"),
        make_commit("2024-03-13T10:00:00Z"),
    ]
    result = run_streaks(commits)
    assert result["longest_streak"] == 4


def test_broken_streak_resets():
    commits = [
        make_commit("2024-03-10T10:00:00Z"),
        make_commit("2024-03-11T10:00:00Z"),
        make_commit("2024-03-14T10:00:00Z"),
        make_commit("2024-03-15T10:00:00Z"),
        make_commit("2024-03-16T10:00:00Z"),
    ]
    result = run_streaks(commits)
    assert result["longest_streak"] == 3


def test_current_streak_counts_up_to_today():
    today = date(2024, 3, 20)
    commits = [
        make_commit("2024-03-18T10:00:00Z"),
        make_commit("2024-03-19T10:00:00Z"),
        make_commit("2024-03-20T10:00:00Z"),
    ]
    result = run_streaks(commits, today=today)
    assert result["current_streak"] == 3


def test_current_streak_zero_when_no_recent_commits():
    commits = [
        make_commit("2024-03-01T10:00:00Z"),
        make_commit("2024-03-02T10:00:00Z"),
    ]
    result = run_streaks(commits, today=date(2024, 3, 20))
    assert result["current_streak"] == 0


def test_total_active_days_deduplicates():
    commits = [
        make_commit("2024-03-10T09:00:00Z"),
        make_commit("2024-03-10T17:00:00Z"),
        make_commit("2024-03-11T10:00:00Z"),
    ]
    result = run_streaks(commits)
    assert result["total_active_days"] == 2


def test_forks_are_skipped():
    repos = [{"name": "forked", "fork": True}]
    with patch("analyzers.streaks.requests.get") as mock_get:
        result = analyze_streaks("user", repos, BASE_URL, HEADERS)
    mock_get.assert_not_called()
    assert result["longest_streak"] == 0


def test_non_200_response_is_skipped():
    repos = [{"name": "repo", "fork": False}]
    with patch("analyzers.streaks.requests.get") as mock_get:
        mock_get.return_value = mock_response([], status=403)
        result = analyze_streaks("user", repos, BASE_URL, HEADERS)
    assert result["longest_streak"] == 0


def test_single_day_streak():
    commits = [make_commit("2024-03-10T10:00:00Z")]
    result = run_streaks(commits)
    assert result["longest_streak"] == 1
    assert result["total_active_days"] == 1
