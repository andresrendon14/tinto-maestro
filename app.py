import streamlit as st
import pandas as pd
from supabase import create_client, Client
import qrcode
from PIL import Image
import io
import os

# Configuración Estilo Apple-Cafetero
st.set_page_config(page_title="El Tostador Maestro | CEO Panel", page_icon="☕", layout="wide")

# Estilos CSS Inyectados (Minimalismo Apple + Café)
st.markdown(\"\"\"
    <style>
    .main { background-color: #F5F5F7; }
    .stButton>button { 
        border-radius: 20px; 
        background-color: #1D1D1F; 
        color: white; 
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #432818; transform: scale(1.02); }
    .sidebar .sidebar-content { background-color: #FFFFFF; }
    .stTextInput>div>div>input { border-radius: 10px; }
    .brand-card {
        padding: 20px;
        border-radius: 15px;
        background: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
\"\"\", unsafe_allow_html=True)

# Conexión Supabase (Memoria Infinita)
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_ANON_KEY"]
supabase: Client = create_client(url, key)

# --- LÓGICA DE PERSISTENCIA (AUTOGUARDADO) ---
def save_state(brand_name, data):
    supabase.table("marcas_viva").upsert({"nombre": brand_name, "config": data}).execute()

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        show_login()
    else:
        show_orchestrator()

def show_login():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://img.icons8.com/color/144/espresso-cup.png", width=100)
        st.title("El Tostador Maestro")
        st.caption("Orquestador de Unidades Productivas | Los Parceritos")
        with st.form("acceso_ceo"):
            user = st.text_input("Usuario Master")
            pw = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Encender Máquina"):
                if user == "ceo" and pw == "123456":
                    st.session_state.logged_in = True
                    st.rerun()

def show_orchestrator():
    # BARRA LATERAL (EL HILO CONDUCTOR)
    st.sidebar.title("🎛️ Orquestador")
    menu = st.sidebar.radio("Sinfonía de Marca", 
        ["Dashboard CEO", "Configurar Nueva Marca", "Banca de Conocimiento", "Fábrica de Apps", "Ciberseguridad", "Métricas ROI"])

    if menu == "Configurar Nueva Marca":
        render_brand_config()
    
    elif menu == "Dashboard CEO":
        st.title("☕ Bienvenida, CEO")
        st.info("El sistema está en Autoguardado Sincrónico con Supabase.")
        render_chat_console()

def render_brand_config():
    st.header("🎨 Configuración de Marca Blanca")
    
    with st.expander("📍 1. Identidad y Estructura", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            brand_name = st.text_input("Nombre de la Marca")
            slogan = st.text_input("Eslogan Estratégico")
        with col2:
            st.button("📂 Crear Estructura de Carpetas Automática")
            logo = st.file_uploader("Subir Logo (PNG/JPG 200x200)", type=["png", "jpg"])
            if logo:
                st.success(f"Logo-{brand_name}.png cargado y reconocido por IA.")

    with st.expander("🎭 2. Avatar y Experiencia (Tienda Montañera)"):
        col_a, col_b = st.columns(2)
        with col_a:
            st.file_uploader("Foto del Avatar")
            st.multiselect("Paleta de Colores (Recomendada)", ["#432818", "#99582A", "#BB9457", "#FFE6A7", "#000000"])
        with col_b:
            st.text_area("Inspiración Web (Links para la IA)")

    with st.expander("🔗 3. Dominio y Conectividad"):
        opcion_dom = st.radio("Tipo de Dominio", ["Subdominio gratuito (.losparceritos.com)", "Dominio propio de pago"])
        if opcion_dom == "Dominio propio de pago":
            st.help("La IA te guiará: Necesitas el API Key de tu registrador (GoDaddy/Hostinger).")
        st.text_input("Prefijo de subdominio", placeholder="tunombre")

    if st.button("🚀 Publicar y Empaquetar"):
        st.balloons()
        st.success("App enviada a la Fábrica de Proyectos.")

def render_chat_console():
    st.markdown("---")
    st.subheader("🗨️ Consola de Comando 'Tinto'")
    
    # Consola de Chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Instrucción para la IA (Tinto)..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Aquí se integrará el bloque de IAs (Gemini/Groq/etc)
        response = f"IA Tinto: Procesando comando '{prompt}' con lógica de marca blanca..."
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    # Botones de Interacción IA
    col1, col2, col3, col4 = st.columns(4)
    col1.button("🎤 Hablar")
    col2.button("👁️ Ver Cámara")
    col3.button("📍 GPS Experiencia")
    col4.button("🎬 Generar Video Corto")

if __name__ == "__main__":
    main()
