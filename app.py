import streamlit as st
import pickle
import os

# Initialize or load session state
if 'tabs' not in st.session_state:
    st.session_state.tabs = {}
if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = None
if 'show_about' not in st.session_state:
    st.session_state.show_about = False

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

    # About link
    if st.button("About"):
        st.session_state.show_about = not st.session_state.show_about

    if st.session_state.show_about:
        st.subheader("About This Application")
        st.write("""
        Welcome to **Notepad Web**! This simple and intuitive web-based notepad application allows you to create, manage, and download multiple notes across different tabs. Designed with ease of use in mind, the application lets you seamlessly switch between notes and save your work directly to your device.

        **Features:**
        
        - **Multiple Tabs**: You can create up to 5 tabs for organizing your notes. Each tab can hold a different note, allowing you to easily manage multiple topics or tasks.
        - **Automatic Saving**: Your notes are automatically saved as you type. This ensures that your work is never lost and can be quickly accessed later.
        - **Tab Management**: You can add 5 new tabs, delete existing ones, providing flexible note management. The sidebar provides easy access to all your tabs.
        - **Download Notes**: Each note can be downloaded as a plain text file with a single click. This feature is perfect for exporting your notes for offline use or sharing them with others.
        - **Data Storage**: Your tabs and their contents are saved only during the session.
        
        **How to Use:**
        
        1. **Adding a New Tab**: Click the "Add New Tab" button in the sidebar. You can have up to 5 tabs at a time.
        2. **Selecting a Tab**: Click on any tab name in the sidebar to switch to that tab and edit its content.
        3. **Deleting a Tab**: Select a tab and click the "Delete Tab" button to remove it from the list.
        4. **Saving Your Work**: Once you've written your note, click the "Download as Text File" button to save it to your device.
        
        
        **Technical Details:**
        
        Each user's notes are isolated and secure. We are not storing anything on server and all data needs to be downloaded by user.
        """)

# Main content area
if st.session_state.selected_tab:
    st.subheader(f"Editing: {st.session_state.selected_tab}")
    tab_content = st.text_area(
        "Content", 
        value=st.session_state.tabs.get(st.session_state.selected_tab, ""), 
        height=400,  # Bigger text area
        key=f"{st.session_state.selected_tab}_content"
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
