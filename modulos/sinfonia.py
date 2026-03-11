import streamlit as st

def ejecutar():
    st.header("🎨 Configuración de Marca Blanca")
    st.write("Todo lo que agreguemos de diseño, colores y logos irá en este archivo, sin tocar el núcleo.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Nombre de la Marca")
        st.file_uploader("Subir Logo")
    with col2:
        st.color_picker("Color Principal")
        st.button("Guardar Identidad")
