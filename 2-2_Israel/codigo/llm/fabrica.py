import os
from cliente import ProvedorLLM
from provedores import EstrategiaOllama, EstrategiaGemini, EstrategiaOpenAI



class FabricaProvedorLLM:
    """Fábrica responsável estritamente por selecionar e instanciar o provedor."""
    
    @staticmethod
    def obter_provedor() -> ProvedorLLM:
        provedor = os.getenv("PROVEDOR_LLM", "desconhecido").lower()
        
        if provedor == "openai":
            return EstrategiaOpenAI()
        elif provedor == "gemini":
            return EstrategiaGemini()
        elif provedor == "ollama":
            return EstrategiaOllama()
        else:
            raise ValueError(f"Provedor LLM desconhecido ou não especificado: {provedor}")