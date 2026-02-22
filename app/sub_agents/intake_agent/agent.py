"""Intake Agent - Extracts startup idea, problem statement, and target market from user request.

This agent parses the user's natural language request and extracts the
required parameters (startup_idea, problem_statement, target_market) into session state
for use by subsequent agents in the pipeline.
"""

from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from pydantic import BaseModel, Field

from ...config import FAST_MODEL, RETRY_INITIAL_DELAY, RETRY_ATTEMPTS


class UserRequest(BaseModel):
    """Structured output for parsing user's startup idea validation request."""

    startup_idea: str = Field(
        description="A clear, concise description of the startup/business idea (e.g., 'AI-powered resume builder for fresh graduates')"
    )
    problem_statement: str = Field(
        description="What problem the startup is solving and for whom (e.g., 'Fresh graduates struggle to create professional resumes that pass ATS systems')"
    )
    target_market: str = Field(
        description="The target market or customer segment (e.g., 'College graduates aged 20-25 in India and US')"
    )
    industry_vertical: Optional[str] = Field(
        default=None,
        description="The industry or vertical (e.g., 'HR Tech', 'EdTech', 'FinTech', 'HealthTech')"
    )
    additional_context: Optional[str] = Field(
        default=None,
        description="Any additional context about the idea, business model, or unique angle"
    )


def after_intake(callback_context: CallbackContext) -> Optional[types.Content]:
    """After intake, copy the parsed values to state for other agents."""
    parsed = callback_context.state.get("parsed_request", {})

    if isinstance(parsed, dict):
        callback_context.state["startup_idea"] = parsed.get("startup_idea", "")
        callback_context.state["problem_statement"] = parsed.get("problem_statement", "")
        callback_context.state["target_market"] = parsed.get("target_market", "")
        callback_context.state["industry_vertical"] = parsed.get("industry_vertical", "")
        callback_context.state["additional_context"] = parsed.get("additional_context", "")
    elif hasattr(parsed, "startup_idea"):
        callback_context.state["startup_idea"] = parsed.startup_idea
        callback_context.state["problem_statement"] = parsed.problem_statement
        callback_context.state["target_market"] = parsed.target_market
        callback_context.state["industry_vertical"] = parsed.industry_vertical or ""
        callback_context.state["additional_context"] = parsed.additional_context or ""

    stages = callback_context.state.get("stages_completed", [])
    stages.append("intake")
    callback_context.state["stages_completed"] = stages

    return None


INTAKE_INSTRUCTION = """You are a request parser for a startup idea validation system.

Your task is to extract the startup idea, problem statement, target market, and industry from the user's request.

## Examples

User: "I want to build an AI-powered resume builder for fresh graduates who struggle with ATS systems"
→ startup_idea: "AI-powered resume builder for fresh graduates"
→ problem_statement: "Fresh graduates struggle to create professional resumes that pass ATS screening systems"
→ target_market: "College graduates and early-career professionals aged 20-25"
→ industry_vertical: "HR Tech / EdTech"

User: "Thinking of a hyperlocal grocery delivery app for tier-2 cities in India"
→ startup_idea: "Hyperlocal grocery delivery app for tier-2 Indian cities"
→ problem_statement: "Tier-2 city residents lack access to quick, reliable grocery delivery services that metro cities enjoy"
→ target_market: "Urban households in tier-2 cities in India (population 500K-2M)"
→ industry_vertical: "E-commerce / Quick Commerce"

User: "I want to create a platform that connects freelance designers with small businesses"
→ startup_idea: "Freelance designer marketplace for small businesses"
→ problem_statement: "Small businesses struggle to find affordable, quality design talent; freelance designers struggle to find steady clients"
→ target_market: "Small businesses with 1-50 employees and freelance graphic/UI designers"
→ industry_vertical: "Marketplace / Creator Economy"

## Instructions
1. Extract a clear, concise description of the business idea
2. Identify the core problem being solved and for whom
3. Determine the target market/customer segment
4. Classify the industry vertical if possible
5. Note any additional context (business model, monetization, unique angle)

If the user is vague, make reasonable inferences and expand the idea into a structured format.
"""

intake_agent = LlmAgent(
    name="IntakeAgent",
    model=FAST_MODEL,
    description="Parses user request to extract startup idea, problem statement, and target market",
    instruction=INTAKE_INSTRUCTION,
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                initial_delay=RETRY_INITIAL_DELAY,
                attempts=RETRY_ATTEMPTS,
            ),
        ),
    ),
    output_schema=UserRequest,
    output_key="parsed_request",
    after_agent_callback=after_intake,
)
