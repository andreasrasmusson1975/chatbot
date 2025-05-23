"""
Manual assistant streamlit app
------------------------------

This streamlit application provides an interactive assistant for navigating and understanding
technical manuals. Uses can chat with the assistant or browse the full manual.

Features:

- Sidebar menu for selecting manual and view mode (chat or full manual)
- Conversational interface
- 
"""

import streamlit as st
from streamlit_option_menu import option_menu
from pathlib import Path
from classes.manual_assistant import ManualAssistant
import torch
import joblib
import os
import pandas as pd
import re
import hashlib

# Fix PyTorch + Streamlit crash
torch.classes.__path__ = []

st.set_page_config(layout="wide")
st.title("📚 Welcome to the manual assistant!")
st.markdown("⬅️ Choose a manual of interest on the left.")
st.markdown("⬅️ You can also view the full manual by selecting the radio button on the left.")


# -------- Load available manuals --------
@st.cache_data
def get_manuals():
    vector_db_path = Path("vector_databases")
    return sorted([d.name for d in vector_db_path.iterdir() if d.is_dir()])

@st.cache_data
def get_evaluation_df():
    base_dir = Path('.')/'evaluation'
    dfs=[joblib.load(base_dir/df) for df in os.listdir(base_dir)]
    return pd.concat(dfs,axis=0).reset_index()

manuals = get_manuals()
evaluation_df = get_evaluation_df()

# -------- Sidebar: Manual and view mode selection --------
with st.sidebar:
    st.header("📁 Manual Settings")
    selected_manual = st.selectbox("Select a manual:", manuals, key="manual_select")
    tab_selection = st.radio("View Mode", ["💬 Chat", "📖 View Manual"], key="tab_selection")

# -------- Reset assistant on manual change --------
if "manual" not in st.session_state or st.session_state.manual != selected_manual:
    st.session_state.assistant = ManualAssistant(selected_manual)
    st.session_state.manual = selected_manual
    st.session_state.chat = []
    st.session_state.last_image_paths = []

assistant = st.session_state.assistant
st.markdown(f"**Currently helping with:** `{st.session_state.manual}`")

# -------- Chat Tab --------
if tab_selection == "💬 Chat":
    with st.chat_message('assistant'):
        st.markdown("Don't know what to ask? Here are a few to get you started:")
        df = evaluation_df[evaluation_df['Manual']==selected_manual]
        df = df[df['Reference answer']!="I'm afraid I can't find that in the manual."]
        for i in range(len(df)):
            st.markdown(f"  {i+1}. *{df.iloc[i,2]}*")
    for user_msg, assistant_msg in st.session_state.chat:
        with st.chat_message("user"):
            st.markdown(user_msg)
        with st.chat_message("assistant"):
            st.markdown(assistant_msg)

    user_input = st.chat_input("Ask a question about the manual...")
    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            response_area = st.empty()
            full_response = ""
            end_marker = "🦒"
            visible_response = ""
            streaming_answer = True
            sources = ""

            for chunk in assistant.stream_user_query(user_input):
                full_response += chunk
                if streaming_answer:
                    if end_marker in chunk:
                        before_marker, after_marker = chunk.split(end_marker, 1)
                        visible_response += before_marker
                        sources += after_marker
                        streaming_answer = False
                        response_area.markdown(visible_response.strip())
                    else:
                        visible_response += chunk
                        response_area.markdown(visible_response)
                else:
                    sources += chunk
            image_paths = []
            if sources:
                for line in sources.strip().splitlines():
                    if "Source" in line:
                        path = line.split(":")[-1].strip().replace("\\", "/")
                        image_paths.append(path)
            st.session_state.last_image_paths = image_paths
            st.session_state.chat.append((user_input, visible_response))
            if st.session_state.get("last_image_paths") and "I'm afraid I can't find that information in the manual" not in st.session_state.chat[-1][1]:
               with st.expander("📄 View relevant pages"):
                    for path in st.session_state["last_image_paths"]:
                        st.image(path, caption=path, use_container_width=True)
                    st.session_state.last_image_path = []
    #if st.session_state.get("last_image_paths") and "I'm afraid I can't find that information in the manual" not in st.session_state.chat[-1][1]:            
    #    question_hash = hashlib.md5(st.session_state.chat[-1][0].encode()).hexdigest()
    #    if st.button("View relevant pages", key=f"view_pages_{question_hash}"):
    #        for path in st.session_state["last_image_paths"]:
    #            st.image(path, caption=path, use_container_width=True)
    #        st.session_state.last_image_path = []
    

# -------- Manual Viewer Tab --------
if tab_selection == "📖 View Manual":
    st.subheader(f"🖼️ Full Manual: {selected_manual}")
    manual_dir = Path("docs") / selected_manual / "images"

    if manual_dir.exists():
        image_files = sorted(manual_dir.glob("*.[jp][pn]g"))  # .jpg, .jpeg, .png
        for image_path in image_files:
            st.image(image_path, caption=image_path, use_container_width=True)
    else:
        st.warning("No images found for this manual.")
