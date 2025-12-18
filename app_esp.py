# =========================
# IMPORTACIONES
# =========================

# Streamlit: framework para crear apps web con Python
import streamlit as st

# TextBlob: análisis de sentimientos (funciona mejor en inglés)
from textblob import TextBlob

# GoogleTranslator: traduce texto entre idiomas
from deep_translator import GoogleTranslator

# SpeechRecognition: convertir voz a texto
import speech_recognition as sr


# =========================
# CONFIGURACIÓN DE LA APP
# =========================

# Configura el título y el ícono de la pestaña
st.set_page_config(
    page_title="NLP en Español",
    page_icon="🇪🇸"
)

# =========================
# DISEÑO BONITO (SOLO ESTILO)
# =========================
st.markdown("""
<style>
/* Fondo general */
.stApp {
    background: linear-gradient(135deg, #fdfbfb, #e8f0ff);
}

/* Contenedor central tipo tarjeta */
.main > div {
    background: white;
    padding: 2.2rem;
    border-radius: 22px;
    box-shadow: 0 25px 45px rgba(0,0,0,0.08);
    max-width: 720px;
    margin: auto;
}

/* Título principal */
h1 {
    text-align: center;
    color: #2c2c2c;
    font-weight: 700;
}

/* Texto descriptivo */
p {
    text-align: center;
    color: #555;
    font-size: 1.05rem;
}

/* Área de texto */
textarea {
    border-radius: 14px !important;
    border: 1px solid #d0d7ff !important;
    padding: 12px;
}

/* Botones */
button {
    width: 100%;
    border-radius: 14px !important;
    height: 3.1rem;
    font-size: 1rem !important;
    font-weight: 600;
    background: linear-gradient(135deg, #6a85f1, #8fd3f4) !important;
    color: white !important;
    border: none !important;
}

/* Separación entre botones */
div.stButton {
    margin-top: 0.7rem;
}

/* Mensajes (info, error, success) */
div[data-testid="stAlert"] {
    border-radius: 14px;
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)


# Título principal de la app
st.title("🇪🇸 Analizador de Sentimientos")

# Texto descriptivo debajo del título
st.markdown("Escribe una frase o **habla por el micrófono** y la IA detectará el tono.")


# =========================
# ENTRADA DE TEXTO (YA EXISTENTE)
# =========================

# Área de texto donde el usuario puede escribir en español
texto_espanol = st.text_area(
    "Ingresa tu texto aquí:",
    "¡Estoy muy feliz de aprender inteligencia artificial!"
)


# =========================
# ENTRADA DE VOZ (NUEVO)
# =========================

# Botón para grabar audio
if st.button("🎙️ Hablar (usar micrófono)"):
    try:
        # Creamos el reconocedor de voz
        recognizer = sr.Recognizer()

        # Accedemos al micrófono
        with sr.Microphone() as source:
            st.info("🎧 Escuchando... habla ahora")

            # Ajusta el ruido ambiente
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            # Escucha el audio del usuario
            audio = recognizer.listen(source)

        # Convertimos la voz a texto usando Google Speech
        texto_espanol = recognizer.recognize_google(audio, language="es-ES")

        # Mostramos el texto reconocido
        st.success(f"🗣️ Texto reconocido: {texto_espanol}")

    except sr.UnknownValueError:
        # Error si no se entiende la voz
        st.error("❌ No se pudo entender el audio")

    except sr.RequestError as e:
        # Error de conexión con el servicio de Google
        st.error(f"❌ Error del servicio de reconocimiento: {e}")


# =========================
# BOTÓN DE ANÁLISIS (YA EXISTENTE)
# =========================

# Botón que ejecuta el análisis de sentimientos
if st.button("Analizar Sentimiento"):
    if texto_espanol:
        try:
            # =========================
            # PASO 1: TRADUCCIÓN
            # =========================

            # Creamos el traductor de español a inglés
            traductor = GoogleTranslator(source='es', target='en')

            # Traducimos el texto del usuario
            texto_ingles = traductor.translate(texto_espanol)

            # Mostramos la traducción interna
            st.caption(
                f"⚙️ Procesado internamente como: *'{texto_ingles}'*"
            )

            # =========================
            # PASO 2: ANÁLISIS NLP
            # =========================

            # Creamos el objeto TextBlob con el texto en inglés
            blob = TextBlob(texto_ingles)

            # Polaridad: valor entre -1 (negativo) y 1 (positivo)
            polaridad = blob.sentiment.polarity

            # Subjetividad: 0 (objetivo) a 1 (muy subjetivo)
            subjetividad = blob.sentiment.subjectivity

            # =========================
            # PASO 3: MOSTRAR RESULTADOS
            # =========================

            # Separador visual
            st.write("---")
            st.subheader("Resultados:")

            # Clasificación según polaridad
            if polaridad > 0.1:
                st.success(f"😊 Positivo (Score: {polaridad:.2f})")
            elif polaridad < -0.1:
                st.error(f"😠 Negativo (Score: {polaridad:.2f})")
            else:
                st.warning(f"😐 Neutral (Score: {polaridad:.2f})")

            # Mostrar subjetividad
            st.info(
                f"🧐 Subjetividad: {subjetividad:.2f} "
                f"({(subjetividad * 100):.0f}% opinión)"
            )

        except Exception as e:
            # Error general (traducción o NLP)
            st.error(f"Hubo un error con el procesamiento: {e}")

    else:
        # Si no hay texto
        st.warning("Escribe o dicta algo para analizar.")
