import streamlit as st
from modulos import inicio, sinfonia, consola_ia, conocimiento, crm, metricas, publicacion, ciberseguridad, integraciones

st.set_page_config(page_title="Tinto Maestro", page_icon="☕", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("☕ Tinto Maestro")
    with st.form("login"):
        if st.text_input("Usuario") == "ceo" and st.text_input("Password", type="password") == "123456":
            if st.form_submit_button("Acceder"):
                st.session_state.logged_in = True
                st.rerun()
        else: st.form_submit_button("Acceder")
else:
    st.sidebar.title("☕ Menú CEO")
    modulos = {
        "🏠 Inicio": inicio, "🎨 Sinfonía de Marca": sinfonia, "🧠 Cerebro IA": consola_ia, 
        "📚 Conocimiento": conocimiento, "🤝 CRM": crm, "📈 Métricas": metricas, 
        "🚀 Publicación": publicacion, "🛡️ Ciberseguridad": ciberseguridad, "🔌 Integraciones": integraciones
    }
    
    seleccion = st.sidebar.radio("Navegación", list(modulos.keys()))
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()
        
    modulos[seleccion].ejecutar()
