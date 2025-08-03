import streamlit as st
from datetime import datetime
import random
from PIL import Image, ImageDraw, ImageFont

# Token-to-environment mapping
VALID_TOKENS = {
    "premium123": "Premium",
    "standard123": "Standard",
    "compat123": "Compatibility"
}

# Initialize session state
for key in ['adaptive_ready', 'environment', 'token_valid', 'playing', 'mode', 'watermark_id', 'log']:
    if key not in st.session_state:
        if key == 'log':
            st.session_state[key] = []
        elif key in ['adaptive_ready', 'token_valid', 'playing']:
            st.session_state[key] = False
        else:
            st.session_state[key] = None

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_watermark_id():
    return ''.join(random.choices('0123456789ABCDEF', k=8))

def create_watermark_image(wm_text, mode):
    img = Image.new("RGB", (640, 360), color=(20, 20, 20))
    draw = ImageDraw.Draw(img)
    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        font_size = 32 if mode == 'Compatibility' else 20
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), wm_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    if mode == 'Compatibility':
        text_color = (255, 0, 0)
        x = (img.width - text_width) // 2
        y = (img.height - text_height) // 2
    else:
        text_color = (150, 150, 150)
        x = img.width - text_width - 10
        y = img.height - text_height - 10

    draw.text((x, y), wm_text, font=font, fill=text_color)
    return img

# App title
st.title("🎬 VisualKey – Adaptive Secure Playback Prototype")

# Step 0: Simulated environment detection before token entry
if not st.session_state.adaptive_ready:
    st.subheader("🔍 Initial Device Environment Scan")
    option = st.selectbox("Select your simulated device environment:", [
        "Verified Secure Device (e.g., registered home system)",
        "Trusted Home Wi-Fi",
        "VPN / Unknown Network"
    ])

    if st.button("Run Environment Check"):
        if "Secure" in option:
            st.session_state.environment = "Premium"
        elif "Home" in option:
            st.session_state.environment = "Standard"
        else:
            st.session_state.environment = "Compatibility"

        st.session_state.adaptive_ready = True
        st.session_state.log.append(f"{timestamp()}: Environment detected → {st.session_state.environment}")

# Step 1: Token validation only after environment check
if st.session_state.adaptive_ready and not st.session_state.token_valid:
    st.subheader("🔐 Access Authentication")
    st.info(f"Detected Environment Mode: **{st.session_state.environment}**. Please enter a matching or lower-level token.")
    token_input = st.text_input("Enter your access token:", type="password")
    if st.button("Validate and Start Playback"):
        expected_mode = st.session_state.environment
        if token_input.strip() == "":
            st.warning("Please enter a valid token.")
        elif token_input in VALID_TOKENS:
            token_mode = VALID_TOKENS[token_input]
            allowed_modes = ["Premium", "Standard", "Compatibility"]
            if allowed_modes.index(token_mode) >= allowed_modes.index(expected_mode):
                st.session_state.token_valid = True
                st.session_state.mode = token_mode
                st.session_state.watermark_id = generate_watermark_id()
                st.session_state.playing = True
                st.session_state.log.append(f"{timestamp()}: Valid token '{token_input}' accepted for mode {token_mode}")
                st.session_state.log.append(f"{timestamp()}: Watermark ID generated = {st.session_state.watermark_id}")
            else:
                st.error("Token level exceeds allowed environment. Please use a lower-level token.")
        else:
            st.session_state.log.append(f"{timestamp()}: Invalid token attempt – {token_input}")
            st.error("Invalid token. Please try again.")

# Step 2: Playback session
if st.session_state.token_valid and st.session_state.playing and st.session_state.mode:
    st.subheader(f"🔊 Playback Mode: {st.session_state.mode}")
    wm_text = f"ID:{st.session_state.watermark_id}"
    frame_img = create_watermark_image(wm_text, st.session_state.mode)
    st.image(frame_img, caption="Forensic Watermark Preview", use_column_width=True)

    col1, col2 = st.columns(2)
    if col1.button("🔌 Simulate HDMI Copy Attempt"):
        st.session_state.playing = False
        st.session_state.log.append(f"{timestamp()}: ⚠️ HDMI attack detected. Playback stopped.")
        st.error("HDMI output unauthorized. Session terminated.")

    if col2.button("📼 Simulate Screen Recording"):
        st.session_state.playing = False
        st.session_state.log.append(f"{timestamp()}: ⚠️ Screen recorder detected. Playback stopped.")
        st.error("Screen recording detected. Session terminated.")

    if not st.session_state.playing:
        st.warning("🔒 Playback session ended.")
        if st.button("Restart Application"):
            for key in ['adaptive_ready', 'token_valid', 'playing', 'mode', 'watermark_id', 'environment']:
                st.session_state[key] = False if key in ['adaptive_ready', 'token_valid', 'playing'] else None
            st.experimental_rerun()

# Audit Log
if st.session_state.log:
    st.markdown("---")
    st.subheader("📑 Audit Log")
    log_text = "\n".join(st.session_state.log)
    st.text_area("Session Events:", log_text, height=200)
    st.download_button("📥 Download Log", log_text.encode('utf-8'), file_name="visualkey_audit_log.txt")
