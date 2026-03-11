# Version OpenClaw 2.0 - Fix Cache
from __future__ import annotations

import base64
import datetime as dt
import io
import json
import os
import re
from pathlib import Path
from typing import Any

import pandas as pd
import qrcode
import streamlit as st
from PIL import Image

APP_NAME = "Tinto Maestro"
CHATBOT_NAME = "Tinto"
BASE_DIR = Path("tinto_maestro_data")
SYSTEM_DIR = BASE_DIR / "system"
PROJECTS_DIR = BASE_DIR / "projects"
EXPORTS_DIR = BASE_DIR / "exports"

ADMIN_USER = "ceo"
ADMIN_PASS = "123456"

DEFAULT_SYSTEM = {
    "lp_logo": "",
    "lp_logo_name": "",
    "show_lp_logo": True,
    "lp_logo_opacity": 0.82,
    "lp_logo_size": 64,
    "lp_logo_position": "right",
    "updated_at": "",
}

DEFAULT_PROJECT = {
    "brand_name": "Los Parceritos Demo",
    "slogan": "Digitalización popular con sabor a café",
    "description": "Panel CEO para crear, guardar, publicar y escalar web apps con memoria.",
    "business_type": "General",
    "tone": "Cercano",
    "palette": ["#2F1E17", "#F7F2E9", "#537A5A", "#C87B58"],
    "subdomain": "demo.losparceritos.com",
    "custom_domain": "",
    "project_logo": "",
    "project_logo_name": "",
    "avatar": "",
    "catalog_files": [],
    "promo_files": [],
    "knowledge_files": [],
    "references": [],
    "notes": "",
    "voice_style": "Natural",
    "gps_adaptive_voice": True,
    "published": False,
    "blocked": False,
    "payment_mp": False,
    "payment_payu": False,
    "security_level": "Doctorado brillante",
    "created_at": "",
    "updated_at": "",
}

def ensure_dirs() -> None:
    for folder in [BASE_DIR, SYSTEM_DIR, PROJECTS_DIR, EXPORTS_DIR]:
        folder.mkdir(parents=True, exist_ok=True)

def slugify(text: str) -> str:
    text = (text or "").strip().lower()
    text = re.sub(r"[^a-z0-9áéíóúñ\s_-]", "", text)
    text = text.replace(" ", "-")
    text = re.sub(r"-+", "-", text)
    return text.strip("-") or "marca"

def now() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default

def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def system_path() -> Path:
    return SYSTEM_DIR / "system.json"

def get_system() -> dict[str, Any]:
    data = load_json(system_path(), DEFAULT_SYSTEM.copy())
    for k, v in DEFAULT_SYSTEM.items():
        data.setdefault(k, v)
    return data

def save_system(data: dict[str, Any]) -> None:
    data["updated_at"] = now()
    save_json(system_path(), data)

def project_dir(brand_name: str) -> Path:
    return PROJECTS_DIR / slugify(brand_name)

def project_config_path(brand_name: str) -> Path:
    return project_dir(brand_name) / "config.json"

def get_project(brand_name: str) -> dict[str, Any]:
    data = load_json(project_config_path(brand_name), DEFAULT_PROJECT.copy())
    for k, v in DEFAULT_PROJECT.items():
        data.setdefault(k, v)
    if not data.get("brand_name"):
        data["brand_name"] = brand_name
    return data

def save_project(brand_name: str, data: dict[str, Any]) -> None:
    data["brand_name"] = brand_name
    data["updated_at"] = now()
    if not data.get("created_at"):
        data["created_at"] = now()
    save_json(project_config_path(brand_name), data)

def create_project_structure(brand_name: str) -> Path:
    root = project_dir(brand_name)
    folders = [
        "frontend", "backend", "assets/logos", "assets/avatar", "assets/catalogo",
        "assets/promociones", "knowledge", "domain", "qr", "crm", "automations",
        "security", "backups", "production", "sessions", "exports", "docs",
    ]
    for name in folders:
        (root / name).mkdir(parents=True, exist_ok=True)
    cfg = get_project(brand_name)
    save_project(brand_name, cfg)
    append_log(brand_name, f"Estructura base creada para {brand_name}")
    return root

def list_projects() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not PROJECTS_DIR.exists():
        return rows
    for child in PROJECTS_DIR.iterdir():
        if child.is_dir():
            cfg = load_json(child / "config.json", DEFAULT_PROJECT.copy())
            cfg.setdefault("brand_name", child.name)
            cfg["slug"] = child.name
            rows.append(cfg)
    rows.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
    return rows

def log_path(brand_name: str) -> Path:
    return project_dir(brand_name) / "sessions" / "log.json"

def append_log(brand_name: str, message: str, level: str = "INFO") -> None:
    path = log_path(brand_name)
    data = load_json(path, [])
    data.insert(0, {"time": now(), "level": level, "message": message})
    save_json(path, data[:300])

def get_logs(brand_name: str) -> list[dict[str, Any]]:
    return load_json(log_path(brand_name), [])

def memory_path(brand_name: str) -> Path:
    return project_dir(brand_name) / "sessions" / "memory.json"

def get_memory(brand_name: str) -> dict[str, Any]:
    return load_json(memory_path(brand_name), {"history": [], "last_prompt": "", "last_response": "", "next_step": ""})

def save_memory(brand_name: str, prompt: str, response: str) -> None:
    mem = get_memory(brand_name)
    mem["last_prompt"] = prompt
    mem["last_response"] = response
    mem["next_step"] = suggest_next_step(prompt, brand_name)
    mem["history"].insert(0, {"time": now(), "prompt": prompt, "response": response})
    mem["history"] = mem["history"][:50]
    save_json(memory_path(brand_name), mem)

def file_to_data_url(path_str: str) -> str:
    if not path_str:
        return ""
    path = Path(path_str)
    if not path.exists():
        return ""
    suffix = path.suffix.lower()
    mime = "image/png"
    if suffix in [".jpg", ".jpeg"]:
        mime = "image/jpeg"
    b64 = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{b64}"

def save_upload(uploaded, target_dir: Path, preferred_stem: str | None = None) -> str:
    target_dir.mkdir(parents=True, exist_ok=True)
    ext = Path(uploaded.name).suffix.lower() or ".bin"
    stem = preferred_stem or Path(uploaded.name).stem
    name = f"{slugify(stem)}{ext}"
    path = target_dir / name
    path.write_bytes(uploaded.getbuffer())
    return str(path)

def remove_file(path_str: str) -> None:
    try:
        p = Path(path_str)
        if p.exists():
            p.unlink()
    except Exception:
        pass

def make_qr(data: str, fill_color: str = "#2F1E17", back_color: str = "#F7F2E9") -> Image.Image:
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    return img.convert("RGB")

def suggest_next_step(prompt: str, brand_name: str) -> str:
    text = prompt.lower()
    if "logo" in text:
        return f"Revisa la cabecera y el login de {brand_name} para validar proporciones de los dos logos."
    if "dominio" in text:
        return f"Configura DNS o usa el subdominio {slugify(brand_name)}.losparceritos.com."
    if "catalog" in text or "producto" in text:
        return "Sube el catálogo para convertirlo en carrusel de tienda montañera."
    if "public" in text:
        return "Ejecuta la validación final y revisa seguridad, pagos y responsive."
    return "Guarda avances, revisa la bitácora y ejecuta el siguiente bloque funcional."

def sync_to_supabase(brand_name: str, payload: dict[str, Any]) -> str:
    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_ANON_KEY", "").strip()
    table = os.getenv("SUPABASE_TABLE", "lp_sessions").strip()
    if not url or not key:
        return "Guardado local activo. Para Supabase real, define SUPABASE_URL y SUPABASE_ANON_KEY."
    record = {"brand_name": brand_name, "created_at": now(), "payload": payload}
    try:
        import urllib.request
        req = urllib.request.Request(
            f"{url}/rest/v1/{table}",
            data=json.dumps(record).encode("utf-8"),
            headers={"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json", "Prefer": "return=minimal"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=8)
        return "Guardado en Supabase completado."
    except Exception:
        return "No se pudo sincronizar con Supabase, pero el guardado local quedó intacto."

def tinto_response(prompt: str, brand_name: str, provider: str) -> str:
    cfg = get_project(brand_name)
    system = get_system()
    bullets = []
    if cfg.get("project_logo"):
        bullets.append("Ya existe logo del desarrollo cargado y listo para la cabecera.")
    else:
        bullets.append("Falta subir el logo del desarrollo para personalizar la web app.")
    if system.get("lp_logo"):
        bullets.append("El logo institucional de Los Parceritos está activo para header, consola CEO y login.")
    else:
        bullets.append("Falta cargar el logo institucional de Los Parceritos.")
    bullets.append(f"Proveedor activo de IA: {provider}.")
    bullets.append(f"Memoria persistente: última recomendación -> {suggest_next_step(prompt, brand_name)}")
    bullets.append("Autoguardado local listo y preparado para Supabase.")
    lines = [f"### {CHATBOT_NAME} responde", "", f"Entendí tu instrucción para **{brand_name}**.", ""]
    for b in bullets:
        lines.append(f"- {b}")
    lines += ["", "Acción sugerida ahora:", f"**{suggest_next_step(prompt, brand_name)}**"]
    return "\n".join(lines)

def init_session() -> None:
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_brand" not in st.session_state:
        st.session_state.current_brand = DEFAULT_PROJECT["brand_name"]
    if "provider" not in st.session_state:
        st.session_state.provider = "Gemini"
    if "permissions" not in st.session_state:
        st.session_state.permissions = {"camera": False, "speaker": False, "microphone": False, "gps": False}
    if "last_response" not in st.session_state:
        st.session_state.last_response = ""

def inject_css(system_cfg: dict[str, Any]) -> None:
    lp_logo = file_to_data_url(system_cfg.get("lp_logo", ""))
    opacity = float(system_cfg.get("lp_logo_opacity", 0.82))
    size = int(system_cfg.get("lp_logo_size", 64))
    login_logo = ""
    if system_cfg.get("show_lp_logo", True) and lp_logo:
        login_logo = f"""
        .login-card::after {{
            content: ""; position: absolute; width: {size}px; height: {size}px;
            top: 18px; right: 18px; background-image: url('{lp_logo}');
            background-size: contain; background-repeat: no-repeat;
            background-position: center; opacity: {opacity};
            animation: lpFloat 3.8s ease-in-out infinite; filter: drop-shadow(0 8px 18px rgba(0,0,0,0.08));
        }}
        """
    st.markdown(f"""
        <style>
        :root {{ --cafe:#2F1E17; --crema:#F7F2E9; --verde:#537A5A; --terracota:#C87B58; }}
        .stApp {{background: linear-gradient(180deg, #fcfaf7 0%, #f6f0e8 100%);}}
        .login-wrap {{display:flex; justify-content:center; align-items:center; min-height:100vh;}}
        .login-card {{
            position:relative; width: 100%; max-width: 520px; padding: 28px 28px 20px 28px;
            border-radius: 26px; background: rgba(255,255,255,0.78); backdrop-filter: blur(10px);
            box-shadow: 0 14px 40px rgba(47,30,23,0.10); border: 1px solid rgba(47,30,23,0.08);
        }}
        {login_logo}
        @keyframes lpFloat {{
            0% {{transform: translateY(0px); opacity: {opacity};}}
            50% {{transform: translateY(-4px); opacity: {max(0.20, opacity - 0.08)};}}
            100% {{transform: translateY(0px); opacity: {opacity};}}
        }}
        .header-card {{
            display:flex; align-items:center; justify-content:space-between; padding:16px 18px;
            border-radius:22px; background:rgba(255,255,255,0.78); box-shadow: 0 10px 30px rgba(47,30,23,0.08);
            margin-bottom: 14px; border:1px solid rgba(47,30,23,0.08);
        }}
        .brand-stack {{display:flex; align-items:center; gap:14px;}}
        .brand-logo {{width:64px; height:64px; object-fit:cover; border-radius:18px; background:#fff; border:1px solid rgba(47,30,23,0.06);}}
        .lp-logo {{width:48px; height:48px; object-fit:contain; opacity:{opacity}; filter: drop-shadow(0 6px 14px rgba(0,0,0,0.08));}}
        .mini-card {{padding:16px; border-radius:20px; background:rgba(255,255,255,0.82); border:1px solid rgba(47,30,23,0.08); box-shadow:0 8px 22px rgba(47,30,23,0.07);}}
        .kpi {{padding:16px; border-radius:18px; background:white; border:1px solid rgba(47,30,23,0.08); text-align:center;}}
        .tag-ok {{padding:6px 10px; border-radius:999px; background:#eff7ef; color:#2c6a34; font-size:12px; display:inline-block;}}
        .tag-soft {{padding:6px 10px; border-radius:999px; background:#f2ede7; color:#6b5146; font-size:12px; display:inline-block;}}
        .muted {{color:#6b6b6b; font-size:13px;}}
        </style>
        """, unsafe_allow_html=True)

def login_screen(system_cfg: dict[str, Any]) -> None:
    st.markdown('<div class="login-wrap"><div class="login-card">', unsafe_allow_html=True)
    st.markdown(f"## ☕ {APP_NAME}")
    st.caption("Panel CEO inspirado en cultura cafetera, minimalismo y memoria continua.")
    demo_cfg = get_project(st.session_state.current_brand)
    c1, c2 = st.columns([1, 4])
    with c1:
        if demo_cfg.get("project_logo") and Path(demo_cfg["project_logo"]).exists():
            st.image(demo_cfg["project_logo"], width=72)
        elif system_cfg.get("lp_logo") and Path(system_cfg["lp_logo"]).exists():
            st.image(system_cfg["lp_logo"], width=72)
    with c2:
        st.write("Acceso seguro a la consola del asistente CEO.")
    user = st.text_input("Usuario")
    pwd = st.text_input("Contraseña", type="password")
    if st.button("Ingresar", use_container_width=True):
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            st.session_state.logged_in = True
            st.rerun()
        st.error("Credenciales incorrectas.")
    st.markdown("</div></div>", unsafe_allow_html=True)

def render_header(brand_name: str, system_cfg: dict[str, Any], project_cfg: dict[str, Any]) -> None:
    project_logo = file_to_data_url(project_cfg.get("project_logo", ""))
    lp_logo = file_to_data_url(system_cfg.get("lp_logo", "")) if system_cfg.get("show_lp_logo", True) else ""
    project_logo_html = f"<img class='brand-logo' src='{project_logo}'/>" if project_logo else "<div class='brand-logo'></div>"
    lp_logo_html = f"<img class='lp-logo' src='{lp_logo}'/>" if lp_logo else ""
    st.markdown(f"""
        <div class="header-card">
            <div class="brand-stack">
                {project_logo_html}
                <div>
                    <div style="font-size:26px;font-weight:700;line-height:1.1;">{APP_NAME}</div>
                    <div style="font-size:14px;color:#5c514a;">{brand_name} · Orquestador digital</div>
                </div>
            </div>
            <div style="display:flex;align-items:center;gap:14px;">
                {lp_logo_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

def sidebar_nav(projects: list[dict[str, Any]]) -> str:
    st.sidebar.title("Navegación")
    names = [p.get("brand_name") for p in projects if p.get("brand_name")]
    if names:
        idx = names.index(st.session_state.current_brand) if st.session_state.current_brand in names else 0
        st.session_state.current_brand = st.sidebar.selectbox("Marca activa", names, index=idx)
    st.session_state.provider = st.sidebar.selectbox("Motor IA", ["Gemini", "Groq", "Ollama"])
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.rerun()
    return st.sidebar.radio("Ir a", ["Inicio", "Configurar Marca", "Consola IA", "Diseños y Marcas"])

def main() -> None:
    st.set_page_config(page_title=APP_NAME, page_icon="☕", layout="wide")
    ensure_dirs()
    init_session()
    system_cfg = get_system()
    inject_css(system_cfg)

    if not st.session_state.logged_in:
        login_screen(system_cfg)
        return

    projects = list_projects()
    if not projects:
        create_project_structure(DEFAULT_PROJECT["brand_name"])
        projects = list_projects()

    brand_name = st.session_state.current_brand
    if not project_dir(brand_name).exists():
        create_project_structure(brand_name)
    project_cfg = get_project(brand_name)

    render_header(brand_name, system_cfg, project_cfg)
    menu = sidebar_nav(projects)

    if menu == "Inicio":
        st.subheader("Inicio")
        st.write("Bienvenido a la Finca Digital.")
    elif menu == "Configurar Marca":
        st.subheader("Identidad")
        st.write("Configuración de estructura, logo y conocimientos.")
    elif menu == "Consola IA":
        st.subheader("Tinto AI")
        prompt = st.text_input("Orden a Tinto")
        if st.button("Enviar") and prompt:
            st.success(tinto_response(prompt, brand_name, st.session_state.provider))
    elif menu == "Diseños y Marcas":
        st.subheader("Fábrica de Web Apps")
        st.write(f"Marcas activas: {len(projects)}")

if __name__ == "__main__":
    main()
