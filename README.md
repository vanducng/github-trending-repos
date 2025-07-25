# GitHub Trending Repos

A Python application that fetches the top trending GitHub repositories daily and sends a beautifully formatted summary email using Resend. Perfect for staying up-to-date with the latest developments in the open-source community.

## Features

- 📈 Fetches top 10 trending repositories from GitHub daily
- 📧 Sends formatted HTML and text email summaries
- 🤖 Automated daily scheduling via GitHub Actions (7 AM GMT+7)
- 🔧 Configurable trending period (daily/weekly/monthly) and language filters
- 🚀 Built with modern Python and uv package management

## Setup

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- [Resend](https://resend.com) account for sending emails

### Installation

1. Clone the repository:
```bash
git clone https://github.com/vanducng/github-trending-repos.git
cd github-trending-repos
```

2. Install dependencies:
```bash
uv sync
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your actual values
```

Required environment variables:
- `RESEND_API_KEY`: Your Resend API key
- `RECIPIENT_EMAIL`: Email address to receive summaries

Optional environment variables:
- `GH_TOKEN`: GitHub personal access token (for higher rate limits)
- `TRENDING_PERIOD`: daily/weekly/monthly (default: daily)
- `TRENDING_LANGUAGE`: Language filter (empty for all languages)

### Running Locally

```bash
uv run python main.py
```

### GitHub Actions Setup

For automated daily emails, configure your GitHub repository:

**Repository Secrets** (Settings → Secrets and variables → Actions → Secrets):
- `RESEND_API_KEY`: Your Resend API key
- `GH_TOKEN`: GitHub personal access token (optional, for higher rate limits)

**Repository Variables** (Settings → Secrets and variables → Actions → Variables):
- `RECIPIENT_EMAIL`: Email address to receive summaries
- `SENDER_EMAIL`: Sender email address (optional, defaults to Resend test domain)
- `TRENDING_PERIOD`: daily/weekly/monthly (optional, defaults to daily)
- `TRENDING_LANGUAGE`: Language filter (optional, empty for all languages)

The workflow runs daily at 7 AM GMT+7 (midnight UTC).

## Email Preview

The email includes:
- 📊 Summary statistics (total repos, stars, top languages)
- 🔥 Top 10 trending repositories with:
  - Repository name and description
  - Stars, forks, and primary language
  - Topics/tags
  - Direct links to repositories

## Project Structure

```
src/trending_repos/
├── __init__.py          # Package initialization
├── main.py             # Main application logic
├── config.py           # Configuration management
├── github_client.py    # GitHub API client
├── summarizer.py       # Repository summarization
├── email_sender.py     # Resend email integration
└── logger.py           # Logging configuration
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `uv run pytest` (when tests are added)
5. Submit a pull request

## License

MIT License - see LICENSE file for details.