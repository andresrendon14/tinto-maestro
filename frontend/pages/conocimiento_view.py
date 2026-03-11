import streamlit as st
from backend.services.project_service import ProjectService
from backend.services.ingestion_service import IngestionService

def ejecutar():
    st.header("📚 Ingesta de Conocimiento (RAG)")
    
    proyectos = ProjectService.get_active_projects()
    if not proyectos:
        st.warning("⚠️ Ve al CRM para realizar el Onboarding de un cliente primero.")
        return

    opciones_proy = {f"💻 {p['name']} (Marca: {p.get('clients', {}).get('company_name', 'N/A')})": p['id'] for p in proyectos}
    proyecto_seleccionado = st.selectbox("🗂️ Selecciona el Proyecto:", list(opciones_proy.keys()))
    project_id = opciones_proy[proyecto_seleccionado]

    with st.expander("🔗 Referencias e Inspiración Web", expanded=True):
        urls = st.text_area("URLs de sitios web de referencia (separadas por coma)")
        if st.button("Guardar URLs en Bóveda"):
            if urls:
                with st.spinner("Indexando..."):
                    try:
                        for url in urls.split(","):
                            clean_url = url.strip()
                            if clean_url: IngestionService.save_asset_metadata(project_id, "url", clean_url, clean_url)
                        st.success("✅ URLs registradas exitosamente.")
                    except Exception as e: st.error(f"Error: {e}")

    with st.expander("📂 Activos de Marca (PDF, PNG, JPG)", expanded=True):
        archivos = st.file_uploader("Sube manuales o logotipos", accept_multiple_files=True)
        if st.button("Registrar Archivos"):
            if archivos:
                with st.spinner("Registrando huellas..."):
                    try:
                        for f in archivos:
                            tipo = "pdf" if f.name.endswith(".pdf") else "image"
                            IngestionService.save_asset_metadata(project_id, tipo, f.name)
                        st.success(f"✅ {len(archivos)} archivo(s) acoplado(s).")
                    except Exception as e: st.error(f"Error: {e}")
