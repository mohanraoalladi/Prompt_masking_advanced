import yaml
import json
import streamlit as st

from agents.orchestrator_agent import OrchestratorAgent
from color_mapper import colorize_masked_text, get_color_legend


def load_config():
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_sample_prompts():
    with open("sample_prompts.json", "r", encoding="utf-8") as f:
        return json.load(f)


config = load_config()

st.set_page_config(page_title="PII Masking + Gemini + Unmasking", layout="wide")
st.title("🔐 PII Masking → 🤖 Gemini → 🔓 Unmasking")



if "history" not in st.session_state:
    st.session_state.history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

api_key = config.get("GEMINI_API_KEY", "YOUR_KEY_HERE")
model_name = config.get("MODEL_NAME", "gemini-1.5-pro")

pii_enabled_cfg = config.get("PII_CATEGORIES_ENABLED", {})
pii_categories_enabled = {}

st.sidebar.header("PII Categories")
for cat, enabled in pii_enabled_cfg.items():
    pii_categories_enabled[cat] = st.sidebar.checkbox(cat, value=enabled)

use_llm = config.get("USE_LLM", True)

# Load sample prompts
sample_prompts = load_sample_prompts()

# Sample prompts section
st.subheader("📝 Sample Prompts")

def load_sample_callback():
    """Callback to load sample prompt when selected"""
    if st.session_state.sample_selector:
        st.session_state.user_input = sample_prompts[st.session_state.sample_selector]
        st.session_state.sample_selector = ""  # Reset selector

st.selectbox(
    "Select a sample prompt to auto-load:",
    options=[""] + list(sample_prompts.keys()),
    key="sample_selector",
    on_change=load_sample_callback,
    label_visibility="collapsed"
)

# Text input area with session state
user_input = st.text_area(
    "Enter your prompt:",
    height=400,
    key="user_input"
)

if st.button("Run"):
    if not user_input.strip():
        st.warning("Please enter some text.")
    elif use_llm and api_key == "YOUR_KEY_HERE":
        st.error("Please set your GEMINI_API_KEY in config/config.yaml")
    else:
        orchestrator = OrchestratorAgent(
            api_key=api_key,
            model_name=model_name,
            pii_categories_enabled=pii_categories_enabled,
        )
        result = orchestrator.run(user_input, use_llm=use_llm)
        st.session_state.history.append(result)

st.subheader("Conversation History")
# Display color legend
st.markdown("### 🎨 PII Entity Color Guide")
st.markdown(get_color_legend(), unsafe_allow_html=True)
for turn_idx, item in enumerate(reversed(st.session_state.history), start=1):
    total_turns = len(st.session_state.history)
    turn_number = total_turns - turn_idx + 1
    turn_id = f"turn_{int(item['id'])}"
    
    st.markdown(f"### Turn {turn_number}")

    with st.expander("Original Prompt", expanded=True):
        st.text_area("Original Prompt Content", value=item["original_prompt"], height=400, disabled=True, key=f"{turn_id}_orig")

    with st.expander("Masked Prompt (sent to LLM)", expanded=True):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**📍 Colored View**")
            st.markdown("(Hover over colored placeholders to see original values)")
            # Display colored version
            colored_html = colorize_masked_text(item["masked_prompt"], item["mapping"])
            st.markdown(colored_html, unsafe_allow_html=True)
        
        with col2:
            #st.markdown("**📋 Plain Text View**")
            st.markdown("(Copy-paste version)")
            # Show plain text for copying
            st.code(item["masked_prompt"], language="text")

    with st.expander("Mapping (placeholder → original)", expanded=True):
        st.json(item["mapping"])

    with st.expander("LLM Response (on masked prompt)", expanded=True):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**📍 Colored View**")
            st.markdown("(Hover over colored placeholders to see original values)")
            # Display colored version
            colored_html = colorize_masked_text(item["llm_response_masked"], item["mapping"])
            st.markdown(colored_html, unsafe_allow_html=True)
        
        with col2:
            #st.markdown("**📋 Plain Text View**")
            st.markdown("(Copy-paste version)")
            # Show plain text for copying
            st.code(item["llm_response_masked"], language="text")

    with st.expander("Final Output (after unmasking)", expanded=True):
        st.text_area("Final Output Content", value=item["final_output"], height=400, disabled=True, key=f"{turn_id}_final")
