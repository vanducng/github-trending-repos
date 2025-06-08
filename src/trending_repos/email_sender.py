"""Email sending functionality using Resend."""

import os
from typing import Dict, Any
import resend


class EmailSender:
    """Handles sending emails via Resend service."""
    
    def __init__(self, api_key: str):
        """Initialize the email sender.
        
        Args:
            api_key: Resend API key
        """
        resend.api_key = api_key
    
    async def send_trending_summary(self, summary: Dict[str, Any], recipient_email: str) -> bool:
        """Send trending repositories summary email.
        
        Args:
            summary: Repository summary data
            recipient_email: Email address to send to
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            # Generate email content
            html_content = self._generate_html_email(summary)
            text_content = self._generate_text_email(summary)
            
            # Send email
            params = {
                "from": "GitHub Trending <onboarding@resend.dev>",  # Using Resend's test domain
                "to": [recipient_email],
                "subject": f"📈 GitHub Trending Repos - {summary['date']}",
                "html": html_content,
                "text": text_content,
            }
            
            email = resend.Emails.send(params)
            print(f"Email sent successfully: {email}")
            return True
            
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
    
    def _generate_html_email(self, summary: Dict[str, Any]) -> str:
        """Generate HTML email content.
        
        Args:
            summary: Repository summary data
            
        Returns:
            HTML email content
        """
        repos_html = ""
        for repo in summary.get("repos", []):
            topics_badges = ""
            if repo["topics"] != "No topics":
                topics = repo["topics"].split(", ")[:3]  # Limit to 3 topics
                for topic in topics:
                    topics_badges += f'<span style="background: #f1f8ff; color: #0969da; padding: 2px 6px; border-radius: 12px; font-size: 12px; margin-right: 4px;">{topic}</span>'
            
            repos_html += f"""
            <div style="border: 1px solid #e1e4e8; border-radius: 8px; padding: 20px; margin-bottom: 20px; background: white;">
                <div style="display: flex; align-items: center; margin-bottom: 12px;">
                    <h3 style="margin: 0; color: #24292f;">
                        <a href="{repo['url']}" style="color: #0969da; text-decoration: none;">
                            #{repo['rank']} {repo['full_name']}
                        </a>
                    </h3>
                </div>
                
                <p style="color: #656d76; margin: 8px 0; line-height: 1.5;">{repo['description']}</p>
                
                <div style="margin: 12px 0;">
                    {topics_badges}
                </div>
                
                <div style="display: flex; gap: 16px; align-items: center; font-size: 14px; color: #656d76;">
                    <span>⭐ {repo['stars']} stars</span>
                    <span>🍴 {repo['forks']} forks</span>
                    {f'<span>💻 {repo["language"]}</span>' if repo["language"] != "Unknown" else ""}
                    {f'<span>📅 Created {repo["created_date"]}</span>' if repo["created_date"] != "Unknown" else ""}
                </div>
            </div>
            """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>GitHub Trending Repos</title>
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; line-height: 1.6; color: #24292f; max-width: 800px; margin: 0 auto; padding: 20px; background: #f6f8fa;">
            
            <div style="text-align: center; margin-bottom: 32px; padding: 24px; background: white; border-radius: 8px; border: 1px solid #e1e4e8;">
                <h1 style="color: #24292f; margin: 0 0 8px 0;">📈 GitHub Trending Repositories</h1>
                <p style="color: #656d76; margin: 0; font-size: 16px;">{summary['date']}</p>
            </div>
            
            <div style="background: white; padding: 24px; border-radius: 8px; border: 1px solid #e1e4e8; margin-bottom: 24px;">
                <h2 style="color: #24292f; margin: 0 0 16px 0;">📊 Summary</h2>
                <div style="color: #656d76; line-height: 1.6;">
                    {summary['summary_text'].replace('**', '<strong>').replace('**', '</strong>').replace('\n\n', '<br><br>')}
                </div>
            </div>
            
            <div>
                <h2 style="color: #24292f; margin: 0 0 20px 0;">🔥 Top Trending Repositories</h2>
                {repos_html}
            </div>
            
            <div style="text-align: center; margin-top: 32px; padding: 16px; background: white; border-radius: 8px; border: 1px solid #e1e4e8;">
                <p style="color: #656d76; margin: 0; font-size: 14px;">
                    Generated by <a href="https://github.com/vanducng/github-trending-repos" style="color: #0969da;">GitHub Trending Repos</a>
                </p>
            </div>
            
        </body>
        </html>
        """
    
    def _generate_text_email(self, summary: Dict[str, Any]) -> str:
        """Generate plain text email content.
        
        Args:
            summary: Repository summary data
            
        Returns:
            Plain text email content
        """
        content = f"""GitHub Trending Repositories - {summary['date']}

{summary['summary_text']}

Top Trending Repositories:
{'=' * 50}
"""
        
        for repo in summary.get("repos", []):
            content += f"""
#{repo['rank']} {repo['full_name']}
{repo['url']}

{repo['description']}

⭐ {repo['stars']} stars | 🍴 {repo['forks']} forks"""
            
            if repo['language'] != "Unknown":
                content += f" | 💻 {repo['language']}"
            
            if repo['created_date'] != "Unknown":
                content += f" | 📅 Created {repo['created_date']}"
            
            if repo['topics'] != "No topics":
                content += f"\nTopics: {repo['topics']}"
            
            content += "\n" + "-" * 50
        
        content += f"""

Generated by GitHub Trending Repos
https://github.com/vanducng/github-trending-repos
"""
        
        return content