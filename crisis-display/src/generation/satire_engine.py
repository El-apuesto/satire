import json
import random
import requests
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
            ],
            'sports': [
                "Professional athletes announced today that they will consider potentially thinking about maybe possibly competing in upcoming games, according to sources familiar with their thinking patterns.",
                "Sports analysts revealed that teams who practice more tend to win more games, in a study that confirmed what fans already suspected.",
                "League officials confirmed that balls used in competition are, in fact, round, despite earlier speculation that they might be slightly oval."
            ],
            'music': [
                "Music industry insiders revealed that artists are planning to possibly consider releasing new music at some point in the future, according to sources familiar with their creative process.",
                "Record producers announced a groundbreaking new technology that promises to revolutionize how listeners experience songs they already enjoy.",
                "Music critics praised the bold decision to use silence as a creative element in the latest album, calling it 'a revolutionary approach to not making noise.'"
            ],
            'world': [
                "Global leaders gathered today to discuss potentially addressing issues that might need consideration at some point in the future, sources confirmed.",
                "International organizations announced a comprehensive initiative to possibly consider thinking about maybe forming a committee to explore global challenges.",
                "Experts revealed that world events are, in fact, occurring in various locations simultaneously, in findings that have stunned observers."
            ],
            'advice': [
                "DEAR GABBY: My boyfriend keeps leaving his socks everywhere. Is this a cry for help or just poor laundry skills? - SOCKLESS IN SEATTLE",
                "DEAR GABBY: My neighbor's dog only barks when I'm home. Should I be flattered or concerned? - BARKING MAD IN BOSTON",
                "DEAR GABBY: My coworker brings a cactus to every meeting. Is this normal office behavior or am I missing something? - PRICKLY SITUATION IN PHOENIX",
                "DEAR GABBY: My husband thinks 'Netflix and chill' means watching documentaries about streaming services. How do I fix this? - DOCUMENTARY DISASTER IN DENVER",
                "DEAR GABBY: My roommate organizes their spice rack alphabetically. Is this genius or madness? - SPICE GIRL IN AUSTIN"
            ],
            'mens_dating': [
                "DEAR GABBY: Women keep telling me they want a 'sensitive guy' but then date guys who treat them terribly. What's the deal? - CONFUSED IN CHICAGO",
                "DEAR GABBY: My girlfriend says I don't listen, but I literally just heard her say she wanted tacos for dinner and I ordered pizza. Am I wrong? - TACO TUESDAY IN MIAMI",
                "DEAR GABBY: Why do women say 'nothing's wrong' when something is clearly wrong? I've been studying this for years and still can't crack the code. - RESEARCHER IN ATLANTA",
                "DEAR GABBY: My date spent 45 minutes taking selfies of our food. Should I be impressed or concerned about her priorities? - FILTER FREE IN SEATTLE",
                "DEAR GABBY: Women complain men don't communicate, but when I try to talk about feelings, they suddenly remember they have to check their phone. - SILENT TREATMENT IN BOSTON"
            ],
            'womens_dating': [
                "DEAR GABBY: Why do men think 'I'm fine' means 'please tell me what's wrong'? It literally means I'm fine. - FINE REALLY IN DALLAS",
                "DEAR GABBY: My boyfriend showed up to our anniversary with a gas station bouquet. Should I be touched or start looking for apartments? - PUMPED UP IN HOUSTON",
                "DEAR GABBY: Men say they want an 'independent woman' but get intimidated when I make more money than them. Make it make sense. - INDEPENDENTLY WEALTHY IN LA",
                "DEAR GABBY: Why do guys think fixing a leaky faucet makes them marriage material? I hired a plumber. - DRIPPING WITH sarcasm IN CHICAGO",
                "DEAR GABBY: My date spent the whole dinner talking about his ex. Is this a red flag or just a really long story? - EX FILES IN NEW YORK"
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
        
        # Generate related image
        image_url = self.generate_related_image(headline, category)
        
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
            'image_url': image_url,
            'source_url': original_article.get('url', ''),
            'original_title': original_article.get('title', '')
        }
        
        return satire_article
    
    def create_satire_headline(self, original_title: str, category: str) -> str:
        """Create deadpan absurd headline from original title"""
        
        # Extract key elements from original title
        words = original_title.lower().split()
        
        # Deadpan absurd patterns
        patterns = {
            'politics': [
                f"Local Officials Make {random.choice(['Bold', 'Historic', 'Unprecedented'])} Decision To {random.choice(['Consider', 'Think About', 'Ponder'])} {original_title.title()}",
                f"In Move That Stunned {random.choice(['Absolutely No One', 'Experts', 'Local Residents'])}, Politicians {random.choice(['Announce', 'Declare', 'Proclaim'])} Plans Regarding {original_title.title()}",
                f"{original_title.title()} Described As '{random.choice(['Most Important Issue Of Our Time', 'Game-Changer', 'Paradigm Shift'])}' By People Who Should Know Better"
            ],
            'technology': [
                f"New Technology Promises To {random.choice(['Revolutionize', 'Transform', 'Completely Change'])} How We {random.choice(['Think About', 'Interact With', 'Experience'])} {original_title.title()}",
                f"Startup Raises {random.choice(['$50 Million', '$100 Million', 'Undisclosed Amount'])} For {original_title.title()} - Something That Already Existed",
                f"Experts Agree {original_title.title()} Is '{random.choice(['The Future', 'Disruptive Innovation', 'Game-Changer'])}' Despite Having No Idea What It Is"
            ],
            'science': [
                f"Study Reveals {random.choice(['Shocking', 'Surprising', 'Mind-Blowing'])} Connection Between {original_title.title()} And {random.choice(['Things We Already Knew', 'Common Sense', 'Reality'])}",
                f"Scientists Discover {original_title.title()} Is, In Fact, {random.choice(['Real', 'True', 'Actually A Thing'])}",
                f"Research Shows {original_title.title()} {random.choice(['Matters', 'Is Important', 'Exists'])} In Findings That {random.choice(['Confirm Obvious', 'State The Obvious', 'Tell Us What We Already Know'])}"
            ],
            'sports': [
                f"Athletes {random.choice(['Shocked', 'Amazed', 'Stunned'])} By Discovery That {original_title.title()} {random.choice(['Affects Performance', 'Is Important', 'Matters'])}",
                f"Study Shows {original_title.title()} {random.choice(['Helps', 'Hurts', 'Changes'])} Athletic Performance In Ways Everyone Already Knew",
                f"Sports World Reacts To {original_title.title()} With {random.choice(['Surprise', 'Shock', 'Complete Lack Of Surprise'])}"
            ],
            'entertainment': [
                f"{original_title.title()} {random.choice(['Changes Everything', 'Redefines Genre', 'Sets New Standard'])} According To People Who Get Paid To Say That",
                f"Critics Describe {original_title.title()} As '{random.choice(['Masterpiece', 'Game-Changer', 'Revolutionary'])}' In Reviews That Sound Like Every Other Review",
                f"Industry Insiders Agree {original_title.title()} Is '{random.choice(['The Future', 'What People Want', 'Revolutionary'])}' For Reasons That Remain Unclear"
            ],
            'business': [
                f"CEOs {random.choice(['Stunned', 'Shocked', 'Completely Surprised'])} By Discovery That {original_title.title()} {random.choice(['Affects Profits', 'Matters To Shareholders', 'Changes Everything'])}",
                f"Market Reacts To {original_title.title()} With {random.choice(['Wild Enthusiasm', 'Complete Indifference', 'Predictable Panic'])}",
                f"Business Experts Agree {original_title.title()} Is '{random.choice(['Game-Changer', 'Paradigm Shift', 'Revolutionary'])}' Despite Nobody Understanding What It Is"
            ],
            'finance': [
                f"Wall Street {random.choice(['Stunned', 'Shocked', 'Completely Amazed'])} By {original_title.title()} In Move That {random.choice(['Changes Everything', 'Changes Nothing', 'Changes Something Slightly'])}",
                f"Financial Experts Describe {original_title.title()} As '{random.choice(['Historic', 'Unprecedented', 'Completely Expected'])}' Development In Market That Does What It Always Does",
                f"Investors React To {original_title.title()} With {random.choice(['Optimism', 'Panic', 'Utter Confusion'])} Despite Having No Idea What Just Happened"
            ],
            'health': [
                f"Medical Community {random.choice(['Stunned', 'Shocked', 'Completely Amazed'])} By Discovery That {original_title.title()} {random.choice(['Affects Health', 'Matters', 'Is Actually True'])}",
                f"Study Shows {original_title.title()} {random.choice(['Helps', 'Hurts', 'Changes'])} Health In Ways Everyone Already Knew",
                f"Health Experts Agree {original_title.title()} Is '{random.choice(['Revolutionary', 'Game-Changer', 'Exactly What We Expected'])}' In Findings That Surprise Absolutely No One"
            ],
            'world': [
                f"Global Leaders {random.choice(['Stunned', 'Shocked', 'Completely Surprised'])} By {original_title.title()} In Development That {random.choice(['Changes Everything', 'Changes Nothing', 'Was Inevitable'])}",
                f"International Community Reacts To {original_title.title()} With {random.choice(['Concern', 'Indifference', 'Complete Surprise'])}",
                f"World Experts Agree {original_title.title()} Is '{random.choice(['Historic', 'Unprecedented', 'Business As Usual'])}' Despite It Happening Regularly"
            ]
        }
        
        category_patterns = patterns.get(category, patterns['science'])
        return random.choice(category_patterns)
    
    def create_satire_opening(self, original_content: str, category: str) -> str:
        """Create satirical opening paragraph"""
        
        # Filter out placeholder content
        if original_content and "ONLY AVAILABLE IN PAID PLANS" in original_content:
            original_content = "recent developments"
        
        templates = self.satire_templates.get(category, self.satire_templates['science'])
        base_template = random.choice(templates)
        
        # Add category-specific opening
        if category == 'politics':
            buzzword = random.choice(self.bureaucratic_phrases)
            return f"{base_template} The initiative involves a {buzzword} that stakeholders believe will lead to optimal outcomes through synergistic engagement."
        elif category == 'technology':
            buzzword = random.choice(self.corporate_buzzwords)
            return f"{base_template} The {buzzword} solution leverages cutting-edge technology to disrupt traditional workflows while maximizing user engagement."
        elif category == 'business':
            return f"{base_template} The announcement sent shockwaves through Wall Street, with investors scrambling to adjust their portfolios in response to {original_content[:50] if original_content else 'market conditions'}."
        elif category == 'finance':
            return f"{base_template} Market analysts were completely stunned by the development, describing it as '{random.choice(['unprecedented', 'shocking', 'surprising'])}' in a sector that rarely sees {original_content[:50] if original_content else 'surprising developments'}."
        elif category == 'health':
            return f"{base_template} Medical researchers were amazed by the findings, which could revolutionize how we approach {original_content[:50] if original_content else 'healthcare'}."
        elif category == 'world':
            return f"{base_template} Global leaders scrambled to respond to the breaking news about {original_content[:50] if original_content else 'international developments'}, calling emergency meetings to address the situation."
        elif category == 'sports':
            return f"{base_template} The sports world was rocked by the revelation, with coaches and athletes alike struggling to comprehend how {original_content[:50] if original_content else 'this development'} might affect performance."
        elif category == 'entertainment':
            return f"{base_template} Industry insiders were buzzing about the news, with many calling it '{random.choice(['groundbreaking', 'revolutionary', 'game-changing'])}' in a field that desperately needs something to talk about."
        else:
            return f"{base_template} The findings, published in a prestigious journal, have important implications for our understanding of things we already understood."
    
    def create_satire_body(self, original_content: str, category: str) -> List[str]:
        """Create deadpan absurd body paragraphs from original content"""
        
        # Filter out placeholder content
        if original_content and "ONLY AVAILABLE IN PAID PLANS" in original_content:
            original_content = "recent developments that have captured public attention"
        
        # Extract key elements from original content
        content_words = original_content.lower().split() if original_content else ["something", "happened"]
        
        paragraphs = []
        
        if category == 'politics':
            paragraphs.append(f"The announcement, which took approximately {random.randint(30, 90)} minutes to deliver, was met with {random.choice(['cautious optimism', 'utter indifference', 'complete surprise'])} from residents who have grown accustomed to {random.choice(['delayed responses', 'empty promises', 'political theater'])}.")
            paragraphs.append(f"Mayor Thompson explained that this proactive approach to potentially addressing {original_content[:50] if original_content else 'community issues'} represents a bold step forward in municipal governance, even though no specific timeline was provided for when actual consideration might begin.")
            paragraphs.append(f"Opposition parties criticized the plan as '{random.choice(['too ambitious', 'not ambitious enough', 'exactly what you would expect'])}', suggesting that forming a committee to consider discussing issues might set an unrealistic precedent for taking action.")
            
        elif category == 'technology':
            paragraphs.append(f"The new platform, which requires {random.randint(2, 5)} separate apps and a monthly subscription, adds several additional steps to processes that previously took seconds to complete.")
            paragraphs.append(f"Investors have poured ${random.randint(10, 100)} million into the venture, citing the enormous potential of convincing people they need solutions to problems they didn't know they had.")
            paragraphs.append(f"Early adopters report being '{random.choice(['impressed', 'confused', 'both'])}' in equal measure, with many praising the innovation while struggling to understand what it actually does.")
            
        elif category == 'science':
            paragraphs.append(f"The {random.randint(3, 10)}-year study followed {random.randint(1000, 10000)} participants, {random.randint(60, 95)}% of whom were included in at least one study during the research period.")
            paragraphs.append(f"Researchers noted that participants who {random.choice(['read the most studies', 'breathed air', 'existed'])} were {random.randint(200, 500)}% more likely to be cited in subsequent studies about people who {random.choice(['read studies', 'breathe air', 'exist'])}.")
            paragraphs.append(f"The scientific community has hailed the findings as '{random.choice(['revolutionary', 'obvious', 'both'])}' and '{random.choice(['groundbreaking', 'predictable', 'expected'])}', with calls for additional funding to study why studies require so much funding.")
            
        elif category == 'sports':
            paragraphs.append(f"The discovery has sent shockwaves through the athletic community, with players reportedly {random.choice(['stunned', 'amazed', 'completely unfazed'])} by the revelation that {original_content[:50] if original_content else 'basic athletic principles'} might affect performance.")
            paragraphs.append(f"Coaches are already incorporating these findings into training regimens, adding {random.randint(1, 4)} new drills to practice sessions that already last {random.randint(2, 6)} hours.")
            paragraphs.append(f"League officials are considering rule changes based on the research, though insiders suggest any changes will be implemented {random.choice(['immediately', 'after extensive study', 'never'])}.")
            
        elif category == 'entertainment':
            paragraphs.append(f"Industry insiders are calling the development '{random.choice(['game-changing', 'revolutionary', 'exactly like everything else'])}' in a field that desperately needs something to talk about.")
            paragraphs.append(f"Experts predict this will {random.choice(['change everything', 'change nothing', 'change something slightly'])} for the next {random.randint(6, 24)} months, at which point something else will become the thing that changes everything.")
            paragraphs.append(f"Fans have reacted with {random.choice(['enthusiasm', 'indifference', 'confusion'])}, with many taking to social media to express opinions that will be completely forgotten by tomorrow.")
            
        elif category == 'business':
            paragraphs.append(f"The announcement, which took approximately {random.randint(15, 60)} minutes to deliver, was met with {random.choice(['wild enthusiasm', 'complete indifference', 'market panic'])} from investors who have grown accustomed to {random.choice(['corporate jargon', 'empty promises', 'quarterly earnings calls'])}.")
            paragraphs.append(f"CEO Thompson explained that this proactive approach to potentially addressing {original_content[:50] if original_content else 'market conditions'} represents a bold step forward in corporate governance, even though no specific timeline was provided for when actual profits might begin.")
            paragraphs.append(f"Market analysts criticized the plan as '{random.choice(['too ambitious', 'not ambitious enough', 'exactly what you would expect'])}', suggesting that forming a committee to consider discussing quarterly results might set an unrealistic precedent for taking action.")
            
        elif category == 'finance':
            paragraphs.append(f"The financial markets reacted with {random.choice(['wild optimism', 'utter panic', 'complete confusion'])} to the development, with traders reportedly {random.choice(['buying everything', 'selling everything', 'doing nothing'])} in response to {original_content[:50] if original_content else 'market news'}.")
            paragraphs.append(f"Wall Street experts explained that this represents either a {random.choice(['major turning point', 'minor inconvenience', 'complete non-event'])} in the ongoing saga of numbers going up and down for reasons nobody understands.")
            paragraphs.append(f"Federal Reserve officials are considering policy changes based on the news, though insiders suggest any changes will be implemented {random.choice(['immediately', 'after extensive study', 'never'])}.")
            
        elif category == 'health':
            paragraphs.append(f"The medical community was {random.choice(['stunned', 'shocked', 'completely amazed'])} by the discovery, with doctors reportedly {random.choice(['reconsidering everything', 'confirming what they already knew', 'asking for more funding'])}.")
            paragraphs.append(f"The {random.randint(5, 15)}-year study followed {random.randint(500, 5000)} participants, {random.randint(60, 95)}% of whom were {random.choice(['surprised by the findings', 'not surprised at all', 'confused by the methodology'])}.")
            paragraphs.append(f"Health experts are calling for {random.choice(['immediate action', 'more research', 'a balanced approach'])}, though most agree that {original_content[:50] if original_content else 'this health issue'} probably {random.choice(['matters', 'doesnt matter', 'might matter slightly'])}.")
            
        elif category == 'world':
            paragraphs.append(f"Global leaders gathered to discuss the development, which has been described as '{random.choice(['historic', 'unprecedented', 'business as usual'])}' by people who get paid to describe things as historic.")
            paragraphs.append(f"The international community reacted with {random.choice(['concern', 'indifference', 'complete surprise'])} to the news, with many nations {random.choice(['calling for action', 'ignoring it completely', 'forming committees'])}.")
            paragraphs.append(f"United Nations officials are considering a resolution regarding {original_content[:50] if original_content else 'global issues'}, though insiders suggest any resolution will be {random.choice(['immediately implemented', 'ignored completely', 'vetoed by major powers'])}.")
            
        else:  # general/fallback
            paragraphs.append(f"The situation, which has been developing for {random.randint(1, 10)} years, has finally reached the point where people are talking about it, at least until something more interesting happens.")
            paragraphs.append(f"Experts agree that this represents either a {random.choice(['major turning point', 'minor inconvenience', 'complete non-event'])} in the ongoing saga of things that happen.")
            paragraphs.append(f"Further research is planned, though most expect the findings to confirm what everyone already suspected all along.")
        
        return paragraphs
    
    def create_expert_quotes(self, category: str) -> List[Dict[str, str]]:
        """Generate satirical expert quotes"""
        quotes = []
        
        if category == 'politics':
            quotes.append({
                'expert': 'Dr. Patricia Roberts',
                'affiliation': 'Institute for Political Satire Studies',
                'quote': 'This represents a paradigm shift in governmental procrastination. We\'re moving from ignoring problems to actively ignoring them in a more structured way.'
            })
            quotes.append({
                'expert': 'Jennifer Walsh',
                'affiliation': 'Municipal Governance Institute',
                'quote': 'The formation of a committee to consider discussing issues is truly groundbreaking. It\'s like democracy, but with more meetings.'
            })
        elif category == 'technology':
            quotes.append({
                'expert': 'Dr. Christopher Chen',
                'affiliation': 'Silicon Valley Analyst',
                'quote': 'This is exactly what the market was missing - a way to monetize simplicity by making it feel exclusive and complicated.'
            })
            quotes.append({
                'expert': 'Mark Stevens',
                'affiliation': 'Tech Innovation Lab',
                'quote': 'The beauty of this solution is that it creates problems that only it can solve, which is the essence of disruptive innovation.'
            })
        elif category == 'science':
            quotes.append({
                'expert': 'Dr. Emily Watson',
                'affiliation': 'Institute of Obvious Conclusions',
                'quote': 'This research confirms what we suspected All along - things are, in fact, the way they are. The implications are staggering.'
            })
            quotes.append({
                'expert': 'Dr. Robert Miller',
                'affiliation': 'Center for Academic Research',
                'quote': 'Our findings suggest a self-perpetuating cycle of study-reading that could revolutionize how we conduct future studies about study-reading patterns.'
            })
        elif category == 'sports':
            quotes.append({
                'expert': 'Coach Michael Richardson',
                'affiliation': 'Sports Analytics Institute',
                'quote': 'This represents a paradigm shift in athletic performance analysis. We\'re moving from simply watching games to actually understanding why athletes win by not winning at all.'
            })
            quotes.append({
                'expert': 'Jessica Martinez',
                'affiliation': 'Athletic Performance Journal',
                'quote': 'The data shows that teams who practice less tend to have better injury outcomes, in findings that have stunned the sports medicine community.'
            })
        elif category == 'music':
            quotes.append({
                'expert': 'Dr. David Chen',
                'affiliation': 'Music Industry Weekly',
                'quote': 'The trend toward silence in music production reflects a fundamental shift in how artists express creativity, or rather, the lack thereof.'
            })
            quotes.append({
                'expert': 'Maria Rodriguez',
                'affiliation': 'Audio Engineering Magazine',
                'quote': 'Artists are increasingly using technology to create sounds that never existed, which is either revolutionary or deeply confusing to everyone involved.'
            })
        elif category == 'world':
            quotes.append({
                'expert': 'Dr. James Wilson',
                'affiliation': 'Global Affairs Institute',
                'quote': 'International diplomacy increasingly resembles a reality show where everyone knows the script but pretends to be improvising.'
            })
            quotes.append({
                'expert': 'Dr. Sarah Thompson',
                'affiliation': 'World Policy Forum',
                'quote': 'Global events are, in fact, occurring in various locations simultaneously, which suggests either unprecedented coordination or widespread coincidence.'
            })
        
        elif category == 'business':
            quotes.append({
                'expert': 'Dr. Michael Thompson',
                'affiliation': 'Harvard Business Review',
                'quote': 'This represents a paradigm shift in corporate strategy. We\'re moving from ignoring market trends to actively ignoring them in a more structured way.'
            })
            quotes.append({
                'expert': 'Jennifer Walsh',
                'affiliation': 'Wall Street Analytics',
                'quote': 'The beauty of this business model is that it creates problems that only it can solve, which is the essence of disruptive innovation.'
            })
        elif category == 'finance':
            quotes.append({
                'expert': 'Dr. Robert Chen',
                'affiliation': 'Federal Reserve Institute',
                'quote': 'This represents either unprecedented coordination or widespread coincidence in financial markets, depending on who you ask.'
            })
            quotes.append({
                'expert': 'Sarah Martinez',
                'affiliation': 'Investment Weekly',
                'quote': 'The data suggests that money goes up and down for reasons that make sense only in retrospect, which is the essence of financial analysis.'
            })
        elif category == 'health':
            quotes.append({
                'expert': 'Dr. Emily Watson',
                'affiliation': 'Medical Journal Today',
                'quote': 'This research confirms what doctors suspected all along - health is, in fact, affected by things that affect health.'
            })
            quotes.append({
                'expert': 'Dr. Richard Kim',
                'affiliation': 'Global Health Organization',
                'quote': 'Our findings suggest a self-perpetuating cycle of health advice that could revolutionize how we give health advice about giving health advice.'
            })
        elif category == 'world':
            quotes.append({
                'expert': 'Dr. James Wilson',
                'affiliation': 'International Affairs Institute',
                'quote': 'Global events are, in fact, occurring in various locations simultaneously, which suggests either unprecedented coordination or widespread coincidence.'
            })
            quotes.append({
                'expert': 'Dr. Anna Petrova',
                'affiliation': 'United Nations Policy Forum',
                'quote': 'International diplomacy increasingly resembles a reality show where everyone knows the script but pretends to be improvising.'
            })
        
        return quotes
    
    def generate_byline(self, category: str) -> str:
        """Generate satirical author names"""
        authors = {
            'politics': ['Patricia Roberts', 'Jennifer Walsh', 'Tom Harris'],
            'technology': ['Dr. Christopher Chen', 'Mark Stevens', 'Lisa Chang'],
            'science': ['Dr. Emily Watson', 'Dr. Robert Miller', 'Dr. Jennifer Lee', 'Dr. Richard Kim'],
            'sports': ['Coach Michael Richardson', 'Jessica Martinez', 'Chris Johnson'],
            'music': ['Dr. David Chen', 'Maria Rodriguez', 'Emily Taylor', 'Justin Timberlake'],
            'world': ['Dr. James Wilson', 'Sarah Thompson', 'Michael Davis', 'Anna Petrova'],
            'business': ['Dr. Michael Thompson', 'Jennifer Walsh', 'Tom Anderson'],
            'finance': ['Dr. Robert Chen', 'Sarah Martinez', 'Mark Johnson'],
            'health': ['Dr. Emily Watson', 'Dr. Richard Kim', 'Lisa Davis'],
            'entertainment': ['Dr. David Chen', 'Maria Rodriguez', 'Emily Taylor'],
            'advice': ['Gabby Thompson'],
            'mens_dating': ['Guy Breux'],
            'womens_dating': ['Gabby Thompson']
        }
        
        category_authors = authors.get(category, authors['science'])
        return random.choice(category_authors)
    
    def generate_related_image(self, headline: str, category: str) -> str:
        """Generate or find a related image for the article"""
        return None  # Only generate images for featured story
    
    def batch_generate_satire(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert multiple articles to satire"""
        satire_articles = []
        
        for i, article in enumerate(articles):
            try:
                satire_article = self.generate_satire_article(article)
                
                # Only generate image for the first article (featured story)
                if i == 0:
                    satire_article['image_url'] = self.generate_featured_image(satire_article['headline'], satire_article['category'])
                else:
                    satire_article['image_url'] = None
                    
                satire_articles.append(satire_article)
            except Exception as e:
                print(f"Error generating satire for article: {e}")
                continue
        
        return satire_articles
    
    def generate_featured_image(self, headline: str, category: str) -> str:
        """Generate image only for featured story"""
        try:
            image_keywords = {
                'politics': ['government', 'politics', 'election', 'congress'],
                'technology': ['tech', 'computer', 'innovation', 'digital'],
                'science': ['science', 'research', 'laboratory', 'discovery'],
                'sports': ['sports', 'athlete', 'competition', 'stadium'],
                'music': ['music', 'concert', 'performance', 'studio'],
                'world': ['world', 'global', 'international', 'news'],
                'entertainment': ['entertainment', 'movie', 'celebrity', 'show'],
                'business': ['business', 'finance', 'corporate', 'office'],
                'finance': ['finance', 'money', 'market', 'trading'],
                'health': ['health', 'medical', 'hospital', 'doctor'],
                'lifestyle': ['lifestyle', 'health', 'wellness', 'living']
            }
            
            # Extract keywords from headline
            headline_words = headline.lower().split()
            category_words = image_keywords.get(category.lower(), ['news'])
            
            # Find best matching keyword
            for word in headline_words:
                for cat_word in category_words:
                    if word in cat_word or cat_word in word:
                        return f"https://picsum.photos/800/400?random={random.randint(1,1000)}&blur=1"
            
            # Fallback to category-based image
            return f"https://picsum.photos/800/400?random={random.randint(1,1000)}&blur=1"
            
        except Exception as e:
            print(f"Error generating image: {e}")
            return "https://picsum.photos/800/400?random=999&blur=1"
