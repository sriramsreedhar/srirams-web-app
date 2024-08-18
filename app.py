import streamlit as st

# Initialize session state variables
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

# Function to delete a tab
def delete_tab(tab_name):
    if tab_name in st.session_state.tabs:
        del st.session_state.tabs[tab_name]
        if st.session_state.selected_tab == tab_name:
            st.session_state.selected_tab = None
            if st.session_state.tabs:
                st.session_state.selected_tab = list(st.session_state.tabs.keys())[0]  # Set to first tab if available

# Interface
st.title("Welcome to Notepad Web!")

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
        - **Tab Management**: You can add new tabs and delete existing ones, providing flexible note management. The sidebar provides easy access to all your tabs.
        - **Download Notes**: Each note can be downloaded as a plain text file with a single click. This feature is perfect for exporting your notes for offline use or sharing them with others.
        
        **How to Use:**
        
        1. **Adding a New Tab**: Click the "Add New Tab" button in the sidebar. You can have up to 5 tabs at a time.
        2. **Selecting a Tab**: Click on any tab name in the sidebar to switch to that tab and edit its content.
        3. **Deleting a Tab**: Select a tab and click the "Delete Tab" button to remove it from the list. Once a tab is deleted, it can only be added back after all tabs have been deleted.
        4. **Downloading Notes**: Once you've written your note, click the "Download as Text File" button to save it to your device.
        
        **Technical Details:**
        
        Each user's notes are isolated and secure. We are not storing anything on the server, and all data needs to be downloaded by the user. We are not responsible for any data loss.
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
