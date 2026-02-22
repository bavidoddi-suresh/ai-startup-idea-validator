# Event Collaboration Intelligence - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Set Up Environment

Create `.env` file in `app/` directory:

```bash
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Agent

```bash
cd /path/to/event_collab
adk web event_collaboration_intelligence
```

### Step 4: Open in Browser

Navigate to: `http://localhost:8000`

### Step 5: Start Chatting

**Example conversation:**

```
You: Hi, I need help preparing for an event.

Agent: Hello! I'm your event networking intelligence partner. I can help you identify 
and engage the right collaboration opportunities at major industry events.

To get started, I need two pieces of information:
1. EVENT_NAME: What event are you attending?
2. COMPANY_NAME: What is your company name?

You can also optionally share your STRATEGIC_GOAL (e.g., "Find investors", 
"Build partnerships", "Recruit talent").

You: I'm going to the World Economic Forum Annual Meeting 2025 in Davos. 
My company is NextWave Disruptive Technologies and we want to find ed-tech 
partnerships and Series B investors.

Agent: Perfect! I have:
- Event: World Economic Forum Annual Meeting 2025
- Company: NextWave Disruptive Technologies
- Goal: Find ed-tech partnerships and Series B investors

Let me process this and run the full intelligence analysis...

[Agent runs pipeline...]

Agent: Analysis complete! I've generated:
✅ Comprehensive event and company intelligence
✅ 73 attendees discovered and cataloged
✅ 30 targets scored and ranked
✅ Top 10 battle cards with engagement strategies
✅ Executive briefing book (download: event_briefing_book.html)
✅ Network ecosystem map (download: ecosystem_map.png)

Here are your top 3 networking targets:

1. **Microsoft Education** (Score: 92/100) - Potential Partner
   - Why: Strong alignment with your ed-tech mission
   - Hook: "I saw you're launching AI learning tools..."
   - Meeting: Visit their booth at Congress Center, attend their panel on AI in Education

2. **Sequoia Capital** (Score: 88/100) - Investor Target
   - Why: Active in ed-tech Series B, portfolio alignment
   - Hook: "Your portfolio company Khan Academy is doing similar work..."
   - Meeting: They're at the Tech for Good reception, Tuesday 6pm

3. **Khan Academy** (Score: 85/100) - Potential Partner
   - Why: Complementary offerings, shared mission
   - Hook: "We're solving the teacher shortage problem with AI..."
   - Meeting: Find them at the Education Hub, Wednesday morning

[Full briefing book and ecosystem map available for download]
```

---

## 📥 What You Get

### 1. Battle Cards (JSON)
Download `collaboration_report.json` - Full structured data with:
- Top 10 targets with detailed battle cards
- 20-30 alternative targets
- Strategic insights and opportunities
- Phased action plan (pre/during/post-event)

### 2. Executive Briefing Book (HTML)
Download `event_briefing_book.html` - 7-slide McKinsey-style presentation:
- Slide 1: Executive Summary
- Slide 2: Event Intelligence
- Slide 3-4: Top Priority Targets (Battle Cards)
- Slide 5: Secondary Targets
- Slide 6: Strategic Insights
- Slide 7: Action Plan

**Pro tip:** Open in browser and "Print to PDF" for a polished document.

### 3. Ecosystem Map (PNG)
Download `ecosystem_map.png` - Visual network graph:
- Your company at center (gold star)
- Targets clustered by category (color-coded)
- Node size = synergy score
- High-priority targets labeled

---

## 🎯 Sample Use Cases

### Use Case 1: Tech Startup at Industry Conference

**Input:**
- Event: "Web Summit Lisbon 2025"
- Company: "DataFlow AI"
- Goal: "Find European expansion partners"

**Output:**
- Battle cards for European cloud providers
- Hooks referencing GDPR compliance and local partnerships
- Meeting locations at specific booth zones

### Use Case 2: Corporate Attending Trade Show

**Input:**
- Event: "Mobile World Congress Barcelona 2025"
- Company: "TelcoGiant Inc"
- Goal: "Scout 5G technology partners"

**Output:**
- Battle cards for 5G equipment vendors, chipmakers
- Value propositions around network deployment
- Tactical timing for booth visits and demo sessions

### Use Case 3: Investor at Startup Summit

**Input:**
- Event: "Collision Toronto 2025"
- Company: "Venture Capital Partners"
- Goal: "Discover Series A investment opportunities in AI"

**Output:**
- Battle cards for promising AI startups
- Hooks about funding gaps and market positioning
- Meeting strategies for startup pitch sessions

---

## 💡 Pro Tips

### 1. Be Specific with Strategic Goal
❌ Generic: "Networking"
✅ Specific: "Find Series B investors in ed-tech sector with $10-50M check size"

### 2. Add Company Context
Before starting, prepare:
- Company mission statement
- Recent news/funding rounds
- Key offerings and differentiators
- Target markets

This helps the agent better match you with aligned targets.

### 3. Research Event in Advance
The agent works best when the event has:
- Published speaker lineup
- Sponsor information
- Session agenda
- Participant announcements

For brand new events, results may be limited.

### 4. Use the Briefing Book on Mobile
The HTML briefing book is responsive - perfect for reading on your phone while at the event.

### 5. Pre-Event Outreach
Use the pre-event action plan to reach out 1-2 weeks before:
- LinkedIn connection requests
- Email introductions via mutual contacts
- Schedule confirmed meetings in advance

---

## 🔧 Customization

### Change Models

Edit `app/config.py`:

```python
# For faster/cheaper (but less detailed)
FAST_MODEL = "gemini-2.5-flash"
PRO_MODEL = "gemini-2.5-flash"

# For maximum quality (but slower/costlier)
FAST_MODEL = "gemini-3-pro-preview"
PRO_MODEL = "gemini-3-pro-preview"
```

### Adjust Synergy Scoring Weights

Edit `app/sub_agents/synergy_engine/agent.py`:

```python
# Default weights in prompt:
# Semantic Similarity: 40%
# Strategic Alignment: 30%
# Engagement Feasibility: 20%
# Mutual Benefit: 10%

# Adjust these percentages to prioritize different factors
```

### Add Custom Categories

Edit `app/schemas/event_collaboration_schema.py`:

```python
class BattleCard(BaseModel):
    category: str = Field(
        description="Category (e.g., 'Potential Partner', 'Investor Target', 
        'Customer Prospect', 'Policy Ally', 'Talent Source', 'Competitor', 
        'Media Contact', 'Academic Collaborator')"  # Add your custom categories
    )
```

---

## 🐛 Common Issues

### "No attendees found"
**Cause:** Event too new or attendee lists not public  
**Fix:** Try broader search terms, use past year's data, or manually input known attendees

### "Low synergy scores across all targets"
**Cause:** Strategic goal too vague or misaligned  
**Fix:** Refine your strategic goal to be more specific and aligned with event theme

### "Model overloaded (503 error)"
**Cause:** Gemini API high demand  
**Fix:** Switch to `gemini-2.5-pro` (more stable) or retry later

### "Briefing book HTML looks broken"
**Cause:** Browser compatibility  
**Fix:** Try Chrome/Firefox, or check if HTML was fully downloaded

---

## 📚 Next Steps

1. ✅ Run your first analysis
2. 📖 Read full docs: `EVENT_COLLABORATION_README.md`
3. 🔧 Customize agents for your specific needs
4. 🚀 Deploy to production with Vertex AI (see DEVELOPER_GUIDE.md)
5. 🤝 Integrate with CRM/LinkedIn for seamless follow-up

---

## 🎓 Learning Resources

- **ADK Documentation**: https://github.com/google/adk
- **Gemini API**: https://ai.google.dev/
- **Prompt Engineering Guide**: See agent instructions in `app/sub_agents/*/agent.py`
- **Schema Design**: See `app/schemas/event_collaboration_schema.py`

---

## 📞 Support

Questions? Check:
1. `EVENT_COLLABORATION_README.md` - Full documentation
2. GitHub Issues - Community support
3. ADK Discord - Real-time help

---

**Happy Networking! 🎉**
