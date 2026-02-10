import logging
import schedule
import time
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# Import config separately to ensure it's available
try:
    from config.settings import Config
    config_imported = True
except ImportError as e:
    print(f"Config import error: {e}")
    Config = None
    config_imported = False

# Import our modules - fix path issues
try:
    from src.fetchers.news_fetcher import NewsFetcher
    from src.evaluators.story_evaluator import StoryEvaluator
    from src.generators.article_generator import ArticleGenerator
    from src.generators.image_generator import ImageGenerator
    from src.generators.comic_generator import ComicGenerator
    from src.website.app import Website
    
    # Create website instance
    website = Website()
    modules_imported = True
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.error(f"Import error: {e}")
    # Fallback for basic functionality
    website = None
    modules_imported = False

logger = logging.getLogger(__name__)

class AutomationScheduler:
    """Main automation system that runs the twice-daily news publishing cycle."""
    
    def __init__(self):
        try:
            self.news_fetcher = NewsFetcher()
            self.story_evaluator = StoryEvaluator()
            self.article_generator = ArticleGenerator()
            self.image_generator = ImageGenerator()
            self.comic_generator = ComicGenerator()
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            self.news_fetcher = None
            self.story_evaluator = None
            self.article_generator = None
            self.image_generator = None
            self.comic_generator = None
        
        # Ensure directories exist
        os.makedirs('logs', exist_ok=True)
        os.makedirs('data', exist_ok=True)
        
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.LOG_FILE),
                logging.StreamHandler()
            ]
        )
    
    def run_morning_cycle(self):
        """Run the morning news publishing cycle."""
        logger.info("=== STARTING MORNING NEWS CYCLE ===")
        self.run_publishing_cycle("morning")
        logger.info("=== MORNING NEWS CYCLE COMPLETED ===")
    
    def run_evening_cycle(self):
        """Run the evening news publishing cycle."""
        logger.info("=== STARTING EVENING NEWS CYCLE ===")
        self.run_publishing_cycle("evening")
        logger.info("=== EVENING NEWS CYCLE COMPLETED ===")
    
    def run_cycle(self):
        """Run a complete publishing cycle (called by admin app)."""
        if not config_imported:
            return {"error": "Config not imported", "articles": [], "comics": []}
        if not modules_imported:
            return {"error": "Modules not imported", "articles": [], "comics": []}
        
        return self.run_publishing_cycle("manual")
    
    def run_publishing_cycle(self, cycle_name: str):
        """
        Run a complete publishing cycle.
        
        Args:
            cycle_name: Name of the cycle (morning/evening)
        """
        try:
            # Phase 1: News Aggregation
            logger.info(f"Phase 1: Fetching news stories for {cycle_name} cycle")
            news_stories = self.fetch_news_stories()
            
            if not news_stories:
                logger.warning("No news stories fetched, aborting cycle")
                return
            
            # Phase 2: Story Evaluation and Selection
            logger.info("Phase 2: Evaluating stories for satirical potential")
            selected_stories = self.evaluate_and_select_stories(news_stories)
            
            if not selected_stories:
                logger.warning("No stories selected for satire, aborting cycle")
                return
            
            # Phase 3: Article Generation
            logger.info("Phase 3: Generating satirical articles")
            generated_articles = self.generate_articles(selected_stories)
            
            # Phase 4: Image Generation
            logger.info("Phase 4: Generating article images")
            self.generate_article_images(generated_articles)
            
            # Phase 5: Comic Generation
            logger.info("Phase 5: Generating comic strips")
            generated_comics = self.generate_comics(selected_stories)
            
            # Phase 6: Editorial Content
            logger.info("Phase 6: Generating editorial content")
            editorial = self.generate_editorial(selected_stories)
            
            # Phase 7: Publishing
            logger.info("Phase 7: Publishing content to website")
            self.publish_content(generated_articles, generated_comics, editorial)
            
            # Phase 8: Cleanup
            logger.info("Phase 8: Performing cleanup and maintenance")
            self.perform_cleanup()
            
            logger.info(f"{cycle_name.title()} cycle completed successfully")
            
        except Exception as e:
            logger.error(f"Error in {cycle_name} cycle: {e}")
            raise
    
    def fetch_news_stories(self) -> List[Dict]:
        """Fetch news stories from various sources."""
        try:
            stories = self.news_fetcher.fetch_news(hours_back=12, max_stories=Config.MAX_NEWS_STORIES)
            
            # Validate stories
            valid_stories = []
            for story in stories:
                if self.news_fetcher.validate_story(story):
                    valid_stories.append(story)
            
            logger.info(f"Fetched and validated {len(valid_stories)} news stories")
            return valid_stories
            
        except Exception as e:
            logger.error(f"Error fetching news stories: {e}")
            return []
    
    def evaluate_and_select_stories(self, stories: List[Dict]) -> List[Dict]:
        """Evaluate stories and select the best candidates for satire."""
        try:
            evaluated_stories = self.story_evaluator.evaluate_stories(
                stories, 
                num_to_select=Config.ARTICLES_PER_CYCLE
            )
            
            # Extract just the story dictionaries
            selected_stories = [story for story, score in evaluated_stories]
            
            logger.info(f"Selected {len(selected_stories)} stories for satire")
            for i, (story, score) in enumerate(evaluated_stories):
                logger.info(f"  {i+1}. {story.get('title', 'Unknown')} (Score: {score:.2f})")
            
            return selected_stories
            
        except Exception as e:
            logger.error(f"Error evaluating stories: {e}")
            return []
    
    def generate_articles(self, selected_stories: List[Dict]) -> List[Dict]:
        """Generate satirical articles from selected stories."""
        articles = []
        
        for i, story in enumerate(selected_stories):
            try:
                logger.info(f"Generating article {i+1}/{len(selected_stories)}")
                
                # Get satire angles
                angles = self.story_evaluator.get_satire_angles(story)
                selected_angle = angles[0] if angles else None
                
                # Generate article
                article = self.article_generator.generate_article(
                    story, 
                    angle=selected_angle
                )
                
                if article:
                    article['original_story'] = story
                    articles.append(article)
                    logger.info(f"Generated article: {article.get('title', 'Unknown')}")
                else:
                    logger.warning(f"Failed to generate article from: {story.get('title', 'Unknown')}")
                    
            except Exception as e:
                logger.error(f"Error generating article from {story.get('title', 'Unknown')}: {e}")
        
        logger.info(f"Generated {len(articles)} articles")
        return articles
    
    def generate_article_images(self, articles: List[Dict]):
        """Generate images for articles."""
        for article in articles:
            try:
                title = article.get('title', '')
                content = article.get('content', '')
                category = article.get('category', '')
                
                image_path = self.image_generator.generate_article_image(
                    title, content, category
                )
                
                if image_path:
                    article['image_path'] = image_path
                    logger.info(f"Generated image for: {title}")
                else:
                    logger.warning(f"Failed to generate image for: {title}")
                    
            except Exception as e:
                logger.error(f"Error generating image for article {article.get('title', 'Unknown')}: {e}")
    
    def generate_comics(self, selected_stories: List[Dict]) -> List[Dict]:
        """Generate comic strips from selected stories."""
        comics = []
        
        # Generate comics for top stories
        comic_stories = selected_stories[:Config.COMICS_PER_CYCLE]
        
        for i, story in enumerate(comic_stories):
            try:
                logger.info(f"Generating comic {i+1}/{len(comic_stories)}")
                
                title = story.get('title', '')
                content = story.get('content', '')
                category = story.get('fetched_category', '')
                
                comic_path = self.comic_generator.generate_comic_strip(
                    title, content, category
                )
                
                if comic_path:
                    comic = {
                        'title': f"Comic: {title[:30]}...",
                        'image_path': comic_path,
                        'original_story': story,
                        'created_at': datetime.now().isoformat()
                    }
                    comics.append(comic)
                    logger.info(f"Generated comic for: {title}")
                else:
                    logger.warning(f"Failed to generate comic for: {title}")
                    
            except Exception as e:
                logger.error(f"Error generating comic for {story.get('title', 'Unknown')}: {e}")
        
        logger.info(f"Generated {len(comics)} comics")
        return comics
    
    def generate_editorial(self, selected_stories: List[Dict]) -> Optional[Dict]:
        """Generate editorial content."""
        try:
            editorial = self.article_generator.generate_editorial_content(selected_stories)
            
            if editorial:
                logger.info("Generated editorial content")
                return editorial
            else:
                logger.warning("Failed to generate editorial")
                return None
                
        except Exception as e:
            logger.error(f"Error generating editorial: {e}")
            return None
    
    def publish_content(self, articles: List[Dict], comics: List[Dict], editorial: Optional[Dict]):
        """Publish generated content to the website."""
        try:
            # Save articles
            for article in articles:
                website.save_article(article)
                logger.info(f"Published article: {article.get('title', 'Unknown')}")
            
            # Save comics
            for comic in comics:
                website.save_comic(comic)
                logger.info(f"Published comic: {comic.get('title', 'Unknown')}")
            
            # Save editorial if exists
            if editorial:
                website.save_article(editorial)
                logger.info("Published editorial")
            
            logger.info(f"Published {len(articles)} articles and {len(comics)} comics")
            
        except Exception as e:
            logger.error(f"Error publishing content: {e}")
    
    def perform_cleanup(self):
        """Perform cleanup and maintenance tasks."""
        try:
            # Clean up old temporary files
            temp_dirs = ['temp', 'cache']
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    # Remove files older than 24 hours
                    current_time = time.time()
                    for filename in os.listdir(temp_dir):
                        filepath = os.path.join(temp_dir, filename)
                        if os.path.isfile(filepath):
                            file_age = current_time - os.path.getmtime(filepath)
                            if file_age > 86400:  # 24 hours
                                os.remove(filepath)
                                logger.info(f"Cleaned up old file: {filepath}")
            
            # Clean up old images (keep last configured amounts)
            self._cleanup_old_images()
            
            # Log system status
            logger.info("System cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def _cleanup_old_images(self):
        """Clean up old image files to prevent storage overflow."""
        try:
            from config.settings import Config
            
            # Clean up article images (keep last configured amount)
            images_dir = "static/images"
            if os.path.exists(images_dir):
                image_files = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
                image_files.sort(key=lambda x: os.path.getmtime(os.path.join(images_dir, x)), reverse=True)
                
                # Remove oldest images beyond limit
                for old_image in image_files[Config.MAX_IMAGES_STORED:]:
                    old_path = os.path.join(images_dir, old_image)
                    os.remove(old_path)
                    logger.info(f"Removed old image: {old_path}")
            
            # Clean up comic images (keep last configured amount)
            comics_dir = "static/comics"
            if os.path.exists(comics_dir):
                comic_files = [f for f in os.listdir(comics_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
                comic_files.sort(key=lambda x: os.path.getmtime(os.path.join(comics_dir, x)), reverse=True)
                
                # Remove oldest comics beyond limit
                for old_comic in comic_files[Config.MAX_COMIC_IMAGES_STORED:]:
                    old_path = os.path.join(comics_dir, old_comic)
                    os.remove(old_path)
                    logger.info(f"Removed old comic: {old_comic}")
                    
        except Exception as e:
            logger.error(f"Error cleaning up images: {e}")
    
    def start_scheduler(self):
        """Start the automated scheduler."""
        logger.info("Starting satire news automation scheduler")
        
        # Schedule morning and evening runs
        schedule.every().day.at(Config.MORNING_RUN_TIME).do(self.run_morning_cycle)
        schedule.every().day.at(Config.EVENING_RUN_TIME).do(self.run_evening_cycle)
        
        logger.info(f"Scheduled daily runs at {Config.MORNING_RUN_TIME} and {Config.EVENING_RUN_TIME}")
        
        # Run the scheduler
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                logger.info("Scheduler stopped by user")
                break
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying
    
    def run_test_cycle(self):
        """Run a test cycle for debugging purposes."""
        logger.info("=== RUNNING TEST CYCLE ===")
        self.run_publishing_cycle("test")
        logger.info("=== TEST CYCLE COMPLETED ===")

def main():
    """Main entry point."""
    scheduler = AutomationScheduler()
    
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # Run a test cycle
        scheduler.run_test_cycle()
    else:
        # Start the scheduler
        scheduler.start_scheduler()

if __name__ == '__main__':
    main()
