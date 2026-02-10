# Satire News Publishing System

An automated satire news publishing system that operates twice daily to create a humor news website. The system fetches real news stories, evaluates them for satirical potential, transforms them into various styles of satirical articles, generates accompanying images, and publishes them to a sophisticated deadpan news website.

## Features

- **Automated News Aggregation**: Fetches real news from NewsData.io API
- **AI-Powered Story Evaluation**: Uses Google Gemini to evaluate stories for satirical potential
- **Dynamic Article Generation**: Creates satirical articles in multiple styles (deadpan, absurdist, ironic, parody, exaggeration)
- **Image Generation**: Generates article images using Replicate AI with fallbacks to Pexels/Unsplash
- **Comic Strip Creation**: Automatically generates 3-panel comic strips
- **Deadpan News Website**: Professional news website with satirical content
- **Twice-Daily Automation**: Scheduled publishing at 8:00 AM and 8:00 PM CST
- **Comprehensive Logging**: Full system monitoring and error tracking

## System Architecture

### Technical Infrastructure

- **News Source**: NewsData.io Free Tier (100 API calls/day)
- **AI Processing**: Google Gemini 2.0 Flash (1,500 requests/day)
- **Image Generation**: Replicate API + Pexels + Unsplash fallbacks
- **Web Framework**: Flask with Jinja2 templates
- **Scheduling**: Python schedule library
- **Data Storage**: JSON files for articles and comics

### Directory Structure

```
├── src/
│   ├── api/           # News fetching modules
│   ├── evaluators/    # Story evaluation system
│   ├── generators/    # Content generation (articles, images, comics)
│   ├── schedulers/    # Automation system
│   └── website/       # Flask web application
├── templates/        # HTML templates
├── static/           # Static assets (images, comics)
├── config/           # Configuration settings
├── data/             # Published content storage
├── logs/             # System logs
└── requirements.txt  # Python dependencies
```

## Installation

### Prerequisites

- Python 3.8+
- API keys for external services (see Configuration)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd satire-news-system
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Create necessary directories**:
   ```bash
   mkdir -p logs data static/images static/comics
   ```

## Configuration

### Required API Keys

Edit the `.env` file with your API keys:

```env
# News API
NEWSDATA_API_KEY=your_newsdata_io_api_key

# Google Gemini AI
GEMINI_API_KEY=your_google_gemini_api_key

# Image Generation (optional - fallbacks available)
REPLICATE_API_TOKEN=your_replicate_api_token
PEXELS_API_KEY=your_pexels_api_key
UNSPLASH_API_KEY=your_unsplash_api_key
```

### Optional Settings

```env
# Website Configuration
WEBSITE_HOST=localhost
WEBSITE_PORT=5000

# Scheduling
MORNING_RUN_TIME=08:00
EVENING_RUN_TIME=20:00

# Content Generation
ARTICLES_PER_CYCLE=3
COMICS_PER_CYCLE=2
```

## Usage

### Running the System

1. **Start the automated scheduler**:
   ```bash
   python main.py scheduler
   ```

2. **Run the website only**:
   ```bash
   python main.py website
   ```

3. **Run a test cycle**:
   ```bash
   python main.py test
   ```

4. **Run a manual publishing cycle**:
   ```bash
   python main.py manual
   ```

### Website Access

Once running, visit `http://localhost:5000` to view the published satire news website.

## Daily Workflow

The system operates twice daily with the following phases:

### Morning Cycle (8:00 AM CST)
1. **News Aggregation** (8:00-8:05 AM) - Fetch 20-25 stories from last 12 hours
2. **Story Evaluation** (8:05-8:15 AM) - AI evaluates satirical potential
3. **Article Generation** (8:15-8:30 AM) - Create 3-4 satirical articles
4. **Image Generation** (8:30-8:40 AM) - Generate article images
5. **Comic Creation** (8:40-8:50 AM) - Create 2-3 comic strips
6. **Editorial Content** (8:50-8:55 AM) - Generate editorial piece
7. **Publishing** (8:55-9:00 AM) - Publish all content to website

### Evening Cycle (8:00 PM CST)
Same workflow as morning cycle with fresh news content.

## Content Generation

### Satire Styles

The system generates content in multiple satire styles:
- **Deadpan**: Serious tone with absurd content
- **Absurdist**: Completely ridiculous scenarios
- **Ironic**: Dramatic and situational irony
- **Parody**: Mimicking news tropes and genres
- **Exaggeration**: Over-the-top interpretations

### Article Structure

Each generated article includes:
- Compounding headline
- Professional byline
- 3-5 paragraphs with fake quotes
- Accompanying image
- Original story attribution

### Comic Strips

3-panel comics featuring:
- Consistent characters (reporters, experts, officials, citizens)
- Dialogue-based humor
- Simple visual representations
- Story-relevant scenarios

## Monitoring and Maintenance

### Logging

The system provides comprehensive logging:
- File logging: `logs/satire_news.log`
- Console output for real-time monitoring
- Configurable log levels (INFO, DEBUG, WARNING, ERROR)

### Error Handling

- Graceful fallbacks for API failures
- Automatic retry mechanisms
- System recovery procedures
- Detailed error reporting

### Data Management

- Automatic cleanup of temporary files
- Content rotation (keeps latest 50 articles, 20 comics)
- JSON-based storage for easy backup
- Timestamp tracking for all content

## API Limits and Usage

### Daily Limits

- **NewsData.io**: 100 API calls/day (50 per cycle)
- **Google Gemini**: 1,500 requests/day
- **Replicate**: Variable based on plan
- **Pexels/Unsplash**: 200 requests/hour

### Rate Limiting

Built-in rate limiting to prevent API abuse:
- Staggered API calls
- Request queuing
- Automatic backoff on failures

## Troubleshooting

### Common Issues

1. **No articles generated**: Check API keys and internet connectivity
2. **Image generation fails**: Verify Replicate API or check fallback services
3. **Website not loading**: Ensure Flask server is running on correct port
4. **Scheduler not working**: Check system time and scheduling configuration

### Debug Mode

Run test cycle to debug issues:
```bash
python main.py test
```

Check logs for detailed error information:
```bash
tail -f logs/satire_news.log
```

## Development

### Adding New Features

1. **New satire styles**: Add to `Config.SATIRE_STYLES`
2. **Additional image sources**: Extend `ImageGenerator` class
3. **New content types**: Create new generator classes
4. **Website enhancements**: Modify Flask templates and routes

### Testing

Run the test suite:
```bash
python main.py test
```

## License

This project is for educational and entertainment purposes. All generated content is satirical and fictional.

## Contributing

Feel free to submit issues and enhancement requests!

---

**Disclaimer**: This system generates satirical content. All articles, images, and comics are fictional and intended for humor purposes only.
