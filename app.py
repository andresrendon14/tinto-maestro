import streamlit as st
from modulos import inicio, sinfonia, consola_ia, conocimiento, crm, metricas, publicacion, ciberseguridad, integraciones

st.set_page_config(page_title="Tinto Maestro", page_icon="☕", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #FDFBF7; }
    .stButton>button { border-radius: 12px; background-color: #4A3B32; color: white; border: none; }
    .stButton>button:hover { background-color: #2C211A; }
    .sidebar .sidebar-content { background-color: #FFFFFF; }
</style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        st.markdown("<h1 style='text-align: center; color: #4A3B32;'>☕ Tinto Maestro</h1>", unsafe_allow_html=True)
        with st.form("login"):
            u = st.text_input("Usuario")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Acceder", use_container_width=True):
                if u == "ceo" and p == "123456":
                    st.session_state.logged_in = True
                    st.rerun()
                else: st.error("Acceso denegado")
else:
    st.sidebar.title("☕ Menú CEO")
    modulos = {
        "🏠 Inicio": inicio, "🎨 Sinfonía de Marca": sinfonia, "🧠 Cerebro IA": consola_ia, 
        "📚 Conocimiento": conocimiento, "🤝 CRM": crm, "📈 Métricas": metricas, 
        "🚀 Publicación": publicacion, "🛡️ Ciberseguridad": ciberseguridad, "🔌 Integraciones": integraciones
    }
    
    seleccion = st.sidebar.radio("Navegación", list(modulos.keys()))
    st.sidebar.markdown("---")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()
        
    # Ejecutar módulo seleccionado
    modulos[seleccion].ejecutar()
