import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from analyzers.scorer import calculate_score, WEIGHTS


EMPTY_FREQUENCY = {"total_commits": 0, "by_day": {}}
EMPTY_STREAKS = {"longest_streak": 0, "total_active_days": 0}
EMPTY_LANGUAGE = []
EMPTY_REPO_STATS = {"original_count": 0, "fork_ratio": 0, "most_starred": []}

FULL_FREQUENCY = {"total_commits": 500, "by_day": {d: 1 for d in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]}}
FULL_STREAKS = {"longest_streak": 30, "total_active_days": 100}
FULL_LANGUAGE = [("Python", 50), ("JavaScript", 30), ("Go", 10), ("Rust", 5), ("C", 5)]
FULL_REPO_STATS = {"original_count": 10, "fork_ratio": 0, "most_starred": [("repo", 50)]}


def test_zero_activity_only_scores_original_ratio():
    result = calculate_score(EMPTY_FREQUENCY, EMPTY_STREAKS, EMPTY_LANGUAGE, EMPTY_REPO_STATS)
    assert result["overall"] == WEIGHTS["original_ratio"]
    assert result["breakdown"]["original_ratio"] == WEIGHTS["original_ratio"]
    assert result["breakdown"]["commit_volume"] == 0.0
    assert result["breakdown"]["longest_streak"] == 0.0


def test_full_inputs_give_maximum_score():
    result = calculate_score(FULL_FREQUENCY, FULL_STREAKS, FULL_LANGUAGE, FULL_REPO_STATS)
    assert result["overall"] == 100.0


def test_overall_is_sum_of_breakdown():
    result = calculate_score(FULL_FREQUENCY, FULL_STREAKS, FULL_LANGUAGE, FULL_REPO_STATS)
    assert abs(result["overall"] - sum(result["breakdown"].values())) < 0.1


def test_score_never_exceeds_100():
    overloaded_frequency = {"total_commits": 99999, "by_day": {d: 1 for d in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]}}
    overloaded_streaks = {"longest_streak": 9999, "total_active_days": 9999}
    overloaded_repos = {"original_count": 9999, "fork_ratio": 0, "most_starred": [("repo", 9999)]}
    overloaded_language = [(f"lang-{i}", 1) for i in range(100)]
    result = calculate_score(overloaded_frequency, overloaded_streaks, overloaded_language, overloaded_repos)
    assert result["overall"] <= 100.0


def test_weights_sum_to_100():
    assert sum(WEIGHTS.values()) == 100


def test_breakdown_keys_match_weights():
    result = calculate_score(EMPTY_FREQUENCY, EMPTY_STREAKS, EMPTY_LANGUAGE, EMPTY_REPO_STATS)
    assert set(result["breakdown"].keys()) == set(WEIGHTS.keys())


def test_breakdown_values_within_weight_bounds():
    result = calculate_score(FULL_FREQUENCY, FULL_STREAKS, FULL_LANGUAGE, FULL_REPO_STATS)
    for key, value in result["breakdown"].items():
        assert 0 <= value <= WEIGHTS[key], f"{key}: {value} exceeds max {WEIGHTS[key]}"


def test_fork_ratio_100_zeroes_original_ratio():
    repo_stats = {"original_count": 5, "fork_ratio": 100, "most_starred": []}
    result = calculate_score(EMPTY_FREQUENCY, EMPTY_STREAKS, EMPTY_LANGUAGE, repo_stats)
    assert result["breakdown"]["original_ratio"] == 0.0


def test_no_forks_gives_full_original_ratio():
    repo_stats = {"original_count": 0, "fork_ratio": 0, "most_starred": []}
    result = calculate_score(EMPTY_FREQUENCY, EMPTY_STREAKS, EMPTY_LANGUAGE, repo_stats)
    assert result["breakdown"]["original_ratio"] == WEIGHTS["original_ratio"]


def test_partial_score_is_between_zero_and_100():
    frequency = {"total_commits": 50, "by_day": {"Monday": 5, "Wednesday": 3}}
    streaks = {"longest_streak": 7, "total_active_days": 20}
    language = [("Python", 70), ("JavaScript", 30)]
    repo_stats = {"original_count": 3, "fork_ratio": 30, "most_starred": [("repo", 10)]}
    result = calculate_score(frequency, streaks, language, repo_stats)
    assert 0 < result["overall"] < 100
