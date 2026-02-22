# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""HTML Report Generator tool for creating executive reports.

Uses direct text generation to create McKinsey/BCG style 7-slide HTML
presentations from startup validation report data.
Saves the generated HTML as an artifact for download in adk web.
"""

import logging
from datetime import datetime
from google.adk.tools import ToolContext
from google.genai import types
from google.genai.errors import ServerError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from ..config import PRO_MODEL

logger = logging.getLogger("StartupValidationPipeline")


async def generate_html_report(report_data: str, tool_context: ToolContext) -> dict:
    """Generate a McKinsey/BCG style HTML executive report and save as artifact.

    This tool creates a professional 7-slide HTML presentation from the
    startup validation report data using direct text generation with Gemini.

    Args:
        report_data: The startup validation report data containing idea overview,
                    competitors, weaknesses, value proposition, scores, and next steps.
        tool_context: ADK ToolContext for saving artifacts.

    Returns:
        dict with status, message, artifact_filename, artifact_version, html_length,
        or error_message if failed.
    """
    try:
        from google import genai

        # Initialize client (uses GOOGLE_API_KEY from env)
        client = genai.Client()

        current_date = datetime.now().strftime("%Y-%m-%d")

        prompt = f"""Generate a comprehensive, professional HTML report for a startup idea validation analysis.

This report should be in the style of McKinsey/BCG consulting presentations:
- Multi-slide format using full-screen scrollable sections
- Modern, clean, executive-ready design
- Data-driven visualizations
- Professional color scheme and typography

CRITICAL REQUIREMENTS:

1. STRUCTURE - Create 7 distinct slides (full-screen sections):

   SLIDE 1 - EXECUTIVE SUMMARY
   - Startup idea name and one-line description
   - Large, prominent viability score (X/100) with visual gauge
   - Market validation verdict (Strong/Moderate/Weak)
   - Problem statement and target market
   - Eye-catching hero section

   SLIDE 2 - MARKET OPPORTUNITY
   - Market size (TAM/SAM/SOM)
   - Growth trend with supporting data
   - Target demographics
   - Demand signals and timing assessment

   SLIDE 3 - COMPETITIVE LANDSCAPE
   - Total competitors found
   - Top competitor profiles (name, what they do, strengths, weaknesses)
   - Visual cards for each major competitor
   - Market position categorization

   SLIDE 4 - COMPETITOR WEAKNESSES & MARKET GAPS
   - Key weaknesses across competitors (with opportunity each creates)
   - Identified market gaps
   - Unmet needs and underserved segments
   - Feature gap matrix if applicable

   SLIDE 5 - YOUR VALUE PROPOSITION
   - Large, prominent display of recommended VP headline
   - Key differentiators (3-5 items with visual icons)
   - Target customer profile
   - Why this VP wins against competitors
   - Alternative positioning options

   SLIDE 6 - RISKS & NEXT STEPS
   - Risk assessment (risk, severity, mitigation) in a table/card format
   - Actionable next steps (numbered, categorized by timeline)
   - Key strategic insights

   SLIDE 7 - METHODOLOGY
   - How the analysis was performed
   - Data sources and approach

2. DESIGN:
   - Use professional consulting color palette:
     * Primary: Navy blue (#1e3a8a, #3b82f6) for headers/trust
     * Success: Green (#059669, #10b981) for positive metrics
     * Warning: Amber (#d97706, #f59e0b) for concerns
     * Neutral: Grays (#6b7280, #e5e7eb) for backgrounds
   - Modern sans-serif fonts (system: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto)
   - Cards with subtle shadows and rounded corners
   - Generous white space and padding
   - Responsive grid layouts

3. TECHNICAL:
   - Self-contained: ALL CSS embedded in <style> tag
   - No external dependencies (no CDNs, no external images)
   - Each slide: min-height: 100vh; page-break-after: always;
   - Smooth scroll behavior
   - Print-friendly

4. DATA TO INCLUDE (use EXACTLY this data, do not invent):

{report_data}

5. OUTPUT:
   - Generate ONLY the complete HTML code
   - Start with <!DOCTYPE html>
   - End with </html>
   - NO explanations before or after the HTML
   - NO markdown code fences

Make it visually stunning, data-rich, and executive-ready.

Current date: {current_date}
"""

        logger.info("Generating HTML report using Gemini...")

        # Retry wrapper for handling model overload errors
        @retry(
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=2, min=2, max=30),
            retry=retry_if_exception_type(ServerError),
            before_sleep=lambda retry_state: logger.warning(
                f"Gemini API error, retrying in {retry_state.next_action.sleep} seconds... "
                f"(attempt {retry_state.attempt_number}/3)"
            ),
        )
        def generate_with_retry():
            return client.models.generate_content(
                model=PRO_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=1.0),
            )

        # Direct text generation (NOT code execution)
        # Same as original notebook: types.GenerateContentConfig(temperature=1.0)
        response = generate_with_retry()

        # Extract HTML from response.text
        html_code = response.text
        # Strip markdown code fences if present
        if html_code.startswith("```"):
            # Remove opening fence (```html or ```)
            if html_code.startswith("```html"):
                html_code = html_code[7:]
            elif html_code.startswith("```HTML"):
                html_code = html_code[7:]
            else:
                html_code = html_code[3:]

            # Remove closing fence
            if html_code.rstrip().endswith("```"):
                html_code = html_code.rstrip()[:-3]

            html_code = html_code.strip()

        # Validate we got HTML
        if not html_code.strip().startswith("<!DOCTYPE") and not html_code.strip().startswith("<html"):
            logger.warning("Generated content may not be valid HTML")

        # Save as artifact with proper MIME type so it appears in ADK web UI
        html_artifact = types.Part.from_bytes(
            data=html_code.encode('utf-8'),
            mime_type="text/html"
        )
        artifact_filename = "executive_report.html"

        version = await tool_context.save_artifact(
            filename=artifact_filename,
            artifact=html_artifact
        )

        # Also store in state for AG-UI frontend display
        tool_context.state["html_report_content"] = html_code

        logger.info(f"Saved HTML report artifact: {artifact_filename} (version {version})")

        return {
            "status": "success",
            "message": f"HTML report generated and saved as artifact '{artifact_filename}'",
            "artifact_filename": artifact_filename,
            "artifact_version": version,
            "html_length": len(html_code),
        }

    except Exception as e:
        logger.error(f"Failed to generate HTML report: {e}")
        return {
            "status": "error",
            "error_message": f"Failed to generate HTML report: {str(e)}",
        }
