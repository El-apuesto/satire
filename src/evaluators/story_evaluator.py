import logging
import re
import time
import random
import os
from typing import List, Dict, Tuple
from datetime import datetime
from groq import Groq
from config.settings import Config

# Force disable proxies before any imports
os.environ['NO_PROXY'] = '*'
os.environ['no_proxy'] = '*'
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

logger = logging.getLogger(__name__)

class StoryEvaluator:
    """Evaluates news stories for satirical potential using AI."""
    
    def __init__(self):
        if Config.GROQ_API_KEY:
            # Disable proxies at HTTP level
            import os
            os.environ['NO_PROXY'] = '*'
            os.environ['no_proxy'] = '*'
            
            self.client = Groq(api_key=Config.GROQ_API_KEY)
            self.model = "llama-3.1-8b-instant"
            self.last_request_time = 0
            self.min_delay = 0.5  # 0.5 seconds between requests
        else:
            logger.warning("Groq API key not configured")
            self.client = None
            self.last_request_time = 0
            self.min_delay = 0.5
    
    def evaluate_stories(self, stories: List[Dict], num_to_select: int = None) -> List[Tuple[Dict, float]]:
        """
        Evaluate stories and return top candidates with scores.
        
        Args:
            stories: List of news story dictionaries
            num_to_select: Number of top stories to select
            
        Returns:
            List of tuples (story, score) sorted by score descending
        """
        if not self.model:
            logger.error("Gemini model not available for evaluation")
            return []
        
        num_to_select = num_to_select or Config.ARTICLES_PER_CYCLE
        evaluated_stories = []
        
        logger.info(f"Evaluating {len(stories)} stories for satirical potential")
        
        for story in stories:
            try:
                score = self._evaluate_single_story(story)
                if score > 0:
                    evaluated_stories.append((story, score))
                    logger.debug(f"Story scored {score:.2f}: {story.get('title', 'Unknown')}")
            except Exception as e:
                logger.error(f"Error evaluating story {story.get('title', 'Unknown')}: {e}")
        
        # Sort by score descending
        evaluated_stories.sort(key=lambda x: x[1], reverse=True)
        
        top_stories = evaluated_stories[:num_to_select]
        logger.info(f"Selected top {len(top_stories)} stories for satire")
        
        return top_stories
    
    def _rate_limit(self):
        """Apply rate limiting between API requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_delay:
            sleep_time = self.min_delay - time_since_last + random.uniform(0.1, 0.5)
            logger.info(f"Rate limiting: waiting {sleep_time:.1f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _evaluate_single_story(self, story: Dict) -> float:
        """
        Evaluate a single story for satirical potential.
        
        Args:
            story: News story dictionary
            
        Returns:
            Satirical potential score (0-10)
        """
        title = story.get('title', '')
        description = story.get('description', '')
        content = story.get('content', '')
        category = story.get('fetched_category', '')
        
        # Create evaluation prompt
        prompt = self._create_evaluation_prompt(title, description, content, category)
        
        # Apply rate limiting
        self._rate_limit()
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            response_text = response.choices[0].message.content
            
            # Extract numeric score
            score_match = re.search(r'(\d+\.?\d*)', response_text)
            if score_match:
                score = float(score_match.group(1))
                return min(max(score, 0), 10)  # Ensure score is between 0-10
            else:
                logger.warning(f"Could not extract score from response: {score_text}")
                return 0.0
                
        except Exception as e:
            logger.error(f"Error getting AI evaluation: {e}")
            return 0.0
    
    def _create_evaluation_prompt(self, title: str, description: str, content: str, category: str) -> str:
        """Create the evaluation prompt for the AI."""
        
        prompt = f"""
Evaluate this REAL news story for sarcastic reporting potential on a scale of 0-10.

STORY DETAILS:
Title: {title}
Description: {description}
Content: {content[:500]}...
Category: {category}

EVALUATION CRITERIA:
- Irony factor (0-2): How much inherent irony or absurdity exists in the real situation?
- Commentary potential (0-2): How much room for cynical observations about human behavior?
- Smug reporting value (0-2): How well does it lend itself to world-weary commentary?
- Social relevance (0-2): Does it touch on relatable societal patterns or hypocrisies?
- Deadpan delivery potential (0-2): How effectively can sarcasm be delivered with a straight face?

SCORING:
0-2: Low sarcastic potential (straightforward, factual news)
3-5: Moderate potential (some ironic elements but mostly serious)
6-8: Good potential (clear opportunities for cynical commentary)
9-10: Excellent potential (perfect for sarcastic, smug reporting)

Please analyze the story and provide:
1. A numeric score from 0-10
2. Brief reasoning for your score (1-2 sentences)

Format your response as:
SCORE: [number]
REASONING: [brief explanation]
"""
        return prompt
    
    def get_satire_angles(self, story: Dict) -> List[str]:
        """
        Get potential satirical angles for a story.
        
        Args:
            story: News story dictionary
            
        Returns:
            List of satirical angle suggestions
        """
        if not self.model:
            return []
        
        title = story.get('title', '')
        description = story.get('description', '')
        
        prompt = f"""
Suggest 3-4 satirical angles for this news story:

Title: {title}
Description: {description}

Provide specific, creative angles that could be used for satirical treatment. Focus on:
- Exaggeration of key elements
- Ironic reinterpretations
- Absurdist scenarios
- Social commentary twists

Format as a numbered list of brief angle descriptions.
"""
        
        try:
            response = self.model.generate_content(prompt)
            angles_text = response.text.strip()
            
            # Extract numbered list items
            angles = []
            lines = angles_text.split('\n')
            for line in lines:
                line = line.strip()
                if re.match(r'^\d+\.', line):
                    angles.append(re.sub(r'^\d+\.\s*', '', line))
            
            return angles[:4]  # Return max 4 angles
            
        except Exception as e:
            logger.error(f"Error getting satire angles: {e}")
            return []
