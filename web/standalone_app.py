#!/usr/bin/env python3
"""
Standalone OK Crisis website - no dependencies
"""

from flask import Flask, render_template

app = Flask(__name__, static_folder='static')

# Sample articles - completely self-contained
sample_articles = [
    {
        'id': 1,
        'headline': 'Local Government Announces Plans to Consider Thinking About Maybe Addressing Issues Someday',
        'opening_paragraph': 'City officials held a press conference today to announce their intention to form a committee that will explore the possibility of discussing potential challenges that might need consideration at some point in the future.',
        'category': 'politics',
        'byline': 'Sarah Johnson',
        'timestamp': '2024-01-15T10:00:00Z',
        'body_paragraphs': [
            'The announcement, which took approximately 45 minutes to deliver, was met with cautious optimism from residents who have grown accustomed to delayed responses to community needs.',
            'Mayor Thompson explained that this proactive approach to potentially addressing issues represents a bold step forward in municipal governance, even though no specific timeline was provided for when actual consideration might begin.'
        ],
        'expert_quotes': [
            {
                'expert': 'Dr. Michael Roberts',
                'affiliation': 'University of Public Policy Studies',
                'quote': 'This represents a paradigm shift in governmental procrastination. We\'re moving from ignoring problems to actively ignoring them in a more structured way.'
            }
        ]
    },
    {
        'id': 2,
        'headline': 'Tech Startup Disrupts Industry By Making Things Slightly More Complicated',
        'opening_paragraph': 'Innovation Labs unveiled groundbreaking new technology today that promises to revolutionize how people interact with things they already knew how to use.',
        'category': 'technology',
        'byline': 'Mark Chen',
        'timestamp': '2024-01-15T14:30:00Z',
        'body_paragraphs': [
            'The new platform, which requires three separate apps and a monthly subscription, adds several additional steps to processes that previously took seconds to complete.',
            'Investors have poured $50 million into the venture, citing the enormous potential of convincing people they need solutions to problems they didn\'t know they had.'
        ],
        'expert_quotes': [
            {
                'expert': 'Jennifer Walsh',
                'affiliation': 'Silicon Valley Analyst',
                'quote': 'This is exactly what the market was missing - a way to monetize simplicity by making it feel exclusive and complicated.'
            }
        ]
    },
    {
        'id': 3,
        'headline': 'Study Finds People Who Read Studies Are More Likely To Be In Studies',
        'opening_paragraph': 'Groundbreaking research from the Institute of Obvious Conclusions reveals a strong correlation between reading studies and being included in future studies.',
        'category': 'science',
        'byline': 'Dr. Emily Watson',
        'timestamp': '2024-01-15T09:15:00Z',
        'body_paragraphs': [
            'The five-year study followed 10,000 participants, 87% of whom were included in at least one study during the research period.',
            'Researchers noted that participants who read the most studies were 300% more likely to be cited in subsequent studies about people who read studies.'
        ],
        'expert_quotes': [
            {
                'expert': 'Dr. Robert Miller',
                'affiliation': 'Center for Academic Research',
                'quote': 'Our findings suggest a self-perpetuating cycle of study-reading that could revolutionize how we conduct future studies about study-reading patterns.'
            }
        ]
    }
]

def get_article_by_id(article_id):
    """Get article by ID from sample data."""
    try:
        article_id = int(article_id)
        for article in sample_articles:
            if article['id'] == article_id:
                return article
        return None
    except (ValueError, TypeError):
        return None

@app.route('/')
def home():
    """Homepage with latest articles."""
    featured_article = sample_articles[0] if sample_articles else None
    other_articles = sample_articles[1:] if len(sample_articles) > 1 else []
    
    return render_template('index.html', 
                        featured_article=featured_article,
                        other_articles=other_articles)

@app.route('/article/<int:article_id>')
def article(article_id):
    """Individual article page."""
    article = get_article_by_id(article_id)
    
    if not article:
        return render_template('404.html'), 404
    
    # For now, return empty related articles
    related_articles = sample_articles[:3]
    
    return render_template('article.html', 
                        article=article,
                        related_articles=related_articles)

@app.route('/category/<category>')
def category(category):
    """Category page."""
    # Filter articles by category
    filtered_articles = [article for article in sample_articles if article['category'] == category]
    
    return render_template('category.html',
                        category=category,
                        articles=filtered_articles)

@app.route('/about')
def about():
    """About page."""
    return render_template('about.html')

@app.route('/romance')
def romance():
    """Romance and dating section."""
    return render_template('romance.html')

@app.route('/dear-gabby')
def dear_gabby():
    """Dear Gabby advice column."""
    return render_template('dear_gabby.html')

if __name__ == '__main__':
    print("🚀 Starting STANDALONE OK Crisis app...")
    print("📍 Available at: http://localhost:5000")
    print("📍 Press Ctrl+C to stop")
    app.run(debug=True, host='0.0.0.0', port=5000)
