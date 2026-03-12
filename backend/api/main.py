from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Tinto Maestro Engine")

# Permitir que Streamlit hable con FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "engine": "Tinto Maestro Bionic"}

@app.post("/api/v1/projects/{project_id}/upload-pdf")
async def upload_pdf(project_id: str, file: UploadFile = File(...)):
    # Simulación de procesamiento
    content = await file.read()
    pages = len(content) // 3000  # Estimación burda de páginas
    return {
        "status": "success",
        "project_id": project_id,
        "details": {
            "filename": file.filename,
            "pages_read": max(1, pages),
            "total_chunks_generated": pages * 4
        }
    }
