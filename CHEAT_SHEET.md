# 🚀 OK Crisis News Site - Complete Cheat Sheet

## 🎯 **Quick Access URLs**
- **Live Site**: https://okcrisis-news.surge.sh
- **Admin Panel**: http://localhost:5000/admin (when running locally)
- **Refresh News**: http://localhost:5000/refresh-news
- **API Latest**: http://localhost:5000/api/latest

## 🗣️ **Voice Prompts Setup**
```bash
# Install voice recognition
pip install speechrecognition pyttsx3

# Run with voice commands
python voice_admin.py
```

**Voice Commands:**
- "Refresh news" - Generate new articles
- "Show stats" - Display site statistics  
- "Add comic" - Create new comic
- "Publish" - Deploy updates

## 🎨 **Comics Admin**
```bash
# Create custom comic
curl -X POST http://localhost:5000/api/create-comic \
  -H "Content-Type: application/json" \
  -d '{"headline": "Your Headline", "category": "politics"}'
```

## 🤖 **Full Automation Setup**

### 1. **Automatic News Generation** (Every 6 hours)
```bash
# Add to crontab (Linux/Mac)
0 */6 * * * cd /path/to/news-satire-system && python auto_generate.py

# Windows Task Scheduler
# Run auto_generate.py every 6 hours
```

### 2. **Auto-Deploy to Surge**
```bash
# Install surge CLI
npm install -g surge

# Auto-deploy script
python deploy_to_surge.py
```

### 3. **Social Media Auto-Posting**
```bash
# Twitter automation
pip install tweepy
python auto_tweet.py
```

## 📝 **Admin Commands**

### **Generate New Articles**
```bash
# Manual refresh
curl http://localhost:5000/refresh-news

# Generate specific category
curl "http://localhost:5000/refresh-news?category=politics"
```

### **Site Statistics**
```bash
# Get article count
curl http://localhost:5000/api/stats

# View latest articles
curl http://localhost:5000/api/latest
```

### **Content Management**
```bash
# Add custom article
curl -X POST http://localhost:5000/api/add-article \
  -H "Content-Type: application/json" \
  -d '{
    "headline": "Custom Headline",
    "content": "Article content...",
    "category": "technology"
  }'
```

## 🔧 **Local Development**

### **Start the Server**
```bash
cd web
python app.py
# Server runs on http://localhost:5000
```

### **Generate Test Content**
```bash
python generate_test_content.py
```

### **Reset Database**
```bash
rm -rf data/archive.json
python app.py  # Will regenerate with fresh content
```

## 🎨 **Customization**

### **Add New Categories**
1. Edit `src/generation/satire_engine.py`
2. Add category to `CATEGORIES` list
3. Update templates with new category links

### **Modify Ad Content**
1. Edit `templates/index.html` (line 157-167)
2. Edit `templates/article.html` (line 228-236)
3. Replace placeholder content with real ads

### **Custom Styling**
1. Edit `static/css/style.css`
2. Modify color variables in `templates/base.html`

## 📊 **Analytics & Monitoring**

### **Track Visitors**
```bash
# Add to base.html
<script>
  // Google Analytics or custom tracking
</script>
```

### **Performance Monitoring**
```bash
# Check response times
curl -w "@curl-format.txt" http://localhost:5000/
```

## 🔐 **Security**

### **Environment Variables**
```bash
# Create .env file
NEWS_API_KEY=your_newsdata_key
GEMINI_API_KEY=your_gemini_key
SECRET_KEY=your_secret_key
```

### **Admin Protection**
```bash
# Add password protection
export ADMIN_PASSWORD="your_password"
```

## 🚀 **Deployment Options**

### **Surge (Current)**
```bash
surge --domain okcrisis-news.surge.sh
```

### **Netlify**
```bash
# Install Netlify CLI
npm install -g netlify-cli
netlify deploy --prod
```

### **Vercel**
```bash
# Already configured
vercel --prod
```

## 📱 **Mobile Optimization**

### **Responsive Testing**
- Test on: http://localhost:5000
- Use Chrome DevTools device emulation
- Check mobile ad placement

## 🎯 **Content Strategy**

### **Daily Automation**
- **6 AM**: Generate politics articles
- **12 PM**: Generate tech articles  
- **6 PM**: Generate lifestyle articles
- **12 AM**: Generate comics

### **Weekly Schedule**
- **Monday**: Politics focus
- **Tuesday**: Technology focus
- **Wednesday**: Science focus
- **Thursday**: Business focus
- **Friday**: Culture focus
- **Weekend**: Mixed content

## 🆘 **Troubleshooting**

### **Common Issues**
- **404 Errors**: Check article IDs in archive
- **No New Content**: Verify API keys are valid
- **Slow Loading**: Check image optimization
- **Ads Not Showing**: Clear browser cache

### **Quick Fixes**
```bash
# Restart server
pkill -f python && python app.py

# Clear cache
rm -rf __pycache__/

# Regenerate content
python manual_generate.py
```

## 📞 **Contact Info for Ads**
- **Email**: ads@okcrisis.com
- **Phone**: (555) 123-4567
- **Rates**: Starting at $500/month

---

## 🎮 **One-Command Full Automation**
```bash
# Run this for complete automation
python full_automation.py
```

This script will:
1. Generate new articles
2. Create comics
3. Update ads
4. Deploy to surge
5. Post to social media
6. Send email report

---

*Troubleshooting: Check logs in `logs/` directory*
