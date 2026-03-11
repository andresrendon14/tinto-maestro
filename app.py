import streamlit as st
import pandas as pd
from supabase import create_client, Client
import qrcode
from PIL import Image
import os

# Configuración de página
st.set_page_config(page_title="Tinto Maestro", page_icon="☕", layout="centered")

# Conexión a Supabase (Consola CEO)
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_ANON_KEY"]
supabase: Client = create_client(url, key)

def main():
    st.title("☕ Tinto Maestro")
    st.subheader("Panel CEO - Consola de Control")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        with st.form("login_form"):
            usuario = st.text_input("Usuario")
            clave = st.text_input("Contraseña", type="password")
            submit = st.form_submit_button("Acceder a la Consola")
            
            if submit:
                if usuario == "ceo" and clave == "123456":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
    else:
        st.success("Bienvenido, CEO. Conectado a la base de datos.")
        if st.button("Cerrar Sesión"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
