import streamlit as st
from datetime import datetime
import random
from PIL import Image, ImageDraw, ImageFont

# Token-to-environment mapping
VALID_TOKENS = {
    "premium123": "secure",
    "standard123": "moderate",
    "compat123": "insecure"
}

# Session state setup
if 'token_valid' not in st.session_state:
    st.session_state.token_valid = False
if 'playing' not in st.session_state:
    st.session_state.playing = False
if 'mode' not in st.session_state:
    st.session_state.mode = None
if 'watermark_id' not in st.session_state:
    st.session_state.watermark_id = None
if 'log' not in st.session_state:
    st.session_state.log = []

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

st.title("🎬 VisualKey – Secure Playback Prototype")

if not st.session_state.token_valid:
    st.subheader("Login")
    token_input = st.text_input("Enter your access token:", type="password")
    if st.button("Validate and Start Playback"):
        if token_input.strip() == "":
            st.warning("Please enter a valid token.")
        elif token_input in VALID_TOKENS:
            st.session_state.token_valid = True
            env_status = VALID_TOKENS[token_input]
            if env_status == "secure":
                st.session_state.mode = "Premium"
            elif env_status == "moderate":
                st.session_state.mode = "Standard"
            else:
                st.session_state.mode = "Compatibility"
            wm_id = generate_watermark_id()
            st.session_state.watermark_id = wm_id
            st.session_state.playing = True
            st.session_state.log.append(f"{timestamp()}: Valid token entered. Playback mode = {st.session_state.mode}")
            st.session_state.log.append(f"{timestamp()}: Forensic watermark generated (ID={wm_id})")
        else:
            st.session_state.log.append(f"{timestamp()}: **Authentication failed** – Invalid token: {token_input}")
            st.error("Invalid token. Please try again.")
else:
    if st.session_state.playing and st.session_state.mode:
        st.subheader(f"Now playing in **{st.session_state.mode}** mode")
        if st.session_state.mode == "Premium":
            st.write("✅ <i>Premium Mode:</i> Full playback features enabled.", unsafe_allow_html=True)
        elif st.session_state.mode == "Standard":
            st.write("✅ <i>Standard Mode:</i> Limited controls (no pause/seek).", unsafe_allow_html=True)
        else:
            st.write("✅ <i>Compatibility Mode:</i> Reduced quality with visible security measures.", unsafe_allow_html=True)

        wm_text = f"ID:{st.session_state.watermark_id}"
        frame_img = create_watermark_image(wm_text, st.session_state.mode)
        st.image(frame_img, caption="Playback frame with forensic watermark", use_column_width=True)
        st.info("⚠️ Watermark is displayed visibly for demonstration purposes.")

        col1, col2 = st.columns(2)
        if col1.button("🔌 Simulate Copy Attempt (HDMI Attack)"):
            st.session_state.playing = False
            st.session_state.log.append(f"{timestamp()}: **Threat detected:** Unauthorized HDMI output. Playback stopped.")
            st.error("⚠️ Unauthorized HDMI detected. Playback has been blocked.")
        if col2.button("📼 Simulate Screen Recording"):
            st.session_state.playing = False
            st.session_state.log.append(f"{timestamp()}: **Threat detected:** Screen recorder active. Playback stopped.")
            st.error("⚠️ Screen recording detected. Playback has been blocked.")

        if not st.session_state.playing:
            st.warning("🔒 Playback session ended. Restart required.")
            if st.button("Restart Application"):
                st.session_state.token_valid = False
                st.session_state.playing = False
                st.session_state.mode = None
                st.session_state.watermark_id = None
                st.experimental_rerun()
    else:
        st.warning("Playback has stopped. Please restart.")
        if st.button("Start New Session"):
            st.session_state.token_valid = False
            st.session_state.playing = False
            st.session_state.mode = None
            st.session_state.watermark_id = None
            st.experimental_rerun()

if st.session_state.log:
    st.markdown("---")
    st.subheader("📑 Session Audit Log")
    log_text = "\n".join(st.session_state.log)
    st.text_area("Events Recorded:", log_text, height=200)
    st.download_button("📥 Download Log", log_text.encode('utf-8'), file_name="VisualKey_audit_log.txt")
