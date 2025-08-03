import streamlit as st

st.set_page_config(page_title="VisualKey Prototype", layout="centered")

st.title("🔐 VisualKey Secure Playback Prototype")

# Session state
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.mode = None
    st.session_state.threat_detected = False

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

# Step 2: Simulate Environment Check
elif st.session_state.step == 2:
    st.header("2. Environment Check")
    network = st.checkbox("Secure Network", value=True)
    recorder = st.checkbox("No Screen Recorder", value=True)
    hdmi = st.checkbox("HDMI Output Disabled", value=True)
    location = st.checkbox("Location Verified", value=True)
    device = st.checkbox("Device Authenticated", value=True)

    if st.button("Proceed to Playback"):
        st.session_state.step = 3
        st.rerun()

# Step 3: Playback Simulation
elif st.session_state.step == 3:
    st.header("3. Secure Playback")
    st.success(f"Playback started in {st.session_state.mode} mode.")
    if st.button("⚠️ Simulate Piracy Attempt"):
        st.session_state.threat_detected = True
        st.session_state.step = 4
        st.rerun()

# Step 4: Response to Threat
elif st.session_state.step == 4:
    st.header("4. System Response")
    mode = st.session_state.mode

    if mode == "Premium":
        st.error("🚫 Unauthorized Output Detected – Session Terminated")
    elif mode == "Standard":
        st.warning("⏸️ Screen Recorder Detected – Please close it to continue.")
    elif mode == "Compatibility":
        st.info("🔍 Monitoring Active – Watermark Applied")

    if st.button("View Summary"):
        st.session_state.step = 5
        st.rerun()

# Step 5: Result Summary
elif st.session_state.step == 5:
    st.header("5. Session Summary")
    st.write(f"**Mode:** {st.session_state.mode}")
    st.write("**Piracy Attempt:** Simulated")
    response = {
        "Premium": "Playback Terminated",
        "Standard": "Playback Paused",
        "Compatibility": "Watermark Applied"
    }
    st.write(f"**System Response:** {response[st.session_state.mode]}")
    if st.button("🔄 Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
