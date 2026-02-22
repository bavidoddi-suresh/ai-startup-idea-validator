# Event Collaboration Intelligence System - Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                  USER                                       │
│                                                                             │
│  "I'm attending World Economic Forum. My company is NextWave.              │
│   Looking for ed-tech partnerships and Series B investors."                │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             ROOT AGENT                                      │
│                     (Conversational Orchestrator)                           │
│                                                                             │
│  • Greets user                                                              │
│  • Gathers: event_name, company_name, strategic_goal                       │
│  • Validates inputs                                                         │
│  • Calls IntakeAgent to parse                                               │
│  • Delegates to EventCollaborationPipeline                                  │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                   ┌───────────────┴───────────────┐
                   ▼                               ▼
        ┌──────────────────┐          ┌─────────────────────────────┐
        │  IntakeAgent     │          │   SESSION STATE             │
        │  (Gemini 2.5)    │────────► │                             │
        │                  │          │  event_name: "WEF 2025"     │
        │  Parses request  │          │  company_name: "NextWave"   │
        │  into structured │          │  strategic_goal: "ed-tech"  │
        │  format          │          │  current_date: "2025-01-10" │
        └──────────────────┘          └─────────────────────────────┘
                                                    │
                                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    EVENT COLLABORATION PIPELINE                             │
│                        (SequentialAgent)                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │
    ┌──────────────────────────────┼──────────────────────────────┐
    │                              │                              │
    ▼                              ▼                              ▼
┌─────────────────┐      ┌─────────────────┐          ┌─────────────────┐
│  STAGE 1:       │      │  STAGE 2:       │          │  STAGE 3:       │
│  EventContext   │──────►  AttendeeDiscov │──────────►  SynergyEngine  │
│                 │      │                 │          │                 │
│  • Google       │      │  • Google       │          │  • Python Code  │
│    Search       │      │    Search       │          │    Execution    │
│  • Event intel  │      │  • Speakers     │          │  • pandas       │
│  • Company      │      │  • Sponsors     │          │  • sklearn      │
│    profile      │      │  • Attendees    │          │  • TF-IDF       │
│                 │      │  • 50-100       │          │  • Cosine sim   │
│  Output:        │      │    entities     │          │  • Score 0-100  │
│  event_context  │      │                 │          │  • Categorize   │
│  (text)         │      │  Output:        │          │  • Rank         │
│                 │      │  attendee_disc  │          │                 │
│                 │      │  (text catalog) │          │  Output:        │
│                 │      │                 │          │  synergy_       │
│                 │      │                 │          │  analysis       │
│                 │      │                 │          │  (tables)       │
└─────────────────┘      └─────────────────┘          └─────────────────┘
                                                                │
                                                                │
    ┌───────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STAGE 4: RelationshipStrategist                                            │
│  (Gemini 3 Pro with Extended Reasoning - Thinking Mode)                    │
│                                                                             │
│  Inputs: event_context + attendee_discovery + synergy_analysis             │
│                                                                             │
│  Process:                                                                   │
│  • Synthesize all intelligence                                              │
│  • Create top 10 battle cards:                                              │
│    - Entity name, type, score, category                                     │
│    - 3-5 engagement hooks (conversation starters)                           │
│    - 2-4 value propositions (what you offer)                                │
│    - Tactical approach (when/where/how to meet)                             │
│    - Background intelligence (news, challenges)                             │
│  • Identify 20-30 alternative targets                                       │
│  • Generate strategic insights                                              │
│  • Create phased action plan (pre/during/post-event)                        │
│                                                                             │
│  Output: collaboration_report (EventCollaborationReport schema)             │
│          → Saved as collaboration_report.json artifact                      │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                   ┌───────────────┴───────────────┐
                   ▼                               ▼
┌───────────────────────────────┐  ┌──────────────────────────────────┐
│  STAGE 5:                     │  │  STAGE 6:                        │
│  BriefingBookGenerator        │  │  EcosystemVisualizer             │
│  (Gemini for HTML)            │  │  (Python NetworkX)               │
│                               │  │                                  │
│  • Format report data         │  │  • Extract top 30 targets        │
│  • Call Gemini to generate    │  │  • Create network graph:         │
│    McKinsey-style HTML        │  │    - Company at center (gold ★)  │
│  • 7-slide presentation:      │  │    - Targets as colored nodes    │
│    1. Executive Summary       │  │    - Color by category           │
│    2. Event Intelligence      │  │    - Size by score               │
│    3-4. Battle Cards          │  │    - Edges = strength            │
│    5. Secondary Targets       │  │  • matplotlib rendering          │
│    6. Strategic Insights      │  │                                  │
│    7. Action Plan             │  │  Output:                         │
│                               │  │  ecosystem_visualization_result  │
│  Output:                      │  │  → Saved as ecosystem_map.png    │
│  briefing_book_result         │  │                                  │
│  → Saved as                   │  │                                  │
│    event_briefing_book.html   │  │                                  │
└───────────────────────────────┘  └──────────────────────────────────┘
                   │                               │
                   └───────────────┬───────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ARTIFACTS GENERATED                                  │
│                                                                             │
│  📄 collaboration_report.json    - Full structured data (EventCollab...)   │
│  📊 event_briefing_book.html     - 7-slide executive presentation          │
│  📈 ecosystem_map.png            - Network visualization graph             │
│                                                                             │
│  All downloadable from ADK web interface                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER RECEIVES                                  │
│                                                                             │
│  ✅ Top 10 battle cards with specific engagement strategies                │
│  ✅ 20-30 alternative targets for opportunistic connections                │
│  ✅ Pre-event action plan (LinkedIn outreach, research)                    │
│  ✅ During-event action plan (booth visits, session attendance)            │
│  ✅ Post-event action plan (follow-up emails, meeting scheduling)          │
│  ✅ Executive briefing book to read on flight                              │
│  ✅ Network map to visualize opportunities                                 │
│                                                                             │
│  🎯 READY TO NETWORK STRATEGICALLY AT THE EVENT! 🎯                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Detail

```
USER INPUT
    │
    ├─► event_name: "World Economic Forum Annual Meeting 2025"
    ├─► company_name: "NextWave Disruptive Technologies"  
    └─► strategic_goal: "Find ed-tech partnerships and Series B investors"
        │
        ▼
STATE VARIABLES (shared across pipeline)
    │
    ├─► event_name
    ├─► company_name
    ├─► strategic_goal
    ├─► current_date
    │
    ├─► event_context (from Stage 1)
    ├─► attendee_discovery (from Stage 2)
    ├─► synergy_analysis (from Stage 3)
    ├─► collaboration_report (from Stage 4)
    ├─► briefing_book_result (from Stage 5)
    └─► ecosystem_visualization_result (from Stage 6)
        │
        ▼
ARTIFACTS (saved by after_agent_callbacks)
    │
    ├─► collaboration_report.json (after Stage 4)
    ├─► event_briefing_book.html (after Stage 5)
    └─► ecosystem_map.png (after Stage 6)
```

---

## Technology Stack

```
┌────────────────────────────────────────────────────────────┐
│                     TECHNOLOGY LAYERS                      │
├────────────────────────────────────────────────────────────┤
│  USER INTERFACE                                            │
│  • ADK Web Interface (http://localhost:8000)               │
│  • Chat-based interaction                                  │
│  • Artifact download                                       │
├────────────────────────────────────────────────────────────┤
│  ORCHESTRATION LAYER                                       │
│  • Google ADK (Agent Development Kit)                      │
│  • SequentialAgent for pipeline                            │
│  • LlmAgent for individual agents                          │
│  • CallbackContext for state management                    │
├────────────────────────────────────────────────────────────┤
│  AI/ML LAYER                                               │
│  • Gemini 2.5 Pro (fast agents)                            │
│  • Gemini 3 Pro Preview (reasoning/strategy)               │
│  • ThinkingConfig (extended reasoning)                     │
│  • BuiltInCodeExecutor (Python sandbox)                    │
├────────────────────────────────────────────────────────────┤
│  DATA PROCESSING                                           │
│  • pandas (data manipulation)                              │
│  • scikit-learn (TF-IDF, cosine similarity)                │
│  • numpy (numerical operations)                            │
│  • networkx (graph algorithms)                             │
│  • matplotlib (visualization)                              │
├────────────────────────────────────────────────────────────┤
│  DATA SOURCES                                              │
│  • Google Search (event/attendee discovery)                │
│  • Web scraping (speaker lists, sponsors)                  │
│  • News articles (background intelligence)                 │
├────────────────────────────────────────────────────────────┤
│  OUTPUT FORMATS                                            │
│  • JSON (structured data)                                  │
│  • HTML (presentation/report)                              │
│  • PNG (visualization)                                     │
│  • Pydantic schemas (validation)                           │
└────────────────────────────────────────────────────────────┘
```

---

## Scoring Algorithm Detail

```
SYNERGY SCORE CALCULATION (0-100)
│
├─► Semantic Similarity (40 points)
│   │
│   ├─► Company profile text: "NextWave ed-tech AI learning platform..."
│   ├─► Target description: "Microsoft Education AI tools schools..."
│   │
│   └─► TF-IDF Vectorization + Cosine Similarity
│       • Extract features: ["ed-tech", "AI", "education", "learning"]
│       • Calculate overlap: 0.85 → 34 points (85% of 40)
│
├─► Strategic Goal Alignment (30 points)
│   │
│   ├─► Direct match: "ed-tech partnerships" ↔ Target is ed-tech company
│   │   → +30 points (100%)
│   │
│   ├─► Adjacent match: "ed-tech" ↔ Target is "education policy"
│   │   → +20 points (66%)
│   │
│   └─► Tangential: "ed-tech" ↔ Target is "general tech"
│       → +10 points (33%)
│
├─► Engagement Feasibility (20 points)
│   │
│   ├─► Speaker/session leader → +20 (highly accessible)
│   ├─► Top-tier sponsor → +15 (booth presence)
│   ├─► Known attendee → +10 (findable)
│   └─► General participant → +5 (difficult)
│
└─► Mutual Benefit Potential (10 points)
    │
    ├─► Clear value exchange → +10 (win-win obvious)
    ├─► One-sided value → +5 (you benefit more)
    └─► Unclear benefit → +0 (speculative)

TOTAL SCORE: 34 + 30 + 20 + 10 = 94/100 (High Priority)
```

---

## Battle Card Example

```
┌─────────────────────────────────────────────────────────────┐
│ BATTLE CARD #1                                              │
├─────────────────────────────────────────────────────────────┤
│ Entity: Microsoft Education                                 │
│ Type: Company                                               │
│ Synergy Score: 92/100 ████████████████████░░               │
│ Category: Potential Partner                                 │
├─────────────────────────────────────────────────────────────┤
│ WHY TARGET                                                  │
│ Microsoft is launching AI-powered learning tools for        │
│ schools and needs content partners. Your AI tutoring        │
│ platform could integrate seamlessly.                        │
├─────────────────────────────────────────────────────────────┤
│ ENGAGEMENT HOOKS                                            │
│                                                             │
│ 1. Shared Interest: "I saw your keynote on AI in           │
│    education - we're building AI tutors for the same        │
│    challenge you mentioned: teacher shortage."              │
│                                                             │
│ 2. Problem-Solution: "Your Teams for Education needs       │
│    smart content - we have 10,000 AI-generated lesson       │
│    plans ready to integrate."                               │
│                                                             │
│ 3. Mutual Benefit: "We reach 500K students in India -      │
│    you need emerging market traction. Let's explore         │
│    co-marketing."                                           │
├─────────────────────────────────────────────────────────────┤
│ VALUE PROPOSITIONS                                          │
│                                                             │
│ • Technology: AI content generation engine (plug-and-play)  │
│ • Market Access: 500K users in India, SEA partnerships      │
│ • Partnership Model: API integration + revenue share        │
├─────────────────────────────────────────────────────────────┤
│ TACTICAL APPROACH                                           │
│                                                             │
│ Key Contact: Sarah Chen, VP Education Partnerships          │
│ Session: "AI for Good: Education" - Tuesday 2pm, Hall A    │
│ Booth: #1234, Congress Center Level 2                      │
│                                                             │
│ Timing Strategy:                                            │
│ • Pre-event: LinkedIn connection request (mention shared    │
│   interest in ed-tech AI)                                   │
│ • During: Attend her panel, visit booth after 3pm          │
│ • Post-event: Email with integration proposal deck         │
├─────────────────────────────────────────────────────────────┤
│ BACKGROUND INTELLIGENCE                                     │
│                                                             │
│ Recent News: Launched "Copilot for Education" Nov 2024,    │
│ focusing on K-12 AI assistants. Raised concerns about      │
│ content quality - your strength!                            │
│                                                             │
│ Competitive Landscape: Competing with Google Classroom,    │
│ needs differentiation through superior content.             │
└─────────────────────────────────────────────────────────────┘
```

---

This architecture delivers **actionable networking intelligence** to maximize ROI from event attendance! 🚀
