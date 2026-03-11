import streamlit as st
import pandas as pd
from modulos.db import supabase

def ejecutar():
    st.header("🎨 Sinfonía de Marca: Motor de Renderizado")
    st.caption("Visualizador en vivo del ADN de Marca generado por los Micro-Agentes.")

    if not supabase:
        st.error("❌ Conexión a la bóveda visual perdida.")
        return

    # --- LECTURA DE LA BÓVEDA DE FABRICACIÓN ---
    try:
        respuesta = supabase.table("fabrica_proyectos").select("*").order("created_at", descending=True).execute()
        datos = respuesta.data
    except Exception as e:
        st.error(f"Error de lectura: {e}")
        datos = []

    if not datos:
        st.info("📭 La bóveda visual está vacía.")
        st.markdown("👉 **Instrucción:** Ve al **🤝 CRM**, selecciona un proyecto y ejecuta el Agente **'🚀 Generar Identidad Visual'**.")
        return

    df = pd.DataFrame(datos)
    
    # --- SELECTOR DE PROYECTO A RENDERIZAR ---
    st.markdown("### 🗂️ Seleccionar Lienzo de Proyecto")
    proyecto_seleccionado = st.selectbox("Elige la Web App a previsualizar:", df['nombre_proyecto'].tolist())
    
    datos_proyecto = df[df['nombre_proyecto'] == proyecto_seleccionado].iloc[0]
    config_ui = datos_proyecto.get('configuracion_ui', {})
    
    if not config_ui:
        st.warning("⚠️ Este proyecto no contiene un ADN visual válido.")
        return

    st.success(f"Cargando especificaciones para: **{datos_proyecto.get('cliente_asociado', 'Cliente')}**")
    
    # --- PANEL DE EXTRACCIÓN JSON ---
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    color_pri = config_ui.get('color_primario', '#000000')
    color_sec = config_ui.get('color_secundario', '#FFFFFF')
    
    with col1:
        st.subheader("🎨 Paleta Base")
        # Mostramos los códigos de color exactos que generó el agente
        st.color_picker("Color Primario (Dominante)", color_pri, disabled=True)
        st.color_picker("Color Secundario (Fondo/Contraste)", color_sec, disabled=True)
        st.write(f"**Tema Arquitectónico:** `{config_ui.get('tema', 'N/A')}`")
        
    with col2:
        st.subheader("✍️ Tipografía Corporativa")
        st.info(f"**Títulos (H1/H2):** {config_ui.get('tipografia_titulos', 'N/A')}")
        st.info(f"**Cuerpo de Texto (p):** {config_ui.get('tipografia_textos', 'N/A')}")
        
    # --- RENDERIZADO EN VIVO (SIMULACIÓN DE APP DEL CLIENTE) ---
    st.markdown("---")
    st.subheader("👁️ Previsualización del Producto Final")
    st.caption("Así se verá la interfaz de la Web App de tu cliente con este ADN aplicado.")
    
    # Inyección de HTML/CSS dinámico para simular la vista del cliente
    html_simulacion = f"""
        <div style="background-color: {color_sec}; padding: 30px; border-radius: 12px; border: 2px solid {color_pri}; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h1 style="color: {color_pri}; font-family: '{config_ui.get('tipografia_titulos', 'sans-serif')}'; margin-top: 0;">
                Bienvenido al portal de {datos_proyecto.get('cliente_asociado', 'tu Marca')}
            </h1>
            <p style="color: #F0F2F6; font-family: '{config_ui.get('tipografia_textos', 'sans-serif')}'; font-size: 16px; line-height: 1.6;">
                Esta es una simulación de alta fidelidad. Los Micro-Agentes han inyectado exitosamente el 
                color primario ({color_pri}) en los elementos de acción y el color secundario ({color_sec}) 
                como estructura de fondo para mantener contraste y legibilidad.
            </p>
            <button style="background-color: {color_pri}; color: {color_sec}; border: none; padding: 12px 24px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 16px; margin-top: 10px;">
                Botón de Acción Principal
            </button>
        </div>
    """
    st.markdown(html_simulacion, unsafe_allow_html=True)

