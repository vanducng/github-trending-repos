"""GitHub API client for fetching trending repositories."""

import asyncio
from typing import List, Dict, Any, Optional
import httpx
from bs4 import BeautifulSoup


class GitHubClient:
    """Client for fetching GitHub trending repositories."""
    
    def __init__(self, github_token: Optional[str] = None):
        """Initialize the GitHub client.
        
        Args:
            github_token: Optional GitHub personal access token for higher rate limits
        """
        self.github_token = github_token
        self.headers = {
            "User-Agent": "trending-repos-bot/1.0",
            "Accept": "application/vnd.github.v3+json"
        }
        if github_token:
            self.headers["Authorization"] = f"token {github_token}"
    
    async def fetch_trending_repos(self, period: str = "daily", language: str = "") -> List[Dict[str, Any]]:
        """Fetch trending repositories from GitHub.
        
        Args:
            period: Time period for trending repos (daily, weekly, monthly)
            language: Programming language filter (empty for all languages)
            
        Returns:
            List of repository dictionaries with basic info
        """
        # GitHub doesn't have an official API for trending repos,
        # so we'll scrape the trending page and then get detailed info via API
        trending_url = f"https://github.com/trending/{language}?since={period}"
        
        async with httpx.AsyncClient() as client:
            # First, scrape the trending page to get repo names
            response = await client.get(trending_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            repo_links = soup.find_all('h2', class_='h3 lh-condensed')
            
            repo_names = []
            for link in repo_links[:10]:  # Get top 10 trending repos
                repo_link = link.find('a')
                if repo_link:
                    repo_name = repo_link.get('href').strip('/')
                    repo_names.append(repo_name)
            
            # Now fetch detailed information for each repo via GitHub API
            repos = []
            for repo_name in repo_names:
                try:
                    repo_info = await self._fetch_repo_details(client, repo_name)
                    if repo_info:
                        repos.append(repo_info)
                except Exception as e:
                    print(f"Error fetching details for {repo_name}: {e}")
                    continue
            
            return repos
    
    async def _fetch_repo_details(self, client: httpx.AsyncClient, repo_name: str) -> Optional[Dict[str, Any]]:
        """Fetch detailed repository information from GitHub API.
        
        Args:
            client: HTTP client instance
            repo_name: Repository name in format "owner/repo"
            
        Returns:
            Repository information dictionary or None if error
        """
        api_url = f"https://api.github.com/repos/{repo_name}"
        
        try:
            response = await client.get(api_url, headers=self.headers)
            response.raise_for_status()
            
            repo_data = response.json()
            
            # Extract relevant information
            return {
                "name": repo_data.get("name", ""),
                "full_name": repo_data.get("full_name", ""),
                "description": repo_data.get("description", ""),
                "language": repo_data.get("language", ""),
                "stars": repo_data.get("stargazers_count", 0),
                "forks": repo_data.get("forks_count", 0),
                "url": repo_data.get("html_url", ""),
                "created_at": repo_data.get("created_at", ""),
                "updated_at": repo_data.get("updated_at", ""),
                "topics": repo_data.get("topics", []),
                "license": repo_data.get("license", {}).get("name", "") if repo_data.get("license") else "",
                "owner": {
                    "login": repo_data.get("owner", {}).get("login", ""),
                    "avatar_url": repo_data.get("owner", {}).get("avatar_url", "")
                }
            }
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                print(f"Repository {repo_name} not found")
            else:
                print(f"HTTP error for {repo_name}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error for {repo_name}: {e}")
            return None