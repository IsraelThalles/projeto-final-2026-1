import os
import requests
import json
from llm import ProvedorLLM
from esquemas import RespostaModeracao



class EstrategiaOllama(ProvedorLLM):
    def classificar_texto(self, texto: str, prompt_sistema: str) -> RespostaModeracao:
        url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        modelo = os.getenv("MODELO_LLM", "qwen3:4b")
        tempo_limite = float(os.getenv("TEMPO_LIMITE_INFERENCIA") or 5)

        if not url:
            raise ValueError("Configuração incorreta: A variável 'OLLAMA_URL' não foi encontrada no .env")
        
        if not modelo:
            raise ValueError("Configuração incorreta: A variável 'MODELO_LLM' não foi encontrada no .env")
        
        if tempo_limite <= 0:
            raise ValueError("Configuração incorreta: A variável 'TEMPO_LIMITE_INFERENCIA' deve ser um número positivo.")
        
        payload = {
            "model": modelo,
            "messages": [
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": f"Analise o seguinte comentário:\n\n{texto}"}
            ],
            "format": "json",
            "stream": False
        }
        
        resposta = requests.post(f"{url}/api/chat", json=payload, timeout=tempo_limite)
        resposta.raise_for_status()
        
        dados = resposta.json()
        conteudo = json.loads(dados["message"]["content"])
        
        return RespostaModeracao(**conteudo)