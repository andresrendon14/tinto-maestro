import streamlit as st

# Importar nuestras piezas de Lego (Módulos)
import modulos.sinfonia as sinfonia

st.set_page_config(page_title="Tinto Maestro", page_icon="☕", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("☕ Tinto Maestro")
    with st.form("login"):
        if st.text_input("Usuario") == "ceo" and st.text_input("Clave", type="password") == "123456":
            if st.form_submit_button("Entrar"):
                st.session_state.logged_in = True
                st.rerun()
        else:
            st.form_submit_button("Entrar")
else:
    st.sidebar.title("Panel CEO")
    opcion = st.sidebar.radio("Navegación", ["Inicio", "Sinfonía de Marca", "Consola IA"])
    
    if opcion == "Inicio":
        st.success("Arquitectura Modular Activada. El sistema ahora es escalable.")
    
    # AQUÍ CONECTAMOS EL MÓDULO (El código vive en otro archivo)
    elif opcion == "Sinfonía de Marca":
        sinfonia.ejecutar()
        
    elif opcion == "Consola IA":
        st.info("Módulo de IA en construcción... (Pronto será otro archivo independiente)")
        
    if st.sidebar.button("Salir"):
        st.session_state.logged_in = False
        st.rerun()
