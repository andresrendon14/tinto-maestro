import streamlit as st
st.set_page_config(page_title="Brand OS", page_icon="🎼", layout="wide", initial_sidebar_state="expanded")

from frontend.pages import crm_view, conocimiento_view, sinfonia_view

def main():
    st.sidebar.title("Brand OS ⚡")
    menu = st.sidebar.radio("Navegación Operativa", ["Dashboard", "CRM (Proyectos)", "Conocimiento (RAG)", "Sinfonía (Compilador)"])
    
    if menu == "CRM (Proyectos)":
        crm_view.ejecutar()
    elif menu == "Conocimiento (RAG)":
        conocimiento_view.ejecutar()
    elif menu == "Sinfonía (Compilador)":
        sinfonia_view.ejecutar()
    else:
        st.title("Dashboard Central")
        st.info("Bienvenido al Motor Cognitivo de Marca. Selecciona un módulo en el menú lateral.")

if __name__ == "__main__":
    main()
