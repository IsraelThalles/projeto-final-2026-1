import os
import requests
import json
from llm import ProvedorLLM
from esquemas import RespostaModeracao



class EstrategiaOllama(ProvedorLLM):
    def classificar_texto(self, texto: str, prompt_sistema: str) -> RespostaModeracao:
        url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        modelo = os.getenv("MODELO_LLM", "qwen3:4b")
        
        payload = {
            "model": modelo,
            "messages": [
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": f"Analise o seguinte comentário:\n\n{texto}"}
            ],
            "format": "json",
            "stream": False
        }
        
        resposta = requests.post(f"{url}/api/chat", json=payload, timeout=4.5)
        resposta.raise_for_status()
        
        dados = resposta.json()
        conteudo = json.loads(dados["message"]["content"])
        
        return RespostaModeracao(**conteudo)