import streamlit as st
import streamlit.components.v1 as components
from backend.services.project_service import ProjectService

def inyectar_css_avanzado():
    st.markdown("""
    <style>
        .avatar-flotante {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background-color: #1E1E1E;
            color: #FFFFFF;
            padding: 15px 20px;
            border-radius: 50px;
            box-shadow: 0px 8px 16px rgba(0,0,0,0.5);
            z-index: 9999;
            cursor: pointer;
            border: 2px solid #D4AF37;
            font-size: 14px;
            transition: all 0.3s ease;
        }
        .avatar-flotante:hover { transform: scale(1.05); background-color: #2D2D2D; }
        .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 98%; }
    </style>
    <div class="avatar-flotante">
        ◉ <b>Avatar CEO:</b> <i>"Lienzo Open-Source activado. Puedes arrastrar bloques web reales."</i>
    </div>
    """, unsafe_allow_html=True)

def render_grapesjs_canvas():
    """Inyecta un constructor web Drag & Drop real (Open Source) dentro de Streamlit"""
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/grapesjs/0.21.2/css/grapes.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/grapesjs/0.21.2/grapes.min.js"></script>
        <script src="https://unpkg.com/grapesjs-preset-webpage@1.0.2"></script>
        <style>
            body, html { height: 100%; margin: 0; }
            #gjs { border: 2px solid #444; border-radius: 8px; overflow: hidden; }
        </style>
    </head>
    <body>
        <div id="gjs">
            <h1 style="text-align:center; margin-top:50px; font-family:sans-serif;">Lienzo de Diseño Vivo</h1>
            <p style="text-align:center; font-family:sans-serif;">Arrastra elementos desde el panel derecho hacia aquí.</p>
        </div>
        <script>
            const editor = grapesjs.init({
                container: '#gjs',
                height: '600px',
                width: 'auto',
                plugins: ['gjs-preset-webpage'],
                storageManager: false, // Desactivado para esta demo
            });
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=620, scrolling=False)

def ejecutar():
    inyectar_css_avanzado()

    st.caption("CENTRO MAESTRO DE EJECUCIÓN VIVA")
    col_t1, col_t2, col_t3, col_t4 = st.columns([3, 2, 2, 3])
    with col_t1: st.markdown("**Proyecto:** Landing Los Parceritos | **Cliente:** Empresa X")
    with col_t2: st.info("🟢 Diseño + Código en ejecución")
    with col_t3: vista = st.radio("Vista:", ["Web", "Tablet", "App"], horizontal=True, label_visibility="collapsed")
    with col_t4:
        c_btn1, c_btn2, c_btn3 = st.columns(3)
        c_btn1.button("▶️ Ejecutar", use_container_width=True)
        c_btn2.button("✅ Aprobar", use_container_width=True)
        c_btn3.button("🚀 Publicar", type="primary", use_container_width=True)

    st.divider()

    panel_izq, panel_cen, panel_der = st.columns([2.5, 6, 2])

    with panel_izq:
        st.subheader("🤖 Consola IA")
        tab_chat, tab_agentes = st.tabs(["💬 Chat", "⚡ Agentes"])
        with tab_chat:
            st.text_area("Comando Biónico", placeholder="Ej: Genera un hero section oscuro...", height=100)
            st.button("Enviar al Agente", use_container_width=True, type="primary")
        with tab_agentes:
            st.success("Stitch Visual Agent: Operativo")

    with panel_cen:
        tab_diseno, tab_flujo = st.tabs(["🎨 Canvas (GrapesJS)", "🔀 Flujo"])
        with tab_diseno:
            st.subheader(f"Modo Construcción ({vista})")
            # --- AQUÍ INYECTAMOS EL CANVAS REAL ---
            render_grapesjs_canvas()

    with panel_der:
        st.subheader("⚙️ Inspector")
        st.info("El inspector nativo de GrapesJS está integrado en el lienzo central. Usa este panel lateral para reglas de negocio e IA.")
        st.markdown("**Reglas de Marca:**")
        st.checkbox("Forzar Paleta Aprobada", value=True)
        st.checkbox("Bloquear Copy Estratégico", value=True)
        st.button("Revisión de Calidad IA")
