import streamlit as st
import requests
from backend.services.project_service import ProjectService

def ejecutar():
    proyectos = ProjectService.get_active_projects()
    if not proyectos:
        st.warning("⚠️ Requiere onboarding previo en el CRM.")
        return

    opciones_proy = {f"{p['name']} - {p.get('clients', {}).get('company_name', 'N/A')}": p['id'] for p in proyectos}
    
    col_t, col_s = st.columns([2, 1])
    col_t.header("📚 Sala de Curaduría Semántica")
    proyecto_seleccionado = col_s.selectbox("Proyecto Activo:", list(opciones_proy.keys()), label_visibility="collapsed")
    project_id = opciones_proy[proyecto_seleccionado]
    
    st.caption(f"**Estado del Conocimiento:** 🟡 En proceso | **Cobertura:** 45% | **Última act:** Hoy")
    if st.button("🧠 Procesar Conocimiento y Extraer Evidencia", type="primary"):
        st.toast("Iniciando chunking y embeddings...")

    tab1, tab2, tab3, tab4 = st.tabs(["📥 1. Fuentes", "🔎 2. Evidencia", "🧬 3. ADN de Marca", "📊 4. Calidad y Trazabilidad"])

    with tab1:
        st.subheader("Zona de Ingesta de Activos")
        col_up1, col_up2 = st.columns(2)
        with col_up1:
            archivos = st.file_uploader("Documentos y Visuales", type=["pdf", "docx", "txt", "jpg", "png"], accept_multiple_files=True)
            categoria = st.selectbox("Asignar Categoría:", ["Identidad de Marca", "Portafolio/Productos", "Competencia", "Tono y Comunicación"])
            
            # --- MAGIA AQUÍ: CONEXIÓN AL BACKEND FASTAPI ---
            if st.button("Subir e Indexar Archivos"):
                if archivos:
                    for f in archivos:
                        if f.name.endswith(".pdf"):
                            with st.spinner(f"El Cerebro Backend está leyendo {f.name}..."):
                                try:
                                    # Empaquetamos el archivo para enviarlo por HTTP
                                    files = {"file": (f.name, f.getvalue(), "application/pdf")}
                                    url_api = f"http://localhost:8000/api/v1/projects/{project_id}/upload-pdf"
                                    
                                    # Disparo al servidor FastAPI
                                    response = requests.post(url_api, files=files)
                                    
                                    if response.status_code == 200:
                                        res_data = response.json()
                                        st.success(f"✅ {f.name} destilado: {res_data['details']['pages_read']} páginas, {res_data['details']['total_chunks_generated']} fragmentos extraídos.")
                                    else:
                                        st.error(f"Error del servidor: {response.text}")
                                except Exception as e:
                                    st.error(f"❌ Error de conexión: {e} \n\n**¿El motor FastAPI está encendido en el puerto 8000?**")
                        else:
                            st.warning(f"⚠️ {f.name} encolado. Por ahora, el extractor beta solo lee PDFs.")
                else:
                    st.warning("⚠️ Debes seleccionar un archivo primero.")

        with col_up2:
            st.text_area("URLs de Referencia (Landing pages, Redes)", placeholder="https://...")
            if st.button("Indexar URLs"):
                st.success("Web scraping encolado.")

    with tab2:
        st.subheader("Hallazgos Semánticos (Evidencia)")
        st.info("Esperando que apruebes la evidencia extraída de los PDFs.")

    with tab3:
        st.subheader("Editor de ADN de Marca")
        st.info("Consolidación en construcción...")

    with tab4:
        st.subheader("Centro de Calidad y Reglas")
        st.info("Métricas en construcción...")
