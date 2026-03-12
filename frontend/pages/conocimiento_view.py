import streamlit as st
import requests
from backend.services.project_service import ProjectService
from backend.workers.extraction_worker import ExtractionWorker

def ejecutar():
    st.header("🧠 Sala de Curaduría Semántica")
    proyectos = ProjectService.get_active_projects()
    
    if not proyectos:
        st.warning("⚠️ Realiza el onboarding en el CRM primero.")
        return

    opciones_proy = {f"{p['name']}": p['id'] for p in proyectos}
    proyecto_sel = st.selectbox("Proyecto Activo:", list(opciones_proy.keys()))
    project_id = opciones_proy[proyecto_sel]

    archivo = st.file_uploader("Sube tu manual de marca (PDF)", type=["pdf"])

    if st.button("🚀 Procesar Conocimiento"):
        if archivo:
            file_bytes = archivo.getvalue()
            
            with st.spinner("Analizando documento..."):
                # INTENTO 1: Hablar con FastAPI (Modo Local)
                try:
                    files = {"file": (archivo.name, file_bytes, "application/pdf")}
                    res = requests.post(f"http://localhost:8000/api/v1/projects/{project_id}/upload-pdf", files=files, timeout=2)
                    data = res.json()
                    st.success(f"✅ [MODO LOCAL] {archivo.name} procesado por FastAPI.")
                
                # INTENTO 2: Procesar aquí mismo (Modo WEB/Nube)
                except Exception:
                    st.info("🌐 [MODO NUBE] Servidor local no detectado. Usando extractor interno...")
                    data = ExtractionWorker.process_pdf(file_bytes, archivo.name)
                    st.success(f"✅ {archivo.name} procesado con éxito en la nube.")
                
                st.json(data["details"])
        else:
            st.error("Por favor, sube un archivo.")
