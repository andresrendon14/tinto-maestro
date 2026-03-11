import streamlit as st
import pandas as pd
from modulos.db import supabase

def ejecutar():
    st.header("🤝 CRM Activo (Conectado a Supabase)")
    
    if not supabase:
        st.error("❌ Faltan las llaves de Supabase en los secretos. El CRM está desconectado.")
        return

    st.success("🔌 Conexión estable con la Base de Datos en la Nube.")

    # --- LEER DATOS DE SUPABASE ---
    try:
        respuesta = supabase.table("leads").select("*").execute()
        datos = respuesta.data
    except Exception as e:
        st.warning("⚠️ La base de datos está conectada, pero la tabla 'leads' no existe en tu panel de Supabase.")
        st.info("👉 Ve a tu panel de Supabase > Table Editor > Create a new table. Llámala 'leads' con columnas: nombre, empresa, estado, telefono.")
        datos = []

    # --- MOSTRAR DATOS ---
    st.markdown("### 📋 Directorio de Clientes")
    if datos:
        df = pd.DataFrame(datos)
        # Ocultar la columna ID si existe para que se vea más limpio
        if 'id' in df.columns: df = df.drop(columns=['id'])
        if 'created_at' in df.columns: df = df.drop(columns=['created_at'])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No hay clientes guardados todavía. ¡Agrega el primero abajo!")

    # --- GUARDAR DATOS EN SUPABASE ---
    with st.expander("➕ Agregar Nuevo Cliente", expanded=True):
        with st.form("form_nuevo_lead", clear_on_submit=True):
            c1, c2 = st.columns(2)
            nombre = c1.text_input("👤 Nombre Completo *")
            empresa = c2.text_input("🏢 Empresa")
            estado = c1.selectbox("📌 Estado", ["Nuevo Lead", "En Negociación", "Cierre Exitoso", "Perdido"])
            telefono = c2.text_input("📱 Teléfono")
            
            submit = st.form_submit_button("💾 Guardar en la Nube", use_container_width=True)
            
            if submit:
                if not nombre:
                    st.error("El nombre es obligatorio.")
                else:
                    try:
                        # Insertar directamente en Supabase
                        supabase.table("leads").insert({
                            "nombre": nombre,
                            "empresa": empresa,
                            "estado": estado,
                            "telefono": telefono
                        }).execute()
                        st.success(f"¡{nombre} guardado exitosamente en Supabase!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al guardar. Asegúrate de que las columnas en Supabase coincidan. Detalle: {e}")
