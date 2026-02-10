import logging
import requests
import random
from typing import Optional, Dict
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
from config.settings import Config

logger = logging.getLogger(__name__)

class ImageGenerator:
    """Generates images for articles using multiple services with fallbacks."""
    
    def __init__(self):
        self.replicate_token = Config.REPLICATE_API_TOKEN
        self.pexels_key = Config.PEXELS_API_KEY
        self.unsplash_key = Config.UNSPLASH_API_KEY
        self.image_dir = "static/images"
        
        # Ensure image directory exists
        os.makedirs(self.image_dir, exist_ok=True)
    
    def generate_article_image(self, article_title: str, article_content: str, 
                              category: str = None) -> Optional[str]:
        """
        Generate an image for an article using available services.
        
        Args:
            article_title: Title of the article
            article_content: Content of the article
            category: Article category
            
        Returns:
            Path to generated image file or None if failed
        """
        logger.info(f"Generating image for article: {article_title[:50]}...")
        
        # Try Replicate first (AI generation)
        if self.replicate_token:
            image_path = self._generate_with_replicate(article_title, article_content)
            if image_path:
                return image_path
            logger.warning("Replicate generation failed, trying fallbacks")
        
        # Try Pexels (stock photos)
        if self.pexels_key:
            image_path = self._get_from_pexels(article_title, category)
            if image_path:
                return image_path
            logger.warning("Pexels failed, trying next fallback")
        
        # Try Unsplash (stock photos)
        if self.unsplash_key:
            image_path = self._get_from_unsplash(article_title, category)
            if image_path:
                return image_path
            logger.warning("Unsplash failed, using placeholder")
        
        # Fallback to placeholder with text
        return self._create_placeholder_image(article_title)
    
    def _generate_with_replicate(self, title: str, content: str) -> Optional[str]:
        """Generate image using Replicate API."""
        try:
            import replicate
            
            # Create prompt from article
            prompt = self._create_image_prompt(title, content)
            
            logger.info("Generating image with Replicate...")
            
            # Use Stable Diffusion XL
            output = replicate.run(
                "stability-ai/stable-diffusion-xl:877f9547ed3f549c65a5de8486bf791aaefc6ebde9ec565fe6b258dc58d0adba",
                input={
                    "prompt": prompt,
                    "width": Config.ARTICLE_IMAGE_WIDTH,
                    "height": Config.ARTICLE_IMAGE_HEIGHT,
                    "num_outputs": 1,
                    "num_inference_steps": 30,
                    "guidance_scale": 7.5
                }
            )
            
            if output and len(output) > 0:
                image_url = output[0]
                return self._download_and_save_image(image_url, title)
            
        except Exception as e:
            logger.error(f"Replicate generation failed: {e}")
        
        return None
    
    def _create_image_prompt(self, title: str, content: str) -> str:
        """Create a satirical image prompt from article content."""
        
        # Extract key themes from content
        content_sample = content[:500]
        
        prompt = f"""
Create a satirical news photo illustration for this article:

Title: {title}
Content: {content_sample}

Style requirements:
- Deadpan, serious news photography style
- Slightly absurd or surreal elements
- Professional lighting and composition
- Realistic but with humorous twist
- No text or watermarks
- Editorial photography aesthetic
- Subtle comedy in the imagery

Make it look like a legitimate news photo but with clearly absurd elements that match the satirical nature of the story.
"""
        return prompt.strip()
    
    def _get_from_pexels(self, title: str, category: str = None) -> Optional[str]:
        """Get relevant stock photo from Pexels."""
        try:
            # Search terms based on title and category
            search_terms = self._extract_search_terms(title, category)
            
            for term in search_terms[:3]:  # Try up to 3 search terms
                url = f"https://api.pexels.com/v1/search"
                headers = {"Authorization": self.pexels_key}
                params = {"query": term, "per_page": 1, "orientation": "landscape"}
                
                response = requests.get(url, headers=headers, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                if data.get("photos"):
                    photo = data["photos"][0]
                    image_url = photo["src"]["large"]
                    return self._download_and_save_image(image_url, title)
                    
        except Exception as e:
            logger.error(f"Pexels API failed: {e}")
        
        return None
    
    def _get_from_unsplash(self, title: str, category: str = None) -> Optional[str]:
        """Get relevant stock photo from Unsplash."""
        try:
            search_terms = self._extract_search_terms(title, category)
            
            for term in search_terms[:3]:
                url = f"https://api.unsplash.com/search/photos"
                headers = {"Authorization": f"Client-ID {self.unsplash_key}"}
                params = {"query": term, "per_page": 1, "orientation": "landscape"}
                
                response = requests.get(url, headers=headers, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                if data.get("results"):
                    photo = data["results"][0]
                    image_url = photo["urls"]["regular"]
                    return self._download_and_save_image(image_url, title)
                    
        except Exception as e:
            logger.error(f"Unsplash API failed: {e}")
        
        return None
    
    def _extract_search_terms(self, title: str, category: str = None) -> list:
        """Extract relevant search terms from title and category."""
        terms = []
        
        # Add category if available
        if category:
            terms.append(category)
        
        # Extract key words from title
        title_words = title.lower().split()
        # Filter out common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'was', 'are', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'}
        
        meaningful_words = [word for word in title_words if word not in stop_words and len(word) > 2]
        terms.extend(meaningful_words[:3])  # Take first 3 meaningful words
        
        return [term for term in terms if term]
    
    def _download_and_save_image(self, image_url: str, title: str) -> Optional[str]:
        """Download image from URL and save locally."""
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Generate filename
            safe_title = "".join(c for c in title[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{safe_title}_{random.randint(1000, 9999)}.jpg"
            filepath = os.path.join(self.image_dir, filename)
            
            # Save image
            image = Image.open(BytesIO(response.content))
            
            # Resize if needed
            if image.size != (Config.ARTICLE_IMAGE_WIDTH, Config.ARTICLE_IMAGE_HEIGHT):
                image = image.resize((Config.ARTICLE_IMAGE_WIDTH, Config.ARTICLE_IMAGE_HEIGHT), Image.Resampling.LANCZOS)
            
            image.save(filepath, 'JPEG', quality=85)
            logger.info(f"Image saved: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to download/save image: {e}")
        
        return None
    
    def _create_placeholder_image(self, title: str) -> Optional[str]:
        """Create a placeholder image with text overlay."""
        try:
            # Create blank image
            img = Image.new('RGB', (Config.ARTICLE_IMAGE_WIDTH, Config.ARTICLE_IMAGE_HEIGHT), color='#f0f0f0')
            draw = ImageDraw.Draw(img)
            
            # Try to load a font, fallback to default
            try:
                font_large = ImageFont.truetype("arial.ttf", 48)
                font_small = ImageFont.truetype("arial.ttf", 24)
            except:
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Add title text
            title_lines = self._wrap_text(title, 40)
            y_position = 100
            
            for line in title_lines[:3]:  # Max 3 lines
                bbox = draw.textbbox((0, 0), line, font=font_large)
                text_width = bbox[2] - bbox[0]
                x_position = (Config.ARTICLE_IMAGE_WIDTH - text_width) // 2
                
                draw.text((x_position, y_position), line, fill='#333333', font=font_large)
                y_position += 60
            
            # Add subtitle
            subtitle = "Satire News - Image Coming Soon"
            bbox = draw.textbbox((0, 0), subtitle, font=font_small)
            text_width = bbox[2] - bbox[0]
            x_position = (Config.ARTICLE_IMAGE_WIDTH - text_width) // 2
            
            draw.text((x_position, Config.ARTICLE_IMAGE_HEIGHT - 100), subtitle, fill='#666666', font=font_small)
            
            # Save placeholder
            filename = f"placeholder_{random.randint(1000, 9999)}.jpg"
            filepath = os.path.join(self.image_dir, filename)
            
            img.save(filepath, 'JPEG', quality=85)
            logger.info(f"Placeholder image created: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to create placeholder image: {e}")
        
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
