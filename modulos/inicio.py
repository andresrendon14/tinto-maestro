import streamlit as st
def verificar_secret(llave):
    try: return "✅ OK" if llave in st.secrets else "⏳ Pendiente"
    except: return "⏳ Pendiente"

def ejecutar():
    st.header("🚀 Centro de Mando: Tinto Maestro")
    st.caption("Versión Modular Activa: 1.0.0")
    
    st.markdown("### 📊 Estado del Sistema")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Arquitectura", "Modular")
    c2.metric("Base de Datos", verificar_secret("SUPABASE_URL"))
    c3.metric("Motores IA", verificar_secret("GROQ_API_KEY"))
    c4.metric("UI/UX", "Apple/Coffee")
    
    st.info("💡 Todo el sistema está corriendo sobre módulos independientes. Seguro y reversible.")
