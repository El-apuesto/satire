import logging
import re
from typing import List, Dict, Tuple
from datetime import datetime
import google.generativeai as genai
from config.settings import Config

logger = logging.getLogger(__name__)

class StoryEvaluator:
    """Evaluates news stories for satirical potential using AI."""
    
    def __init__(self):
        if Config.GEMINI_API_KEY:
            import google.generativeai as genai
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        else:
            logger.warning("Gemini API key not configured")
            self.model = None
    
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
        
        try:
            response = self.model.generate_content(prompt)
            score_text = response.text.strip()
            
            # Extract numeric score
            score_match = re.search(r'(\d+\.?\d*)', score_text)
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
Evaluate this news story for satirical potential on a scale of 0-10.

STORY DETAILS:
Title: {title}
Description: {description}
Content: {content[:500]}...
Category: {category}

EVALUATION CRITERIA:
- Absurdity factor (0-2): How inherently ridiculous or unbelievable is the situation?
- Irony potential (0-2): How much dramatic irony or situational irony exists?
- Exaggeration potential (0-2): How easily can the elements be exaggerated for comedic effect?
- Social commentary value (0-2): Does it touch on relatable social issues or human behavior?
- Parody possibilities (0-2): How well does it lend itself to parodying news tropes or genres?

SCORING:
0-2: Low satirical potential (very serious, straightforward news)
3-5: Moderate potential (some unusual elements but mostly factual)
6-8: Good potential (clear absurd or ironic elements)
9-10: Excellent potential (highly satirizable, perfect for comedy)

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
