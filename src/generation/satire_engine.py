import json
import random
from datetime import datetime
from typing import Dict, List, Any

class SatireEngine:
    def __init__(self):
        self.satire_templates = self.load_satire_templates()
        self.exaggeration_words = [
            'breathtakingly', 'shockingly', 'unbelievably', 'astonishingly',
            'mind-bogglingly', 'jaw-droppingly', 'spectacularly', 'dramatically'
        ]
        
        self.corporate_buzzwords = [
            'synergistic', 'paradigm-shifting', 'leveraging', 'optimizing',
            'disrupting', 'innovating', 'revolutionizing', 'transforming'
        ]
        
        self.bureaucratic_phrases = [
            'comprehensive review', 'strategic initiative', 'stakeholder engagement',
            'proactive measures', 'synergistic approach', 'optimal outcomes'
        ]
    
    def load_satire_templates(self):
        """Load satire writing templates"""
        return {
            'politics': [
                "Local officials held a press conference today to announce their intention to form a committee that will explore the possibility of discussing potential challenges that might need consideration at some point in the future.",
                "In a groundbreaking move that stunned absolutely no one, politicians promised to 'look into' the issue that has been systematically ignored for the past three decades.",
                "Sources close to the situation reveal that lawmakers are considering taking action, though insiders suggest this consideration may itself be subject to further consideration."
            ],
            'technology': [
                "Tech startup unveiled groundbreaking new technology today that promises to revolutionize how people interact with things they already knew how to use.",
                "Innovation Labs announced a paradigm-shifting platform that adds several additional steps to processes that previously took seconds to complete.",
                "Silicon Valley investors poured millions into a venture that solves a problem nobody had, using technology nobody understands."
            ],
            'science': [
                "Groundbreaking research from the Institute of Obvious Conclusions reveals a strong correlation between things that are obviously related.",
                "Scientists were shocked to discover that water is, in fact, wet, according to a five-year study that cost approximately $3.2 million.",
                "Researchers noted that participants who breathe air tend to live longer than those who don't, in findings that have stunned the scientific community."
            ]
        }
    
    def generate_satire_article(self, original_article: Dict[str, Any]) -> Dict[str, Any]:
        """Convert real news article into satire"""
        category = original_article.get('category', 'general').lower()
        
        # Generate satire headline
        headline = self.create_satire_headline(original_article.get('title', ''), category)
        
        # Generate satire content
        opening_paragraph = self.create_satire_opening(original_article.get('content', ''), category)
        
        # Generate body paragraphs
        body_paragraphs = self.create_satire_body(original_article.get('content', ''), category)
        
        # Generate expert quotes
        expert_quotes = self.create_expert_quotes(category)
        
        # Create satire article
        satire_article = {
            'id': hash(original_article.get('title', '')) % 10000,
            'headline': headline,
            'opening_paragraph': opening_paragraph,
            'category': category,
            'byline': self.generate_byline(category),
            'timestamp': datetime.now().isoformat(),
            'body_paragraphs': body_paragraphs,
            'expert_quotes': expert_quotes,
            'source_url': original_article.get('url', ''),
            'original_title': original_article.get('title', '')
        }
        
        return satire_article
    
    def create_satire_headline(self, original_title: str, category: str) -> str:
        """Create satirical headline from original title"""
        templates = {
            'politics': [
                "Local Government Announces Plans To Consider Thinking About Maybe Addressing Issues Someday",
                "Politicians Promise To 'Strongly Consider' Taking Action On Issue They've Ignored For Years",
                "Bipartisan Agreement Reached To Form Committee To Discuss Potential Future Considerations"
            ],
            'technology': [
                "Tech Startup Disrupts Industry By Making Things Slightly More Complicated",
                "New App Promises To Revolutionize Daily Life By Adding Extra Steps To Simple Tasks",
                "Innovation Unveiled: Company Solves Problem Nobody Had With Technology Nobody Understands"
            ],
            'science': [
                "Study Finds People Who Read Studies Are More Likely To Be In Studies",
                "Research Reveals Shocking Correlation Between Obvious Things And Other Obvious Things",
                "Scientists Discover That Things Are, In Fact, The Way They Appear To Be"
            ]
        }
        
        category_templates = templates.get(category, templates['science'])
        return random.choice(category_templates)
    
    def create_satire_opening(self, original_content: str, category: str) -> str:
        """Create satirical opening paragraph"""
        templates = self.satire_templates.get(category, self.satire_templates['science'])
        base_template = random.choice(templates)
        
        # Add some random corporate/political speak
        if category == 'politics':
            buzzword = random.choice(self.bureaucratic_phrases)
            return f"{base_template} The initiative involves a {buzzword} that stakeholders believe will lead to optimal outcomes through synergistic engagement."
        elif category == 'technology':
            buzzword = random.choice(self.corporate_buzzwords)
            return f"{base_template} The {buzzword} solution leverages cutting-edge technology to disrupt traditional workflows while maximizing user engagement."
        else:
            return f"{base_template} The findings, published in a prestigious journal, have important implications for our understanding of things we already understood."
    
    def create_satire_body(self, original_content: str, category: str) -> List[str]:
        """Create satirical body paragraphs"""
        paragraphs = []
        
        if category == 'politics':
            paragraphs.append("The announcement, which took approximately 45 minutes to deliver, was met with cautious optimism from residents who have grown accustomed to delayed responses to community needs.")
            paragraphs.append("Mayor Thompson explained that this proactive approach to potentially addressing issues represents a bold step forward in municipal governance, even though no specific timeline was provided for when actual consideration might begin.")
            paragraphs.append("Opposition parties criticized the plan as 'too ambitious,' suggesting that forming a committee to consider discussing issues might set an unrealistic precedent for taking action.")
            
        elif category == 'technology':
            paragraphs.append("The new platform, which requires three separate apps and a monthly subscription, adds several additional steps to processes that previously took seconds to complete.")
            paragraphs.append("Investors have poured $50 million into the venture, citing the enormous potential of convincing people they need solutions to problems they didn't know they had.")
            paragraphs.append("Early adopters report being 'impressed' and 'confused' in equal measure, with many praising the innovation while struggling to understand what it actually does.")
            
        else:  # science/general
            paragraphs.append("The five-year study followed 10,000 participants, 87% of whom were included in at least one study during the research period.")
            paragraphs.append("Researchers noted that participants who read the most studies were 300% more likely to be cited in subsequent studies about people who read studies.")
            paragraphs.append("The scientific community has hailed the findings as 'revolutionary' and 'obvious,' with calls for additional funding to study why studies require so much funding.")
        
        return paragraphs
    
    def create_expert_quotes(self, category: str) -> List[Dict[str, str]]:
        """Generate satirical expert quotes"""
        quotes = []
        
        if category == 'politics':
            quotes.append({
                'expert': 'Dr. Michael Roberts',
                'affiliation': 'University of Public Policy Studies',
                'quote': 'This represents a paradigm shift in governmental procrastination. We\'re moving from ignoring problems to actively ignoring them in a more structured way.'
            })
            quotes.append({
                'expert': 'Jennifer Walsh',
                'affiliation': 'Municipal Governance Institute',
                'quote': 'The formation of a committee to consider discussing issues is truly groundbreaking. It\'s like democracy, but with more meetings.'
            })
            
        elif category == 'technology':
            quotes.append({
                'expert': 'Jennifer Walsh',
                'affiliation': 'Sil Valley Analyst',
                'quote': 'This is exactly what the market was missing - a way to monetize simplicity by making it feel exclusive and complicated.'
            })
            quotes.append({
                'expert': 'Mark Chen',
                'affiliation': 'Tech Innovation Lab',
                'quote': 'The beauty of this solution is that it creates problems that only it can solve, which is the essence of disruptive innovation.'
            })
            
        else:  # science/general
            quotes.append({
                'expert': 'Dr. Robert Miller',
                'affiliation': 'Center for Academic Research',
                'quote': 'Our findings suggest a self-perpetuating cycle of study-reading that could revolutionize how we conduct future studies about study-reading patterns.'
            })
            quotes.append({
                'expert': 'Dr. Emily Watson',
                'affiliation': 'Institute of Obvious Conclusions',
                'quote': 'This research confirms what we suspected all along - things are, in fact, the way they are. The implications are staggering.'
            })
        
        return quotes
    
    def generate_byline(self, category: str) -> str:
        """Generate satirical author names"""
        authors = {
            'politics': ['Sarah Johnson', 'Michael Thompson', 'Jennifer Davis'],
            'technology': ['Mark Chen', 'Alex Kumar', 'Sarah Williams'],
            'science': ['Dr. Emily Watson', 'Dr. Robert Miller', 'Dr. Jennifer Lee']
        }
        
        category_authors = authors.get(category, authors['science'])
        return random.choice(category_authors)
    
    def batch_generate_satire(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert multiple articles to satire"""
        satire_articles = []
        
        for article in articles:
            try:
                satire_article = self.generate_satire_article(article)
                satire_articles.append(satire_article)
            except Exception as e:
                print(f"Error generating satire for article: {e}")
                continue
        
        return satire_articles
