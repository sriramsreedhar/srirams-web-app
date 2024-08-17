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
st.title("Multi-Tab Notepad")

# Display tabs at the top
if st.session_state.tabs:
    tab_names = list(st.session_state.tabs.keys())
    if st.session_state.selected_tab not in tab_names:
        st.session_state.selected_tab = tab_names[0] if tab_names else None

    # Show tabs as buttons at the top
    col1, col2 = st.columns([8, 1])
    with col1:
        for tab_name in tab_names:
            if st.button(tab_name, key=f"tab_button_{tab_name}"):
                st.session_state.selected_tab = tab_name

    with col2:
        # Trash icon button for deleting the selected tab
        if st.session_state.selected_tab:
            if st.button("🗑️", key=f"{st.session_state.selected_tab}_trash"):
                delete_tab(st.session_state.selected_tab)
                # Refresh the content if necessary by reloading tabs
                if st.session_state.selected_tab in st.session_state.tabs:
                    st.session_state.selected_tab = st.session_state.selected_tab
                else:
                    st.session_state.selected_tab = list(st.session_state.tabs.keys())[0] if st.session_state.tabs else None

    # Display content editor for the selected tab
    if st.session_state.selected_tab:
        tab_content = st.text_area("Content", value=st.session_state.tabs.get(st.session_state.selected_tab, ""), height=200, key=f"{st.session_state.selected_tab}_content")
        st.session_state.tabs[st.session_state.selected_tab] = tab_content

        # Download button
        st.download_button(
            label="Download as Text File",
            data=tab_content,
            file_name=f"{st.session_state.selected_tab}.txt",
            mime="text/plain"
        )

# Add New Tab
if len(st.session_state.tabs) < 5:
    st.button("Add New Tab", on_click=add_tab)
else:
    st.warning("Maximum of 5 tabs reached. Please delete a tab before adding a new one.")

# Save the tabs to a file
st.button("Save Tabs", on_click=save_tabs)
