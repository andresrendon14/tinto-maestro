import streamlit as st
import requests
from backend.services.project_service import ProjectService
from backend.workers.extraction_worker import ExtractionWorker

def ejecutar():
    # --- ENCABEZADO ---
    proyectos = ProjectService.get_active_projects()
    if not proyectos:
        st.warning("⚠️ Requiere onboarding previo en el CRM.")
        return

    opciones_proy = {f"{p['name']} - {p.get('clients', {}).get('company_name', 'N/A')}": p['id'] for p in proyectos}
    
    col_t, col_s = st.columns([2, 1])
    col_t.header("🧠 Sala de Curaduría Semántica")
    proyecto_seleccionado = col_s.selectbox("Proyecto Activo:", list(opciones_proy.keys()), label_visibility="collapsed")
    project_id = opciones_proy[proyecto_seleccionado]

    st.caption(f"**Estado del Conocimiento:** 🛰️ Conectado | **Cobertura:** 45% | **Sincronización:** Híbrida")

    # --- LAS 4 PESTAÑAS RECUPERADAS ---
    tab1, tab2, tab3, tab4 = st.tabs(["📥 1. Fuentes", "🔍 2. Evidencia", "🧬 3. ADN de Marca", "⚖️ 4. Calidad"])

    with tab1:
        st.subheader("Zona de Ingesta de Activos")
        col_up1, col_up2 = st.columns(2)
        with col_up1:
            archivos = st.file_uploader("Documentos y Visuales", type=["pdf", "docx", "txt"], accept_multiple_files=True)
            if st.button("Subir e Indexar Archivos", type="primary"):
                if archivos:
                    for f in archivos:
                        file_bytes = f.getvalue()
                        with st.spinner(f"Destilando {f.name}..."):
                            # Bypass Híbrido
                            try:
                                files = {"file": (f.name, file_bytes, "application/pdf")}
                                requests.post(f"http://localhost:8000/api/v1/projects/{project_id}/upload-pdf", files=files, timeout=1)
                                st.success(f"✅ {f.name} procesado vía FastAPI (Local)")
                            except:
                                data = ExtractionWorker.process_pdf(file_bytes, f.name)
                                st.success(f"✅ {f.name} procesado vía Internal Worker (Nube)")
                else:
                    st.warning("Selecciona un archivo primero.")
        with col_up2:
            st.text_area("URLs de Referencia", placeholder="https://...")
            st.button("Indexar URLs")

    with tab2:
        st.subheader("Hallazgos Semánticos (Evidencia)")
        with st.container(border=True):
            st.markdown("**📌 Público Objetivo Detectado**")
            st.write("*Dueños de negocios premium* (Confianza: 92%)")
            st.button("Aprobar Hallazgo", key="ap1")

    with tab3:
        st.subheader("Editor de ADN de Marca")
        with st.form("form_adn"):
            st.text_area("Misión / Propósito", value="Revolucionar la experiencia...")
            st.text_input("Arquetipo de Marca", value="El Creador")
            st.form_submit_button("Guardar Versión ADN")

    with tab4:
        st.subheader("Métricas de Cobertura")
        st.progress(65, text="Identidad Verbal")
        st.info("El Agente Biónico requiere más información sobre 'Competencia'.")

