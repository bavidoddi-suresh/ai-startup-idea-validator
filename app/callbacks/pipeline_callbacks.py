"""Pipeline callbacks for logging, state tracking, and artifact management.

This module provides before/after callbacks for each agent in the
Startup Validation Pipeline. Callbacks handle:
- Logging stage transitions
- Tracking pipeline progress in state
- Saving artifacts (JSON report, HTML report, infographic)
"""

import json
import logging
from datetime import datetime
from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.genai import types

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("StartupValidationPipeline")


# ============================================================================
# BEFORE AGENT CALLBACKS
# ============================================================================

def before_market_research(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log start of market research phase and initialize pipeline tracking."""
    logger.info("=" * 60)
    logger.info("STAGE 1: MARKET RESEARCH - Starting")
    logger.info(f"  Startup Idea: {callback_context.state.get('startup_idea', 'Not set')}")
    logger.info(f"  Problem: {callback_context.state.get('problem_statement', 'Not set')}")
    logger.info(f"  Target Market: {callback_context.state.get('target_market', 'Not set')}")
    logger.info("=" * 60)

    callback_context.state["current_date"] = datetime.now().strftime("%Y-%m-%d")
    callback_context.state["pipeline_stage"] = "market_research"
    callback_context.state["pipeline_start_time"] = datetime.now().isoformat()

    if "stages_completed" not in callback_context.state:
        callback_context.state["stages_completed"] = []

    return None


def before_competitor_mapping(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log start of competitor mapping phase."""
    logger.info("=" * 60)
    logger.info("STAGE 2: COMPETITOR MAPPING - Starting")
    logger.info("  Discovering competitors and analyzing weaknesses...")
    logger.info("=" * 60)

    callback_context.state["current_date"] = datetime.now().strftime("%Y-%m-%d")
    callback_context.state["pipeline_stage"] = "competitor_mapping"

    if "competitor_analysis" not in callback_context.state:
        callback_context.state["competitor_analysis"] = "Competitor data being collected..."

    return None


def before_gap_analysis(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log start of gap analysis phase."""
    logger.info("=" * 60)
    logger.info("STAGE 3: GAP ANALYSIS - Starting")
    logger.info("  Executing Python code for quantitative competitive analysis...")
    logger.info("=" * 60)

    callback_context.state["current_date"] = datetime.now().strftime("%Y-%m-%d")
    callback_context.state["pipeline_stage"] = "gap_analysis"

    if "gap_analysis" not in callback_context.state:
        callback_context.state["gap_analysis"] = "Gap analysis being computed..."

    return None


def before_strategy_advisor(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log start of strategy synthesis phase."""
    logger.info("=" * 60)
    logger.info("STAGE 4: STRATEGY ADVISOR - Starting")
    logger.info("  Crafting value proposition with extended reasoning...")
    logger.info("  Generating structured StartupValidationReport...")
    logger.info("=" * 60)

    callback_context.state["current_date"] = datetime.now().strftime("%Y-%m-%d")
    callback_context.state["pipeline_stage"] = "strategy_synthesis"

    return None


def before_report_generator(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log start of report generation phase."""
    logger.info("=" * 60)
    logger.info("STAGE 5: REPORT GENERATION - Starting")
    logger.info("  Generating McKinsey/BCG style HTML executive deck...")
    logger.info("=" * 60)

    callback_context.state["current_date"] = datetime.now().strftime("%Y-%m-%d")
    callback_context.state["pipeline_stage"] = "report_generation"

    return None


def before_infographic_generator(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log start of infographic generation phase."""
    logger.info("=" * 60)
    logger.info("STAGE 6: INFOGRAPHIC GENERATION - Starting")
    logger.info("  Creating shareable visual summary...")
    logger.info("=" * 60)

    callback_context.state["current_date"] = datetime.now().strftime("%Y-%m-%d")
    callback_context.state["pipeline_stage"] = "infographic_generation"

    return None


# ============================================================================
# AFTER AGENT CALLBACKS
# ============================================================================

def after_market_research(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log completion of market research and update tracking."""
    findings = callback_context.state.get("market_research_findings", "")
    findings_len = len(findings) if isinstance(findings, str) else 0

    logger.info(f"STAGE 1: COMPLETE - Market research findings: {findings_len} characters")

    stages = callback_context.state.get("stages_completed", [])
    stages.append("market_research")
    callback_context.state["stages_completed"] = stages

    return None


def after_competitor_mapping(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log completion of competitor mapping."""
    analysis = callback_context.state.get("competitor_analysis", "")
    analysis_len = len(analysis) if isinstance(analysis, str) else 0

    logger.info(f"STAGE 2: COMPLETE - Competitor analysis: {analysis_len} characters")

    stages = callback_context.state.get("stages_completed", [])
    stages.append("competitor_mapping")
    callback_context.state["stages_completed"] = stages

    return None


def after_gap_analysis(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log completion of gap analysis and extract executed Python code."""
    gap = callback_context.state.get("gap_analysis", "")
    gap_len = len(gap) if isinstance(gap, str) else 0

    logger.info(f"STAGE 3: COMPLETE - Gap analysis: {gap_len} characters")

    extracted_code = _extract_python_code_from_content(gap)

    if not extracted_code:
        extracted_code = _extract_code_from_invocation(callback_context)

    if extracted_code:
        callback_context.state["gap_analysis_code"] = extracted_code
        logger.info(f"  Extracted Python code: {len(extracted_code)} characters")
    else:
        logger.info("  No Python code blocks found to extract")

    stages = callback_context.state.get("stages_completed", [])
    stages.append("gap_analysis")
    callback_context.state["stages_completed"] = stages

    return None


def _extract_code_from_invocation(callback_context: CallbackContext) -> str:
    """Extract Python code from invocation context session events."""
    code_blocks = []

    try:
        invocation = getattr(callback_context, '_invocation_context', None) or \
                     getattr(callback_context, 'invocation_context', None)

        if not invocation:
            return ""

        session = getattr(invocation, 'session', None)
        if not session:
            return ""

        events = getattr(session, 'events', None) or []

        for event in events:
            content = getattr(event, 'content', None)
            if not content:
                continue

            parts = getattr(content, 'parts', None) or []
            for part in parts:
                exec_code = getattr(part, 'executable_code', None)
                if exec_code:
                    code = getattr(exec_code, 'code', None)
                    if code and code.strip():
                        code_blocks.append(code.strip())

    except Exception as e:
        logger.warning(f"Error extracting code from invocation context: {e}")

    return "\n\n# --- Next Code Block ---\n\n".join(code_blocks)


def _extract_python_code_from_content(content: str) -> str:
    """Extract Python code blocks from markdown content."""
    import re

    if not content:
        return ""

    code_blocks = []
    pattern = r'```(?:python|py)\s*\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)

    for match in matches:
        code = match.strip()
        if code:
            code_blocks.append(code)

    return "\n\n# ---\n\n".join(code_blocks)


def after_strategy_advisor(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log completion and save JSON artifact."""
    report = callback_context.state.get("strategic_report", {})
    logger.info("STAGE 4: COMPLETE - Strategic report generated")

    if report:
        try:
            if hasattr(report, "model_dump"):
                report_dict = report.model_dump()
            else:
                report_dict = report

            json_str = json.dumps(report_dict, indent=2, default=str)
            json_artifact = types.Part.from_bytes(
                data=json_str.encode('utf-8'),
                mime_type="application/json"
            )
            callback_context.save_artifact("validation_report.json", json_artifact)
            logger.info("  Saved artifact: validation_report.json")
        except Exception as e:
            logger.warning(f"  Failed to save JSON artifact: {e}")

    stages = callback_context.state.get("stages_completed", [])
    stages.append("strategy_synthesis")
    callback_context.state["stages_completed"] = stages

    return None


def after_report_generator(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log completion of report generation."""
    logger.info("STAGE 5: COMPLETE - HTML executive deck generated")

    stages = callback_context.state.get("stages_completed", [])
    stages.append("report_generation")
    callback_context.state["stages_completed"] = stages

    return None


def after_infographic_generator(callback_context: CallbackContext) -> Optional[types.Content]:
    """Log completion of infographic generation."""
    logger.info("STAGE 6: COMPLETE - Infographic generated")

    stages = callback_context.state.get("stages_completed", [])
    stages.append("infographic_generation")
    callback_context.state["stages_completed"] = stages

    logger.info("=" * 60)
    logger.info("STARTUP VALIDATION PIPELINE COMPLETE")
    logger.info(f"  Stages completed: {stages}")
    logger.info(f"  Total stages: {len(stages)}")
    logger.info("=" * 60)

    return None
