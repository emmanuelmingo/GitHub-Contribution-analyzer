# GitHub Contribution Analyzer


A full-stack web app that analyzes any GitHub user's public activity and generates a **Contributor Score** (0–100) across 8 weighted metrics — commit consistency, language diversity, streak length, repo originality, and more.

## What Makes It Different

Most GitHub profile tools count raw stars or total commits. This analyzer applies **logarithmic scaling** to high-volume metrics so outliers don't dominate, rewards **behavioral signals** like weekday spread and consecutive streaks, and derives everything from public data with **no authentication required**.

## Features

- Composite contributor score with 8 independent metrics and a performance tier (Beginner → Expert)
- Interactive score breakdown showing how each metric contributes
- Language distribution donut chart across all public repos
- Weekly commit pattern bar chart (which days you commit most)
- 90-day activity timeline
- Server-side caching — results cached 1 hour to respect API rate limits
- Handles org accounts, empty profiles, and GitHub rate limit errors gracefully

## Prerequisites

- Python 3.10+
- Node.js 18+

## Getting Started

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
BaseURL=https://api.github.com
DEV_FRONTEND_URL=http://localhost:5173
FRONTEND_URL=
```

```bash
python app.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

| Service  | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend  | http://localhost:5000 |

## Running Tests

```bash
cd backend
pytest tests/ -v
```

42 unit tests covering all 5 analyzer modules.

## Project Structure

```
GitHub Contribution Analyzer/
  backend/
    app.py               # Flask app, single API endpoint
    config.py            # Env vars, cache config, CORS
    analyzers/           # scorer, commit_frequency, streaks, language, repo
    tests/
  frontend/
    src/
      App.jsx            # Root component, state, API call
      components/        # ProfileCard, ScoreCard, charts
```

## License

[MIT](LICENSE)

## Author

[Emmanuel Mingo](mailto:mingoemmanuel06@gmail.com)
