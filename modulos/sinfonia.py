import streamlit as st
import pandas as pd
from modulos.db import supabase

def ejecutar():
    st.header("🎨 Sinfonía de Marca & Arquitectura")
    st.caption("Visualizador en vivo del ADN de Marca y Estructura Web generados por los Micro-Agentes.")

    if not supabase:
        st.error("❌ Conexión a la bóveda visual perdida.")
        return

    # --- LECTURA DE LA BÓVEDA ---
    try:
        respuesta = supabase.table("fabrica_proyectos").select("*").order("created_at", descending=True).execute()
        datos = respuesta.data
    except Exception as e:
        st.error(f"Error de lectura: {e}")
        datos = []

    if not datos:
        st.info("📭 La bóveda visual está vacía.")
        return

    df = pd.DataFrame(datos)
    
    # --- SELECTOR DE PROYECTO ---
    st.markdown("### 🗂️ Seleccionar Lienzo de Proyecto")
    proyecto_seleccionado = st.selectbox("Elige la Web App a previsualizar:", df['nombre_proyecto'].tolist())
    
    datos_proyecto = df[df['nombre_proyecto'] == proyecto_seleccionado].iloc[0]
    
    # Extracción segura de diccionarios JSON
    config_ui = datos_proyecto.get('configuracion_ui') or {}
    estructura_web = datos_proyecto.get('estructura_web') or {}
    
    if not config_ui and not estructura_web:
        st.warning("⚠️ Este proyecto no contiene ADN visual ni estructura base. Ve al CRM a generarlos.")
        return

    st.success(f"Cargando especificaciones para: **{datos_proyecto.get('cliente_asociado', 'Cliente')}**")
    
    # --- PANEL DE EXTRACCIÓN DUAL (DISEÑO + ARQUITECTURA) ---
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    color_pri = config_ui.get('color_primario', '#D4AF37')
    color_sec = config_ui.get('color_secundario', '#1A1A1A')
    
    with col1:
        st.subheader("🎨 Paleta Base")
        st.color_picker("Color Primario", color_pri, disabled=True)
        st.color_picker("Color Secundario", color_sec, disabled=True)
        
    with col2:
        st.subheader("🏗️ Arquitectura Web")
        if estructura_web:
            st.info(f"**Navegación:** {estructura_web.get('navegacion', 'N/A')}")
            st.write("**Páginas Integradas:** " + " | ".join(estructura_web.get('paginas', [])))
            st.write("**Módulos Activos:** " + ", ".join(estructura_web.get('modulos_activos', [])))
        else:
            st.warning("Estructura Web no definida. Ejecuta el Agente de Desarrollo Web en el CRM.")

    # --- RENDERIZADO DE ALTA FIDELIDAD ---
    st.markdown("---")
    st.subheader("👁️ Previsualización del Producto Final")
    
    # Construcción dinámica del menú superior
    paginas = estructura_web.get('paginas', ['Inicio', 'Contacto'])
    nav_links = "".join([f"<span style='margin-left:20px; cursor:pointer; font-size:14px; text-transform:uppercase; letter-spacing:1px;'>{p}</span>" for p in paginas])
    modulos = ", ".join(estructura_web.get('modulos_activos', ['Ninguno']))
    
    html_simulacion = f"""
        <div style="background-color: {color_sec}; padding: 30px; border-radius: 12px; border: 2px solid {color_pri}; box-shadow: 0 8px 16px rgba(0,0,0,0.2); color: #F0F2F6; font-family: '{config_ui.get('tipografia_textos', 'sans-serif')}';">
            
            <div style="border-bottom: 1px solid {color_pri}; padding-bottom: 20px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center;">
                <h2 style="color: {color_pri}; margin: 0; font-family: '{config_ui.get('tipografia_titulos', 'sans-serif')}'; font-size: 24px;">
                    {datos_proyecto.get('cliente_asociado', 'Marca')}
                </h2>
                <div>
                    {nav_links}
                </div>
            </div>

            <h1 style="color: {color_pri}; font-family: '{config_ui.get('tipografia_titulos', 'sans-serif')}'; margin-top: 0; font-size: 36px;">
                Bienvenidos a la Plataforma Inteligente
            </h1>
            <p style="font-size: 18px; line-height: 1.8; opacity: 0.9;">
                Esta vista integra automáticamente la configuración visual y la arquitectura de software. 
                Los siguientes módulos backend están listos para acoplarse: 
                <br><br>
                <span style="color:{color_pri}; font-weight:bold;">⚙️ {modulos}</span>
            </p>
            <br>
            <button style="background-color: {color_pri}; color: {color_sec}; border: none; padding: 14px 28px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 16px; transition: 0.3s;">
                Ejecutar Módulo Principal
            </button>
        </div>
    """
    st.markdown(html_simulacion, unsafe_allow_html=True)

