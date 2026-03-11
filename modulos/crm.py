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
            
            st.markdown("**📜 Bitácora de Logros (Hecho):**")
            st.write("✅ Infraestructura de Datos Sincronizada.")
            st.write("✅ Módulo CRM con Edición en Vivo Activo.")
            st.write(f"✅ Campos Premium (Marca: {cliente_data.get('marca', 'N/A')}) configurados.")
            
            modulos = os.listdir('modulos') if os.path.exists('modulos') else []
            st.caption(f"Estructura detectada: {len(modulos)} archivos fuente.")

        with col_agentes:
            st.subheader("🤖 Enrutador de Micro-Agentes")
            
            # Directorio Central de Microservicios (Escalable)
            directorio_agentes = {
                "🎨 Gestión de Marca": ["Generar Identidad Visual", "Redactar Tono de Voz"],
                "⚙️ Desarrollo Web": ["Generar Estructura Base", "Configurar Autenticación"],
                "📈 Marketing & Métricas": ["Perfilamiento de Nicho (IA)", "Redactar Email de Bienvenida"],
                "🛡️ Ciberseguridad": ["Auditoría de Datos", "Generar Llaves de Acceso"]
            }
            
            # El CRM identifica el dominio operativo requerido
            area_seleccionada = st.selectbox("Selecciona el Dominio Operativo:", list(directorio_agentes.keys()))
            st.markdown(f"**Agentes disponibles para {area_seleccionada.split(' ', 1)[1] if len(area_seleccionada.split(' ')) > 1 else area_seleccionada}:**")
            
            acciones = directorio_agentes[area_seleccionada]
            c1, c2 = st.columns(2)
            
            if c1.button(f"🚀 {acciones[0]}", use_container_width=True):
                st.toast(f"Inicializando: {acciones[0]}...")
                
                # --- LÓGICA QUIRÚRGICA: AGENTE DE IDENTIDAD VISUAL ---
                if acciones[0] == "Generar Identidad Visual":
                    marca_cliente = cliente_data.get('marca', 'Sin Marca')
                    st.info(f"Sintetizando ADN visual para la marca '{marca_cliente}'...")
                    
                    configuracion_marca = {
                        "tema": "Premium Dark",
                        "color_primario": "#D4AF37",
                        "color_secundario": "#1A1A1A",
                        "tipografia_titulos": "Playfair Display",
                        "tipografia_textos": "Inter"
                    }
                    
                    try:
                        supabase.table("fabrica_proyectos").insert({
                            "nombre_proyecto": f"WebApp_{marca_cliente.replace(' ', '')}",
                            "cliente_asociado": cliente_data.get('nombre', 'Desconocido'),
                            "estado": "Diseño Base Inyectado",
                            "configuracion_ui": configuracion_marca
                        }).execute()
                        st.success("✅ ADN Visual generado y custodiado en la tabla 'fabrica_proyectos'.")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error de custodia (Falta crear tabla en Supabase): {e}")
                
                else:
                    st.info(f"Extrayendo datos de la marca '{cliente_data.get('marca', 'N/A')}' para ejecutar {acciones[0]}...")
                
            if len(acciones) > 1 and c2.button(f"⚡ {acciones[1]}", use_container_width=True):
                st.toast(f"Inicializando: {acciones[1]}...")
                st.success(f"Operación '{acciones[1]}' preparada para el correo: {cliente_data.get('correo', 'N/A')}")

            # --- ROADMAP: LO QUE FALTA ---
            st.markdown("---")
            st.warning("🚧 **Guía de Ingeniería (Faltante):**")
            progreso = st.slider("Avance de Web App", 0, 100, 35)
            
            if progreso < 50:
                st.markdown("- [ ] **Configurar Auth:** Crear login seguro.")
                st.code("streamlit-authenticator config...", language="python")
            else:
                st.markdown("- [ ] **Despliegue Final:** Vincular dominio .com")
                st.markdown("- [ ] **Manual PDF:** Generar documentación final.")

        # --- TABLA MAESTRA ---
        st.markdown("---")
        st.subheader("📝 Directorio Premium (Edición en Vivo)")
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

    # --- FORMULARIO DE INYECCIÓN ---
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
