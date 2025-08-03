import streamlit as st
import time

st.set_page_config(page_title="VisualKey Prototype", layout="centered")

st.title("🔐 VisualKey Secure Playback Prototype")

# Session state init
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.mode = None
    st.session_state.piracy_detected = False
    st.session_state.piracy_tool = None

# Simulated piracy detection (mock process check)
def simulate_piracy_detection():
    # Simulated process list
    running_processes = ["system.exe", "chrome.exe", "obs64.exe"]  # Example
    piracy_tools = ["obs64.exe", "camtasia.exe", "snagit.exe", "xsplit.exe"]
    for tool in piracy_tools:
        if tool in running_processes:
            return tool
    return None

# Step 1: Select Mode
if st.session_state.step == 1:
    st.header("1. Choose Playback Mode")
    st.session_state.mode = st.radio(
        "Select a mode:",
        ["Premium", "Standard", "Compatibility"]
    )
    if st.button("Start Environment Check"):
        st.session_state.step = 2
        st.rerun()

# Step 2: Simulated Environment Check
elif st.session_state.step == 2:
    st.header("2. Environment Check")
    st.success("✅ All environment checks passed.")
    if st.button("Proceed to Playback"):
        st.session_state.step = 3
        st.rerun()

# Step 3: Playback Simulation
elif st.session_state.step == 3:
    st.header("3. Playback Started")
    st.success(f"Mode: {st.session_state.mode}")
    st.write("Your content is now playing securely.")
    if st.session_state.mode == "Compatibility":
        st.markdown(
            '<div style="position:absolute; top:10px; right:10px; color:red; opacity:0.5;">'
            '<strong>Watermark: user@visualkey</strong></div>', unsafe_allow_html=True
        )
    if st.button("⚠️ Simulate Piracy Detection"):
        tool = simulate_piracy_detection()
        if tool:
            st.session_state.piracy_detected = True
            st.session_state.piracy_tool = tool
            st.session_state.step = 4
        else:
            st.info("No piracy tool detected.")
        st.rerun()

# Step 4: System Response
elif st.session_state.step == 4:
    st.header("4. Security Response Triggered")
    st.warning(f"Piracy Tool Detected: {st.session_state.piracy_tool}")
    if st.session_state.mode == "Premium":
        st.error("🚫 Session Terminated Immediately")
    elif st.session_state.mode == "Standard":
        st.warning("⏸️ Playback Paused – Please close the unauthorized software.")
    elif st.session_state.mode == "Compatibility":
        st.info("🔍 Monitoring Active – Watermark Applied")
        st.markdown(
            '<div style="position:absolute; top:10px; right:10px; color:red; opacity:0.5;">'
            '<strong>Watermark: user@visualkey</strong></div>', unsafe_allow_html=True
        )
    if st.button("View Summary"):
        st.session_state.step = 5
        st.rerun()

# Step 5: Summary
elif st.session_state.step == 5:
    st.header("5. Session Summary")
    st.write(f"**Mode:** {st.session_state.mode}")
    st.write(f"**Piracy Attempt:** {st.session_state.piracy_detected}")
    if st.session_state.piracy_detected:
        st.write(f"**Tool Detected:** {st.session_state.piracy_tool}")
        responses = {
            "Premium": "Playback Terminated",
            "Standard": "Paused with Warning",
            "Compatibility": "Watermark Applied"
        }
        st.write(f"**System Response:** {responses[st.session_state.mode]}")
    if st.button("🔄 Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
