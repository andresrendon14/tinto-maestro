import streamlit as st
from backend.services.project_service import ProjectService

def ejecutar():
    # --- ENCABEZADO EJECUTIVO ---
    proyectos = ProjectService.get_active_projects()
    if not proyectos:
        st.warning("⚠️ Requiere onboarding previo en el CRM.")
        return

    opciones_proy = {f"{p['name']} - {p.get('clients', {}).get('company_name', 'N/A')}": p['id'] for p in proyectos}
    
    col_t, col_s = st.columns([2, 1])
    col_t.header("📚 Sala de Curaduría Semántica")
    proyecto_seleccionado = col_s.selectbox("Proyecto Activo:", list(opciones_proy.keys()), label_visibility="collapsed")
    
    st.caption(f"**Estado del Conocimiento:** 🟡 En proceso | **Cobertura:** 45% | **Última act:** Hoy")
    if st.button("🧠 Procesar Conocimiento y Extraer Evidencia", type="primary"):
        st.toast("Iniciando chunking y embeddings...")

    # --- LAS 4 PESTAÑAS DE CURADURÍA ---
    tab1, tab2, tab3, tab4 = st.tabs(["📥 1. Fuentes", "🔎 2. Evidencia", "🧬 3. ADN de Marca", "📊 4. Calidad y Trazabilidad"])

    with tab1:
        st.subheader("Zona de Ingesta de Activos")
        col_up1, col_up2 = st.columns(2)
        with col_up1:
            archivos = st.file_uploader("Documentos y Visuales", type=["pdf", "docx", "txt", "jpg", "png"], accept_multiple_files=True)
            categoria = st.selectbox("Asignar Categoría:", ["Identidad de Marca", "Portafolio/Productos", "Competencia", "Tono y Comunicación"])
            if st.button("Subir e Indexar Archivos"):
                st.success(f"{len(archivos)} archivos encolados para vectorización.")
        with col_up2:
            st.text_area("URLs de Referencia (Landing pages, Redes)", placeholder="https://...")
            if st.button("Indexar URLs"):
                st.success("Web scraping encolado.")
        
        st.markdown("**Activos Procesados:**")
        st.dataframe({"Nombre": ["manual_marca_2024.pdf", "logo_vector.png"], "Categoría": ["Identidad", "Visual"], "Estado": ["✅ Indexado", "✅ Extraído"]})

    with tab2:
        st.subheader("Hallazgos Semánticos (Evidencia)")
        st.write("Valida lo que el sistema ha entendido de los archivos subidos.")
        
        # Simulación de cards de evidencia
        with st.container(border=True):
            st.markdown("**🎯 Público Objetivo Detectado**")
            st.write("*"Dueños de restaurantes premium y hoteles boutique" (Confianza: 92%)*")
            st.caption("📍 Fuente: brochure_comercial.pdf (Pág 3)")
            c_e1, c_e2, c_e3 = st.columns([1,1,4])
            c_e1.button("✅ Aprobar", key="ap1")
            c_e2.button("❌ Descartar", key="ds1")

        with st.container(border=True):
            st.markdown("**🗣️ Tono de Comunicación**")
            st.write("*"Sobrio, tecnológico, pero sin perder la calidez artesanal" (Confianza: 88%)*")
            st.caption("📍 Fuente: Inferido de manual_marca.pdf + 2 URLs")
            c_e4, c_e5, c_e6 = st.columns([1,1,4])
            c_e4.button("✅ Aprobar", key="ap2")
            c_e5.button("❌ Descartar", key="ds2")

    with tab3:
        st.subheader("Editor de ADN de Marca")
        st.info("Consolidación final del contexto que usará la IA para generar código y diseño.")
        
        with st.form("form_adn"):
            c_adn1, c_adn2 = st.columns(2)
            c_adn1.text_area("Misión / Propósito", value="Revolucionar la experiencia del café...")
            c_adn2.text_area("Promesa Central", value="El mejor café de especialidad a un clic.")
            
            c_adn3, c_adn4 = st.columns(2)
            c_adn3.text_input("Arquetipo de Marca", value="El Creador / El Sabio")
            c_adn4.text_input("Estilo Visual a Evitar", value="Colores neón, tipografías infantiles")
            
            st.text_input("Palabras Prohibidas", value="barato, económico, básico")
            
            if st.form_submit_button("💾 Guardar Nueva Versión de ADN (v1.2)"):
                st.success("ADN guardado y bloqueado para el Compilador Visual (Sinfonía).")

    with tab4:
        st.subheader("Centro de Calidad y Reglas")
        col_q1, col_q2 = st.columns(2)
        
        with col_q1:
            st.markdown("**Mapa de Cobertura Semántica**")
            st.progress(90, text="Identidad Visual (🟢 Suficiente)")
            st.progress(65, text="Identidad Verbal (🟡 Parcial)")
            st.progress(20, text="Objeciones y Competencia (🔴 Faltante)")
            
            st.markdown("**Veredicto de la IA:**")
            st.warning("Usable con riesgos (Falta contexto de competencia)")

        with col_q2:
            st.markdown("**Reglas Operativas para la IA**")
            st.checkbox("Usar solo contenido aprobado", value=True)
            st.checkbox("Prohibido inventar claims/testimonios", value=True)
            st.checkbox("Priorizar PDF 'Manual de Marca' sobre URLs", value=True)
            st.button("Actualizar Reglas de Compilación")
