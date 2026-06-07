import streamlit as st

# =====================================================
# INITIALIZE PANEL STATE
# =====================================================

def initialize_layout():

    if "intel_panel_open" not in st.session_state:

        st.session_state.intel_panel_open = False

# =====================================================
# TOGGLE PANEL
# =====================================================

def toggle_intel_panel():

    st.session_state.intel_panel_open = (

        not st.session_state.intel_panel_open
    )

# =====================================================
# DYNAMIC LAYOUT
# =====================================================

def create_layout():

    if st.session_state.intel_panel_open:

        return st.columns(
            [4, 1.2]
        )

    else:

        return st.columns(
            [1]
        )

# =====================================================
# PANEL BUTTON
# =====================================================

def render_panel_toggle():

    icon = (

        "🧠 Hide Intelligence Core"

        if st.session_state.intel_panel_open

        else

        "🧠 Open Intelligence Core"
    )

    st.button(

        icon,

        use_container_width=True,

        on_click=toggle_intel_panel
    )