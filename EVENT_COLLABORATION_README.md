# Event Collaboration Intelligence System

## Overview

The **Event Collaboration Intelligence System** is an AI-powered strategic networking platform that helps companies maximize their ROI from major industry events. Given an event name and company name, the system autonomously generates comprehensive networking intelligence including battle cards, executive briefing books, and ecosystem visualizations.

### Example Use Case

**Input:**
- Event: "World Economic Forum Annual Meeting 2025"
- Company: "NextWave Disruptive Technologies"
- Goal: "Find ed-tech partnerships and Series B investors"

**Output:**
- Battle cards for top 10 networking targets with engagement hooks
- Executive HTML briefing book (7-slide McKinsey-style report)
- Network ecosystem visualization showing collaboration opportunities
- Pre/during/post-event action plans

---

## Architecture

### Pipeline Overview

The system uses a **6-stage sequential agent pipeline**:

```
┌─────────────────────────────────────────────────────────────┐
│                    ROOT AGENT                               │
│  (Conversational orchestrator - gathers inputs from user)  │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
         ┌─────────────────┐
         │  IntakeAgent    │ ← Parses natural language request
         └────────┬────────┘
                  │
                  ▼
    ┌─────────────────────────────────────┐
    │  EVENT COLLABORATION PIPELINE       │
    └─────────────────────────────────────┘
           │
           ├──► 1. EventContextAgent
           │      • Google Search for event intelligence
           │      • Company profile research
           │      • Strategic context analysis
           │
           ├──► 2. AttendeeDiscoveryAgent
           │      • Discover speakers, sponsors, participants
           │      • Build attendee database (50-100+ entities)
           │      • Categorize by role/industry
           │
           ├──► 3. SynergyEngineAgent
           │      • Python code execution (pandas, sklearn)
           │      • Semantic similarity scoring (TF-IDF)
           │      • Quantitative target ranking (0-100 score)
           │      • Category classification
           │
           ├──► 4. RelationshipStrategistAgent
           │      • Extended reasoning (thinking mode)
           │      • Generate top 10 battle cards
           │      • Engagement hooks & value propositions
           │      • Tactical meeting strategies
           │      • Structured JSON output
           │
           ├──► 5. BriefingBookGeneratorAgent
           │      • Gemini-powered HTML generation
           │      • McKinsey/BCG style 7-slide report
           │      • Print-ready executive briefing
           │
           └──► 6. EcosystemVisualizerAgent
                  • NetworkX graph visualization
                  • Company at center, targets clustered
                  • Color-coded by category, sized by score
```

---

## Agent Definitions

### 1. **EventContextAgent**
- **Role**: Event intelligence analyst
- **Tools**: Google Search
- **Output**: `event_context` (text)
- **Mission**:
  - Research event details (dates, themes, agenda, attendance)
  - Analyze event significance and networking value
  - Deep dive on company profile (mission, offerings, strategic focus)
  - Identify strategic alignment between company and event

### 2. **AttendeeDiscoveryAgent**
- **Role**: Intelligence analyst for attendee research
- **Tools**: Google Search
- **Output**: `attendee_discovery` (text catalog)
- **Mission**:
  - Search for keynote speakers and session leaders
  - Identify sponsors by tier (Diamond, Platinum, Gold)
  - Discover participating companies and delegations
  - Find high-profile individuals (CEOs, investors, policymakers)
  - Build comprehensive attendee database (50-100+ entities)

### 3. **SynergyEngineAgent**
- **Role**: Data scientist for partnership matching
- **Tools**: Python Code Execution (pandas, sklearn, numpy)
- **Output**: `synergy_analysis` (quantitative scores)
- **Mission**:
  - Parse attendee data into structured DataFrame
  - Perform semantic similarity matching (TF-IDF + cosine similarity)
  - Calculate composite synergy scores (0-100) based on:
    - Semantic alignment (40%)
    - Strategic goal match (30%)
    - Engagement feasibility (20%)
    - Mutual benefit potential (10%)
  - Categorize targets (Partner, Investor, Customer, Policy, Competitor)
  - Rank and segment into High/Medium/Low priority

### 4. **RelationshipStrategistAgent**
- **Role**: Senior networking strategist
- **Tools**: Extended reasoning (ThinkingConfig)
- **Output**: `collaboration_report` (EventCollaborationReport schema)
- **Mission**:
  - Synthesize all intelligence into actionable strategies
  - Create detailed battle cards for top 10 targets:
    - Engagement hooks (3-5 conversation starters)
    - Value propositions (what you offer them)
    - Tactical approach (when/where to meet)
    - Background intelligence
  - Provide 20-30 alternative targets with brief summaries
  - Generate strategic insights and partnership opportunities
  - Create phased action plan (pre/during/post-event)

### 5. **BriefingBookGeneratorAgent**
- **Role**: Executive presentation designer
- **Tools**: `generate_briefing_book` (Gemini HTML generation)
- **Output**: `briefing_book_result` → `event_briefing_book.html`
- **Mission**:
  - Format collaboration report data for presentation
  - Call Gemini to generate McKinsey/BCG style HTML
  - Create 7-slide executive briefing book:
    - Executive Summary
    - Event Intelligence
    - Top Priority Targets (Battle Cards)
    - Secondary Targets
    - Strategic Insights
    - Action Plan
  - Save as downloadable HTML artifact

### 6. **EcosystemVisualizerAgent**
- **Role**: Data visualization specialist
- **Tools**: `generate_ecosystem_map` (NetworkX, matplotlib)
- **Output**: `ecosystem_visualization_result` → `ecosystem_map.png`
- **Mission**:
  - Extract top 30 targets with categories and scores
  - Generate network graph visualization:
    - Company as gold star at center
    - Targets as colored nodes (color = category, size = score)
    - Edges showing collaboration strength
    - Legend and high-priority labels
  - Save as downloadable PNG artifact

---

## Prompt Engineering Patterns

### Standard Instruction Structure

Each agent follows this pattern:

```python
AGENT_INSTRUCTION = """You are a [role description].

Your task is to [mission statement].

EVENT NAME: {event_name}
COMPANY NAME: {company_name}
STRATEGIC GOAL: {strategic_goal}
CURRENT DATE: {current_date}

## Available Data (from previous stages):
{previous_stage_outputs}

## Your Mission
[Detailed step-by-step instructions]

## Step 1: [Action]
[Specific guidance]

## Step 2: [Analysis]
[Specific guidance]

## Step 3: [Output]
[Format requirements]

## Output Format
[Expected structure/schema]
"""
```

### Key Prompt Patterns

1. **Role Definition**: "You are a [specialist] specializing in [domain]"
2. **Context Injection**: Dynamic variables via `{variable_name}` in instructions
3. **Mission Statement**: Clear, concise task definition
4. **Structured Steps**: Numbered, explicit steps for agent to follow
5. **Output Schema**: Pydantic models for structured outputs (JSON)
6. **Examples**: Few-shot examples for clarity (especially IntakeAgent)
7. **Tool Guidance**: Explicit instructions on how to use tools

### State Management

- **Before Callbacks**: Set `current_date`, `pipeline_stage` in state
- **After Callbacks**: Track `stages_completed[]`, save artifacts
- **State Variables**: Flow through pipeline via `output_key`
- **Template Variables**: Inject into instructions via `{variable_name}`

---

## Schemas

### EventCollaborationReport (Main Output)

```python
class EventCollaborationReport(BaseModel):
    event_intelligence: EventIntelligence
    company_profile: CompanyProfile
    statistics: NetworkingStatistics
    top_10_targets: List[BattleCard]
    alternative_targets: List[AlternativeTarget]
    key_insights: List[str]
    sector_opportunities: List[str]
    timing_recommendations: List[str]
    pre_event_actions: List[str]
    during_event_actions: List[str]
    post_event_actions: List[str]
    methodology_summary: str
```

### BattleCard (Top Target Detail)

```python
class BattleCard(BaseModel):
    entity_name: str
    entity_type: str
    synergy_score: int  # 0-100
    category: str  # Partner, Investor, Customer, etc.
    why_target: str
    alignment_factors: List[str]
    hooks: List[EngagementHook]  # Conversation starters
    value_propositions: List[ValueProposition]  # What you offer
    key_contact: Optional[str]
    session_attendance: Optional[str]
    meeting_location: Optional[str]
    timing_strategy: str
    recent_news: Optional[str]
    competitive_landscape: Optional[str]
```

---

## Installation & Setup

### Prerequisites

```bash
python >= 3.10
```

### Environment Variables

Create `.env` file in `app/` directory:

```bash
# Google AI Studio API Key (for Gemini)
GOOGLE_API_KEY=your_google_api_key

# Use AI Studio (not Vertex AI)
GOOGLE_GENAI_USE_VERTEXAI=FALSE

# Optional: Maps API (legacy, not used in event collaboration)
MAPS_API_KEY=your_maps_api_key
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies include:
- `google-generativeai` (Gemini)
- `google-adk` (Agent Development Kit)
- `pandas` (data manipulation)
- `scikit-learn` (semantic matching)
- `networkx` (graph visualization)
- `matplotlib` (plotting)
- `pydantic` (schemas)

### Run the Agent

```bash
adk web event_collaboration_intelligence
```

Then open browser at `http://localhost:8000`

---

## Usage Examples

### Example 1: World Economic Forum

**User Input:**
```
I'm attending the World Economic Forum in Davos this January. 
My company is NextWave Disruptive Technologies and we're 
looking for ed-tech partnerships and Series B investors.
```

**System Output:**
- ✅ Event context research completed
- ✅ 73 attendees discovered (speakers, sponsors, companies)
- ✅ 30 targets scored and ranked
- ✅ Top 10 battle cards generated:
  - Microsoft Education (Score: 92) - Potential Partner
  - Sequoia Capital (Score: 88) - Investor Target
  - Khan Academy (Score: 85) - Potential Partner
  - UNESCO (Score: 82) - Policy Ally
  - ...
- ✅ Executive briefing book generated (7 slides)
- ✅ Ecosystem map visualization created

### Example 2: CES (Consumer Electronics Show)

**User Input:**
```
Event: CES 2025
Company: RoboHome AI
Goal: Find retail distribution partners
```

**System Output:**
- Battle cards for Best Buy, Amazon Devices, Samsung, LG, etc.
- Engagement hooks: "I saw your keynote on smart home ecosystems..."
- Value propositions: "We offer white-label AI assistants..."
- Tactical timing: "Visit booth #1234, attend Smart Home Summit session"

---

## Key Differences from Retail Location Strategy

| Aspect | Retail Location | Event Collaboration |
|--------|----------------|---------------------|
| **Input** | Location + Business Type | Event + Company |
| **Data Source** | Google Maps Places API | Google Search (web scraping) |
| **Analysis** | Geographic zones, foot traffic | People/companies, synergy scores |
| **Scoring** | Saturation Index, Viability | Semantic Similarity, Strategic Fit |
| **Output** | Zone recommendations | Battle cards, briefing book |
| **Use Case** | Where to open a store | Who to meet at an event |

---

## Extensibility

### Adding New Agent

1. **Create agent file**: `app/sub_agents/new_agent/agent.py`
2. **Define instruction**: Follow standard pattern
3. **Add callbacks**: `before_new_agent`, `after_new_agent`
4. **Wire into pipeline**: Add to `event_collaboration_pipeline.sub_agents[]`

### Custom Tools

Create tool in `app/tools/`:

```python
def custom_tool(param: str, tool_context: ToolContext) -> dict:
    """Tool description."""
    try:
        # Implementation
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}
```

Add to agent:
```python
agent = LlmAgent(
    tools=[custom_tool],
    ...
)
```

### Alternative Models

Edit `app/config.py`:

```python
# Use Gemini 3 Pro Preview (latest features)
FAST_MODEL = "gemini-3-pro-preview"
PRO_MODEL = "gemini-3-pro-preview"
CODE_EXEC_MODEL = "gemini-3-pro-preview"

# Or use Flash for speed/cost
FAST_MODEL = "gemini-2.5-flash"
```

---

## Artifacts Generated

1. **collaboration_report.json** - Full structured report (EventCollaborationReport)
2. **event_briefing_book.html** - Executive briefing (7-slide presentation)
3. **ecosystem_map.png** - Network visualization (company + partners)

All artifacts downloadable from ADK web interface.

---

## Troubleshooting

### Issue: Google Search rate limiting

**Solution**: Add delays in search queries, or use API key with higher quota

### Issue: Model overloaded (503 errors)

**Solution**: Switch to `gemini-2.5-pro` (more stable than `gemini-3-pro-preview`)

### Issue: No attendees found

**Solution**: Event may be too new/small, or attendee lists not public. Try broader queries or past year's data.

### Issue: Low synergy scores

**Solution**: Refine strategic goal description to be more specific. Better goal = better matching.

---

## Future Enhancements

1. **LinkedIn Integration** - Scrape attendee LinkedIn profiles for deeper intel
2. **Company Database** - Pre-populate company profiles from Crunchbase/PitchBook
3. **Email Templates** - Auto-generate personalized outreach emails
4. **Calendar Integration** - Schedule meeting slots based on session times
5. **Multi-Event Analysis** - Compare opportunities across multiple events
6. **Sentiment Analysis** - Analyze recent news sentiment for targets
7. **Meeting Confirmation Tracker** - Track confirmed vs. pending meetings

---

## License

Copyright 2025 Google LLC. Licensed under Apache 2.0.

---

## Support

For questions or issues:
- GitHub Issues: [repository]
- ADK Documentation: https://github.com/google/adk
- Gemini API: https://ai.google.dev/
