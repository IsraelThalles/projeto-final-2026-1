import os
import json
from openai import OpenAI
from llm import ProvedorLLM
from esquemas import RespostaModeracao

class EstrategiaOpenAI(ProvedorLLM):
    def classificar_texto(self, texto: str, prompt_sistema: str) -> RespostaModeracao:
        chave_api = os.getenv("CHAVE_DA_API")

        if not chave_api:
            raise ValueError("Configuração incorreta: A variável 'CHAVE_DA_API' não foi encontrada no .env")
        
        modelo_configurado = os.getenv("MODELO_LLM", "gpt-4o-mini")
        
        cliente = OpenAI(api_key=chave_api)
        
        resposta = cliente.chat.completions.create(
            model=modelo_configurado,
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": texto}
            ],
            response_format={"type": "json_object"},
            timeout=4.5
        )
        
        texto_resposta = resposta.choices[0].message.content
        
        if not texto_resposta:
            raise ValueError("A API da OpenAI não retornou nenhum conteúdo de texto.")
            
        conteudo = json.loads(texto_resposta)
        return RespostaModeracao(**conteudo)