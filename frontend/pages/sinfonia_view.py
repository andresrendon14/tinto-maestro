import streamlit as st
from backend.services.project_service import ProjectService

def inyectar_css_avanzado():
    """Hack de CSS para crear el Avatar Flotante y paneles fijos"""
    st.markdown("""
    <style>
        /* Burbuja Flotante del Avatar CEO */
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
        .avatar-flotante:hover {
            transform: scale(1.05);
            background-color: #2D2D2D;
        }
        /* Ajuste de márgenes para maximizar espacio */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 98%;
        }
    </style>
    <div class="avatar-flotante">
        ◉ <b>Avatar CEO:</b> <i>"Desktop aprobado. Te sugiero ajustar el CTA móvil."</i>
    </div>
    """, unsafe_allow_html=True)

def ejecutar():
    inyectar_css_avanzado()

    # --- 1. BARRA DE CONTROL GLOBAL (TOP BAR) ---
    st.caption("CENTRO MAESTRO DE EJECUCIÓN VIVA")
    col_t1, col_t2, col_t3, col_t4 = st.columns([3, 2, 2, 3])
    
    with col_t1:
        st.markdown("**Proyecto:** Landing Los Parceritos | **Cliente:** Empresa X")
    with col_t2:
        st.info("🟢 Diseño + Código en ejecución")
    with col_t3:
        vista = st.radio("Vista:", ["Web", "Tablet", "App"], horizontal=True, label_visibility="collapsed")
    with col_t4:
        c_btn1, c_btn2, c_btn3 = st.columns(3)
        c_btn1.button("▶️ Ejecutar", use_container_width=True)
        c_btn2.button("✅ Aprobar", use_container_width=True)
        c_btn3.button("🚀 Publicar", type="primary", use_container_width=True)

    st.divider()

    # --- ESTRUCTURA DE 3 PANELES ---
    # Izquierda (20%), Centro (60%), Derecha (20%)
    panel_izq, panel_cen, panel_der = st.columns([2.5, 5, 2.5])

    # --- 2. PANEL IZQUIERDO: CONSOLA IA Y AGENTES ---
    with panel_izq:
        st.subheader("🤖 Consola IA")
        tab_chat, tab_agentes, tab_permisos, tab_habilidades = st.tabs(["💬 Chat", "⚡ Agentes", "🔐 Permisos", "🛠️ Habilidades"])
        
        with tab_chat:
            st.text_area("Chat Maestro Operativo", placeholder="Ej: Cambia el botón principal por uno más premium...", height=150)
            st.button("Enviar Comando Biónico", use_container_width=True)
            st.caption("Acciones Rápidas:")
            st.button("✨ Mejorar Hero", use_container_width=True)
            st.button("📱 Corregir Móvil", use_container_width=True)
            
        with tab_agentes:
            with st.container(border=True):
                st.markdown("**🎨 Stitch Visual Agent**")
                st.caption("Tarea: Rediseñando Hero | Estado: En curso")
                st.button("Intervenir", key="btn_stitch")
            with st.container(border=True):
                st.markdown("**⚙️ Antigravity Dev**")
                st.caption("Tarea: Act. Componente | Estado: 🟡 Esperando permiso")
                st.button("Aprobar", key="btn_anti", type="primary")

        with tab_permisos:
            st.warning("1 Permiso pendiente: Modificar Header.")
        
        with tab_habilidades:
            st.info("Fábrica de habilidades en construcción.")

    # --- 3. PANEL CENTRAL: CANVAS OPERATIVO ---
    with panel_cen:
        tab_diseno, tab_flujo, tab_preview, tab_comparar = st.tabs(["🎨 Diseñar", "🔀 Flujo", "📱 Vista Previa", "⚖️ Comparar"])
        
        with tab_diseno:
            st.subheader(f"Lienzo Visual Inteligente ({vista})")
            with st.container(border=True, height=400):
                st.markdown("<div style='text-align: center; margin-top: 100px; color: gray;'>", unsafe_allow_html=True)
                st.markdown("### 🏗️ Área del Canvas (Simulador de Componentes)")
                st.markdown(f"Aquí se renderiza dinámicamente el `render_spec.json` para **{vista}**.")
                st.button("[ Botón Primario a Editar ]", use_container_width=False)
                st.markdown("</div>", unsafe_allow_html=True)
                
            c_herr1, c_herr2, c_herr3 = st.columns(3)
            c_herr1.button("➕ Añadir Bloque")
            c_herr2.button("📝 Editar Copy")
            c_herr3.button("🖼️ Cambiar Imagen")

        with tab_flujo:
            st.info("Mapa de nodos y conexiones de la aplicación.")
        with tab_preview:
            st.success("Vista limpia sin herramientas de edición.")

    # --- 4. PANEL DERECHO: INSPECTOR INTELIGENTE ---
    with panel_der:
        st.subheader("⚙️ Inspector")
        tab_prop, tab_accion, tab_ia, tab_historial = st.tabs(["Estilo", "Acción", "🧠 IA", "⏱️ Historial"])
        
        with tab_prop:
            st.markdown("**Elemento:** `BotonPrimario`")
            st.color_picker("Color Principal", "#D4AF37")
            st.select_slider("Tamaño", options=["S", "M", "L", "XL"], value="M")
            st.slider("Border Radius", 0, 50, 8)
            
        with tab_accion:
            st.selectbox("Trigger", ["onClick", "onHover", "onLoad"])
            st.selectbox("Acción", ["Abrir Modal", "Llamar Agente", "Guardar CRM"])
            
        with tab_ia:
            st.info("💡 **Recomendación:** Este CTA tiene baja claridad respecto al ADN de marca. ¿Deseas que Gemini lo reescriba?")
            st.button("Aplicar Parche IA")

    # --- 5. BOTTOM BAR (TIMELINE) ---
    st.divider()
    col_b1, col_b2, col_b3 = st.columns(3)
    col_b1.caption("🕒 **Timeline:** Hace 2m - Stitch propuso cambio de color.")
    col_b2.caption("⚠️ **Alertas:** 0 Conflictos detectados.")
    col_b3.caption("🏗️ **Build:** Versión v1.2 estable.")

