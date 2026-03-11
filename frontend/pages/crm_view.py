import streamlit as st
from backend.services.project_service import ProjectService

def ejecutar():
    st.header("🤝 CRM & Orquestación de Proyectos")
    
    with st.expander("➕ Nuevo Onboarding de Marca", expanded=True):
        with st.form("form_onboarding"):
            col1, col2 = st.columns(2)
            contact_name = col1.text_input("👤 Nombre del Contacto")
            company_name = col2.text_input("🏢 Nombre de la Marca / Empresa")
            email = col1.text_input("📧 Correo Electrónico")
            project_name = col2.text_input("💻 Nombre del Proyecto (App/Web)")

            if st.form_submit_button("🚀 Inicializar Arquitectura"):
                if company_name and project_name:
                    with st.spinner("Construyendo ontología..."):
                        try:
                            ProjectService.create_client_and_project(contact_name, company_name, email, project_name)
                            st.success(f"✅ Proyecto '{project_name}' acoplado al sistema.")
                        except Exception as e:
                            st.error(str(e))
                else:
                    st.warning("⚠️ La Marca y el Nombre del Proyecto son obligatorios.")

    st.markdown("---")
    st.subheader("🗄️ Proyectos en Curso")
    proyectos = ProjectService.get_active_projects()
    
    if proyectos:
        for p in proyectos:
            marca = p.get('clients', {}).get('company_name', 'Desconocida')
            c_info, c_fase, c_accion = st.columns([3, 2, 1])
            c_info.markdown(f"**{p['name']}** \n*Marca: {marca}*")
            c_fase.info(f"Fase: {p['current_stage'].upper()}")
            c_accion.button("Operar", key=f"btn_{p['id']}", use_container_width=True)
            st.divider()
    else:
        st.info("📭 No hay proyectos. Inicia un Onboarding arriba.")
