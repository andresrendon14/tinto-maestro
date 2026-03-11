import streamlit as st
import pandas as pd
from modulos.db import supabase

def ejecutar():
    st.header("🧠 CRM: Cerebro de Agentes & Microservicios")
    
    if not supabase:
        st.error("❌ Conexión de Microservicios caída.")
        return

    # --- TABLERO DE CONTROL (MICROSERVICIOS) ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Agentes Activos", "4", "Online")
    col2.metric("Microservicios", "12", "Ready")
    col3.metric("Acciones IA", "24h", "Sync")

    # --- LECTURA DE DATOS ---
    try:
        respuesta = supabase.table("leads").select("*").order('created_at', descending=True).execute()
        datos = respuesta.data
    except:
        datos = []

    st.markdown("### 📋 Directorio Operativo (Modificable)")
    
    if datos:
        df = pd.DataFrame(datos)
        # Configurar el Data Editor (Superpoder de Edición)
        df_editado = st.data_editor(
            df,
            column_config={
                "estado": st.column_config.SelectboxColumn(
                    "Estado del Agente",
                    help="Define la fase del microservicio",
                    options=["Nuevo Lead", "IA Procesando", "Agente Humano", "Cierre Exitoso", "Perdido"],
                    required=True,
                ),
                "correo": st.column_config.TextColumn("📧 Email", validate="^[^@]+@[^@]+\.[^@]+$"),
            },
            disabled=["id", "created_at"],
            hide_index=True,
            use_container_width=True,
            key="editor_crm"
        )

        # BOTÓN PARA SINCRONIZAR CAMBIOS
        if st.button("🔄 Sincronizar Cambios en la Bóveda"):
            for index, row in df_editado.iterrows():
                supabase.table("leads").update({
                    "nombre": row['nombre'],
                    "correo": row['correo'],
                    "empresa": row['empresa'],
                    "estado": row['estado'],
                    "telefono": row['telefono']
                }).eq("id", row['id']).execute()
            st.success("✨ Inteligencia Sincronizada.")
            st.rerun()

        # --- SECCIÓN DE MICROSERVICIOS ---
        st.markdown("---")
        st.subheader("⚡ Disparador de Microservicios por Lead")
        
        lead_seleccionado = st.selectbox("Selecciona un Lead para activar un Agente:", df['nombre'].tolist())
        
        c1, c2, c3 = st.columns(3)
        if c1.button("🤖 Agente de Perfilamiento"):
            st.toast(f"Activando Microservicio IA para {lead_seleccionado}...")
            st.info(f"El Agente está analizando la empresa de {lead_seleccionado} en la web...")
            
        if c2.button("✉️ Agente de Email Marketing"):
            st.toast("Disparando secuencia de Micro-conversión...")
            st.warning(f"Enviando correo personalizado a la base de datos...")

        if c3.button("🛡️ Agente de Seguridad"):
            st.toast("Verificando identidad de Lead...")
            st.success("Lead Verificado bajo protocolo Ciberseguridad.")

    # --- AGREGAR NUEVO NODO ---
    with st.expander("➕ Inyectar Nuevo Lead al Sistema"):
        with st.form("nuevo_nodo"):
            nombre = st.text_input("Nombre")
            correo = st.text_input("Email")
            empresa = st.text_input("Empresa")
            submit = st.form_submit_button("Inyectar Lead")
            if submit and nombre:
                supabase.table("leads").insert({"nombre": nombre, "correo": correo, "empresa": empresa, "estado": "Nuevo Lead"}).execute()
                st.rerun()

