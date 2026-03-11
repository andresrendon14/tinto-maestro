import streamlit as st

# 1. Importar las piezas de Lego que ya están en tu GitHub
import modulos.sinfonia as sinfonia
import modulos.consola_ia as consola_ia

# 2. Configuración base
st.set_page_config(page_title="Tinto Maestro | CEO", page_icon="☕", layout="wide")

# 3. Lógica de Login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("☕ Tinto Maestro")
        st.caption("Consola Central de Operaciones")
        with st.form("login_form"):
            u = st.text_input("Usuario Master")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Entrar a la Fábrica"):
                if u == "ceo" and p == "123456":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
else:
    # 4. El Menú del CEO (El enrutador)
    st.sidebar.title("🎛️ Panel CEO")
    
    menu = st.sidebar.radio("Navegación", [
        "Inicio", 
        "Sinfonía de Marca", 
        "Cerebro IA & CRM"
    ])
    
    if menu == "Inicio":
        st.title("Centro de Mando")
        st.success("¡Arquitectura Modular Conectada con Éxito!")
        st.write("Tus módulos de IA y Marca están a salvo en la carpeta 'modulos'. Selecciona uno en el menú izquierdo.")
        
    elif menu == "Sinfonía de Marca":
        sinfonia.ejecutar()
        
    elif menu == "Cerebro IA & CRM":
        consola_ia.ejecutar()
        
    st.sidebar.markdown("---")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()
