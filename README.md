# Startup Idea Validator — Multi-Agent AI Pipeline

Test your startup or business idea with AI. Enter your idea, and the system will find competitors, point out their weaknesses, and suggest a stronger value proposition to help you compete.

Built with [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) and Gemini.

---

## What It Does

You give it a startup idea. It runs a 7-stage AI pipeline and returns:

- **Existing competitors** already doing something similar
- **Their weaknesses** (user complaints, missing features, pricing gaps)
- **A unique value proposition** crafted to help you stand out
- **A viability score** (0–100) with risk assessment
- **An HTML executive deck** (McKinsey/BCG style)
- **A shareable infographic** summarizing everything

---

## How It Works — The Pipeline

```
User enters idea
     │
     ▼
┌─────────────────────────────────────────────────────┐
│  IntakeAgent (Tool)                                 │
│  Extracts: idea, problem, target market, industry   │
└────────────────────┬────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────┐
│  Stage 1: Market Research Agent                     │
│  Validates market size, growth, demographics,       │
│  demand signals using live Google Search             │
└────────────────────┬────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────┐
│  Stage 2: Competitor Mapping Agent                  │
│  Discovers 5–15 competitors via deep web research,  │
│  profiles strengths & weaknesses, finds user         │
│  complaints and feature gaps                         │
└────────────────────┬────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────┐
│  Stage 3: Gap Analysis Agent                        │
│  Runs Python code to compute saturation score,      │
│  opportunity score, differentiation potential,       │
│  and builds a competitive feature matrix             │
└────────────────────┬────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────┐
│  Stage 4: Strategy Advisor Agent                    │
│  Synthesizes everything into a 0–100 viability      │
│  score, crafts a killer value proposition,           │
│  identifies risks + next steps                       │
└────────────────────┬────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────┐
│  Stage 5: Report Generator Agent                    │
│  Produces a 7-slide McKinsey/BCG-style HTML deck    │
└────────────────────┬────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────┐
│  Stage 6: Infographic Generator Agent               │
│  Creates a shareable visual summary image            │
└─────────────────────────────────────────────────────┘
```

---

## Quick Start (Local Setup)

### Prerequisites

- **Python 3.10–3.12** — [Download](https://www.python.org/downloads/)
- **uv** (Python package manager) — [Install](https://github.com/astral-sh/uv)
- **Google AI Studio API Key** (free) — [Get one here](https://aistudio.google.com/app/apikey)

### Step 1: Clone the repo

```bash
git clone https://github.com/paidinesh7/adk_awesome_collab.git
cd adk_awesome_collab
```

### Step 2: Install dependencies

```bash
make install
```

This installs `uv` (if not already installed) and syncs all Python dependencies.

### Step 3: Set up your API key

Copy the example env file into the `app/` folder and add your key:

```bash
cp .env.example app/.env
```

Now open `app/.env` and replace the placeholder with your actual API key:

```
GOOGLE_API_KEY=paste_your_actual_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

> **Where to get the key:** Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey), sign in with your Google account, and create an API key. It's free.

### Step 4: Run it

```bash
make dev
```

### Step 5: Use it

1. Open **http://localhost:8501** in your browser
2. Select **"app"** from the agent dropdown (top-left)
3. Type your startup idea, for example:

   > "I want to build an AI-powered resume builder for fresh graduates"

4. Watch the 6-stage pipeline run automatically:
   - Market Research → Competitor Mapping → Gap Analysis → Strategy Advisor → Report → Infographic

5. Check the **Artifacts** tab in the UI to download the HTML report and infographic

---

## Example Prompts to Try

| Idea | Prompt |
|------|--------|
| EdTech | "I want to build an AI tutor for competitive exam prep in India" |
| SaaS | "A project management tool specifically for freelancers and solopreneurs" |
| HealthTech | "An app that connects patients with dietitians for personalized meal plans" |
| FinTech | "A micro-investment app for college students to invest spare change" |
| Creator Economy | "A platform connecting freelance designers with small businesses" |
| Quick Commerce | "Hyperlocal grocery delivery for tier-2 cities in India" |
| Developer Tools | "An AI code review tool that integrates with GitHub PRs" |
| Social Impact | "A marketplace for sustainable/eco-friendly products" |

---

## Project Structure

```
adk_awesome_collab/
├── Makefile                  # make install, make dev, etc.
├── pyproject.toml            # Python dependencies
├── .env.example              # Template for app/.env
│
└── app/                      # The agent package
    ├── __init__.py            # Exports root_agent
    ├── agent.py               # Root agent + SequentialAgent pipeline
    ├── config.py              # Model selection, retry config
    ├── .env                   # Your API keys (not committed)
    │
    ├── sub_agents/            # 7 specialized agents
    │   ├── intake_agent/      # Parses user input into structured data
    │   ├── market_research/   # Google Search for market validation
    │   ├── competitor_mapping/# Deep web research for competitors
    │   ├── gap_analysis/      # Python code execution for scoring
    │   ├── strategy_advisor/  # Extended reasoning for value proposition
    │   ├── report_generator/  # HTML executive deck
    │   └── infographic_generator/ # Visual summary image
    │
    ├── tools/                 # Custom function tools
    │   ├── html_report_generator.py  # Generates HTML report via Gemini
    │   └── image_generator.py        # Generates infographic via Gemini
    │
    ├── schemas/               # Pydantic output schemas
    │   └── startup_validation_schema.py  # StartupValidationReport
    │
    └── callbacks/             # Pipeline lifecycle callbacks
        └── pipeline_callbacks.py  # Logging, state tracking, artifacts
```

---

## Model Configuration

The default model is `gemini-2.5-pro`. You can change it in `app/config.py`:

| Option | Text Models | Image Model | Notes |
|--------|-------------|-------------|-------|
| **Gemini 2.5 Pro** (default) | `gemini-2.5-pro` | `gemini-3-pro-image-preview` | Stable, recommended |
| **Gemini 3 Pro Preview** | `gemini-3-pro-preview` | `gemini-3-pro-image-preview` | Latest features, may have availability issues |
| **Gemini 2.5 Flash** | `gemini-2.5-flash` | `gemini-2.0-flash-exp` | Fastest, lowest cost |

To switch, open `app/config.py` and uncomment the option you want.

---

## Vertex AI Setup (Alternative)

If you prefer using Google Cloud Vertex AI instead of AI Studio:

```bash
# In app/.env:
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

Make sure you're authenticated:

```bash
gcloud auth application-default login
```

Then run `make dev` as usual.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Missing key inputs argument` error | You haven't set up `app/.env`. Follow Step 3 above. |
| `uv: command not found` | Run `curl -LsSf https://astral.sh/uv/install.sh \| sh` then restart your terminal. |
| `503 model overloaded` | Switch to `gemini-2.5-flash` in `app/config.py` for better availability. |
| `No .env file found for app` | Make sure `.env` is inside the `app/` folder, not the project root. |
| Agent shows in dropdown but errors on chat | Check that `GOOGLE_API_KEY` in `app/.env` is a valid key (no quotes needed). |
| `ModuleNotFoundError` | Run `make install` again to sync dependencies. |

---

## Makefile Commands

| Command | What it does |
|---------|-------------|
| `make install` | Install all Python dependencies |
| `make dev` | Start the ADK web server on port 8501 |
| `make test` | Run tests |
| `make lint` | Run linters (ruff, mypy, codespell) |
| `make clean` | Remove build artifacts and caches |

---

## License

Apache 2.0
