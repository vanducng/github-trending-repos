"""Main application logic."""

import asyncio
import sys
from .config import Config
from .github_client import GitHubClient
from .summarizer import RepoSummarizer
from .email_sender import EmailSender
from .logger import logger


async def main():
    """Main application entry point."""
    logger.info("🚀 Starting GitHub Trending Repos...")
    
    # Validate configuration
    if not Config.validate_required_settings():
        logger.error("Configuration validation failed")
        sys.exit(1)
    
    try:
        # Initialize clients
        github_client = GitHubClient(Config.GITHUB_TOKEN)
        summarizer = RepoSummarizer()
        email_sender = EmailSender(Config.RESEND_API_KEY)
        
        logger.info("📈 Fetching trending repositories...")
        
        # Fetch trending repositories
        repos = await github_client.fetch_trending_repos(
            period=Config.TRENDING_PERIOD,
            language=Config.TRENDING_LANGUAGE
        )
        
        if not repos:
            logger.warning("❌ No trending repositories found")
            return
        
        logger.info(f"✅ Found {len(repos)} trending repositories")
        
        # Create summary
        logger.info("📝 Creating summary...")
        summary = summarizer.create_summary(repos)
        
        # Send email
        logger.info(f"📧 Sending email to {Config.RECIPIENT_EMAIL}...")
        success = await email_sender.send_trending_summary(summary, Config.RECIPIENT_EMAIL, Config.SENDER_EMAIL)
        
        if success:
            logger.info("✅ Email sent successfully!")
        else:
            logger.error("❌ Failed to send email")
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"❌ Application error: {e}", exc_info=True)
        sys.exit(1)


def sync_main():
    """Synchronous wrapper for main function."""
    asyncio.run(main())