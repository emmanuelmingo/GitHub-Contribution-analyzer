
def analyze_repo(repos):
    originals = [r for r in repos if not r.get('fork')]
    forks = [r for r in repos if r.get('fork')]

    most_starred = sorted(originals, key=lambda r: r.get('stargazers_count', 0), reverse=True)[:5]
    most_active = sorted(repos, key=lambda r: r.get('pushed_at', ''), reverse=True)[:5]

    return {
        "total_repos": len(repos),
        "original_count": len(originals),
        "fork_count": len(forks),
        "fork_ratio": round(len(forks) / len(repos) * 100, 2) if repos else 0,
        "most_starred": [(r['name'], r.get('stargazers_count', 0)) for r in most_starred],
        "most_active": [(r['name'], r.get('pushed_at')) for r in most_active]
    }