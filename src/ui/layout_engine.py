import streamlit as st


def initialize_layout():
    if "intel_panel_open" not in st.session_state:
        st.session_state.intel_panel_open = False
    if "is_mobile" not in st.session_state:
        st.session_state.is_mobile = False


def toggle_intel_panel():
    st.session_state.intel_panel_open = (
        not st.session_state.intel_panel_open
    )


def create_layout():
    if st.session_state.intel_panel_open:
        return st.columns([4, 1.2])
    else:
        return [st.container()]


def render_panel_toggle():
    icon = (
        "🧠 Hide Intelligence Core"
        if st.session_state.intel_panel_open
        else "🧠 Open Intelligence Core"
    )
    st.button(
        icon,
        use_container_width=True,
        on_click=toggle_intel_panel,
    )


def get_columns(mobile_count=1, tablet_count=2, desktop_count=3):
    screen = st.session_state.get("screen_width", 1200)
    if screen < 768:
        return st.columns(mobile_count)
    elif screen < 1024:
        return st.columns(tablet_count)
    else:
        return st.columns(desktop_count)