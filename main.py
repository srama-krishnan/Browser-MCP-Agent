import asyncio
import os
import streamlit as st
from textwrap import dedent

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.workflows.llm.augmented_llm import RequestParams

st.set_page_config(page_title="Browser MCP Agent", layout="wide")

st.markdown("<h1 class='main-header'> Browser MCP Agent</h1>", unsafe_allow_html=True)
st.markdown("Interact with a powerful web browsing agent that can navigate and interact with websites")

with st.sidebar:
    st.markdown("### Example commands")
    st.markdown("**Navigation**")
    st.markdown("Go to wikipedia.org/wiki/computer_vision")

    st.markdown("**Interaction**")
    st.markdown("Click on the link to object detection and take a screenshot")
    st.markdown("Scroll down and summarize the page")

    st.markdown("**Multi-step Tasks**")
    st.markdown("Navigate to wikipedia.org/wiki/computer_vision, scroll down and report details")
    st.markdown("Scroll down and summarize the wikipedia page")

    st.caption("The agent uses puppeteer to control the browser")

query = st.text_area("Your command", placeholder="Ask the agent to navigate to websites and interact with them")
