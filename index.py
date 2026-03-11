import os
import sys
from streamlit.web.cli import main

if __name__ == "__main__":
    # Forzamos a Streamlit a correr en el puerto que Vercel asigne
    sys.argv = [
        "streamlit",
        "run",
        "app.py",
        "--server.port",
        os.getenv("PORT", "8080"),
        "--server.address",
        "0.0.0.0",
        "--server.headless",
        "true"
    ]
    sys.exit(main())
