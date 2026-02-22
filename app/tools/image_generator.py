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

"""Gemini image generation tool for creating shareable startup validation infographics.

Uses Google AI Studio (API key) for authentication.
Uses gemini-3-pro-image-preview model for image generation.
Saves the generated infographic as an artifact accessible in adk web UI.
"""

import base64
import logging
from google.adk.tools import ToolContext
from google.genai import types
from google.genai.errors import ServerError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from ..config import IMAGE_MODEL

logger = logging.getLogger("StartupValidationPipeline")


async def generate_infographic(data_summary: str, tool_context: ToolContext) -> dict:
    """Generate an infographic image using Gemini's image generation capabilities.

    Creates a shareable visual summary of the startup validation results.

    Args:
        data_summary: A concise summary of the startup validation report
                     including viability score, competitors, value proposition, and key metrics.
        tool_context: ADK ToolContext for saving artifacts and accessing state.

    Returns:
        dict with status, message, artifact_saved, or error_message.
    """
    try:
        from google import genai

        # Initialize Gemini client using AI Studio (not Vertex AI)
        # This uses GOOGLE_API_KEY from environment automatically
        client = genai.Client()

        prompt = f"""Generate a professional, shareable business infographic for a startup idea validation report.

DATA TO VISUALIZE:
{data_summary}

DESIGN REQUIREMENTS:
- Professional, clean startup/VC pitch style
- Use a bold color palette (deep blue, teal, coral accents)
- Large, prominent viability score display
- Clear visual hierarchy with sections
- Show competitor count and key metrics prominently
- Feature the value proposition headline prominently
- Include icons or simple graphics for each section
- Make it suitable for sharing on LinkedIn/Twitter
- 16:9 aspect ratio

Create an infographic that a startup founder would share with investors or on social media.
"""

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
                model=IMAGE_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"],
                    image_config=types.ImageConfig(
                        aspect_ratio="16:9",
                    ),
                ),
            )

        # Generate the image using Gemini 3 Pro Image model
        response = generate_with_retry()

        # Check for successful generation
        if response.candidates and len(response.candidates) > 0:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "inline_data") and part.inline_data:
                    image_bytes = part.inline_data.data
                    mime_type = part.inline_data.mime_type or "image/png"

                    # Save the image directly as an artifact using tool_context
                    # This is the recommended ADK pattern for saving binary artifacts
                    # Note: save_artifact is async, so we must await it
                    try:
                        image_artifact = types.Part.from_bytes(
                            data=image_bytes,
                            mime_type=mime_type
                        )
                        artifact_filename = "infographic.png"
                        version = await tool_context.save_artifact(
                            filename=artifact_filename,
                            artifact=image_artifact
                        )
                        logger.info(f"Saved infographic artifact: {artifact_filename} (version {version})")

                        # Also store base64 in state for AG-UI frontend display
                        b64_image = base64.b64encode(image_bytes).decode('utf-8')
                        tool_context.state["infographic_base64"] = f"data:{mime_type};base64,{b64_image}"

                        return {
                            "status": "success",
                            "message": f"Infographic generated and saved as artifact '{artifact_filename}'",
                            "artifact_saved": True,
                            "artifact_filename": artifact_filename,
                            "artifact_version": version,
                            "mime_type": mime_type,
                        }
                    except Exception as save_error:
                        logger.warning(f"Failed to save artifact: {save_error}")
                        # Still return success with base64 data as fallback
                        return {
                            "status": "success",
                            "message": "Infographic generated but artifact save failed",
                            "artifact_saved": False,
                            "image_data": base64.b64encode(image_bytes).decode("utf-8"),
                            "mime_type": mime_type,
                            "save_error": str(save_error),
                        }

        # No image found in response
        return {
            "status": "error",
            "error_message": "No image was generated in the response. The model may have returned text only.",
        }

    except Exception as e:
        logger.error(f"Failed to generate infographic: {e}")
        return {
            "status": "error",
            "error_message": f"Failed to generate infographic: {str(e)}",
        }
