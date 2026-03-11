import streamlit as st
import pandas as pd

def verificar_llave(nombre_llave):
    """Verifica si la llave existe en los secretos sin mostrarla."""
    try:
        if st.secrets[nombre_llave]:
            return "✅ Conectado"
    except:
        return "❌ Desconectado"

def ejecutar():
    st.header("🧠 Cerebro Maestro (IA & CRM)")
    st.write("Centro de mando multi-motor blindado con Bóveda de Secretos.")
    
    # Panel de Estado de los Motores
    with st.expander("🔌 Estado de Conexión de Motores", expanded=False):
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Groq", verificar_llave("GROQ_API_KEY"))
        c2.metric("Grok (xAI)", verificar_llave("GROK_API_KEY"))
        c3.metric("Gemini", verificar_llave("GEMINI_API_KEY"))
        c4.metric("Mistral", verificar_llave("MISTRAL_API_KEY"))
        c5.metric("Ollama / MCP", "📍 Localhost")
    
    tab_chat, tab_conocimiento, tab_crm = st.tabs(["🗨️ Multi-IA Chat", "📚 Cuadernos RAG", "🤝 CRM Open Source"])
    
    # --- PESTAÑA 1: CHAT MULTI-MOTOR ---
    with tab_chat:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("### ⚙️ Enrutador")
            motor = st.selectbox("Selecciona la Red Neuronal", [
                "OpenClaw (Natívo)", 
                "Groq (Llama 3)", 
                "Grok (xAI)", 
                "Gemini Pro", 
                "Mistral", 
                "Ollama (Servidor Local)",
                "Google Stitch / MCP"
            ])
            st.info(f"Enrutando a: **{motor}**")
            
        with col2:
            st.markdown("### 📡 Terminal de Mando")
            chat_container = st.container(height=300)
            with chat_container:
                st.chat_message("assistant").write(f"Iniciando enlace seguro con {motor}... Listo para recibir instrucciones.")
            
            prompt = st.chat_input("Comando para el motor...")
            if prompt:
                st.success(f"Solicitud interceptada por el router. Preparando envío a {motor} (MVP Front-end).")

    # --- PESTAÑA 2: CONOCIMIENTO ---
    with tab_conocimiento:
        st.markdown("### 📓 Alimentación de Memoria")
        st.write("Conecta PDFs y TXTs para dar contexto a Groq, Gemini o Mistral usando RAG.")
        st.file_uploader("Subir archivos clasificados", accept_multiple_files=True)
        st.button("🧠 Procesar con IA")

    # --- PESTAÑA 3: CRM ---
    with tab_crm:
        st.markdown("### 🤝 CRM Base (Código Abierto)")
        if "crm_data" not in st.session_state:
            st.session_state.crm_data = pd.DataFrame({
                "Nombre": ["Andrés CEO"],
                "Empresa": ["Tinto Maestro"],
                "Estado": ["Arquitecto Jefe"],
                "Teléfono": ["Secret"]
            })
        st.dataframe(st.session_state.crm_data, use_container_width=True)
