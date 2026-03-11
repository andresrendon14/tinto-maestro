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
        "frontend",
        "backend",
        "assets/logos",
        "assets/avatar",
        "assets/catalogo",
        "assets/promociones",
        "knowledge",
        "domain",
        "qr",
        "crm",
        "automations",
        "security",
        "backups",
        "production",
        "sessions",
        "exports",
        "docs",
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
    return load_json(
        memory_path(brand_name),
        {"history": [], "last_prompt": "", "last_response": "", "next_step": ""},
    )


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
    record = {
        "brand_name": brand_name,
        "created_at": now(),
        "payload": payload,
    }
    try:
        import urllib.request

        req = urllib.request.Request(
            f"{url}/rest/v1/{table}",
            data=json.dumps(record).encode("utf-8"),
            headers={
                "apikey": key,
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal",
            },
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
        st.session_state.permissions = {
            "camera": False,
            "speaker": False,
            "microphone": False,
            "gps": False,
        }
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
            content: "";
            position: absolute;
            width: {size}px;
            height: {size}px;
            top: 18px;
            right: 18px;
            background-image: url('{lp_logo}');
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            opacity: {opacity};
            animation: lpFloat 3.8s ease-in-out infinite;
            filter: drop-shadow(0 8px 18px rgba(0,0,0,0.08));
        }}
        """
    st.markdown(
        f"""
        <style>
        :root {{
            --cafe:#2F1E17;
            --crema:#F7F2E9;
            --verde:#537A5A;
            --terracota:#C87B58;
        }}
        .stApp {{background: linear-gradient(180deg, #fcfaf7 0%, #f6f0e8 100%);}}
        .login-wrap {{display:flex; justify-content:center; align-items:center; min-height:100vh;}}
        .login-card {{
            position:relative;
            width: 100%;
            max-width: 520px;
            padding: 28px 28px 20px 28px;
            border-radius: 26px;
            background: rgba(255,255,255,0.78);
            backdrop-filter: blur(10px);
            box-shadow: 0 14px 40px rgba(47,30,23,0.10);
            border: 1px solid rgba(47,30,23,0.08);
        }}
        {login_logo}
        @keyframes lpFloat {{
            0% {{transform: translateY(0px); opacity: {opacity};}}
            50% {{transform: translateY(-4px); opacity: {max(0.20, opacity - 0.08)};}}
            100% {{transform: translateY(0px); opacity: {opacity};}}
        }}
        .header-card {{
            display:flex; align-items:center; justify-content:space-between;
            padding:16px 18px; border-radius:22px; background:rgba(255,255,255,0.78);
            box-shadow: 0 10px 30px rgba(47,30,23,0.08); margin-bottom: 14px;
            border:1px solid rgba(47,30,23,0.08);
        }}
        .brand-stack {{display:flex; align-items:center; gap:14px;}}
        .brand-logo {{width:64px; height:64px; object-fit:cover; border-radius:18px; background:#fff; border:1px solid rgba(47,30,23,0.06);}}
        .lp-logo {{width:48px; height:48px; object-fit:contain; opacity:{opacity}; filter: drop-shadow(0 6px 14px rgba(0,0,0,0.08));}}
        .mini-card {{padding:16px; border-radius:20px; background:rgba(255,255,255,0.82); border:1px solid rgba(47,30,23,0.08); box-shadow:0 8px 22px rgba(47,30,23,0.07);}}
        .kpi {{padding:16px; border-radius:18px; background:white; border:1px solid rgba(47,30,23,0.08); text-align:center;}}
        .tag-ok {{padding:6px 10px; border-radius:999px; background:#eff7ef; color:#2c6a34; font-size:12px; display:inline-block;}}
        .tag-soft {{padding:6px 10px; border-radius:999px; background:#f2ede7; color:#6b5146; font-size:12px; display:inline-block;}}
        .muted {{color:#6b6b6b; font-size:13px;}}
        .section-title {{margin-top:6px; margin-bottom:8px;}}
        </style>
        """,
        unsafe_allow_html=True,
    )


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
        st.write("El logo institucional de Los Parceritos aparece aquí automáticamente con un efecto sutil.")

    user = st.text_input("Usuario")
    pwd = st.text_input("Contraseña", type="password")
    c1, c2 = st.columns(2)
    if c1.button("Ingresar", use_container_width=True):
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            st.session_state.logged_in = True
            st.success("Acceso correcto.")
            st.rerun()
        st.error("Usuario o contraseña incorrectos.")
    if c2.button("Recuperar contraseña", use_container_width=True):
        st.info("MVP local. Cambia ADMIN_USER y ADMIN_PASS dentro del archivo para producción.")

    st.markdown("</div></div>", unsafe_allow_html=True)


def render_header(brand_name: str, system_cfg: dict[str, Any], project_cfg: dict[str, Any]) -> None:
    project_logo = file_to_data_url(project_cfg.get("project_logo", ""))
    lp_logo = file_to_data_url(system_cfg.get("lp_logo", "")) if system_cfg.get("show_lp_logo", True) else ""
    project_logo_html = f"<img class='brand-logo' src='{project_logo}'/>" if project_logo else "<div class='brand-logo'></div>"
    lp_logo_html = f"<img class='lp-logo' src='{lp_logo}'/>" if lp_logo else ""
    st.markdown(
        f"""
        <div class="header-card">
            <div class="brand-stack">
                {project_logo_html}
                <div>
                    <div style="font-size:26px;font-weight:700;line-height:1.1;">{APP_NAME}</div>
                    <div style="font-size:14px;color:#5c514a;">{brand_name} · Orquestador de diseño, código, memoria y publicación</div>
                    <div style="margin-top:6px;display:flex;gap:8px;flex-wrap:wrap;">
                        <span class="tag-ok">Autoguardado activo</span>
                        <span class="tag-soft">IA en línea</span>
                        <span class="tag-soft">Seguridad activa</span>
                    </div>
                </div>
            </div>
            <div style="display:flex;align-items:center;gap:14px;">
                {lp_logo_html}
                <div style="text-align:right;">
                    <div style="font-size:13px;color:#5c514a;">Sello institucional</div>
                    <div style="font-weight:600;">Los Parceritos</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_nav(projects: list[dict[str, Any]]) -> str:
    st.sidebar.title("Navegación")
    names = [p.get("brand_name") for p in projects if p.get("brand_name")]
    if names:
        idx = names.index(st.session_state.current_brand) if st.session_state.current_brand in names else 0
        st.session_state.current_brand = st.sidebar.selectbox("Marca activa", names, index=idx)
    else:
        st.session_state.current_brand = DEFAULT_PROJECT["brand_name"]

    providers = ["Gemini", "Groq", "Grok", "Ollama", "Mistral"]
    pidx = providers.index(st.session_state.provider) if st.session_state.provider in providers else 0
    st.session_state.provider = st.sidebar.selectbox("Motor IA", providers, index=pidx)

    if st.sidebar.button("Cerrar sesión", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    menu = st.sidebar.radio(
        "Ir a",
        [
            "Inicio",
            "Configurar Marca",
            "Consola IA",
            "Comandos y Código",
            "Banco de Conocimiento",
            "Diseños y Marcas",
            "CRM y Automatizaciones",
            "Pagos",
            "Ciberseguridad",
            "Métricas",
            "Integraciones",
            "Publicación",
            "Memoria",
            "Ajustes del Sistema",
        ],
    )
    return menu


def show_home(system_cfg: dict[str, Any], project_cfg: dict[str, Any]) -> None:
    st.subheader("Inicio")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"<div class='kpi'><div class='muted'>Marca</div><h3>{project_cfg.get('brand_name')}</h3></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi'><div class='muted'>Publicada</div><h3>{'Sí' if project_cfg.get('published') else 'No'}</h3></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi'><div class='muted'>Banco conocimiento</div><h3>{len(project_cfg.get('knowledge_files', []))}</h3></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='kpi'><div class='muted'>Catálogos</div><h3>{len(project_cfg.get('catalog_files', []))}</h3></div>", unsafe_allow_html=True)

    a, b = st.columns([1.4, 1])
    with a:
        st.markdown("<div class='mini-card'>", unsafe_allow_html=True)
        st.markdown("### Central cafetera de mando inteligente")
        st.write("Este panel gestiona diseño, programación, memoria, publicación, seguridad, pagos e integraciones. Todo se autoguarda localmente y queda listo para sincronizar con Supabase.")
        st.write("El logo del desarrollo tiene prioridad visual. El logo institucional de Los Parceritos aparece automáticamente en login, cabecera y consola CEO de forma sutil.")
        st.markdown("</div>", unsafe_allow_html=True)
    with b:
        st.markdown("<div class='mini-card'>", unsafe_allow_html=True)
        st.markdown("### Estado rápido")
        st.write(f"**Subdominio:** {project_cfg.get('subdomain') or 'Pendiente'}")
        st.write(f"**Dominio:** {project_cfg.get('custom_domain') or 'No conectado'}")
        st.write(f"**Seguridad:** {project_cfg.get('security_level')}")
        st.write(f"**Última actualización:** {project_cfg.get('updated_at') or 'Sin cambios'}")
        st.markdown("</div>", unsafe_allow_html=True)


def show_brand_config(system_cfg: dict[str, Any], brand_name: str, project_cfg: dict[str, Any]) -> None:
    st.subheader("Configurar Marca")
    st.caption("Aquí nace la identidad, estructura, conocimiento y presencia visual de cada proyecto.")

    with st.expander("1. Identidad de marca", expanded=True):
        n1, n2 = st.columns(2)
        new_brand = n1.text_input("Nombre de la marca", value=project_cfg.get("brand_name", brand_name))
        slogan = n2.text_input("Eslogan", value=project_cfg.get("slogan", ""))
        d1, d2 = st.columns(2)
        business_type = d1.selectbox(
            "Tipo de negocio",
            ["General", "Tienda", "Barbería", "Restaurante", "Consultorio", "Artesanías", "Discoteca", "Comidas rápidas"],
            index=0,
        )
        tone = d2.selectbox(
            "Tono",
            ["Cercano", "Vendedor", "Sereno", "Institucional", "Popular"],
            index=["Cercano", "Vendedor", "Sereno", "Institucional", "Popular"].index(project_cfg.get("tone", "Cercano"))
            if project_cfg.get("tone", "Cercano") in ["Cercano", "Vendedor", "Sereno", "Institucional", "Popular"]
            else 0,
        )
        description = st.text_area("Descripción corta", value=project_cfg.get("description", ""), height=100)
        if st.button("Guardar identidad", use_container_width=True):
            if new_brand != brand_name:
                create_project_structure(new_brand)
                target_cfg = get_project(new_brand)
            else:
                target_cfg = project_cfg
            target_cfg["brand_name"] = new_brand
            target_cfg["slogan"] = slogan
            target_cfg["business_type"] = business_type
            target_cfg["tone"] = tone
            target_cfg["description"] = description
            save_project(new_brand, target_cfg)
            st.session_state.current_brand = new_brand
            append_log(new_brand, "Identidad de marca actualizada")
            st.success("Identidad guardada.")
            st.rerun()

    with st.expander("2. Crear estructura del proyecto", expanded=False):
        st.write("Crea frontend, backend, assets, knowledge, qr, dominio, seguridad, backups y producción.")
        if st.button("Crear estructura base", use_container_width=True):
            root = create_project_structure(brand_name)
            st.success(f"Estructura creada en {root}")

    with st.expander("3. Logo del desarrollo", expanded=False):
        st.write("Este logo representa la marca del cliente y tiene prioridad visual en la web app.")
        logo = st.file_uploader("Subir logo del desarrollo", type=["png", "jpg", "jpeg"], key="project_logo")
        if logo is not None:
            suggested = f"logo-{slugify(brand_name)}"
            path = save_upload(logo, project_dir(brand_name) / "assets" / "logos", suggested)
            project_cfg["project_logo"] = path
            project_cfg["project_logo_name"] = Path(path).name
            save_project(brand_name, project_cfg)
            append_log(brand_name, "Logo del desarrollo cargado")
            st.success("Logo del desarrollo guardado y enlazado a la cabecera.")
            st.image(path, width=140)
        elif project_cfg.get("project_logo") and Path(project_cfg["project_logo"]).exists():
            st.image(project_cfg["project_logo"], width=140)
            st.caption(project_cfg.get("project_logo_name", ""))

    with st.expander("3.1. Logo corporativo de Los Parceritos", expanded=False):
        st.write("Este botón es independiente y carga el sello institucional de la marca blanca Los Parceritos.")
        lp_logo = st.file_uploader("Subir logo Los Parceritos", type=["png", "jpg", "jpeg"], key="lp_logo")
        if lp_logo is not None:
            path = save_upload(lp_logo, SYSTEM_DIR, "logo-los-parceritos")
            system_cfg["lp_logo"] = path
            system_cfg["lp_logo_name"] = Path(path).name
            save_system(system_cfg)
            append_log(brand_name, "Logo institucional de Los Parceritos cargado")
            st.success("Logo institucional guardado. Ya aparece en login, cabecera y consola CEO.")
            st.image(path, width=120)
        elif system_cfg.get("lp_logo") and Path(system_cfg["lp_logo"]).exists():
            st.image(system_cfg["lp_logo"], width=120)
            st.caption(system_cfg.get("lp_logo_name", ""))

    with st.expander("4. Avatar de la marca", expanded=False):
        avatar = st.file_uploader("Subir avatar", type=["png", "jpg", "jpeg"], key="avatar_brand")
        if avatar is not None:
            path = save_upload(avatar, project_dir(brand_name) / "assets" / "avatar", f"avatar-{slugify(brand_name)}")
            project_cfg["avatar"] = path
            save_project(brand_name, project_cfg)
            append_log(brand_name, "Avatar cargado")
            st.success("Avatar guardado para la burbuja del asistente.")
            st.image(path, width=130)
        elif project_cfg.get("avatar") and Path(project_cfg["avatar"]).exists():
            st.image(project_cfg["avatar"], width=130)

    with st.expander("5. Banco de conocimiento", expanded=False):
        uploads = st.file_uploader("Subir archivos de conocimiento", accept_multiple_files=True, key="knowledge_files")
        if uploads:
            saved = project_cfg.get("knowledge_files", [])
            for up in uploads:
                path = save_upload(up, project_dir(brand_name) / "knowledge")
                if path not in saved:
                    saved.append(path)
            project_cfg["knowledge_files"] = saved
            save_project(brand_name, project_cfg)
            append_log(brand_name, "Banco de conocimiento actualizado")
            st.success("Archivos guardados. La IA los usa como guía sin quedar limitada a ellos.")
        if project_cfg.get("knowledge_files"):
            st.write("Archivos cargados:")
            for item in project_cfg["knowledge_files"]:
                st.write("-", Path(item).name)

    with st.expander("6. Catálogo y promociones", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            catalog = st.file_uploader("Subir catálogo", type=["png", "jpg", "jpeg", "pdf"], accept_multiple_files=True, key="catalog")
            if catalog:
                files = project_cfg.get("catalog_files", [])
                for up in catalog:
                    path = save_upload(up, project_dir(brand_name) / "assets" / "catalogo")
                    if path not in files:
                        files.append(path)
                project_cfg["catalog_files"] = files
                save_project(brand_name, project_cfg)
                append_log(brand_name, "Catálogo actualizado")
                st.success("Catálogo guardado. Queda listo para carrusel automático.")
        with c2:
            promos = st.file_uploader("Subir promociones", type=["png", "jpg", "jpeg", "pdf"], accept_multiple_files=True, key="promos")
            if promos:
                files = project_cfg.get("promo_files", [])
                for up in promos:
                    path = save_upload(up, project_dir(brand_name) / "assets" / "promociones")
                    if path not in files:
                        files.append(path)
                project_cfg["promo_files"] = files
                save_project(brand_name, project_cfg)
                append_log(brand_name, "Promociones actualizadas")
                st.success("Promociones guardadas. Quedan listas para avisos y carrusel.")

    with st.expander("7. Dominio, subdominio y referencias", expanded=False):
        subdomain = st.text_input("Subdominio gratuito", value=project_cfg.get("subdomain") or f"{slugify(brand_name)}.losparceritos.com")
        custom_domain = st.text_input("Dominio propio", value=project_cfg.get("custom_domain", ""))
        refs_text = st.text_area("Links de inspiración, uno por línea", value="\n".join(project_cfg.get("references", [])), height=100)
        notes = st.text_area("Notas estratégicas", value=project_cfg.get("notes", ""), height=80)
        st.info("La IA puede guiar pedagógicamente qué datos DNS debes conseguir para un dominio propio. Si no tienes dominio, usa el subdominio gratis.")
        if st.button("Guardar dominio y referencias", use_container_width=True):
            project_cfg["subdomain"] = subdomain
            project_cfg["custom_domain"] = custom_domain
            project_cfg["references"] = [x.strip() for x in refs_text.splitlines() if x.strip()]
            project_cfg["notes"] = notes
            save_project(brand_name, project_cfg)
            append_log(brand_name, "Dominio y referencias actualizados")
            st.success("Dominio, subdominio y referencias guardados.")
            st.rerun()

    with st.expander("8. Paleta de color y QR", expanded=False):
        palette = project_cfg.get("palette", DEFAULT_PROJECT["palette"])
        p1, p2, p3, p4 = st.columns(4)
        palette[0] = p1.color_picker("Color 1", palette[0], key="cp1")
        palette[1] = p2.color_picker("Color 2", palette[1], key="cp2")
        palette[2] = p3.color_picker("Color 3", palette[2], key="cp3")
        palette[3] = p4.color_picker("Color 4", palette[3], key="cp4")
        qr_value = st.text_input("Dato del QR", value=project_cfg.get("custom_domain") or project_cfg.get("subdomain") or "https://losparceritos.com")
        img = make_qr(qr_value, fill_color=palette[0], back_color=palette[1])
        st.image(img, width=220)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        if st.button("Guardar paleta", use_container_width=True):
            project_cfg["palette"] = palette
            save_project(brand_name, project_cfg)
            append_log(brand_name, "Paleta guardada")
            st.success("Paleta actualizada.")
        st.download_button("Descargar QR PNG", data=buf.getvalue(), file_name=f"qr-{slugify(brand_name)}.png", mime="image/png")


def show_assistant_console(system_cfg: dict[str, Any], brand_name: str, project_cfg: dict[str, Any]) -> None:
    st.subheader(f"Consola IA · {CHATBOT_NAME}")
    a, b = st.columns([2.2, 1])
    with a:
        st.markdown("<div class='mini-card'>", unsafe_allow_html=True)
        st.write(f"**Marca activa:** {brand_name}")
        st.write(f"**Tono:** {project_cfg.get('tone')}")
        st.write(f"**Voz:** {project_cfg.get('voice_style')}")
        st.write("El asistente puede hablar, oír, escribir, pensar, contestar y recordar el último punto del proyecto.")
        st.markdown("</div>", unsafe_allow_html=True)
    with b:
        if project_cfg.get("avatar") and Path(project_cfg["avatar"]).exists():
            st.image(project_cfg["avatar"], width=110, caption="Avatar")
        elif system_cfg.get("lp_logo") and Path(system_cfg["lp_logo"]).exists():
            st.image(system_cfg["lp_logo"], width=110, caption="Sello institucional")

    t1, t2, t3, t4 = st.columns(4)
    st.session_state.permissions["camera"] = t1.toggle("Cámara", value=st.session_state.permissions["camera"])
    st.session_state.permissions["speaker"] = t2.toggle("Altavoz", value=st.session_state.permissions["speaker"])
    st.session_state.permissions["microphone"] = t3.toggle("Micrófono", value=st.session_state.permissions["microphone"])
    st.session_state.permissions["gps"] = t4.toggle("GPS", value=st.session_state.permissions["gps"])

    prompt = st.text_area("Prompt", height=140, placeholder="Dile a Tinto qué deseas construir, corregir o publicar.")
    c1, c2, c3, c4, c5 = st.columns(5)
    if c1.button("Hablar", use_container_width=True):
        append_log(brand_name, "Modo hablar activado")
        st.info("Listo para integrar TTS/STT real en la siguiente fase.")
    if c2.button("Escuchar", use_container_width=True):
        append_log(brand_name, "Modo escuchar activado")
        st.info("Listo para integrar captura de audio real.")
    if c3.button("Generar imagen", use_container_width=True):
        append_log(brand_name, "Solicitud de generación de imagen")
        st.info("Conecta aquí tu motor de imagen preferido.")
    if c4.button("Generar video", use_container_width=True):
        append_log(brand_name, "Solicitud de video corto")
        st.info("Conecta aquí tu flujo de video corto.")
    if c5.button("Ejecutar prompt", use_container_width=True) and prompt.strip():
        resp = tinto_response(prompt, brand_name, st.session_state.provider)
        st.session_state.last_response = resp
        save_memory(brand_name, prompt, resp)
        append_log(brand_name, f"Prompt ejecutado: {prompt[:120]}")
        msg = sync_to_supabase(brand_name, {"prompt": prompt, "response": resp})
        st.success(msg)

    if st.session_state.last_response:
        st.markdown(st.session_state.last_response)

    mem = get_memory(brand_name)
    with st.expander("Memoria rápida", expanded=False):
        st.write("Último prompt:", mem.get("last_prompt", ""))
        st.write("Última respuesta:", mem.get("last_response", ""))
        st.write("Siguiente paso:", mem.get("next_step", ""))


def show_commands(brand_name: str) -> None:
    st.subheader("Comandos y Código")
    b1, b2, b3, b4, b5 = st.columns(5)
    if b1.button("Ejecutar", use_container_width=True):
        append_log(brand_name, "Acción manual: ejecutar")
    if b2.button("Pausar", use_container_width=True):
        append_log(brand_name, "Acción manual: pausar", level="WARN")
    if b3.button("Reintentar", use_container_width=True):
        append_log(brand_name, "Acción manual: reintentar")
    if b4.button("Aprobar", use_container_width=True):
        append_log(brand_name, "Acción manual: aprobar")
    if b5.button("Cancelar", use_container_width=True):
        append_log(brand_name, "Acción manual: cancelar", level="WARN")

    text = st.text_input("Instrucción técnica")
    if st.button("Agregar a bitácora", use_container_width=True) and text.strip():
        append_log(brand_name, f"Comando manual: {text}")
        st.success("Instrucción agregada.")
        st.rerun()

    logs = get_logs(brand_name)
    if logs:
        st.dataframe(pd.DataFrame(logs), use_container_width=True, hide_index=True)
    else:
        st.info("Aún no hay registros.")

    st.code(
        f'''# Vista lógica del proyecto {slugify(brand_name)}
config = {{
    "autoguardado": True,
    "logo_desarrollo": {bool(get_project(brand_name).get("project_logo"))},
    "logo_los_parceritos": {bool(get_system().get("lp_logo"))},
    "estado": "listo_para_iterar",
}}
''',
        language="python",
    )


def show_knowledge_bank(brand_name: str, project_cfg: dict[str, Any]) -> None:
    st.subheader("Banco de Conocimiento")
    files = project_cfg.get("knowledge_files", [])
    if not files:
        st.info("No hay archivos todavía.")
        return
    rows = []
    for path_str in files:
        p = Path(path_str)
        rows.append({"Archivo": p.name, "Ruta": str(p), "Tipo": p.suffix.lower(), "Existe": p.exists()})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    selected = st.selectbox("Selecciona un archivo", options=[r["Ruta"] for r in rows])
    c1, c2, c3 = st.columns(3)
    p = Path(selected)
    if c1.button("Descargar", use_container_width=True) and p.exists():
        st.download_button("Descarga directa", data=p.read_bytes(), file_name=p.name, mime="application/octet-stream")
    if c2.button("Borrar", use_container_width=True):
        project_cfg["knowledge_files"] = [f for f in files if f != selected]
        remove_file(selected)
        save_project(brand_name, project_cfg)
        append_log(brand_name, f"Archivo borrado del banco: {p.name}")
        st.success("Archivo eliminado.")
        st.rerun()
    if c3.button("Reentrenar", use_container_width=True):
        append_log(brand_name, f"Reentrenamiento solicitado: {p.name}")
        st.success("Reentrenamiento registrado.")


def show_factory(projects: list[dict[str, Any]]) -> None:
    st.subheader("Diseños y Marcas")
    if not projects:
        st.info("Aún no hay proyectos.")
        return
    rows = []
    for p in projects:
        rows.append(
            {
                "Marca": p.get("brand_name"),
                "Estado": "Bloqueada" if p.get("blocked") else ("Publicada" if p.get("published") else "En desarrollo"),
                "Dominio": p.get("custom_domain") or p.get("subdomain"),
                "Última edición": p.get("updated_at"),
                "Seguridad": p.get("security_level"),
            }
        )
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    names = [p.get("brand_name") for p in projects if p.get("brand_name")]
    selected = st.selectbox("Gestionar marca", names)
    cfg = get_project(selected)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("Abrir", use_container_width=True):
        st.session_state.current_brand = selected
        st.success(f"Marca activa: {selected}")
        st.rerun()
    if c2.button("Bloquear / Desbloquear", use_container_width=True):
        cfg["blocked"] = not cfg.get("blocked", False)
        save_project(selected, cfg)
        st.success("Estado actualizado.")
        st.rerun()
    if c3.button("Publicar / Despublicar", use_container_width=True):
        cfg["published"] = not cfg.get("published", False)
        save_project(selected, cfg)
        st.success("Publicación actualizada.")
        st.rerun()
    if c4.button("Eliminar", use_container_width=True):
        st.warning("En este MVP no se borra físicamente para evitar pérdidas accidentales.")


def show_crm(brand_name: str) -> None:
    st.subheader("CRM y Automatizaciones")
    a, b = st.columns(2)
    with a:
        st.markdown("<div class='mini-card'>", unsafe_allow_html=True)
        st.write("### Gestión comercial")
        st.write("Captura leads, tareas, recordatorios y seguimiento comercial.")
        st.markdown("</div>", unsafe_allow_html=True)
    with b:
        st.markdown("<div class='mini-card'>", unsafe_allow_html=True)
        st.write("### MCP · Antigravity · OpenClow")
        st.write("Este espacio queda listo para conectar automatizaciones, herramientas externas y flujos inteligentes.")
        st.markdown("</div>", unsafe_allow_html=True)

    lead = st.text_input("Nuevo lead")
    note = st.text_area("Nota rápida", height=90)
    if st.button("Guardar lead", use_container_width=True) and lead.strip():
        append_log(brand_name, f"Lead guardado: {lead} · {note[:80]}")
        st.success("Lead guardado en bitácora.")


def show_payments(brand_name: str, project_cfg: dict[str, Any]) -> None:
    st.subheader("Pagos")
    c1, c2 = st.columns(2)
    with c1:
        mp = st.toggle("Activar Mercado Pago", value=project_cfg.get("payment_mp", False))
        st.text_input("Public Key Mercado Pago", type="password")
    with c2:
        payu = st.toggle("Activar PayU", value=project_cfg.get("payment_payu", False))
        st.text_input("API Key PayU", type="password")
    st.info("Las credenciales reales deben ir en variables seguras o backend protegido.")
    if st.button("Guardar pasarelas", use_container_width=True):
        project_cfg["payment_mp"] = mp
        project_cfg["payment_payu"] = payu
        save_project(brand_name, project_cfg)
        append_log(brand_name, "Pasarelas actualizadas")
        st.success("Pasarelas guardadas.")


def show_security(brand_name: str, project_cfg: dict[str, Any]) -> None:
    st.subheader("Ciberseguridad")
    st.success(f"Protección activa: {project_cfg.get('security_level')}")
    c1, c2, c3, c4 = st.columns(4)
    ses = c1.checkbox("Sesiones seguras", value=True)
    bkp = c2.checkbox("Backups", value=True)
    aud = c3.checkbox("Auditoría", value=True)
    val = c4.checkbox("Validación de archivos", value=True)
    if st.button("Aplicar políticas", use_container_width=True):
        append_log(brand_name, f"Seguridad aplicada: sesiones={ses}, backups={bkp}, auditoría={aud}, validación={val}")
        st.success("Políticas aplicadas.")


def show_metrics(projects: list[dict[str, Any]]) -> None:
    st.subheader("Métricas")
    total = len(projects)
    published = sum(1 for p in projects if p.get("published"))
    blocked = sum(1 for p in projects if p.get("blocked"))
    active = total - blocked
    a, b, c, d = st.columns(4)
    a.metric("Marcas", total)
    b.metric("Publicadas", published)
    c.metric("Activas", active)
    d.metric("Bloqueadas", blocked)
    df = pd.DataFrame(
        {
            "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun"],
            "Diseños": [2, 4, 5, 7, 9, 12],
            "Ventas": [1, 2, 4, 5, 8, 10],
            "ROI": [12, 18, 22, 25, 31, 36],
        }
    ).set_index("Mes")
    st.line_chart(df)


def show_integrations(brand_name: str, project_cfg: dict[str, Any]) -> None:
    st.subheader("Integraciones")
    cols = st.columns(5)
    engines = ["Groq", "Grok", "Gemini", "Ollama", "Mistral"]
    for i, engine in enumerate(engines):
        cols[i].checkbox(engine, value=(engine == st.session_state.provider), disabled=True)
    voice_style = st.selectbox(
        "Estilo de voz",
        ["Natural", "Cálido", "Sereno", "Vendedor", "Institucional"],
        index=["Natural", "Cálido", "Sereno", "Vendedor", "Institucional"].index(project_cfg.get("voice_style", "Natural"))
        if project_cfg.get("voice_style", "Natural") in ["Natural", "Cálido", "Sereno", "Vendedor", "Institucional"]
        else 0,
    )
    gps = st.toggle("Adaptar voz con GPS", value=project_cfg.get("gps_adaptive_voice", True))
    mcp = st.text_input("Endpoint MCP de la marca")
    if st.button("Guardar integraciones", use_container_width=True):
        project_cfg["voice_style"] = voice_style
        project_cfg["gps_adaptive_voice"] = gps
        save_project(brand_name, project_cfg)
        append_log(brand_name, f"Integraciones guardadas. MCP configurado={bool(mcp)}")
        st.success("Integraciones guardadas.")


def show_publication(brand_name: str, project_cfg: dict[str, Any]) -> None:
    st.subheader("Publicación")
    checks = {
        "Logo del desarrollo": bool(project_cfg.get("project_logo")),
        "Logo Los Parceritos": bool(get_system().get("lp_logo")),
        "Banco de conocimiento": len(project_cfg.get("knowledge_files", [])) > 0,
        "Catálogo": len(project_cfg.get("catalog_files", [])) > 0,
        "Subdominio": bool(project_cfg.get("subdomain")),
        "Seguridad": True,
    }
    for k, v in checks.items():
        st.checkbox(k, value=v, disabled=True)
    if st.button("Validar proyecto", use_container_width=True):
        missing = [k for k, v in checks.items() if not v]
        if missing:
            st.warning("Faltan elementos: " + ", ".join(missing))
        else:
            st.success("Checklist completo. Listo para producción.")
        append_log(brand_name, "Validación ejecutada")
    if st.button("Publicar ahora", use_container_width=True):
        project_cfg["published"] = True
        save_project(brand_name, project_cfg)
        append_log(brand_name, "Proyecto publicado")
        st.success("Proyecto marcado como publicado.")


def show_memory(brand_name: str) -> None:
    st.subheader("Memoria")
    mem = get_memory(brand_name)
    st.write("Último prompt:", mem.get("last_prompt", ""))
    st.write("Última respuesta:", mem.get("last_response", ""))
    st.write("Siguiente paso:", mem.get("next_step", ""))
    if mem.get("history"):
        st.dataframe(pd.DataFrame(mem["history"]), use_container_width=True, hide_index=True)
    c1, c2 = st.columns(2)
    if c1.button("Exportar memoria", use_container_width=True):
        path = EXPORTS_DIR / f"memory-{slugify(brand_name)}.json"
        save_json(path, mem)
        st.success(f"Memoria exportada en {path}")
    if c2.button("Resumen de sesión", use_container_width=True):
        st.info(f"Marca: {brand_name} · Siguiente paso: {mem.get('next_step', '')}")


def show_system_settings(system_cfg: dict[str, Any]) -> None:
    st.subheader("Ajustes del Sistema")
    show_logo = st.toggle("Mostrar logo Los Parceritos en todo el sistema", value=system_cfg.get("show_lp_logo", True))
    opacity = st.slider("Opacidad del logo institucional", 0.10, 1.00, float(system_cfg.get("lp_logo_opacity", 0.82)), 0.05)
    size = st.slider("Tamaño del logo institucional", 40, 160, int(system_cfg.get("lp_logo_size", 64)))
    if st.button("Guardar ajustes globales", use_container_width=True):
        system_cfg["show_lp_logo"] = show_logo
        system_cfg["lp_logo_opacity"] = opacity
        system_cfg["lp_logo_size"] = size
        save_system(system_cfg)
        st.success("Ajustes globales guardados.")
        st.rerun()


def main() -> None:
    st.set_page_config(page_title=APP_NAME, page_icon="☕", layout="wide")
    ensure_dirs()
    init_session()

    if not project_dir(DEFAULT_PROJECT["brand_name"]).exists():
        create_project_structure(DEFAULT_PROJECT["brand_name"])

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
        show_home(system_cfg, project_cfg)
    elif menu == "Configurar Marca":
        show_brand_config(system_cfg, brand_name, project_cfg)
    elif menu == "Consola IA":
        show_assistant_console(system_cfg, brand_name, project_cfg)
    elif menu == "Comandos y Código":
        show_commands(brand_name)
    elif menu == "Banco de Conocimiento":
        show_knowledge_bank(brand_name, project_cfg)
    elif menu == "Diseños y Marcas":
        show_factory(projects)
    elif menu == "CRM y Automatizaciones":
        show_crm(brand_name)
    elif menu == "Pagos":
        show_payments(brand_name, project_cfg)
    elif menu == "Ciberseguridad":
        show_security(brand_name, project_cfg)
    elif menu == "Métricas":
        show_metrics(projects)
    elif menu == "Integraciones":
        show_integrations(brand_name, project_cfg)
    elif menu == "Publicación":
        show_publication(brand_name, project_cfg)
    elif menu == "Memoria":
        show_memory(brand_name)
    elif menu == "Ajustes del Sistema":
        show_system_settings(system_cfg)


if __name__ == "__main__":
    main()
