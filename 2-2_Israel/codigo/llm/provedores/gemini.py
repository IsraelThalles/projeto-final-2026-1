import os
import json
import google.generativeai as genai
from llm import ProvedorLLM
from esquemas import RespostaModeracao

class EstrategiaGemini(ProvedorLLM):
    def classificar_texto(self, texto: str, prompt_sistema: str) -> RespostaModeracao:
        chave_api = os.getenv("CHAVE_DA_API")

        if not chave_api:
            raise ValueError("Configuração incorreta: A variável 'CHAVE_DA_API' não foi encontrada no .env")
        
        modelo_configurado = os.getenv("MODELO_LLM", "gemini-2.5-flash")
        
        genai.configure(api_key=chave_api) # type: ignore
        modelo = genai.GenerativeModel(modelo_configurado, system_instruction=prompt_sistema) # type: ignore
        
        resposta = modelo.generate_content(
            texto,
            generation_config=genai.GenerationConfig( # type: ignore
                response_mime_type="application/json"
            )
        )
        
        conteudo = json.loads(resposta.text)
        return RespostaModeracao(**conteudo)