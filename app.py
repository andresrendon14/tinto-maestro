import streamlit as st

st.set_page_config(page_title="El Tostador Maestro", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("☕ El Tostador Maestro")
    st.subheader("Panel CEO Orquestador")
    with st.form("login"):
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.form_submit_button("Entrar"):
            if u == "ceo" and p == "123456":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Acceso denegado")
else:
    st.sidebar.title("Menu CEO")
    op = st.sidebar.selectbox("Modulos", ["Dashboard", "Sinfonia de Marca", "IA Tinto Chat"])
    
    if op == "Sinfonia de Marca":
        st.header("🎨 Configurar Marca Blanca")
        st.text_input("Nombre de la Marca")
        st.button("📂 Crear Carpetas")
        st.file_uploader("Logo")
        st.color_picker("Color")
    
    elif op == "IA Tinto Chat":
        st.header("🗨️ IA Tinto Chat")
        st.chat_input("Instrucciones...")
        st.button("🎤 Voz")
        st.button("📸 Camara")

    if st.sidebar.button("Cerrar Sesion"):
        st.session_state.logged_in = False
        st.rerun()
