from unittest.mock import MagicMock


def make_commit(date_str):
    return {"commit": {"author": {"date": date_str}}}


def mock_response(data, status=200):
    m = MagicMock()
    m.status_code = status
    m.json.return_value = data
    return m


SAMPLE_REPOS = [
    {
        "name": "project-alpha",
        "language": "Python",
        "fork": False,
        "stargazers_count": 40,
        "pushed_at": "2024-03-10T00:00:00Z",
    },
    {
        "name": "project-beta",
        "language": "JavaScript",
        "fork": False,
        "stargazers_count": 15,
        "pushed_at": "2024-02-20T00:00:00Z",
    },
    {
        "name": "project-gamma",
        "language": "Python",
        "fork": False,
        "stargazers_count": 5,
        "pushed_at": "2024-01-05T00:00:00Z",
    },
    {
        "name": "forked-lib",
        "language": "Go",
        "fork": True,
        "stargazers_count": 0,
        "pushed_at": "2023-12-01T00:00:00Z",
    },
]

SAMPLE_COMMITS = [
    make_commit("2024-03-11T09:00:00Z"),
    make_commit("2024-03-11T14:00:00Z"),
    make_commit("2024-03-12T10:00:00Z"),
    make_commit("2024-03-13T08:00:00Z"),
]
