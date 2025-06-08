# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GitHub Trending Repos is a Python application that fetches trending GitHub repositories daily and sends formatted email summaries using Resend. It runs automatically via GitHub Actions and is built with modern Python tooling.

## Development Commands

- **Install dependencies**: `uv sync`
- **Run the application**: `uv run python main.py`
- **Format code**: `uv run black .`
- **Lint code**: `uv run ruff check .`
- **Run tests**: `uv run pytest` (when tests are added)

## Architecture

The application follows a modular architecture with clear separation of concerns:

- **`src/trending_repos/main.py`**: Main application orchestration and async flow
- **`src/trending_repos/github_client.py`**: GitHub API interaction and web scraping
- **`src/trending_repos/summarizer.py`**: Data processing and formatting for email
- **`src/trending_repos/email_sender.py`**: Resend integration with HTML/text templates
- **`src/trending_repos/config.py`**: Environment-based configuration management
- **`src/trending_repos/logger.py`**: Centralized logging setup

## Key Technical Details

- Uses **httpx** for async HTTP requests to GitHub API and trending page scraping
- Implements **BeautifulSoup** for parsing GitHub's trending page HTML
- **Resend** integration for professional email delivery with HTML templates
- **GitHub Actions** workflow scheduled for daily execution at 7 AM GMT+7
- Environment variables for configuration (API keys, email addresses, etc.)

## Configuration Requirements

Required environment variables:
- `RESEND_API_KEY`: Resend service API key
- `RECIPIENT_EMAIL`: Target email address (currently me@vanducng.dev)

Optional environment variables:
- `GITHUB_TOKEN`: For higher API rate limits
- `TRENDING_PERIOD`: daily/weekly/monthly
- `TRENDING_LANGUAGE`: Programming language filter

## Data Flow

1. GitHub trending page scraping → repository names
2. GitHub API calls → detailed repository metadata
3. Data summarization → statistics and formatting
4. Email template generation → HTML and text versions
5. Resend API → email delivery