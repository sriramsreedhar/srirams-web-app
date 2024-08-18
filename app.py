import streamlit as st

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

# Function to delete a tab
def delete_tab(tab_name):
    if tab_name in st.session_state.tabs:
        del st.session_state.tabs[tab_name]
        if st.session_state.selected_tab == tab_name:
            st.session_state.selected_tab = None
            if st.session_state.tabs:
                st.session_state.selected_tab = list(st.session_state.tabs.keys())[0]  # Set to first tab if available

# Interface
st.title("Notepad Web")

# Arrange components on the left pane
left_pane = st.sidebar.container()

with left_pane:
    # Add New Tab button
    if len(st.session_state.tabs) < 5:
        st.button("Add New Tab", on_click=add_tab, key="add_new_tab")
    else:
        st.warning("Maximum of 5 tabs reached. Please delete a tab before adding a new one.")

    # Display tabs
    tab_names = list(st.session_state.tabs.keys())
    if st.session_state.selected_tab not in tab_names:
        st.session_state.selected_tab = tab_names[0] if tab_names else None

    for tab_name in tab_names:
        if st.button(tab_name, key=f"tab_button_{tab_name}"):
            st.session_state.selected_tab = tab_name

    # Trash icon button for deleting the selected tab
    if st.session_state.selected_tab:
        if st.button("🗑️ Delete Tab", key=f"{st.session_state.selected_tab}_trash"):
            delete_tab(st.session_state.selected_tab)

# Display content editor for the selected tab
if st.session_state.selected_tab:
    tab_content = st.text_area("Content", value=st.session_state.tabs.get(st.session_state.selected_tab, ""), height=300, key=f"{st.session_state.selected_tab}_content")
    st.session_state.tabs[st.session_state.selected_tab] = tab_content

    # Update download button based on content availability
    if tab_content.strip() != "":
        st.download_button(
            label="Download as Text File",
            data=tab_content,
            file_name=f"{st.session_state.selected_tab}.txt",
            mime="text/plain",
            key=f"{st.session_state.selected_tab}_download"
        )
    else:
        st.write("No content to download. Start typing to create content.")
