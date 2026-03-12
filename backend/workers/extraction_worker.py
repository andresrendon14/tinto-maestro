import io
from pypdf import PdfReader

class ExtractionWorker:
    @staticmethod
    def process_pdf(file_bytes, filename):
        # Leer el PDF directamente desde la memoria
        pdf_file = io.BytesIO(file_bytes)
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        return {
            "status": "success",
            "details": {
                "filename": filename,
                "pages_read": len(reader.pages),
                "total_chunks_generated": len(text) // 500
            }
        }
