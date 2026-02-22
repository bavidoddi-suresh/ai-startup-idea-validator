"""Startup Idea Validator Agent - Root Agent Definition.

This module defines the root agent for the Startup Validation Pipeline.
It uses a SequentialAgent to orchestrate 6 specialized sub-agents:

1. MarketResearchAgent - Market size, trends, and demand validation with Google Search
2. CompetitorMappingAgent - Competitor discovery and weakness analysis with deep web research
3. GapAnalysisAgent - Quantitative gap analysis with Python code execution
4. StrategyAdvisorAgent - Value proposition crafting with extended reasoning
5. ReportGeneratorAgent - McKinsey/BCG-style HTML exec deck
6. InfographicGeneratorAgent - Shareable visual summary

The pipeline validates a startup idea and produces a unique value proposition
to help founders compete effectively.

Authentication:
    Uses Google AI Studio (API key) instead of Vertex AI.
    Set environment variables:
        GOOGLE_API_KEY=your_api_key
        GOOGLE_GENAI_USE_VERTEXAI=FALSE
"""

from google.adk.agents import SequentialAgent
from google.adk.agents.llm_agent import Agent
from google.adk.tools.agent_tool import AgentTool


from .sub_agents.intake_agent.agent import intake_agent
from .sub_agents.market_research.agent import market_research_agent
from .sub_agents.competitor_mapping.agent import competitor_mapping_agent
from .sub_agents.gap_analysis.agent import gap_analysis_agent
from .sub_agents.strategy_advisor.agent import strategy_advisor_agent
from .sub_agents.report_generator.agent import report_generator_agent
from .sub_agents.infographic_generator.agent import infographic_generator_agent

from .config import FAST_MODEL, APP_NAME

startup_validation_pipeline = SequentialAgent(
    name="StartupValidationPipeline",
    description="""Comprehensive startup idea validation pipeline.

This agent analyzes a startup/business idea to produce:
1. Market research with real-time data (size, trends, demographics)
2. Competitor discovery and weakness analysis
3. Quantitative gap analysis and opportunity scoring
4. A unique value proposition to beat competitors
5. Professional HTML executive deck
6. Shareable visual infographic

Input from state:
- startup_idea: {startup_idea}
- problem_statement: {problem_statement}
- target_market: {target_market}
- industry_vertical: {industry_vertical}

The analysis runs automatically through all stages and produces artifacts
including JSON report, HTML exec deck, and infographic.
""",
    sub_agents=[
        market_research_agent,          # Stage 1: Market validation
        competitor_mapping_agent,       # Stage 2: Competitor discovery & weaknesses
        gap_analysis_agent,             # Stage 3: Quantitative gap analysis
        strategy_advisor_agent,         # Stage 4: Value proposition & scoring
        report_generator_agent,         # Stage 5: HTML exec deck
        infographic_generator_agent,    # Stage 6: Visual infographic
    ],
)

root_agent = Agent(
    model=FAST_MODEL,
    name=APP_NAME,
    description='An AI-powered startup idea validator that finds competitors, identifies their weaknesses, and crafts a unique value proposition to help you compete.',
    instruction="""You are a startup idea validation assistant. Your job is to help founders test their business ideas.

1. Start by greeting the user warmly and explaining what you do:
   - You validate startup/business ideas using AI
   - You find companies already doing something similar
   - You point out their weaknesses
   - You suggest a stronger value proposition to help them compete

2. Ask for their startup/business idea. You need:
   - **What is the idea?** (the product/service they want to build)
   - **What problem does it solve?** (the pain point they're addressing)
   - **Who is it for?** (their target market/customer)
   
   If they provide all this in one message, great. If not, ask follow-up questions.

3. Once you have the idea details, call the `IntakeAgent` tool to parse and structure their input.

4. After the IntakeAgent succeeds, delegate the full analysis to the `StartupValidationPipeline`.

5. The pipeline will automatically:
   - Research the market opportunity
   - Find all existing competitors and their weaknesses
   - Run quantitative gap analysis
   - Craft a unique value proposition
   - Generate a professional HTML report
   - Create a shareable infographic

Be encouraging but honest. Help founders understand their competitive landscape clearly.""",
    sub_agents=[startup_validation_pipeline],
    tools=[AgentTool(intake_agent)],
)

from google.adk.apps.app import App

app = App(root_agent=root_agent, name="app")
