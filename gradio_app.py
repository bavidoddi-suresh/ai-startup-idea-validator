"""Gradio web interface for the AI Startup Idea Validator.

Wraps the ADK multi-agent pipeline in a Gradio chat UI with an API key
input field, making it deployable on Hugging Face Spaces or any platform.
Users provide their own Google AI Studio API key to run the analysis.
"""

import os
import logging

import gradio as gr

os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "FALSE")
os.environ.setdefault("GOOGLE_API_KEY", "not-set-yet")

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

from app.agent import root_agent
from app.config import APP_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GradioApp")


async def respond(message: str, history: list, api_key: str):
    """Process user message through the ADK agent pipeline."""

    if not api_key or not api_key.strip():
        yield (
            "⚠️ **Please enter your Google AI Studio API key** in the "
            "field above before chatting.\n\n"
            "Get a free key at: "
            "[aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)"
        )
        return

    os.environ["GOOGLE_API_KEY"] = api_key.strip()

    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id="web_user",
    )

    content = genai_types.Content(
        role="user",
        parts=[genai_types.Part(text=message)],
    )

    full_response = ""
    current_agent = ""

    try:
        async for event in runner.run_async(
            user_id="web_user",
            session_id=session.id,
            new_message=content,
        ):
            if (
                hasattr(event, "author")
                and event.author
                and event.author != current_agent
            ):
                current_agent = event.author
                full_response += f"\n\n---\n**🔄 {current_agent}**\n\n"
                yield full_response

            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        full_response += part.text
                        yield full_response

    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower() or "missing key" in error_msg.lower():
            yield (
                full_response
                + "\n\n❌ **Invalid API Key.** Please check your key and try again."
            )
        else:
            yield full_response + f"\n\n❌ **Error:** {error_msg}"
        return

    if not full_response.strip():
        yield "✅ Pipeline completed."


with gr.Blocks(theme=gr.themes.Soft(), title="AI Startup Idea Validator") as demo:
    gr.Markdown("# 🚀 AI Startup Idea Validator")
    gr.Markdown(
        "**Test your startup/business idea with AI.** Enter your Google AI "
        "Studio API key below, then describe your idea. The AI will find "
        "competitors, point out their weaknesses, and suggest a unique value "
        "proposition to help you compete.\n\n"
        "⏱️ Full analysis takes 3–8 minutes (6 AI agents run sequentially)."
    )

    api_key = gr.Textbox(
        label="🔑 Google AI Studio API Key (required)",
        placeholder="Paste your API key here (get one free at aistudio.google.com/app/apikey)",
        type="password",
    )

    chatbot = gr.Chatbot(height=500, label="Startup Validator")
    msg = gr.Textbox(
        label="Your startup idea",
        placeholder="e.g. I want to build an AI-powered resume builder for fresh graduates...",
    )

    with gr.Row():
        submit_btn = gr.Button("Analyze", variant="primary")
        clear_btn = gr.ClearButton([msg, chatbot], value="Clear")

    gr.Examples(
        examples=[
            "I want to build an AI-powered resume builder for fresh graduates who struggle with ATS systems",
            "A hyperlocal grocery delivery app for tier-2 cities in India",
            "An app connecting patients with dietitians for personalized meal plans",
            "A micro-investment platform for college students to invest spare change",
            "A project management tool specifically for freelancers and solopreneurs",
        ],
        inputs=msg,
    )

    async def user_message(message, history):
        """Add user message to chat and clear input."""
        return "", history + [{"role": "user", "content": message}]

    async def bot_response(history, key):
        """Generate bot response via the ADK pipeline."""
        user_msg = history[-1]["content"]
        history.append({"role": "assistant", "content": ""})

        async for chunk in respond(user_msg, history, key):
            history[-1]["content"] = chunk
            yield history

    msg.submit(user_message, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot_response, [chatbot, api_key], chatbot
    )
    submit_btn.click(user_message, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot_response, [chatbot, api_key], chatbot
    )

if __name__ == "__main__":
    demo.queue()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
    )
