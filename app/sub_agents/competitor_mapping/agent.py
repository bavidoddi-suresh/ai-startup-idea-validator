"""Competitor Mapping Agent - Stage 2 of the Startup Validation Pipeline.

This agent discovers and analyzes existing competitors using Google Search
for deep research, and optionally Google Maps for location-based businesses.
"""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.genai import types

from ...config import FAST_MODEL, RETRY_INITIAL_DELAY, RETRY_ATTEMPTS
from ...callbacks import before_competitor_mapping, after_competitor_mapping


COMPETITOR_MAPPING_INSTRUCTION = """You are a competitive intelligence analyst specializing in startup landscapes.

Your task is to find ALL existing companies/products doing something similar to this startup idea,
analyze their strengths and weaknesses, and map the competitive landscape.

STARTUP IDEA: {startup_idea}
PROBLEM STATEMENT: {problem_statement}
TARGET MARKET: {target_market}
INDUSTRY: {industry_vertical}
CURRENT DATE: {current_date}

## Your Mission
Use Google Search extensively to discover every relevant competitor.

## Step 1: Discover Competitors
Search for:
- Direct competitors (solving the exact same problem)
- Indirect competitors (solving a related problem or serving the same audience differently)
- Emerging competitors (startups recently funded in this space)
- Adjacent players (large companies that could pivot into this space)

Search queries to try:
- "[problem] solution" or "[problem] app/platform/tool"
- "alternatives to [known competitor]"
- "[industry] startups funded 2025 2026"
- "[target market] [solution type]"
- "best [solution type] for [target audience]"
- Product Hunt, G2, Capterra listings for this category

## Step 2: Deep-Dive Each Competitor
For each competitor found, research:
- **What they do**: Core offering and value proposition
- **Who they serve**: Target audience and customer segments
- **How big they are**: Funding raised, team size, user base (if available)
- **Strengths**: What they do well (features, UX, brand, distribution)
- **Weaknesses**: Where they fall short (user complaints, missing features, poor UX, pricing issues)
- **User sentiment**: App store reviews, Reddit/Twitter complaints, G2/Capterra reviews

## Step 3: Identify Competitor Weaknesses (CRITICAL)
For each competitor, specifically search for:
- Negative reviews and user complaints
- Missing features users are asking for
- Pricing complaints
- Customer service issues
- "Why I left [competitor]" or "[competitor] problems" searches
- Reddit/forum discussions about competitor limitations

## Step 4: Map the Competitive Landscape
Categorize competitors by:
- **Market position**: Leader / Challenger / Niche Player / New Entrant
- **Pricing tier**: Free / Freemium / Mid-market / Enterprise
- **Geographic focus**: Global / Regional / Local
- **Key differentiator**: What makes each one unique?

## Output Format
Provide a detailed competitive landscape report with:
1. Complete list of competitors found (aim for 5-15 competitors)
2. Detailed profile of each competitor with strengths AND weaknesses
3. Common weaknesses across the competitive landscape
4. Gaps that NO competitor is addressing well
5. The biggest opportunities for differentiation

Be thorough and specific. The user needs to understand exactly who they're up against and where the openings are.
"""

competitor_mapping_agent = LlmAgent(
    name="CompetitorMappingAgent",
    model=FAST_MODEL,
    description="Discovers and analyzes existing competitors using deep web research to map the competitive landscape",
    instruction=COMPETITOR_MAPPING_INSTRUCTION,
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                initial_delay=RETRY_INITIAL_DELAY,
                attempts=RETRY_ATTEMPTS,
            ),
        ),
    ),
    tools=[google_search],
    output_key="competitor_analysis",
    before_agent_callback=before_competitor_mapping,
    after_agent_callback=after_competitor_mapping,
)
