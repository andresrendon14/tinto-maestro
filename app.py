import streamlit as st
import pandas as pd
from supabase import create_client, Client
import qrcode
from PIL import Image

# Configuración visual
st.set_page_config(page_title="Tinto Maestro", page_icon="☕")

# Carga de Secrets con manejo de errores
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Error de configuración: Faltan las llaves en Secrets.")
    st.stop()

def main():
    st.title("☕ Tinto Maestro")
    st.markdown("---")
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.subheader("Acceso a Consola CEO")
        with st.form("login"):
            user = st.text_input("Usuario")
            pw = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Entrar"):
                if user == "ceo" and pw == "123456":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Acceso denegado")
    else:
        st.success("💻 Consola CEO Activada")
        st.info("Conexión con Supabase: ESTABLE")
        if st.button("Cerrar Sesión"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
