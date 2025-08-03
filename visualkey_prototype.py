import streamlit as st
from datetime import datetime
import io

# Page configuration
st.set_page_config(page_title="VisualKey Prototype", layout="wide")
st.title("🔐 VisualKey Secure Playback Prototype")

# Sidebar: simulate environment and user details
st.sidebar.header("🌐 Environment Simulation")
secure_network = st.sidebar.checkbox("Secure Network", True)
screen_rec = st.sidebar.checkbox("Screen Recording Software Active", False)
hdmi = st.sidebar.checkbox("HDMI Output Active", False)
location = st.sidebar.checkbox("Location Verified", True)
device_auth = st.sidebar.checkbox("Device Authenticated", True)
simulate_obs = st.sidebar.checkbox("Simulate OBS Running", False)

st.sidebar.header("👤 User Info")
user_email = st.sidebar.text_input("Watermark Email", "user@visualkey.io")

# Determine playback mode based on environment flags
if secure_network and not screen_rec and not hdmi and location and device_auth:
    mode = "Premium"
elif secure_network and not screen_rec and location and device_auth:
    mode = "Standard"
else:
    mode = "Compatibility"

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.update({
        'step': 1,
        'piracy_detected': False,
        'piracy_tool': None,
        'logs': []
    })

# Logging function
def log(event: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.logs.append(f"{timestamp} – {event}")

# Step 1: Environment Scan
if st.session_state.step == 1:
    st.header("1. Environment Scan")
    st.markdown(f"- Secure Network: {'✅' if secure_network else '❌'}  ")
    st.markdown(f"- Screen Recorder: {'❌' if not screen_rec else '⚠️'}  ")
    st.markdown(f"- HDMI Active: {'❌' if not hdmi else '⚠️'}  ")
    st.markdown(f"- Location Verified: {'✅' if location else '❌'}  ")
    st.markdown(f"- Device Authenticated: {'✅' if device_auth else '❌'}  ")
    st.info(f"**Mode Selected:** {mode}")
    if st.button("▶️ Proceed to Playback"):
        log(f"Environment scan completed – Mode: {mode}")
        st.session_state.step = 2
        st.experimental_rerun()

# Step 2: Playback Simulation
elif st.session_state.step == 2:
    st.header("2. Secure Playback")
    st.success(f"Playback started in **{mode}** mode.")
    log("Playback initiated")
    
    # Watermark for Compatibility mode
    if mode == "Compatibility":
        st.markdown(
            f'<div style="position: fixed; top: 10px; right: 10px; '
            'font-size: 12px; color: red; opacity: 0.5;">'
            f'<strong>{user_email}</strong></div>', unsafe_allow_html=True
        )
    
    if st.button("⚠️ Simulate Piracy Attempt"):
        tool = "OBS" if simulate_obs else ("Screen Recorder" if screen_rec else None)
        if tool:
            st.session_state.piracy_detected = True
            st.session_state.piracy_tool = tool
            log(f"Piracy tool detected: {tool}")
        else:
            st.info("No piracy tool detected.")
            log("No piracy tool detected")
        st.session_state.step = 3
        st.experimental_rerun()

# Step 3: System Response
elif st.session_state.step == 3:
    st.header("3. System Response")
    if st.session_state.piracy_detected:
        tool = st.session_state.piracy_tool
        st.warning(f"Detected: {tool}")
        if mode == "Premium":
            st.error("🚫 Unauthorized output – Session terminated.")
            log("Response applied: Terminated session")
        elif mode == "Standard":
            st.warning("⏸️ Playback paused – Close unauthorized software.")
            log("Response applied: Paused playback")
        elif mode == "Compatibility":
            st.info("🔍 Monitoring active – Watermark persists.")
            log("Response applied: Monitoring with watermark")
    else:
        st.success("✅ No threats detected during playback.")
        log("No threats detected at response stage")
    
    if st.button("📊 View Summary and Logs"):
        st.session_state.step = 4
        st.experimental_rerun()

# Step 4: Summary & Logs
elif st.session_state.step == 4:
    st.header("4. Summary & Event Log")
    st.write(f"**Mode:** {mode}")
    st.write(f"**Piracy Attempt:** {st.session_state.piracy_detected}")
    if st.session_state.piracy_detected:
        st.write(f"**Tool Detected:** {st.session_state.piracy_tool}")
    st.subheader("Event Log")
    for entry in st.session_state.logs:
        st.text(entry)
    
    # Offer log download
    log_data = "\n".join(st.session_state.logs)
    st.download_button(
        label="⬇️ Download Logs",
        data=log_data,
        file_name="visualkey_session_logs.txt",
        mime="text/plain"
    )
    
    if st.button("🔄 Restart Simulation"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()
