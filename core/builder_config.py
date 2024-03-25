"""Configuration."""
import streamlit as st
import os

### DEFINE BUILDER_LLM #####

## OpenAI
from llama_index.llms import OpenAI

# set OpenAI Key - use Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets.openai_key
# load LLM
BUILDER_LLM = OpenAI(model="gpt-4-1106-preview")

# # Anthropic (記得安裝 `pip install anthropic`)
# from llama_index.llms import Anthropic
