import logging
import time
import random
from typing import Dict, List, Optional
from groq import Groq
from config.settings import Config

logger = logging.getLogger(__name__)

class ArticleGenerator:
    """Generates satirical articles from news stories using AI."""
    
    def __init__(self):
        if Config.GROQ_API_KEY:
            self.client = Groq(api_key=Config.GROQ_API_KEY)
            self.model = "llama-3.1-8b-instant"
            self.last_request_time = 0
            self.min_delay = 0.5
        else:
            logger.warning("Groq API key not configured")
            self.client = None
            self.last_request_time = 0
            self.min_delay = 0.5
    
    def generate_article(self, story: Dict, satire_style: str = None, angle: str = None) -> Optional[Dict]:
        """
        Generate a satirical article from a news story.
        
        Args:
            story: Original news story dictionary
            satire_style: Style of satire to use
            angle: Specific satirical angle to pursue
            
        Returns:
            Dictionary containing generated article or None if failed
        """
        if not self.model:
            logger.error("Gemini model not available for article generation")
            return None
        
        satire_style = satire_style or random.choice(Config.SATIRE_STYLES)
        
        try:
            article_content = self._generate_article_content(story, satire_style, angle)
            if article_content:
                article = self._format_article(article_content, story, satire_style)
                logger.info(f"Generated {satire_style} article: {article.get('title', 'Unknown')}")
                return article
            else:
                logger.warning("Failed to generate article content")
                return None
                
        except Exception as e:
            logger.error(f"Error generating article: {e}")
            return None
    
    def _rate_limit(self):
        """Apply rate limiting between API requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_delay:
            sleep_time = self.min_delay - time_since_last + random.uniform(0.1, 0.3)
            logger.info(f"Rate limiting: waiting {sleep_time:.1f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _generate_article_content(self, story: Dict, satire_style: str, angle: str = None) -> Optional[str]:
        """Generate the raw article content using AI."""
        
        title = story.get('title', '')
        description = story.get('description', '')
        content = story.get('content', '')
        category = story.get('fetched_category', '')
        
        prompt = self._create_article_prompt(title, description, content, category, satire_style, angle)
        
        # Apply rate limiting
        self._rate_limit()
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.8
            )
            content = response.choices[0].message.content
            return content
        except Exception as e:
            logger.error(f"Error generating article content: {e}")
            return None
    
    def _create_article_prompt(self, title: str, description: str, content: str, 
                              category: str, satire_style: str, angle: str = None) -> str:
        """Create the article generation prompt."""
        
        angle_instruction = f"\nSPECIFIC ANGLE: {angle}" if angle else ""
        
        prompt = f"""
You are a journalist for "OK Crisis" - a deadpan satire news outlet. Take this REAL news story and transform it into satirical content while maintaining a completely serious, deadpan tone. The humor comes from the absurdity of the situation, not from jokes.

ORIGINAL STORY:
Title: {title}
Description: {description}
Content: {content[:1000]}...
Category: {category}

STYLE: Deadpan satire - completely serious tone, but the content is satirical
TONE: Absolutely serious, no winking, no "just kidding" - deliver absurd content as if it's completely normal

RULES:
- Start with REAL news facts as the foundation
- You CAN exaggerate, add absurd details, and create fake quotes
- The key is delivering everything with a straight face
- Use phrases like "In a completely expected development..." or "As predicted by experts..."
- Treat ridiculous events as if they're perfectly normal
- Include fake quotes from fictional experts who state the obvious
- Add absurd details that enhance the comedy
- The humor comes from the contrast between serious tone and absurd content

ARTICLE STRUCTURE:
1. Serious-sounding headline about the absurd situation
2. Straightforward opening treating ridiculous events as normal
3. Body paragraphs with fake quotes and absurd details
4. Conclusion that treats the absurdity as completely expected

Write the complete article in markdown format. The goal is deadpan satire - completely serious tone delivering absurd content.
"""
        return prompt
    
    def _format_article(self, content: str, original_story: Dict, satire_style: str) -> Dict:
        """Format the generated content into a structured article."""
        
        lines = content.split('\n')
        
        # Extract headline (first non-empty line that looks like a title)
        headline = ""
        body_start = 0
        
        for i, line in enumerate(lines):
            line = line.strip()
            if line and not line.startswith('#') and len(line) > 10:
                headline = line
                body_start = i + 1
                break
        
        if not headline:
            # Fallback: create headline from original
            headline = f"Breaking: {original_story.get('title', 'Local Event Occurs')}"
        
        # Extract body content
        body_lines = lines[body_start:]
        body = '\n'.join(body_lines).strip()
        
        # Generate a satirical byline
        byline = self._generate_byline()
        
        # Create article metadata
        article = {
            'title': headline,
            'byline': byline,
            'content': body,
            'satire_style': satire_style,
            'original_title': original_story.get('title', ''),
            'original_source': original_story.get('source_id', ''),
            'category': original_story.get('fetched_category', ''),
            'published_at': original_story.get('published_at', ''),
            'word_count': len(body.split()),
            'created_at': self._get_current_timestamp()
        }
        
        return article
    
    def _generate_byline(self) -> str:
        """Generate a satirical journalist name."""
        first_names = ["Skip", "Brenda", "Chuck", "Mildred", "Bartholomew", "Penelope"]
        last_names = ["McGee", "Henderson", "Fiddlebottom", "Winklestein", "Puddington", "Snodgrass"]
        
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        titles = ["Staff Writer", "Senior Correspondent", "Investigative Journalist", "Cultural Analyst"]
        
        return f"{name}, {random.choice(titles)}"
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def generate_editorial_content(self, top_stories: List[Dict]) -> Optional[Dict]:
        """
        Generate editorial content for the website.
        
        Args:
            top_stories: List of top selected stories
            
        Returns:
            Dictionary containing editorial content or None if failed
        """
        if not self.model:
            return None
        
        # Create summary of top stories for editorial context
        story_summaries = []
        for story in top_stories:
            story_summaries.append(f"- {story.get('title', '')}")
        
        stories_text = '\n'.join(story_summaries)
        
        prompt = f"""
Write a deadpan editorial for a satire news website based on today's top stories:

TOP STORIES:
{stories_text}

EDITORIAL REQUIREMENTS:
- Write as "The Editorial Board" 
- Comment on the absurd state of current events
- Maintain serious, thoughtful tone while being completely satirical
- Reference 2-3 of the stories in ironic ways
- End with a deadpan observation about society
- Length: 200-300 words
- Style: Pretend to be a legitimate editorial while being completely absurd

Write the editorial in markdown format.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.8
            )
            content = response.choices[0].message.content
            
            editorial = {
                'title': "Today's Editorial: A Moment of Reflection",
                'byline': "The Editorial Board",
                'content': content,
                'type': 'editorial',
                'created_at': self._get_current_timestamp()
            }
            
            return editorial
            
        except Exception as e:
            logger.error(f"Error generating editorial: {e}")
            return None
