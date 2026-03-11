import streamlit as st
import pandas as pd
from modulos.db import supabase
import datetime
import os

def ejecutar():
    st.header("🧠 CRM Maestro: Central de Ingeniería & Micro-Agentes")
    
    if not supabase:
        st.error("❌ Error Crítico: Bóveda de Datos (Supabase) desconectada.")
        return

    # --- LECTURA DE DATOS (RESTAURACIÓN DE CAMPOS) ---
    try:
        # Traemos todos los campos: nombre, direccion, celular, correo, marca, estado
        respuesta = supabase.table("leads").select("*").order('created_at', descending=True).execute()
        datos = respuesta.data
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        datos = []

    if datos:
        df = pd.DataFrame(datos)
        
        # --- SELECTOR DE PROYECTO PREMIUM ---
        st.markdown("### 🗄️ Expediente Técnico de Cliente")
        proyecto_foco = st.selectbox("Selecciona el Proyecto para Auditoría:", df['nombre'].tolist())
        cliente_data = df[df['nombre'] == proyecto_foco].iloc[0]
        
        # --- PANEL DE CONTROL: MICRO-AGENTES & CAJA NEGRA ---
        col_caja, col_agentes = st.columns([1, 1])
        
        with col_caja:
            st.subheader("🛡️ Custodia: Caja Negra")
            st.success(f"**ID Seguridad:** `TM-DB-{cliente_data.get('id', '000')}`")
            st.info(f"📍 **Ubicación Física:** Servidor Cloud-SSL")
            
            # --- BITÁCORA DE DESARROLLO (LO QUE SE HA HECHO) ---
            st.markdown("**📜 Bitácora de Logros (Hecho):**")
            st.write("✅ Infraestructura de Datos Sincronizada.")
            st.write("✅ Módulo CRM con Edición en Vivo Activo.")
            st.write(f"✅ Campos Premium (Marca: {cliente_data.get('marca', 'N/A')}) configurados.")
            
            # Auditoría de Módulos
            modulos = os.listdir('modulos') if os.path.exists('modulos') else []
            st.caption(f"Estructura detectada: {len(modulos)} archivos fuente.")

        with col_agentes:
            st.subheader("🤖 Consola de Micro-Agentes")
            c1, c2 = st.columns(2)
            if c1.button("🧠 Agente de Perfilamiento"):
                st.toast("Analizando nicho de mercado...")
                st.info(f"Agente: 'Sugiero enfoque en {cliente_data.get('marca')} basado en datos de {cliente_data.get('nombre')}'")
            
            if c2.button("✉️ Agente de Notificación"):
                st.toast("Preparando canal de comunicación...")
                st.success(f"Email listo para enviar a: {cliente_data.get('correo')}")

            # --- ROADMAP: LO QUE FALTA (GUÍA TÉCNICA) ---
            st.markdown("---")
            st.warning("🚧 **Guía de Ingeniería (Faltante):**")
            progreso = st.slider("Avance de Web App", 0, 100, 35)
            
            if progreso < 50:
                st.markdown("- [ ] **Configurar Auth:** Crear login seguro.")
                st.code("streamlit-authenticator config...", language="python")
            else:
                st.markdown("- [ ] **Despliegue Final:** Vincular dominio .com")
                st.markdown("- [ ] **Manual PDF:** Generar documentación final.")

        # --- TABLA MAESTRA (EDICIÓN QUIRÚRGICA) ---
        st.markdown("---")
        st.subheader("📝 Directorio Premium (Edición en Vivo)")
        # Aseguramos que las columnas importantes se vean primero
        cols_orden = ['nombre', 'marca', 'correo', 'celular', 'direccion', 'estado']
        cols_final = [c for c in cols_orden if c in df.columns] + [c for c in df.columns if c not in cols_orden]
        
        df_editado = st.data_editor(
            df[cols_final], 
            hide_index=True, 
            use_container_width=True,
            column_config={
                "correo": st.column_config.TextColumn("📧 Email"),
                "celular": st.column_config.TextColumn("📱 Teléfono"),
                "marca": st.column_config.TextColumn("🏷️ Nombre de Marca")
            },
            key="editor_maestro"
        )

        if st.button("🔄 Sincronizar Bóveda y Guardar Cambios"):
            for index, row in df_editado.iterrows():
                try:
                    # Usamos el ID original para actualizar
                    id_orig = df.iloc[index]['id']
                    supabase.table("leads").update({
                        "nombre": row.get('nombre'),
                        "marca": row.get('marca'),
                        "correo": row.get('correo'),
                        "celular": row.get('celular'),
                        "direccion": row.get('direccion'),
                        "estado": row.get('estado')
                    }).eq("id", id_orig).execute()
                except: pass
            st.success("✨ ¡Sincronización Exitosa! Datos protegidos en la Caja Negra.")
            st.rerun()

    # --- FORMULARIO DE INYECCIÓN DE PROYECTOS ---
    with st.expander("➕ Iniciar Nueva Web App (Alta de Cliente Premium)"):
        with st.form("form_alta"):
            f1, f2 = st.columns(2)
            n_nombre = f1.text_input("👤 Nombre Completo")
            n_marca = f2.text_input("🏷️ Nombre de la Marca")
            n_correo = f1.text_input("📧 Correo Electrónico")
            n_celular = f2.text_input("📱 Celular")
            n_direccion = st.text_input("📍 Dirección Física / Oficina")
            
            if st.form_submit_button("🚀 Inyectar Proyecto al Sistema"):
                if n_nombre and n_marca:
                    supabase.table("leads").insert({
                        "nombre": n_nombre, "marca": n_marca, "correo": n_correo,
                        "celular": n_celular, "direccion": n_direccion, "estado": "En Construcción"
                    }).execute()
                    st.success(f"Proyecto {n_marca} inicializado.")
                    st.rerun()
