import streamlit as st
import pickle
import os

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

# Function to load tabs from pickle file
def load_tabs():
    if os.path.exists('data/tabs_data.pkl'):
        with open('data/tabs_data.pkl', 'rb') as file:
            return pickle.load(file)
    return {}

# Function to save tabs to pickle file
def save_tabs():
    with open('data/tabs_data.pkl', 'wb') as file:
        pickle.dump(st.session_state.tabs, file)

# Function to delete a tab
def delete_tab(tab_name):
    if tab_name in st.session_state.tabs:
        del st.session_state.tabs[tab_name]
        save_tabs()  # Save changes after deletion
        if st.session_state.selected_tab == tab_name:
            # Reset selected tab
            st.session_state.selected_tab = None
            if st.session_state.tabs:
                st.session_state.selected_tab = list(st.session_state.tabs.keys())[0]  # Set to first tab if available

# Load tabs from file if not already in session state
if not st.session_state.tabs:
    st.session_state.tabs = load_tabs()

# Interface
st.title("Notepad Web")

# Sidebar for tab management
with st.sidebar:
    st.header("Tabs Management")
    if st.session_state.tabs:
        for tab_name in st.session_state.tabs.keys():
            if st.button(tab_name, key=f"tab_button_{tab_name}"):
                st.session_state.selected_tab = tab_name

        # Button to delete the selected tab
        if st.session_state.selected_tab:
            if st.button("Delete Tab", key=f"{st.session_state.selected_tab}_delete"):
                delete_tab(st.session_state.selected_tab)

    # Button to add a new tab
    if len(st.session_state.tabs) < 5:
        st.button("Add New Tab", on_click=add_tab)
    else:
        st.warning("Maximum of 5 tabs reached. Please delete a tab before adding a new one.")

    # Button to save tabs
    st.button("Save Tabs", on_click=save_tabs)

# Main content area
if st.session_state.selected_tab:
    st.subheader(f"Editing: {st.session_state.selected_tab}")
    tab_content = st.text_area(
        "Content", 
        value=st.session_state.tabs.get(st.session_state.selected_tab, ""), 
        height=400,  # Bigger text area
        key=f"{st.session_state.selected_tab}_content",
        on_change=save_tabs  # Save changes as you type
    )
    # Update the session state with the latest content
    st.session_state.tabs[st.session_state.selected_tab] = tab_content

    # Ensure content is up-to-date before offering download
    if tab_content.strip():  # Check if there's any content to download
        st.download_button(
            label="Download as Text File",
            data=tab_content.encode('utf-8'),
            file_name=f"{st.session_state.selected_tab}.txt",
            mime="text/plain"
        )
    else:
        st.warning("No content to download.")
else:
    st.write("Select a tab from the sidebar to start editing.")
