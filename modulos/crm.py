import streamlit as st
import pandas as pd
from modulos.db import supabase

def ejecutar():
    st.header("🤝 CRM Activo (Conectado a Supabase)")
    
    if not supabase:
        st.error("❌ Faltan las llaves de Supabase en los secretos.")
        return

    try:
        respuesta = supabase.table("leads").select("*").execute()
        datos = respuesta.data
    except Exception as e:
        datos = []

    st.markdown("### 📋 Directorio de Clientes")
    if datos:
        df = pd.DataFrame(datos)
        if 'id' in df.columns: df = df.drop(columns=['id'])
        if 'created_at' in df.columns: df = df.drop(columns=['created_at'])
        
        # Organizar columnas
        columnas_orden = ['nombre', 'correo', 'empresa', 'telefono', 'estado']
        columnas_actuales = [col for col in columnas_orden if col in df.columns]
        otras = [col for col in df.columns if col not in columnas_actuales]
        df = df[columnas_actuales + otras]
        
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No hay clientes guardados todavía.")

    with st.expander("➕ Agregar Nuevo Cliente", expanded=True):
        with st.form("form_nuevo_lead", clear_on_submit=True):
            c1, c2 = st.columns(2)
            nombre = c1.text_input("👤 Nombre Completo *")
            correo = c2.text_input("📧 Correo Electrónico")
            empresa = c1.text_input("🏢 Empresa")
            telefono = c2.text_input("📱 Teléfono")
            estado = st.selectbox("📌 Estado", ["Nuevo Lead", "En Negociación", "Cierre Exitoso", "Perdido"])
            
            submit = st.form_submit_button("💾 Guardar en la Nube", use_container_width=True)
            
            if submit:
                if not nombre:
                    st.error("El nombre es obligatorio.")
                else:
                    try:
                        supabase.table("leads").insert({
                            "nombre": nombre, "correo": correo, "empresa": empresa,
                            "estado": estado, "telefono": telefono
                        }).execute()
                        st.success("¡Guardado exitosamente!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")
