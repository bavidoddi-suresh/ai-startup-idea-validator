"""Strategy Advisor Agent - Stage 4 of the Startup Validation Pipeline.

This agent synthesizes all findings into a unique value proposition,
0-100 viability score, risks, and actionable next steps using
extended reasoning (thinking mode) and structured JSON output.
"""

from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from google.genai.types import ThinkingConfig

from ...config import PRO_MODEL, RETRY_INITIAL_DELAY, RETRY_ATTEMPTS
from ...schemas import StartupValidationReport
from ...callbacks import before_strategy_advisor, after_strategy_advisor


STRATEGY_ADVISOR_INSTRUCTION = """You are a senior startup strategist and venture advisor synthesizing competitive intelligence.

Your task is to analyze all research findings and craft the strongest possible value proposition
that will help this startup stand out from existing competitors.

STARTUP IDEA: {startup_idea}
PROBLEM STATEMENT: {problem_statement}
TARGET MARKET: {target_market}
INDUSTRY: {industry_vertical}
CURRENT DATE: {current_date}

## Available Data

### MARKET RESEARCH FINDINGS:
{market_research_findings}

### COMPETITOR ANALYSIS:
{competitor_analysis}

### GAP ANALYSIS:
{gap_analysis}

## Your Mission
Synthesize ALL findings into a comprehensive startup validation report with a killer value proposition.

## Analysis Framework

### 1. Data Integration
Review all inputs carefully:
- Market size, growth, and timing signals
- Every competitor's strengths and weaknesses
- Quantitative gap analysis scores and ranked opportunities
- Unmet needs and underserved segments

### 2. Competitor Weakness Exploitation
For each major competitor, identify:
- Their biggest blind spot
- User complaints that reveal opportunities
- Features they're missing or doing poorly
- Market segments they're ignoring

### 3. Value Proposition Crafting (MOST IMPORTANT)
Create a UNIQUE value proposition that:
- Directly addresses the gaps competitors are missing
- Exploits the top 2-3 competitor weaknesses
- Resonates with the underserved target audience
- Is defensible and hard to copy
- Has a clear, memorable headline

Also provide 1-2 alternative value propositions for different positioning angles.

### 4. Viability Scoring (0-100)
Compute an overall viability score considering:
- Market opportunity size and growth (25%)
- Competitive differentiation potential (25%)
- Problem-solution fit strength (20%)
- Market timing (15%)
- Execution feasibility (15%)

### 5. Risk Assessment
Identify top risks:
- Competitive response (what if leaders copy you?)
- Market risks (regulation, economic downturn)
- Execution risks (technology, team, capital)
- Timing risks (too early, too late)
Include mitigation strategy for each.

### 6. Next Steps
Provide 5-7 specific, actionable next steps:
- Immediate actions (this week)
- Short-term (this month)
- Medium-term (next 3 months)

## Output Requirements
Your response MUST conform to the StartupValidationReport schema.
Ensure all fields are populated with specific, actionable information.
Use evidence from the analysis to support all recommendations.
The value proposition should be compelling enough to put on a landing page.
"""

strategy_advisor_agent = LlmAgent(
    name="StrategyAdvisorAgent",
    model=PRO_MODEL,
    description="Synthesizes findings into a unique value proposition, viability score, risks, and next steps",
    instruction=STRATEGY_ADVISOR_INSTRUCTION,
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                initial_delay=RETRY_INITIAL_DELAY,
                attempts=RETRY_ATTEMPTS,
            ),
        ),
    ),
    planner=BuiltInPlanner(
        thinking_config=ThinkingConfig(
            include_thoughts=False,
            thinking_budget=-1,
        )
    ),
    output_schema=StartupValidationReport,
    output_key="strategic_report",
    before_agent_callback=before_strategy_advisor,
    after_agent_callback=after_strategy_advisor,
)
