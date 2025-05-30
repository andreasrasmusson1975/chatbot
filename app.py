"""
Manual assistant streamlit app
------------------------------

This streamlit application provides an interactive assistant for navigating and understanding
technical manuals. Uses can chat with the assistant or browse the full manual.

Features:

- Sidebar menu for selecting manual and view mode (chat or full manual)
- Conversational interface with possibility of viewing source pages for 
  answers
"""

# Perform necessary imports
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

# Set layout, title and user instructions
st.set_page_config(layout="wide")
st.title("📚 Welcome to the manual assistant!")
st.markdown("⬅️ Choose a manual of interest on the left.")
st.markdown("⬅️ You can also view the full manual by selecting the radio button on the left.")

############ Utility functions ############
@st.cache_data
def get_manuals() -> list:
    """
    Returns a sorted list of available manual names based on subdirectories 
    found in the 'vector_databases/' folder.

    Returns:
        list: Alphabetically sorted names of all manuals (as strings), 
              where each name corresponds to a subdirectory in 'vector_databases/'.

    Caching:
        Streamlit caches the result to avoid re-reading the filesystem on every rerun.
    """
    vector_db_path = Path("vector_databases")
    return sorted([d.name for d in vector_db_path.iterdir() if d.is_dir()])

@st.cache_data
def get_evaluation_df():
    """
    Loads and combines all evaluation DataFrames stored as joblib files 
    in the 'evaluation/' directory.

    Returns:
        pandas.DataFrame: A single concatenated DataFrame containing all 
        evaluation results, with the index reset.

    Caching:
        Streamlit caches the result to avoid reloading and recomputing 
        on every rerun.
    """
    base_dir = Path('.')/'evaluation'
    dfs=[joblib.load(base_dir/df) for df in os.listdir(base_dir)]
    return pd.concat(dfs,axis=0).reset_index()

# Get the manual names and the evaluation dataframe.
manuals = get_manuals()
evaluation_df = get_evaluation_df()

############ Web page creation ############

# Create and populate a sidebar with a selectbox for manual names
# and radio buttons for view mode (chatting or reading the manual)
with st.sidebar:
    st.header("📁 Manual Settings")
    selected_manual = st.selectbox("Select a manual:", manuals, key="manual_select")
    tab_selection = st.radio("View Mode", ["💬 Chat", "📖 View Manual"], key="tab_selection")

# If a new manual is selected, we create a new manual assistant object for the
# new manual and reset the chat list and last_image_path list
if "manual" not in st.session_state or st.session_state.manual != selected_manual:
    st.session_state.assistant = ManualAssistant(selected_manual)
    st.session_state.manual = selected_manual
    st.session_state.chat = []
    st.session_state.last_image_paths = []
assistant = st.session_state.assistant

# Display which manual is currently under consideration
st.markdown(f"**Currently helping with:** `{st.session_state.manual}`")

# If the chat view is selected, proceed as follows
if tab_selection == "💬 Chat":
    # Display example questions for the current manual
    with st.chat_message('assistant'):
        st.markdown("Don't know what to ask? Here are a few to get you started:")
        df = evaluation_df[evaluation_df['Manual']==selected_manual]
        df = df[df['Local answer']!="I'm afraid I can't find that in the manual."]
        for i in range(len(df)):
            st.markdown(f"  {i+1}. *{df.iloc[i,2]}*")
    # Display the conversation had so far
    for user_msg, assistant_msg in st.session_state.chat:
        with st.chat_message("user"):
            st.markdown(user_msg)
        with st.chat_message("assistant"):
            st.markdown(assistant_msg)
    # Display the user input chat box
    user_input = st.chat_input("Ask a question about the manual...")
    # When the user sends his input, we proceed as follows
    if user_input:
        # Display the user's message
        with st.chat_message("user"):
            st.markdown(user_input)
        # Initialize a chat message reply
        with st.chat_message("assistant"):
            # Clear the response area
            response_area = st.empty()
            # Initialize the response string
            full_response = ""
            # This is the marker for "end of message and start of sources enumeration"
            # Naturally, a giraffe was chosen to be the end marker.
            end_marker = "🦒"
            # This is the part of the response string that we are going to show to the user
            visible_response = ""
            # We want to stream the answer, chunk by chunk, to the user so that they
            # don't have to wait for it and the have it presented all at once. But when
            # we are done presenting the answer and instead focus on the sources for the
            # answer, we will set this to false.
            streaming_answer = True
            # Placeholder string for the source pages of the manual
            sources = ""
            # Iterate over the reply from the call to the assistants stream_user_query method
            # For each chunk, do the following:
            for chunk in assistant.stream_user_query(user_input):
                # Add the chunk to the full response
                full_response += chunk
                # If we are still streaming, do the following:
                if streaming_answer:
                    # If the end marker is in the current chunk, proceed as follows:
                    if end_marker in chunk:
                        # Split the chunk containing the end marker into a before-
                        # and after part.
                        before_marker, after_marker = chunk.split(end_marker, 1)
                        # add the before part to the visible response
                        visible_response += before_marker
                        # Add the after part to the sources 
                        sources += after_marker
                        # From now on, we are no longer streaming
                        streaming_answer = False
                        # Display the visible response in the response area
                        response_area.markdown(visible_response.strip())
                    else:
                        # Add the current chunk to the visible response and
                        # display it in the response area
                        visible_response += chunk
                        response_area.markdown(visible_response)
                else:
                    # We are no longer streaming, so add the current chunk to
                    # the sources
                    sources += chunk
            # Initialize a list that will (possibly) contain image paths
            image_paths = []
            # If the answer contained sources, do the following
            if sources:
                # Iterate over the lines in the source string
                for line in sources.strip().splitlines():
                    # If the word "Source" occurs in this line 
                    if "Source" in line:
                        # Extract the path part and add it to image_paths
                        path = line.split(":")[-1].strip().replace("\\", "/")
                        image_paths.append(path)
            # Set the session state last_image_paths list to be equal to image_paths
            st.session_state.last_image_paths = sorted(image_paths)
            # Add the user_input and visible_response strings to the chat history
            st.session_state.chat.append((user_input, visible_response))

            # We want to check if:
            # 1. The last_image_paths list is not empty
            # 2. The last response was one based on sources
            check1 = st.session_state.get("last_image_paths")
            check2 =  "I'm afraid I can't find that information in the manual" not in st.session_state.chat[-1][1]
            # If this is the case, do the following
            if check1 and check2:
               # Display an expander for viewing the manual pages relevant to the answer
               with st.expander("📄 View relevant pages"):
                    # Iterate over the paths in last_image_paths
                    for path in st.session_state["last_image_paths"]:
                        # Show the image
                        st.image(path, use_container_width=True)
                    # When we are done, clear last_image_paths
                    st.session_state.last_image_path = []
    

# If instead the view mode is view manual, do the following
if tab_selection == "📖 View Manual":
    # Define the path to the manual pages
    manual_dir = Path("docs") / selected_manual / "images"
    # If this path exists, do the following
    if manual_dir.exists():
        # Create a list of all the image file paths in the folder
        image_files = sorted(manual_dir.glob("*.[jp][pn]g"))
        # Iterate over the file paths
        for image_path in image_files:
            # Show the image
            st.image(image_path, use_container_width=True)
    else:
        st.warning("No images found for this manual.")
