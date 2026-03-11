import streamlit as st
from supabase import create_client, Client

# Configuración Maestra
st.set_page_config(page_title="El Tostador Maestro", page_icon="☕", layout="wide")

# Estilo Minimalista Apple + Café
st.markdown(\"\"\"
    <style>
    .stApp { background-color: #F5F5F7; }
    .stButton>button { border-radius: 25px; background-color: #1D1D1F; color: white; }
    .css-1offfwp { background-color: white !important; }
    </style>
\"\"\", unsafe_allow_html=True)

# Inicializar Base de Datos (Seguridad de Hilo)
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Error de conexión: Revisa los Secrets en Streamlit Cloud.")

# --- INTERFAZ ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.image("https://img.icons8.com/color/144/espresso-cup.png", width=80)
    st.title("El Tostador Maestro")
    st.subheader("Orquestador de Unidades Productivas")
    with st.form("login"):
        u = st.text_input("CEO ID")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("Entrar a la Fábrica"):
            if u == "ceo" and p == "123456":
                st.session_state.logged_in = True
                st.rerun()
else:
    st.sidebar.title("🎛️ El Tostador")
    op = st.sidebar.selectbox("Panel Principal", ["Sinfonía de Marca", "Fábrica de Apps", "Tinto Chat", "Métricas"])
    
    if op == "Sinfonía de Marca":
        st.header("🎨 Diseño de Marca Blanca")
        brand = st.text_input("Nombre de la Marca")
        st.button("📂 Crear Estructura de Carpetas")
        st.file_uploader("Logo 200x200 (logo_nombre.png)")
        st.color_picker("Paleta de Color Maestro")
        
    elif op == "Tinto Chat":
        st.title("🗨️ IA Tinto")
        st.chat_input("Instrucción para la orquesta...")
        st.button("🎤 Voz")
        st.button("📸 Cámara")

st.sidebar.markdown("---")
if st.sidebar.button("Cerrar Sesión"):
    st.session_state.logged_in = False
    st.rerun()
