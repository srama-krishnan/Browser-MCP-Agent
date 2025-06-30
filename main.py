import asyncio
import os
import streamlit as st
from textwrap import dedent
from dotenv import load_dotenv

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.workflows.llm.augmented_llm import RequestParams

load_dotenv()

st.set_page_config(page_title="Browser MCP Agent", layout="wide")

# -------- Sidebar UI -------- #
with st.sidebar:
    st.title("🧭 MCP Command Center")
    st.subheader("Example Commands")

    with st.expander("🌐 Navigation"):
        st.markdown("- `Go to wikipedia.org/wiki/computer_vision`")
        st.markdown("- `Go to example.com and extract fonts`")

    with st.expander("🖱️ Interactions"):
        st.markdown("- `Click on object detection link`")
        st.markdown("- `Scroll down and summarize page`")

    with st.expander("🧩 Multi-step Tasks"):
        st.markdown("- `Navigate to site and summarize all headings`")
        st.markdown("- `Click, extract info, and take screenshot`")

    st.divider()
    st.caption("💡 Powered by Puppeteer + OpenAI")
    
    if st.button("🔁 Reset Session", use_container_width=True):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# --------- Header --------- #
st.markdown("<h1 class='main-header'>🧠 Browser MCP Agent</h1>", unsafe_allow_html=True)
st.markdown("Interact with a powerful web browsing agent that can **navigate**, **extract**, and **reason** with live websites.")

# --------- User Input --------- #
query = st.text_area("📥 Your Command", placeholder="Ask the agent to navigate to websites and interact with them")

# --------- Session Init --------- #
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.mcp_app = MCPApp(name="streamlit_mcp_agent")
    st.session_state.mcp_context = None
    st.session_state.mcp_agent_app = None
    st.session_state.browser_agent = None
    st.session_state.llm = None
    st.session_state.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(st.session_state.loop)

# --------- Agent Setup --------- #
async def setup_agent():
    if not st.session_state.initialized:
        try:
            st.session_state.mcp_context = st.session_state.mcp_app.run()
            st.session_state.mcp_agent_app = await st.session_state.mcp_context.__aenter__()
            st.session_state.browser_agent = Agent(
                name="browser",
                instruction=dedent("""
                    You are a helpful web browsing assistant that can interact with websites using puppeteer.
                    - Navigate to websites and perform browser actions (click, scroll, type)
                    - Extract information from web pages (text, CSS, colors, fonts)
                    - Take screenshots when useful
                    - Provide summaries of web content
                    - Follow multi-step sequences with precision
                """),
                server_names=["puppeteer"]
            )
            await st.session_state.browser_agent.initialize()
            st.session_state.llm = await st.session_state.browser_agent.attach_llm(OpenAIAugmentedLLM)
            st.session_state.initialized = True
        except Exception as e:
            return f"❌ Error during initialization: {str(e)}"
    return None

# --------- Task Run Logic --------- #
async def run_mcp_agent(message):
    if not os.getenv("OPENAI_API_KEY"):
        return "❌ Error: No OpenAI API key found."

    try:
        error = await setup_agent()
        if error:
            return error

        result = await st.session_state.llm.generate_str(
            message=message,
            request_params=RequestParams(use_history=True, max_messages=3)
        )
        return result

    except Exception as e:
        return f"❌ Error: {str(e)}"

# --------- Run Button --------- #
if st.button("🚀 Run Command", type="primary", use_container_width=True):
    if not query.strip():
        st.warning("⚠️ Please enter a command first.")
    else:
        with st.spinner("Processing your result..."):
            result = st.session_state.loop.run_until_complete(run_mcp_agent(query))
        st.markdown("## 🧾 Response")
        st.markdown(result)
