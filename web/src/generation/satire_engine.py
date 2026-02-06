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
            ],
            'sports': [
                "Athletes Announce Plans To Possibly Consider Maybe Competing In Upcoming Games",
                "Sports Study Reveals Teams Who Practice More Tend To Win More Games",
                "League Officials Confirm Balls Are Round, Despite Earlier Speculation"
            ],
            'music': [
                "Artists Planning To Possibly Consider Releasing Music At Some Point In Future",
                "Music Industry Announces Technology That Revolutionizes How People Experience Songs",
                "Silence Praised As Revolutionary Creative Element In Latest Album"
            ],
            'world': [
                "Global Leaders Gather To Discuss Potentially Addressing Issues Someday",
                "International Organizations Announce Initiative To Consider Forming Committees",
                "Experts Reveal World Events Occurring In Multiple Locations Simultaneously"
            ],
            'advice': [
                "Dear Abby Columnist Announces Plans To Actually Consider Answering Questions",
                "Advice Column Reveals People Have Problems That Could Be Solved With Common Sense",
                "Readers Write In With Questions That Could Be Answered By Simply Thinking"
            ],
            'mens_dating': [
                "Study Finds Men Who Listen To Women Still Don't Understand What They Said",
                "Research Reveals Men Think 'Nothing's Wrong' Means Something Is Actually Wrong",
                "Scientists Discover Men Who Try To Fix Things Often Make Them Worse"
            ],
            'womens_dating': [
                "Women Announce They're Fine When They're Actually Not Fine, Study Confirms",
                "Research Shows Men Who Think They're Right Usually Aren't, Scientists Say",
                "Dating Experts Confirm Women Always Right, Men Always Wrong"
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
            'advice': ['Gabby Thompson'],
            'mens_dating': ['Guy Breux'],
            'womens_dating': ['Gabby Thompson']
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
