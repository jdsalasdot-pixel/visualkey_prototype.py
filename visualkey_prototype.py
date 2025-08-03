import streamlit as st
import time
from datetime import datetime
import base64

st.set_page_config(page_title="VisualKey Secure Playback", layout="wide")

st.title("🔐 VisualKey – Secure Content Playback System")

# Initialize session state
if "state" not in st.session_state:
    st.session_state.state = "start"
    st.session_state.mode = None
    st.session_state.logs = []
    st.session_state.piracy_tool = None
    st.session_state.piracy_detected = False
    st.session_state.user_id = "user123@visualkey"

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.logs.append(f"[{timestamp}] {message}")

def simulate_piracy_detection():
    # Mock piracy detection with preset process list
    active_processes = ["system.exe", "chrome.exe", "obs64.exe"]
    suspicious = ["obs64.exe", "camtasia.exe", "snagit.exe", "xsplit.exe"]
    for proc in suspicious:
        if proc in active_processes:
            return proc
    return None

def show_watermark():
    st.markdown(
        f"<div style='position:fixed; top:10px; right:20px; color:red; opacity:0.5;'>"
        f"<strong>Watermark: {st.session_state.user_id}</strong></div>",
        unsafe_allow_html=True
    )

def download_log():
    log_content = "\n".join(st.session_state.logs)
    b64 = base64.b64encode(log_content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="visualkey_session_log.txt">📄 Download Log File</a>'
    st.markdown(href, unsafe_allow_html=True)

# UI Flow
if st.session_state.state == "start":
    st.header("Step 1: Select Playback Mode")
    st.session_state.mode = st.radio("Choose security level:", ["Premium", "Standard", "Compatibility"])
    if st.button("Begin Environment Check"):
        log_event(f"Mode selected: {st.session_state.mode}")
        st.session_state.state = "env_check"
        st.rerun()

elif st.session_state.state == "env_check":
    st.header("Step 2: Running Environment Validation...")
    with st.spinner("Analyzing environment..."):
        time.sleep(2)
    log_event("Environment check: PASSED")
    st.success("✅ Environment is secure for playback.")
    if st.button("Start Secure Playback"):
        st.session_state.state = "playback"
        log_event("Playback started.")
        st.rerun()

elif st.session_state.state == "playback":
    st.header("Step 3: Playback In Progress")
    st.success(f"Mode: {st.session_state.mode}")
    st.write("🎬 Your content is playing securely.")
    if st.session_state.mode == "Compatibility":
        show_watermark()

    col1, col2 = st.columns(2)
    if col1.button("⚠️ Simulate Piracy Detection"):
        tool = simulate_piracy_detection()
        if tool:
            st.session_state.piracy_detected = True
            st.session_state.piracy_tool = tool
            log_event(f"Piracy tool detected: {tool}")
            st.session_state.state = "response"
        else:
            log_event("Piracy check: no threats detected")
            st.info("No piracy detected.")
        st.rerun()
    if col2.button("⏹️ End Playback"):
        log_event("Playback ended manually")
        st.session_state.state = "summary"
        st.rerun()

elif st.session_state.state == "response":
    st.header("Step 4: Security Response Triggered")
    tool = st.session_state.piracy_tool
    st.warning(f"Unauthorized tool detected: **{tool}**")
    if st.session_state.mode == "Premium":
        st.error("🚫 Playback Terminated Immediately.")
        log_event("Response: Playback Terminated (Premium Mode)")
    elif st.session_state.mode == "Standard":
        st.warning("⏸️ Playback Paused. Please close the unauthorized application.")
        log_event("Response: Playback Paused (Standard Mode)")
    elif st.session_state.mode == "Compatibility":
        st.info("🔍 Monitoring Active. Watermark Applied.")
        show_watermark()
        log_event("Response: Monitoring + Watermark (Compatibility Mode)")
    if st.button("Proceed to Summary"):
        st.session_state.state = "summary"
        st.rerun()

elif st.session_state.state == "summary":
    st.header("Step 5: Session Summary")
    st.write(f"**Selected Mode:** {st.session_state.mode}")
    st.write(f"**Piracy Attempt Detected:** {'Yes' if st.session_state.piracy_detected else 'No'}")
    if st.session_state.piracy_detected:
        st.write(f"**Detected Tool:** {st.session_state.piracy_tool}")
    st.subheader("📝 Security Log")
    for log in st.session_state.logs:
        st.text(log)
    download_log()
    if st.button("🔁 Restart Simulation"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
