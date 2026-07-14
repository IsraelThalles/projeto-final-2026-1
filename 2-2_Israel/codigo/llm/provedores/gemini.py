import os
import json
from google import genai
from google.genai import types
from llm import ProvedorLLM
from esquemas import RespostaModeracao

class EstrategiaGemini(ProvedorLLM):
    def classificar_texto(self, texto: str, prompt_sistema: str) -> RespostaModeracao:
        chave_api = os.getenv("CHAVE_DA_API")

        if not chave_api:
            raise ValueError("Configuração incorreta: A variável 'CHAVE_DA_API' não foi encontrada no .env")
        
        modelo_configurado = os.getenv("MODELO_LLM", "gemini-2.5-flash")
        
        cliente = genai.Client(api_key=chave_api)

        resposta = cliente.models.generate_content(
            model=modelo_configurado,
            contents=texto,
            config=types.GenerateContentConfig(
                system_instruction=prompt_sistema,
                response_mime_type="application/json",
            ),
        )

        if resposta.text is None:
            raise RuntimeError("O Gemini não retornou conteúdo textual.")

        conteudo = json.loads(resposta.text)
        return RespostaModeracao(**conteudo)
