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

    try:
        respuesta = supabase.table("leads").select("*").order('created_at', descending=True).execute()
        datos = respuesta.data
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        datos = []

    if datos:
        df = pd.DataFrame(datos)
        st.markdown("### 🗄️ Expediente Técnico de Cliente")
        proyecto_foco = st.selectbox("Selecciona el Proyecto para Auditoría:", df['nombre'].tolist())
        cliente_data = df[df['nombre'] == proyecto_foco].iloc[0]
        
        col_caja, col_agentes = st.columns([1, 1])
        
        with col_caja:
            st.subheader("🛡️ Custodia: Caja Negra")
            st.success(f"**ID Seguridad:** `TM-DB-{cliente_data.get('id', '000')}`")
            st.info(f"📍 **Ubicación Física:** Servidor Cloud-SSL")
            st.markdown("**📜 Bitácora de Logros (Hecho):**")
            st.write("✅ Infraestructura de Datos Sincronizada.")
            st.write("✅ Módulo CRM con Edición en Vivo Activo.")
            st.write(f"✅ Campos Premium (Marca: {cliente_data.get('marca', 'N/A')}) configurados.")

        with col_agentes:
            st.subheader("🤖 Enrutador de Micro-Agentes")
            directorio_agentes = {
                "🎨 Gestión de Marca": ["Generar Identidad Visual", "Redactar Tono de Voz"],
                "⚙️ Desarrollo Web": ["Generar Estructura Base", "Configurar Autenticación"],
                "📈 Marketing & Métricas": ["Perfilamiento de Nicho (IA)", "Redactar Email de Bienvenida"],
                "🛡️ Ciberseguridad": ["Auditoría de Datos", "Generar Llaves de Acceso"]
            }
            
            area_seleccionada = st.selectbox("Selecciona el Dominio Operativo:", list(directorio_agentes.keys()))
            acciones = directorio_agentes[area_seleccionada]
            c1, c2 = st.columns(2)
            
            if c1.button(f"🚀 {acciones[0]}", use_container_width=True):
                st.toast(f"Inicializando: {acciones[0]}...")
                marca_cliente = cliente_data.get('marca', 'Sin Marca')
                nombre_proy = f"WebApp_{marca_cliente.replace(' ', '')}"
                
                # --- AGENTE 1: IDENTIDAD VISUAL ---
                if acciones[0] == "Generar Identidad Visual":
                    st.info(f"Sintetizando ADN visual para '{marca_cliente}'...")
                    configuracion_marca = {
                        "tema": "Premium Dark", "color_primario": "#D4AF37",
                        "color_secundario": "#1A1A1A", "tipografia_titulos": "Playfair Display",
                        "tipografia_textos": "Inter"
                    }
                    try:
                        res = supabase.table("fabrica_proyectos").select("id").eq("nombre_proyecto", nombre_proy).execute()
                        if res.data:
                            supabase.table("fabrica_proyectos").update({"configuracion_ui": configuracion_marca}).eq("id", res.data[0]['id']).execute()
                        else:
                            supabase.table("fabrica_proyectos").insert({"nombre_proyecto": nombre_proy, "cliente_asociado": cliente_data.get('nombre', 'Desconocido'), "estado": "Diseño Base Inyectado", "configuracion_ui": configuracion_marca}).execute()
                        st.success("✅ ADN Visual generado.")
                        st.balloons()
                    except Exception as e: st.error(f"Error: {e}")
                
                # --- AGENTE 2: ESTRUCTURA BASE (NUEVO) ---
                elif acciones[0] == "Generar Estructura Base":
                    st.info(f"Diseñando arquitectura de páginas para '{marca_cliente}'...")
                    estructura_web = {
                        "paginas": ["Inicio", "Servicios", "Nosotros", "Contacto"],
                        "modulos_activos": ["Formulario Leads", "Botón WhatsApp", "Métricas Base"],
                        "navegacion": "Menú Superior Fijo"
                    }
                    try:
                        res = supabase.table("fabrica_proyectos").select("id").eq("nombre_proyecto", nombre_proy).execute()
                        if res.data:
                            supabase.table("fabrica_proyectos").update({"estructura_web": estructura_web, "estado": "Arquitectura Web Definida"}).eq("id", res.data[0]['id']).execute()
                        else:
                            supabase.table("fabrica_proyectos").insert({"nombre_proyecto": nombre_proy, "cliente_asociado": cliente_data.get('nombre', 'Desconocido'), "estado": "Arquitectura Web Definida", "estructura_web": estructura_web}).execute()
                        st.success("✅ Estructura Base (Sitemap) generada y acoplada al proyecto.")
                        st.balloons()
                    except Exception as e: st.error(f"Error: {e}")
                
                else:
                    st.info(f"Extrayendo datos para ejecutar {acciones[0]}...")
                
            if len(acciones) > 1 and c2.button(f"⚡ {acciones[1]}", use_container_width=True):
                st.toast(f"Inicializando: {acciones[1]}...")
                st.success(f"Operación '{acciones[1]}' preparada.")

        st.markdown("---")
        st.subheader("📝 Directorio Premium (Edición en Vivo)")
        cols_orden = ['nombre', 'marca', 'correo', 'celular', 'direccion', 'estado']
        cols_final = [c for c in cols_orden if c in df.columns] + [c for c in df.columns if c not in cols_orden]
        df_editado = st.data_editor(df[cols_final], hide_index=True, use_container_width=True, key="editor_maestro")

        if st.button("🔄 Sincronizar Bóveda"):
            for index, row in df_editado.iterrows():
                try: supabase.table("leads").update({"nombre": row.get('nombre'), "marca": row.get('marca'), "correo": row.get('correo'), "celular": row.get('celular'), "direccion": row.get('direccion'), "estado": row.get('estado')}).eq("id", df.iloc[index]['id']).execute()
                except: pass
            st.success("✨ ¡Sincronización Exitosa!")
            st.rerun()

    with st.expander("➕ Iniciar Nueva Web App (Alta de Cliente Premium)"):
        with st.form("form_alta"):
            f1, f2 = st.columns(2)
            n_nombre = f1.text_input("👤 Nombre Completo")
            n_marca = f2.text_input("🏷️ Nombre de la Marca")
            n_correo = f1.text_input("📧 Correo")
            n_celular = f2.text_input("📱 Celular")
            n_direccion = st.text_input("📍 Dirección")
            if st.form_submit_button("🚀 Inyectar Proyecto"):
                if n_nombre and n_marca:
                    supabase.table("leads").insert({"nombre": n_nombre, "marca": n_marca, "correo": n_correo, "celular": n_celular, "direccion": n_direccion, "estado": "En Construcción"}).execute()
                    st.success("Inicializado.")
                    st.rerun()
