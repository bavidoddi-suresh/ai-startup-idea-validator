"""Pydantic schemas for Startup Idea Validation Report structured output."""

from typing import List
from pydantic import BaseModel, Field


class CompetitorWeakness(BaseModel):
    """A specific weakness identified in an existing competitor."""

    competitor_name: str = Field(description="Name of the competitor")
    weakness: str = Field(description="The specific weakness or gap")
    opportunity: str = Field(description="How this weakness creates an opportunity for the user's startup")


class CompetitorProfile(BaseModel):
    """Profile of an existing competitor in the space."""

    name: str = Field(description="Company/product name")
    website_or_source: str = Field(description="Website URL or source where found")
    what_they_do: str = Field(description="Brief description of their offering")
    target_audience: str = Field(description="Who they serve")
    estimated_scale: str = Field(description="Estimated scale: Early-stage / Growing / Established / Market Leader")
    strengths: List[str] = Field(description="Their key strengths (2-4 items)")
    weaknesses: List[str] = Field(description="Their key weaknesses or gaps (2-4 items)")
    rating_or_sentiment: str = Field(description="Overall market sentiment or user ratings if available")


class MarketOpportunity(BaseModel):
    """A specific market gap or opportunity identified."""

    gap_name: str = Field(description="Name/title of the gap")
    description: str = Field(description="Detailed description of the unmet need")
    demand_signal: str = Field(description="Evidence of demand for this gap (search trends, user complaints, etc.)")
    difficulty_to_address: str = Field(description="How hard it is to fill: Easy / Medium / Hard")


class ValueProposition(BaseModel):
    """A recommended unique value proposition for the startup."""

    headline: str = Field(description="One-line value proposition headline")
    description: str = Field(description="Detailed explanation of the value proposition")
    differentiators: List[str] = Field(description="3-5 specific differentiators from competitors")
    target_customer: str = Field(description="Ideal customer profile this VP serves")
    why_it_wins: str = Field(description="Why this VP beats existing competitors")


class RiskAssessment(BaseModel):
    """A risk identified for the startup idea."""

    risk: str = Field(description="The risk factor")
    severity: str = Field(description="Low / Medium / High / Critical")
    mitigation: str = Field(description="Recommended mitigation strategy")


class StartupValidationReport(BaseModel):
    """Complete startup idea validation report."""

    startup_idea: str = Field(description="The startup/business idea being validated")
    problem_statement: str = Field(description="The problem the startup aims to solve")
    target_market: str = Field(description="Target market description")
    analysis_date: str = Field(description="Date of the analysis")

    market_size_estimate: str = Field(description="Estimated TAM/SAM/SOM or qualitative market size")
    market_growth_trend: str = Field(description="Growing / Stable / Declining with supporting data")
    market_validation_verdict: str = Field(description="Overall market validation: Strong / Moderate / Weak")

    competitors_found: int = Field(description="Total number of competitors identified")
    competitor_profiles: List[CompetitorProfile] = Field(description="Detailed profiles of top competitors")
    key_competitor_weaknesses: List[CompetitorWeakness] = Field(description="Key weaknesses across competitors")

    market_gaps: List[MarketOpportunity] = Field(description="Identified market gaps and opportunities")

    overall_viability_score: int = Field(description="Overall viability score 0-100", ge=0, le=100)
    recommended_value_proposition: ValueProposition = Field(description="The strongest recommended value proposition")
    alternative_value_propositions: List[ValueProposition] = Field(description="1-2 alternative value propositions")

    risks: List[RiskAssessment] = Field(description="Key risks with mitigation strategies")
    next_steps: List[str] = Field(description="5-7 actionable next steps for the founder")
    key_insights: List[str] = Field(description="4-6 key strategic insights from the analysis")
    methodology_summary: str = Field(description="Summary of how the analysis was performed")
