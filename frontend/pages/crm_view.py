import streamlit as st
from backend.services.project_service import ProjectService
import datetime

def ejecutar():
    st.header("🤝 Gemelo Operativo & Orquestación de Cuentas")
    
    # --- NÚCLEO 1: ONBOARDING Y CUENTAS ---
    with st.expander("➕ Inicializar Nueva Cuenta (Onboarding)", expanded=False):
        with st.form("form_onboarding"):
            st.subheader("Datos Legales y de Contacto")
            c1, c2, c3 = st.columns(3)
            contact_name = c1.text_input("👤 Nombre de Contacto")
            celular = c2.text_input("📱 Celular (WhatsApp)")
            email = c3.text_input("📧 Correo Electrónico")
            
            c4, c5 = st.columns(2)
            company_name = c4.text_input("🏢 Nombre de la Marca")
            project_name = c5.text_input("💻 Nombre del Proyecto")
            
            st.markdown("---")
            politicas = st.checkbox("✅ El cliente acepta políticas de privacidad y autoriza el tratamiento de datos.")

            if st.form_submit_button("🚀 Desplegar Arquitectura de Cuenta"):
                if company_name and project_name and politicas:
                    try:
                        ProjectService.create_client_and_project(contact_name, company_name, email, project_name)
                        st.success(f"Cuenta para '{company_name}' creada. Ecosistema listo.")
                    except Exception as e:
                        st.error(str(e))
                elif not politicas:
                    st.warning("⚠️ Debes confirmar la autorización de tratamiento de datos.")
                else:
                    st.warning("⚠️ Marca y Proyecto son obligatorios.")

    # --- NÚCLEO 2: CONSOLA DE AGENTES BIÓNICOS ---
    st.markdown("---")
    st.subheader("🧠 Centro de Mando: Enjambre de Inteligencia")
    st.caption("Orquesta tareas específicas usando el modelo adecuado para cada carga cognitiva.")
    
    col_agentes, col_prompt = st.columns([1, 2])
    
    with col_agentes:
        cerebro_activo = st.selectbox("Selecciona el Cerebro Operativo:", [
            "🧠 Gemini (Estrategia y ADN de Marca)",
            "⚡ Groq (Inferencia rápida / Routing)",
            "🕵️ Mistral (Extracción de datos / Privacidad)",
            "🛡️ Ollama (Memoria local / Fallback)",
            "🚀 OpenClaw (Agentes / Automatizaciones)",
            "🌌 Antigravity (Desarrollo Agentic / Código)",
            "🎨 Stitch (Exportación Visual / UI)"
        ])
        
        fecha_ejecucion = st.date_input("🗓️ Programador Estratégico (Fecha)")
        hora_ejecucion = st.time_input("⏰ Hora de Ejecución")

    with col_prompt:
        instruccion = st.text_area("Comando para el Agente Biónico:", height=130, 
                                   placeholder="Ej: Extrae los claims principales del PDF subido y genera un draft del hero section. Si la claridad es < 80%, reitera.")
        
        c_btn1, c_btn2 = st.columns(2)
        if c_btn1.button("⚡ Ejecutar Ahora", use_container_width=True, type="primary"):
            st.toast(f"Enrutando comando a {cerebro_activo.split(' ')[1]} vía MCP...")
            st.info("Agente inicializado. Revisa el timeline vivo.")
            
        if c_btn2.button("📅 Programar Tarea", use_container_width=True):
            st.success(f"Tarea programada para el {fecha_ejecucion} a las {hora_ejecucion}.")

    # --- NÚCLEO 3: TIMELINE Y ESTADO DE PROYECTOS ---
    st.markdown("---")
    st.subheader("🗄️ Torre de Control de Proyectos")
    proyectos = ProjectService.get_active_projects()
    
    if proyectos:
        for p in proyectos:
            marca = p.get('clients', {}).get('company_name', 'Desconocida')
            with st.container(border=True):
                c_info, c_fase, c_salud, c_accion = st.columns([2, 2, 1, 1])
                c_info.markdown(f"**{p['name']}**\n*{marca}*")
                c_fase.info(f"Fase actual: {p['current_stage'].upper()}")
                c_salud.success("Salud: 98%")
                c_accion.button("Ver 360", key=f"btn_{p['id']}", use_container_width=True)
    else:
        st.info("No hay proyectos activos.")
