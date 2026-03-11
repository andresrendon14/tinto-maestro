import streamlit as st
def ejecutar():
    st.header("🎨 Sinfonía de Marca")
    st.caption("UI Lista / Backend de guardado pendiente")
    
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Nombre de la Marca", "Los Parceritos")
        st.text_input("Eslogan")
        st.file_uploader("Cargar Logo Principal")
    with c2:
        st.color_picker("Color Principal", "#432818")
        st.text_input("Dominio Propio Sugerido", "losparceritos.com")
        st.button("💾 Guardar Identidad", use_container_width=True)
    st.success("✨ Branding configurado para el frontend.")
