import logging
import random
import os
from typing import Dict, List, Optional
from PIL import Image, ImageDraw, ImageFont
try:
    from groq import Groq
except ImportError:
    from groq import Client as Groq
from config.settings import Config

logger = logging.getLogger(__name__)

class ComicGenerator:
    """Generates comic strips with satirical content."""
    
    def __init__(self):
        if Config.GROQ_API_KEY:
            try:
                # Try new API first
                self.client = Groq(api_key=Config.GROQ_API_KEY)
            except TypeError as e:
                if 'proxies' in str(e):
                    # Fallback to older API if proxies error
                    self.client = Groq(api_key=Config.GROQ_API_KEY, http_client=None)
                else:
                    # Re-raise if different error
                    raise e
            self.model = "llama-3.1-8b-instant"
            self.last_request_time = 0
            self.min_delay = 0.5
        else:
            logger.warning("Groq API key not configured")
            self.client = None
            self.last_request_time = 0
            self.min_delay = 0.5
        
        self.comic_dir = "static/comics"
        os.makedirs(self.comic_dir, exist_ok=True)
        
        # Comic character templates
        self.characters = {
            "reporter": {"name": "Skip McGee", "style": "eager journalist with notepad"},
            "expert": {"name": "Dr. Winklestein", "style": "absurd academic with glasses"},
            "official": {"name": "Bartholomew Puddington", "style": "confused bureaucrat"},
            "citizen": {"name": "Mildred Henderson", "style": "concerned regular person"}
        }
        
        # Comic scenarios
        self.scenarios = [
            "press conference with ridiculous announcement",
            "expert explaining something completely obvious",
            "official trying to solve simple problem",
            "citizen reacting to absurd news",
            "reporter getting completely wrong story"
        ]
    
    def generate_comic_strip(self, article_title: str, article_content: str, 
                           category: str = None) -> Optional[str]:
        """
        Generate a 3-panel comic strip based on an article.
        
        Args:
            article_title: Title of the article
            article_content: Content of the article
            category: Article category
            
        Returns:
            Path to generated comic strip or None if failed
        """
        if not self.client:
            logger.error("Groq model not available for comic generation")
            return self._create_placeholder_comic(article_title)
        
        try:
            # Generate comic dialogue
            dialogue = self._generate_comic_dialogue({'title': article_title, 'content': article_content})
            if not dialogue:
                return self._create_placeholder_comic(article_title)
            
            # Create comic strip with dialogue
            comic_path = self._create_comic_strip(dialogue, article_title)
            
            if comic_path:
                logger.info(f"Generated comic strip: {comic_path}")
                return comic_path
            else:
                return self._create_placeholder_comic(article_title)
                
        except Exception as e:
            logger.error(f"Error generating comic strip: {e}")
            return self._create_placeholder_comic(article_title)
    
    def _rate_limit(self):
        """Apply rate limiting between API requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_delay:
            sleep_time = self.min_delay - time_since_last + random.uniform(0.1, 0.3)
            logger.info(f"Rate limiting: waiting {sleep_time:.1f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _generate_comic_dialogue(self, story: Dict) -> Optional[Dict]:
        """Generate dialogue for a 3-panel comic strip."""
        
        content_sample = story["content"][:800]  # First 800 chars for context
        
        prompt = f"""
Create a 3-panel comic strip dialogue based on this REAL news story, but with sarcastic, cynical commentary.

Title: {story.get('title', '')}
Content: {content_sample}

REQUIREMENTS:
- Create exactly 3 panels with dialogue
- Use these characters: Reporter (Skip McGee), Expert (Dr. Winklestein), Official (Bartholomew Puddington), or Citizen (Mildred Henderson)
- Each panel should be: PANEL [number]: [CHARACTER NAME]: [dialogue]
- Make it sarcastic and deadpan
- Reference the real news situation ironically
- Keep dialogue short and punchy

PANEL 1:
[CHARACTER NAME]: [dialogue]

PANEL 2:
[CHARACTER NAME]: [dialogue]

PANEL 3:
[CHARACTER NAME]: [dialogue]

Choose 2-3 different characters and create a mini-story that comments sarcastically on the real news situation.
"""
        
        # Apply rate limiting
        self._rate_limit()
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.9
            )
            dialogue_text = response.choices[0].message.content
            
            # Parse the dialogue
            panels = self._parse_comic_dialogue(dialogue_text)
            return panels
            
        except Exception as e:
            logger.error(f"Error generating comic dialogue: {e}")
            return None
    
    def _parse_comic_dialogue(self, dialogue_text: str) -> Optional[Dict]:
        """Parse the AI-generated dialogue into structured format."""
        
        panels = {}
        current_panel = None
        
        lines = dialogue_text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Check for panel headers
            if line.startswith('PANEL ') and ':' in line:
                panel_num = line.split()[1].replace(':', '')
                current_panel = f"panel_{panel_num}"
                panels[current_panel] = []
            
            # Check for character dialogue
            elif current_panel and ':' in line:
                if '[' in line and ']' in line:
                    # Extract character and dialogue
                    parts = line.split(']:', 1)
                    if len(parts) == 2:
                        character = parts[0].replace('[', '').strip()
                        dialogue = parts[1].strip()
                        
                        panels[current_panel].append({
                            'character': character,
                            'dialogue': dialogue
                        })
        
        # Ensure we have 3 panels
        if len(panels) == 3:
            return panels
        else:
            logger.warning(f"Expected 3 panels, got {len(panels)}")
            return None
    
    def _create_comic_strip(self, dialogue: Dict, title: str) -> Optional[str]:
        """Create a visual comic strip with the dialogue."""
        
        try:
            # Create blank comic strip
            img = Image.new('RGB', (Config.COMIC_STRIP_WIDTH, Config.COMIC_STRIP_HEIGHT), color='white')
            draw = ImageDraw.Draw(img)
            
            # Panel dimensions
            panel_width = Config.COMIC_STRIP_WIDTH // 3
            panel_height = Config.COMIC_STRIP_HEIGHT
            
            # Try to load fonts
            try:
                title_font = ImageFont.truetype("arial.ttf", 16)
                dialogue_font = ImageFont.truetype("arial.ttf", 12)
                label_font = ImageFont.truetype("arial.ttf", 10)
            except:
                title_font = ImageFont.load_default()
                dialogue_font = ImageFont.load_default()
                label_font = ImageFont.load_default()
            
            # Draw panels and add dialogue
            for i, panel_key in enumerate(['panel_1', 'panel_2', 'panel_3']):
                x_offset = i * panel_width
                
                # Draw panel border
                draw.rectangle([x_offset, 0, x_offset + panel_width - 2, panel_height], 
                             outline='black', width=2)
                
                # Add panel number
                panel_label = f"Panel {i+1}"
                draw.text((x_offset + 5, 5), panel_label, fill='black', font=label_font)
                
                # Add dialogue
                if panel_key in dialogue:
                    panel_dialogue = dialogue[panel_key]
                    y_position = 30
                    
                    for item in panel_dialogue:
                        character = item.get('character', '')
                        text = item.get('dialogue', '')
                        
                        # Character name
                        char_text = f"{character}:"
                        draw.text((x_offset + 10, y_position), char_text, 
                                fill='black', font=dialogue_font)
                        y_position += 15
                        
                        # Dialogue (wrap if needed)
                        dialogue_lines = self._wrap_text(text, 40)
                        for line in dialogue_lines[:3]:  # Max 3 lines per character
                            draw.text((x_offset + 10, y_position), line, 
                                    fill='black', font=dialogue_font)
                            y_position += 12
                        
                        y_position += 5  # Space between characters
                
                # Add simple character representation
                self._draw_simple_character(draw, x_offset, panel_height - 80, panel_width - 20)
            
            # Save comic strip
            filename = f"comic_{random.randint(1000, 9999)}.jpg"
            filepath = os.path.join(self.comic_dir, filename)
            
            img.save(filepath, 'JPEG', quality=85)
            return filepath
            
        except Exception as e:
            logger.error(f"Error creating comic strip: {e}")
            return None
    
    def _draw_simple_character(self, draw, x: int, y: int, width: int):
        """Draw a simple character representation."""
        # Draw a very simple stick figure
        center_x = x + width // 2
        
        # Head
        draw.ellipse([center_x - 15, y, center_x + 15, y + 30], outline='black', width=2)
        
        # Body
        draw.line([center_x, y + 30, center_x, y + 60], fill='black', width=2)
        
        # Arms
        draw.line([center_x - 20, y + 40, center_x + 20, y + 40], fill='black', width=2)
        
        # Legs
        draw.line([center_x, y + 60, center_x - 15, y + 75], fill='black', width=2)
        draw.line([center_x, y + 60, center_x + 15, y + 75], fill='black', width=2)
    
    def _create_placeholder_comic(self, title: str) -> Optional[str]:
        """Create a placeholder comic when generation fails."""
        
        try:
            img = Image.new('RGB', (Config.COMIC_STRIP_WIDTH, Config.COMIC_STRIP_HEIGHT), color='#f8f8f8')
            draw = ImageDraw.Draw(img)
            
            # Try to load font
            try:
                font = ImageFont.truetype("arial.ttf", 14)
            except:
                font = ImageFont.load_default()
            
            # Draw panels
            panel_width = Config.COMIC_STRIP_WIDTH // 3
            for i in range(3):
                x_offset = i * panel_width
                draw.rectangle([x_offset, 0, x_offset + panel_width - 2, Config.COMIC_STRIP_HEIGHT], 
                             outline='black', width=2)
                
                # Add placeholder text
                text = f"Panel {i+1}\nComing Soon"
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                text_x = x_offset + (panel_width - text_width) // 2
                text_y = Config.COMIC_STRIP_HEIGHT // 2 - text_height // 2
                
                draw.text((text_x, text_y), text, fill='black', font=font)
            
            # Save placeholder
            filename = f"comic_placeholder_{random.randint(1000, 9999)}.jpg"
            filepath = os.path.join(self.comic_dir, filename)
            
            img.save(filepath, 'JPEG', quality=85)
            return filepath
            
        except Exception as e:
            logger.error(f"Error creating placeholder comic: {e}")
            return None
    
    def _wrap_text(self, text: str, max_chars: int) -> list:
        """Wrap text to fit within specified character limit per line."""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + word) <= max_chars:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines
