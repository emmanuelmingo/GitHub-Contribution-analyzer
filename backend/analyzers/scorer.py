import math

WEIGHTS = {
    "commit_volume":      20,
    "commit_spread":      10,
    "longest_streak":     15,
    "active_days":        10,
    "language_diversity": 20,
    "original_repos":     10,
    "star_count":          5,
    "original_ratio":     10,
}


def _log_scale(value, cap):
    if value <= 0:
        return 0.0
    return min(math.log1p(value) / math.log1p(cap), 1.0)


def _linear_scale(value, cap):
    if value <= 0:
        return 0.0
    return min(value / cap, 1.0)


def calculate_score(frequency, streaks, language, repo_stats):
    breakdown = {}

    total_commits = frequency.get("total_commits", 0)
    breakdown["commit_volume"] = round(
        _log_scale(total_commits, 500) * WEIGHTS["commit_volume"], 2
    )

    by_day = frequency.get("by_day", {})
    unique_days = len(by_day)
    breakdown["commit_spread"] = round(
        _linear_scale(unique_days, 7) * WEIGHTS["commit_spread"], 2
    )

    longest = streaks.get("longest_streak", 0)
    breakdown["longest_streak"] = round(
        _linear_scale(longest, 30) * WEIGHTS["longest_streak"], 2
    )

    active_days = streaks.get("total_active_days", 0)
    breakdown["active_days"] = round(
        _linear_scale(active_days, 100) * WEIGHTS["active_days"], 2
    )

    unique_languages = len(language)
    breakdown["language_diversity"] = round(
        _linear_scale(unique_languages, 5) * WEIGHTS["language_diversity"], 2
    )

    original_count = repo_stats.get("original_count", 0)
    breakdown["original_repos"] = round(
        _linear_scale(original_count, 10) * WEIGHTS["original_repos"], 2
    )

    most_starred = repo_stats.get("most_starred", [])
    total_stars = sum(stars for _, stars in most_starred)
    breakdown["star_count"] = round(
        _log_scale(total_stars, 50) * WEIGHTS["star_count"], 2
    )

    fork_ratio = repo_stats.get("fork_ratio", 0)
    breakdown["original_ratio"] = round(
        ((100 - fork_ratio) / 100) * WEIGHTS["original_ratio"], 2
    )

    overall = round(sum(breakdown.values()), 1)

    return {
        "overall": overall,
        "breakdown": breakdown,
        "weights": WEIGHTS,
    }
