
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

# Initialize session state
for key in ['token_valid', 'playing', 'mode', 'watermark_id', 'log']:
    if key not in st.session_state:
        if key == 'log':
            st.session_state[key] = []
        elif key in ['token_valid', 'playing']:
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

# App Title
st.title("🎬 VisualKey – Secure Playback Prototype")

# Step 1: Token validation
if not st.session_state.token_valid:
    st.subheader("Login")
    token_input = st.text_input("Enter your access token:", type="password")
    if st.button("Validate and Start Playback"):
        if token_input.strip() == "":
            st.warning("Please enter a valid token.")
        elif token_input in VALID_TOKENS:
            st.session_state.token_valid = True
            env_status = VALID_TOKENS[token_input]
            st.session_state.mode = "Premium" if env_status == "secure" else "Standard" if env_status == "moderate" else "Compatibility"
            st.session_state.watermark_id = generate_watermark_id()
            st.session_state.playing = True
            st.session_state.log.append(f"{timestamp()}: Valid token. Playback mode = {st.session_state.mode}")
            st.session_state.log.append(f"{timestamp()}: Watermark ID generated = {st.session_state.watermark_id}")
        else:
            st.session_state.log.append(f"{timestamp()}: **Invalid token attempt** – {token_input}")
            st.error("Invalid token. Please try again.")
else:
    if st.session_state.playing and st.session_state.mode:
        st.subheader(f"Playback Mode: {st.session_state.mode}")
        st.success(f"✅ {st.session_state.mode} mode active.")

        wm_text = f"ID:{st.session_state.watermark_id}"
        frame_img = create_watermark_image(wm_text, st.session_state.mode)
        st.image(frame_img, caption="Forensic Watermark Preview", use_column_width=True)
        st.info("Watermark is shown for demo purposes only.")

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
                for key in ['token_valid', 'playing', 'mode', 'watermark_id']:
                    st.session_state[key] = False if key in ['token_valid', 'playing'] else None
                st.experimental_rerun()
    else:
        st.warning("Playback ended. Restart to continue.")
        if st.button("Start New Session"):
            for key in ['token_valid', 'playing', 'mode', 'watermark_id']:
                st.session_state[key] = False if key in ['token_valid', 'playing'] else None
            st.experimental_rerun()

# Audit Log
if st.session_state.log:
    st.markdown("---")
    st.subheader("📑 Audit Log")
    log_text = "\n".join(st.session_state.log)
    st.text_area("Session Events:", log_text, height=200)
    st.download_button("📥 Download Log", log_text.encode('utf-8'), file_name="visualkey_audit_log.txt")
