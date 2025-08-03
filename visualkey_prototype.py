import streamlit as st
from datetime import datetime
import random
from PIL import Image, ImageDraw, ImageFont

# Configuración inicial: tokens válidos y sus entornos simulados
VALID_TOKENS = {
    "premium123": "secure",     # Token de ejemplo para modo Premium (entorno seguro)
    "standard123": "moderate",  # Token de ejemplo para modo Standard (entorno común)
    "compat123": "insecure"     # Token de ejemplo para modo Compatibilidad (entorno inseguro)
}

# Inicializar estado de la sesión al cargar la app
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

# Funciones auxiliares
def timestamp():
    """Devuelve timestamp formateado para log."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_watermark_id():
    """Genera un identificador único de 8 caracteres hexadecimales para la marca de agua."""
    return ''.join(random.choices('0123456789ABCDEF', k=8))

def create_watermark_image(wm_text, mode):
    """
    Crea una imagen simulada (ej. un fotograma de video) con la marca de agua forense superpuesta.
    - wm_text: texto de la marca de agua (ID).
    - mode: modo de reproducción (afecta la visibilidad de la marca).
    """
    # Crear una imagen base (p.ej., fondo oscuro simulando video)
    img = Image.new("RGB", (640, 360), color=(20, 20, 20))  # fondo gris oscuro
    draw = ImageDraw.Draw(img)
    # Escoger fuente (usa una fuente de sistema, si disponible)
    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        font_size = 32 if mode == 'Compatibility' else 20  # más grande si modo compatibilidad
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()
    # Determinar posición y color según modo
    if mode == 'Compatibility':
        text_color = (255, 0, 0)   # rojo brillante para visibilidad en modo inseguro
        # Centrar texto en la imagen
        bbox = draw.textbbox((0, 0), wm_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (img.width - text_width) // 2
        y = (img.height - text_height) // 2
        draw.text((x, y), wm_text, font=font, fill=text_color)
    else:
        text_color = (150, 150, 150)  # gris semitransparente para Premium/Standard (menos visible)
        bbox = draw.textbbox((0, 0), wm_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        # Posicionar en esquina inferior derecha
        x = img.width - text_width - 10
        y = img.height - text_height - 10
        draw.text((x, y), wm_text, font=font, fill=text_color)
    return img

# Título de la aplicación
st.title("🎬 VisualKey – Prototipo de Reproducción Segura")

# Paso 1: Ingreso y validación del token de acceso
if not st.session_state.token_valid:
    st.subheader("Inicio de sesión")
    token_input = st.text_input("Ingrese su token de acceso:", type="password")
    if st.button("Validar y reproducir"):
        if token_input.strip() == "":
            st.warning("Por favor ingrese un token válido.")  # Caso de campo vacío
        elif token_input in VALID_TOKENS:
            # Token válido
            st.session_state.token_valid = True
            # Simular comprobación del entorno del dispositivo
            with st.spinner("Verificando token y entorno del dispositivo..."):
                env_status = VALID_TOKENS[token_input]
                # (Simulación breve - en un caso real habría más lógica aquí)
            # Determinar modo de reproducción según entorno
            if env_status == "secure":
                st.session_state.mode = "Premium"
            elif env_status == "moderate":
                st.session_state.mode = "Standard"
            else:
                st.session_state.mode = "Compatibility"
            # Generar ID de marca de agua para la sesión
            wm_id = generate_watermark_id()
            st.session_state.watermark_id = wm_id
            # Marcar que la reproducción puede iniciar
            st.session_state.playing = True
            # Registrar eventos en log
            st.session_state.log.append(f"{timestamp()}: Token válido ingresado. Modo de reproducción = {st.session_state.mode}")
            st.session_state.log.append(f"{timestamp()}: Marca de agua forense generada (ID={wm_id})")
        else:
            # Token inválido
            st.session_state.log.append(f"{timestamp()}: **Fallo de autenticación** – Token inválido: {token_input}")
            st.error("Token de acceso no válido. Inténtelo de nuevo.")
            # (Permanece en la pantalla de inicio de sesión para reintento)
else:
    # Paso 2: Simulación de la reproducción si el token fue validado
    if st.session_state.playing and st.session_state.mode:
        st.subheader(f"Reproduciendo contenido en modo **{st.session_state.mode}**")
        # Mensajes según modo
        if st.session_state.mode == "Premium":
            st.write("✅ <i>Modo Premium:</i> Controles completos habilitados (pausar, adelantar, etc.).", unsafe_allow_html=True)
        elif st.session_state.mode == "Standard":
            st.write("✅ <i>Modo Standard:</i> Reproducción con controles limitados (pausa/adelanto deshabilitados).", unsafe_allow_html=True)
        else:  # Compatibility
            st.write("✅ <i>Modo Compatibilidad:</i> Calidad reducida y medidas de seguridad visibles activadas.", unsafe_allow_html=True)
        # Mostrar marca de agua forense en pantalla (visible solo para demostración)
        wm_text = f"ID:{st.session_state.watermark_id}"
        frame_img = create_watermark_image(wm_text, st.session_state.mode)
        st.image(frame_img, caption="Vista del contenido con marca de agua forense", use_column_width=True)
        st.info("⚠️ La marca de agua forense se muestra visiblemente solo con fines de demostración.")  # nota aclaratoria
        # Botones para simular amenazas durante la reproducción
        col1, col2 = st.columns(2)
        if col1.button("🔌 Simular intento de copia (HDMI desconectado)"):
            # Simular detección de salida HDMI no autorizada
            st.session_state.playing = False
            st.session_state.log.append(f"{timestamp()}: **Amenaza detectada:** Salida HDMI no permitida. Reproducción detenida.")
            st.error("⚠️ Conexión HDMI no autorizada detectada. La reproducción ha sido bloqueada por seguridad.")
        if col2.button("📼 Simular grabación de pantalla"):
            # Simular detección de software de grabación en ejecución
            st.session_state.playing = False
            st.session_state.log.append(f"{timestamp()}: **Amenaza detectada:** Screen recorder en ejecución. Reproducción detenida.")
            st.error("⚠️ Grabación de pantalla detectada. La reproducción ha sido bloqueada por seguridad.")
        # Si la reproducción fue detenida por alguna amenaza, mostrar mensaje de finalización
        if not st.session_state.playing:
            st.warning("🔒 La sesión de reproducción ha finalizado. Inicie una nueva sesión para continuar.")
            # Botón para reiniciar toda la sesión (permitir un nuevo inicio)
            if st.button("Reiniciar aplicación"):
                st.session_state.token_valid = False
                st.session_state.playing = False
                st.session_state.mode = None
                st.session_state.watermark_id = None
                # Nota: El log no se borra intencionalmente, para mantener registro histórico en la sesión
                st.experimental_rerun()
    else:
        # Caso de seguridad: token válido pero reproducción no activa (ej. ya se detuvo)
        st.warning("La reproducción se ha detenido. Por favor, reinicie para iniciar una nueva sesión.")
        if st.button("Iniciar nueva sesión"):
            st.session_state.token_valid = False
            st.session_state.playing = False
            st.session_state.mode = None
            st.session_state.watermark_id = None
            # Conservar log de eventos previos
            st.experimental_rerun()

# Mostrar siempre el log de auditoría actual
if st.session_state.log:
    st.markdown("---")
    st.subheader("📑 Log de auditoría de la sesión")
    # Mostrar eventos en formato de texto
    log_text = "\n".join(st.session_state.log)
    st.text_area("Eventos registrados:", log_text, height=200)
    # Botón para descargar el log como archivo de texto
    st.download_button("📥 Descargar log", log_text.encode('utf-8'), file_name="VisualKey_auditoria.log")
