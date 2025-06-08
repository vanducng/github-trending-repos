"""Repository summarization functionality."""

from typing import List, Dict, Any
from datetime import datetime


class RepoSummarizer:
    """Summarizes trending repositories for email digest."""
    
    def create_summary(self, repos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a summary of trending repositories.
        
        Args:
            repos: List of repository dictionaries
            
        Returns:
            Dictionary containing summary information
        """
        if not repos:
            return {
                "total_repos": 0,
                "summary_text": "No trending repositories found today.",
                "repos": []
            }
        
        # Calculate summary statistics
        total_stars = sum(repo.get("stars", 0) for repo in repos)
        languages = {}
        
        for repo in repos:
            lang = repo.get("language", "Unknown")
            if lang:
                languages[lang] = languages.get(lang, 0) + 1
        
        # Sort languages by frequency
        top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Create summary text
        summary_parts = [
            f"📈 **{len(repos)} trending repositories** discovered today",
            f"⭐ **{total_stars:,} total stars** across all repositories"
        ]
        
        if top_languages:
            lang_text = ", ".join([f"{lang} ({count})" for lang, count in top_languages])
            summary_parts.append(f"💻 **Top languages**: {lang_text}")
        
        summary_text = "\n\n".join(summary_parts)
        
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_repos": len(repos),
            "total_stars": total_stars,
            "top_languages": top_languages,
            "summary_text": summary_text,
            "repos": self._format_repos_for_email(repos)
        }
    
    def _format_repos_for_email(self, repos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format repository data for email display.
        
        Args:
            repos: List of repository dictionaries
            
        Returns:
            List of formatted repository dictionaries
        """
        formatted_repos = []
        
        for i, repo in enumerate(repos, 1):
            # Format creation date
            created_date = ""
            if repo.get("created_at"):
                try:
                    created_dt = datetime.fromisoformat(repo["created_at"].replace("Z", "+00:00"))
                    created_date = created_dt.strftime("%B %Y")
                except:
                    created_date = "Unknown"
            
            # Format description
            description = repo.get("description", "No description available")
            if len(description) > 150:
                description = description[:147] + "..."
            
            # Format topics
            topics = repo.get("topics", [])
            topics_text = ", ".join(topics[:5]) if topics else "No topics"
            
            formatted_repo = {
                "rank": i,
                "name": repo.get("name", "Unknown"),
                "full_name": repo.get("full_name", "Unknown"),
                "description": description,
                "language": repo.get("language", "Unknown"),
                "stars": f"{repo.get('stars', 0):,}",
                "forks": f"{repo.get('forks', 0):,}",
                "url": repo.get("url", ""),
                "created_date": created_date,
                "topics": topics_text,
                "license": repo.get("license", "No license"),
                "owner_name": repo.get("owner", {}).get("login", "Unknown"),
                "owner_avatar": repo.get("owner", {}).get("avatar_url", "")
            }
            
            formatted_repos.append(formatted_repo)
        
        return formatted_repos