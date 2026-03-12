import os
import requests
from dotenv import load_dotenv

# Cargar las llaves secretas desde la bóveda (.env)
load_dotenv()

class OpenClawOrchestrator:
    """
    Motor principal de enrutamiento de agentes.
    Decide qué IA usar y formatea la petición según la API correspondiente.
    """
    
    @staticmethod
    def execute_task(prompt: str, cerebro: str = "Groq"):
        cerebro = cerebro.lower()
        
        try:
            if "groq" in cerebro:
                return OpenClawOrchestrator._call_groq(prompt)
            elif "gemini" in cerebro:
                return OpenClawOrchestrator._call_gemini(prompt)
            elif "mistral" in cerebro:
                return OpenClawOrchestrator._call_mistral(prompt)
            else:
                return {"status": "error", "message": f"Cerebro '{cerebro}' no implementado aún."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def _call_groq(prompt: str):
        # Groq es ultrarrápido, ideal para routing y tareas veloces
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key: return {"status": "error", "message": "Llave de Groq no encontrada."}
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3-8b-8192", # Modelo base rápido en Groq
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            return {"status": "success", "data": response.json()["choices"][0]["message"]["content"]}
        return {"status": "error", "message": response.text}

    @staticmethod
    def _call_gemini(prompt: str):
        # Gemini para estrategia y multimodalidad
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key: return {"status": "error", "message": "Llave de Gemini no encontrada."}
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return {"status": "success", "data": response.json()["candidates"][0]["content"]["parts"][0]["text"]}
        return {"status": "error", "message": response.text}
        
    @staticmethod
    def _call_mistral(prompt: str):
        # Mistral para extracción estructurada
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key: return {"status": "error", "message": "Llave de Mistral no encontrada."}
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "mistral-tiny",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            return {"status": "success", "data": response.json()["choices"][0]["message"]["content"]}
        return {"status": "error", "message": response.text}

