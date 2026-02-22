"""Report Generator Agent - Stage 5 of the Startup Validation Pipeline.

This agent generates a professional McKinsey/BCG-style HTML executive deck
from the structured StartupValidationReport data.
"""

from google.adk.agents import LlmAgent
from google.genai import types

from ...config import FAST_MODEL, RETRY_INITIAL_DELAY, RETRY_ATTEMPTS
from ...tools import generate_html_report
from ...callbacks import before_report_generator, after_report_generator


REPORT_GENERATOR_INSTRUCTION = """You are an executive report generator for startup idea validation analysis.

Your task is to create a professional HTML executive deck using the generate_html_report tool.

STARTUP IDEA: {startup_idea}
PROBLEM STATEMENT: {problem_statement}
TARGET MARKET: {target_market}
CURRENT DATE: {current_date}

## Strategic Report Data
{strategic_report}

## Your Mission
Format the strategic report data and call the generate_html_report tool to create a
McKinsey/BCG-style 7-slide HTML presentation for this startup validation.

## Steps

### Step 1: Format the Report Data
Prepare a comprehensive data summary, including:
- Startup idea overview (idea, problem, target market, industry)
- Market validation (market size, growth trend, validation verdict)
- Competitor landscape (total competitors, top competitor profiles with strengths/weaknesses)
- Key competitor weaknesses and market gaps
- Overall viability score (0-100) with breakdown
- Recommended value proposition (headline, differentiators, why it wins)
- Alternative value propositions
- Risk assessment with mitigations
- Next steps (actionable items for the founder)
- Key strategic insights
- Methodology summary

### Step 2: Call the Tool
Call the generate_html_report tool with the formatted report data.

### Step 3: Report Result
Confirm the report was generated successfully or report any errors.
"""

report_generator_agent = LlmAgent(
    name="ReportGeneratorAgent",
    model=FAST_MODEL,
    description="Generates professional McKinsey/BCG-style HTML executive deck for startup validation",
    instruction=REPORT_GENERATOR_INSTRUCTION,
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                initial_delay=RETRY_INITIAL_DELAY,
                attempts=RETRY_ATTEMPTS,
            ),
        ),
    ),
    tools=[generate_html_report],
    output_key="report_generation_result",
    before_agent_callback=before_report_generator,
    after_agent_callback=after_report_generator,
)
