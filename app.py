import streamlit as st
import os
import pickle

# Generate a unique identifier for the system (could be more complex if needed)
system_id = "local_session"

# Path to the local session file
session_file_path = f"data/session_{system_id}.pkl"

# Initialize or load session state
if 'tabs' not in st.session_state:
    st.session_state.tabs = {}
if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = None

# Function to add a new tab
def add_tab():
    if len(st.session_state.tabs) < 5:
        tab_name = f"Tab {len(st.session_state.tabs) + 1}"
        st.session_state.tabs[tab_name] = ""
        if st.session_state.selected_tab is None:
            st.session_state.selected_tab = tab_name

# Function to load tabs from the session file
def load_tabs():
    if os.path.exists(session_file_path):
        with open(session_file_path, 'rb') as file:
            return pickle.load(file)
    return {}

# Function to save tabs to the session file
def save_tabs():
    os.makedirs(os.path.dirname(session_file_path), exist_ok=True)
    with open(session_file_path, 'wb') as file:
        pickle.dump(st.session_state.tabs, file)

# Function to delete a tab
def delete_tab(tab_name):
    if tab_name in st.session_state.tabs:
        del st.session_state.tabs[tab_name]
        save_tabs()  # Save changes after deletion
        if st.session_state.selected_tab == tab_name:
            st.session_state.selected_tab = None
            if st.session_state.tabs:
                st.session_state.selected_tab = list(st.session_state.tabs.keys())[0]

# Load tabs from the file if not already in session state
if not st.session_state.tabs:
    st.session_state.tabs = load_tabs()

# Interface
st.title("Notepad Web")

# Sidebar layout
with st.sidebar:
    st.header("Tabs")
    if st.session_state.tabs:
        tab_names = list(st.session_state.tabs.keys())
        if st.session_state.selected_tab not in tab_names:
            st.session_state.selected_tab = tab_names[0] if tab_names else None

        # Show tabs as buttons
        for tab_name in tab_names:
            if st.button(tab_name, key=f"tab_button_{tab_name}"):
                st.session_state.selected_tab = tab_name

        # Delete button for the selected tab
        if st.session_state.selected_tab:
            if st.button("Delete Tab", key=f"{st.session_state.selected_tab}_delete"):
                delete_tab(st.session_state.selected_tab)

    # Add New Tab button
    if len(st.session_state.tabs) < 5:
        st.button("Add New Tab", on_click=add_tab, key="add_new_tab")
    else:
        st.warning("Maximum of 5 tabs reached. Please delete a tab before adding a new one.")

    # Save Tabs button
    st.button("Save Tabs", on_click=save_tabs, key="save_tabs_sidebar")

# Main area layout
if st.session_state.selected_tab:
    tab_content = st.text_area("Content", value=st.session_state.tabs.get(st.session_state.selected_tab, ""), height=400, key=f"{st.session_state.selected_tab}_content")
    st.session_state.tabs[st.session_state.selected_tab] = tab_content

    # Download button
    if tab_content:
        st.download_button(
            label="Download as Text File",
            data=tab_content,
            file_name=f"{st.session_state.selected_tab}.txt",
            mime="text/plain",
            key="download_file"
        )
    else:
        st.write("No content to download.")

# Automatically save session on content change
st.button("Save Tabs", on_click=save_tabs, key="save_tabs_main")
