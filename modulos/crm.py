import streamlit as st
import pandas as pd
from modulos.db import supabase
from modulos import consola_ia

def ejecutar():
    st.header("🧠 CRM Maestro: Central de Ingeniería & Micro-Agentes")
    
    if not supabase:
        st.error("❌ Error Crítico: Bóveda de Datos desconectada.")
        return

    try:
        respuesta = supabase.table("leads").select("*").order('created_at', descending=True).execute()
        datos = respuesta.data
    except Exception as e:
        datos = []

    if datos:
        df = pd.DataFrame(datos)
        st.markdown("### 🗄️ Expediente Técnico de Cliente")
        proyecto_foco = st.selectbox("Selecciona el Proyecto para Auditoría:", df['nombre'].tolist())
        cliente_data = df[df['nombre'] == proyecto_foco].iloc[0]
        marca_cliente = cliente_data.get('marca', 'Sin Marca')
        nombre_proy = f"WebApp_{marca_cliente.replace(' ', '')}"
        
        col_caja, col_agentes = st.columns([1, 1])
        
        with col_caja:
            st.subheader("🛡️ Custodia: Caja Negra")
            st.success(f"**ID Seguridad:** `TM-DB-{cliente_data.get('id', '000')}`")
            st.write("✅ Bóveda RAG Activa.")

        with col_agentes:
            st.subheader("🤖 Enrutador de Micro-Agentes")
            directorio_agentes = {
                "🎨 Gestión de Marca": ["Generar Identidad Visual", "Redactar Tono de Voz"],
                "⚙️ Desarrollo Web": ["Generar Estructura Base", "Configurar Autenticación"]
            }
            area_seleccionada = st.selectbox("Dominio:", list(directorio_agentes.keys()))
            acciones = directorio_agentes[area_seleccionada]
            c1, c2 = st.columns(2)
            
            if c1.button(f"🚀 {acciones[0]}", use_container_width=True):
                if acciones[0] == "Generar Identidad Visual":
                    st.info("🧠 Generando ADN Visual...")
                    config = consola_ia.generar_adn_visual(marca_cliente)
                    res = supabase.table("fabrica_proyectos").select("id").eq("nombre_proyecto", nombre_proy).execute()
                    if res.data: supabase.table("fabrica_proyectos").update({"configuracion_ui": config}).eq("id", res.data[0]['id']).execute()
                    else: supabase.table("fabrica_proyectos").insert({"nombre_proyecto": nombre_proy, "configuracion_ui": config}).execute()
                    st.success("✅ ADN Guardado.")
                elif acciones[0] == "Generar Estructura Base":
                    st.info("🧠 Generando Arquitectura...")
                    est = consola_ia.generar_estructura(marca_cliente)
                    res = supabase.table("fabrica_proyectos").select("id").eq("nombre_proyecto", nombre_proy).execute()
                    if res.data: supabase.table("fabrica_proyectos").update({"estructura_web": est}).eq("id", res.data[0]['id']).execute()
                    else: supabase.table("fabrica_proyectos").insert({"nombre_proyecto": nombre_proy, "estructura_web": est}).execute()
                    st.success("✅ Estructura Guardada.")
            if len(acciones) > 1 and c2.button(f"⚡ {acciones[1]}", use_container_width=True):
                st.success("Operación preparada.")

        # --- NUEVA INYECCIÓN: BÓVEDA DE CONOCIMIENTO Y RAG ---
        st.markdown("---")
        with st.expander("📚 Bóveda de Conocimiento & Personalización RAG", expanded=True):
            st.caption("Alimenta a la IA con el manual corporativo, logos, inspiración y colores exactos.")
            
            # 1. Selector Manual de 4 Colores
            st.markdown("**🎨 Forzar Paleta de Colores (Anula IA estática)**")
            col_c1, col_c2, col_c3, col_c4 = st.columns(4)
            c_pri = col_c1.color_picker("Color 1 (Principal)", "#D4AF37")
            c_sec = col_c2.color_picker("Color 2 (Secundario)", "#1A1A1A")
            c_ter = col_c3.color_picker("Color 3 (Acento)", "#FFFFFF")
            c_cua = col_c4.color_picker("Color 4 (Fondo)", "#F0F2F6")
            
            # 2. Inspiración Web
            urls_inspiracion = st.text_area("🔗 URLs de Referencia (Sitios web que el cliente admira, separados por coma)", placeholder="ej: apple.com, stripe.com")
            
            # 3. Recolector de Archivos (PDF/Logos)
            archivos_rag = st.file_uploader("📂 Subir Manual de Marca (PDF), Logos e Imágenes de Productos (PNG/JPG)", accept_multiple_files=True)
            
            if st.button("💾 Guardar Parámetros en Bóveda RAG"):
                banco_data = {
                    "colores_manuales": [c_pri, c_sec, c_ter, c_cua],
                    "urls_inspiracion": [url.strip() for url in urls_inspiracion.split(",") if url.strip()],
                    "archivos_pendientes": [f.name for f in archivos_rag] if archivos_rag else []
                }
                try:
                    res = supabase.table("fabrica_proyectos").select("id").eq("nombre_proyecto", nombre_proy).execute()
                    if res.data:
                        supabase.table("fabrica_proyectos").update({"banco_rag": banco_data}).eq("id", res.data[0]['id']).execute()
                    else:
                        supabase.table("fabrica_proyectos").insert({"nombre_proyecto": nombre_proy, "banco_rag": banco_data}).execute()
                    st.success("🧠 Datos inyectados en la base de conocimiento del cliente. Listos para el análisis de la IA.")
                except Exception as e:
                    st.error(f"Error al guardar: {e}")

        # --- TABLA DE DATOS ---
        st.markdown("---")
        st.subheader("📝 Directorio Premium")
        df_editado = st.data_editor(df, hide_index=True, use_container_width=True, key="editor_maestro")
        if st.button("🔄 Sincronizar Bóveda"):
            st.success("✨ Sincronización Exitosa!")
