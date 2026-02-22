"""Gap Analysis Agent - Stage 3 of the Startup Validation Pipeline.

This agent performs quantitative gap analysis using Python code execution
to compute competitive saturation, demand signals, opportunity scoring,
and identify the best positioning for the startup.
"""

from google.adk.agents import LlmAgent
from google.adk.code_executors import BuiltInCodeExecutor
from google.genai import types

from ...config import CODE_EXEC_MODEL, RETRY_INITIAL_DELAY, RETRY_ATTEMPTS
from ...callbacks import before_gap_analysis, after_gap_analysis


GAP_ANALYSIS_INSTRUCTION = """You are a data scientist analyzing startup competitive landscapes using quantitative methods.

Your task is to perform advanced gap analysis on the market research and competitor data collected.

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

## Your Mission
Write and execute Python code to perform quantitative competitive analysis.

## Analysis Steps

### Step 1: Parse Competitor Data
Extract from the competitor analysis:
- Competitor names and categories (direct/indirect/emerging)
- Strengths count and weakness count per competitor
- Market position (Leader/Challenger/Niche/New)
- Pricing tier
- Key features offered (build a feature matrix)

### Step 2: Build Competitive Feature Matrix
Create a matrix showing:
- Rows: Competitors
- Columns: Key features/capabilities in this space
- Values: 1 (has feature), 0 (doesn't have), 0.5 (partial)
- Identify which features are table-stakes vs differentiators

### Step 3: Compute Competitive Metrics

**Market Saturation Score (0-100):**
- Number of direct competitors (weight: 40%)
- Combined funding of competitors (weight: 20%)
- Market leader dominance (weight: 20%)
- Feature coverage overlap (weight: 20%)

**Opportunity Score (0-100):**
- Number of unaddressed gaps (weight: 35%)
- Severity of competitor weaknesses (weight: 25%)
- Market growth rate (weight: 20%)
- Underserved segments identified (weight: 20%)

**Differentiation Potential (0-100):**
- Features no competitor offers (weight: 40%)
- Weakness exploitation potential (weight: 30%)
- Unique positioning angles (weight: 30%)

### Step 4: Identify Top Gaps
Rank the market gaps by:
- How many competitors miss this gap
- How strong the demand signal is
- How feasible it is to address

### Step 5: Compute Overall Viability Score
Weighted composite:
- Market opportunity (30%)
- Differentiation potential (30%)
- Competitive saturation (inverted) (20%)
- Market timing (20%)

### Step 6: Output Results
Generate clear output showing:
1. Competitive feature matrix
2. Saturation, opportunity, and differentiation scores
3. Top 3-5 ranked gaps with justification
4. Overall viability score with breakdown
5. Recommended positioning strategy

## Code Guidelines
- Use pandas for data manipulation
- Print all results clearly formatted
- Include intermediate calculations for transparency
- Handle missing data gracefully

Execute the code and provide actionable insights based on the quantitative findings.
"""

gap_analysis_agent = LlmAgent(
    name="GapAnalysisAgent",
    model=CODE_EXEC_MODEL,
    description="Performs quantitative gap analysis using Python code execution for competitive scoring and opportunity ranking",
    instruction=GAP_ANALYSIS_INSTRUCTION,
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                initial_delay=RETRY_INITIAL_DELAY,
                attempts=RETRY_ATTEMPTS,
            ),
        ),
    ),
    code_executor=BuiltInCodeExecutor(),
    output_key="gap_analysis",
    before_agent_callback=before_gap_analysis,
    after_agent_callback=after_gap_analysis,
)
