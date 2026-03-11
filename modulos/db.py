import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def iniciar_conexion():
    """Crea y mantiene viva la conexión con Supabase."""
    url = st.secrets.get("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_ANON_KEY")
    
    if url and key:
        try:
            return create_client(url, key)
        except Exception as e:
            print(f"Error de conexión: {e}")
            return None
    return None

# Instancia global para importar en cualquier módulo
supabase: Client = iniciar_conexion()
