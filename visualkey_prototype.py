import streamlit as st
import hashlib
import time
from datetime import datetime

st.set_page_config(page_title="VisualKey Secure Prototype", layout="centered")
st.title("🔐 VisualKey – Secure Playback Simulation")

# Session initialization
if "step" not in st.session_state:
    st.session_state.update({
        "step": 1,
        "mode": None,
        "token_valid": False,
        "env_safe": False,
        "watermark": None,
        "threat": None,
        "logs": []
    })

# Logging
def log_event(event):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.logs.append(f"[{timestamp}] {event}")

# Step 1: User authentication & token validation
if st.session_state.step == 1:
    st.header("1. User Authentication & Mode Selection")
    user_id = st.text_input("User ID or Email")
    access_token = st.text_input("Access Token", type="password")
    st.session_state.mode = st.radio("Select Playback Mode:", ["Premium", "Standard", "Compatibility"])

    if st.button("Validate Access"):
        combined = f"{user_id}:{access_token}"
        hashed = hashlib.sha256(combined.encode()).hexdigest()
        st.session_state.token_valid = len(access_token) >= 8  # Simplified validation logic
        st.session_state.watermark = f"WM-{hashed[:10]}"
        if st.session_state.token_valid:
            log_event(f"Token validated for user: {user_id}")
            st.session_state.step = 2
        else:
            st.error("Invalid token. Please try again.")
        st.experimental_rerun()

# Step 2: Environment scan
elif st.session_state.step == 2:
    st.header("2. Environment Security Check")
    hdmi_active = st.checkbox("HDMI Output Detected", False)
    recorder_running = st.checkbox("Screen Recorder Running", False)
    is_virtual_machine = st.checkbox("Running in Virtual Machine", False)
    os_modified = st.checkbox("Modified OS or Rooted Device", False)

    if st.button("Run Scan"):
        if not (hdmi_active or recorder_running or is_virtual_machine or os_modified):
            st.session_state.env_safe = True
            log_event("Environment scan: PASSED")
        else:
            st.session_state.env_safe = False
            issues = []
            if hdmi_active: issues.append("HDMI output")
            if recorder_running: issues.append("Screen recorder")
            if is_virtual_machine: issues.append("Virtual machine")
            if os_modified: issues.append("Modified OS")
            log_event(f"Environment scan: FAILED ({', '.join(issues)})")
        st.session_state.step = 3
        st.experimental_rerun()

# Step 3: Playback initiation
elif st.session_state.step == 3:
    st.header("3. Playback Engine")
    if not st.session_state.token_valid or not st.session_state.env_safe:
        st.error("Access Denied: Security validation failed.")
        log_event("Playback denied due to failed security validation.")
    else:
        st.success(f"Playback allowed – Mode: {st.session_state.mode}")
        st.markdown(f"**Forensic Watermark:** `{st.session_state.watermark}`")
        log_event("Playback initiated")
        log_event(f"Watermark applied: {st.session_state.watermark}")

        if st.session_state.mode == "Standard":
            st.info("Note: In Standard mode, skipping and fast-forward are disabled.")
        elif st.session_state.mode == "Compatibility":
            st.warning("Reduced quality + watermark overlays will apply.")

        if st.button("⚠️ Simulate Threat Detection"):
            st.session_state.step = 4
        if st.button("📄 View Logs"):
            st.session_state.step = 5

# Step 4: Threat response
elif st.session_state.step == 4:
    st.header("4. Real-Time Threat Detected")
    st.session_state.threat = "OBS Screen Recorder"
    log_event("Threat detected during playback: OBS Recorder")

    if st.session_state.mode == "Premium":
        st.error("🚫 Session Terminated Immediately")
        log_event("Response: Session terminated (Premium mode)")
    elif st.session_state.mode == "Standard":
        st.warning("⏸️ Playback Paused. Unauthorized software must be closed.")
        log_event("Response: Playback paused (Standard mode)")
    else:
        st.info("🔍 Monitoring Activated. Playback continues with persistent watermark.")
        log_event("Response: Monitoring with persistent watermark (Compatibility mode)")

    if st.button("📄 View Logs"):
        st.session_state.step = 5

# Step 5: Audit log
elif st.session_state.step == 5:
    st.header("5. Session Summary & Log")
    st.subheader("🔍 Event Log")
    for entry in st.session_state.logs:
        st.text(entry)

    # Download option
    log_text = "\n".join(st.session_state.logs)
    st.download_button("⬇️ Download Log", data=log_text, file_name="visualkey_log.txt", mime="text/plain")

    if st.button("🔄 Restart Simulation"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
