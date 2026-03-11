import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def iniciar_conexion():
    url = st.secrets.get("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_ANON_KEY")
    if url and key:
        try: return create_client(url, key)
        except: return None
    return None

supabase: Client = iniciar_conexion()
