from abc import ABC, abstractmethod
from esquemas import RespostaModeracao



class ProvedorLLM(ABC):
    """Interface abstrata para integração com diferentes provedores de IA."""
    
    @abstractmethod
    def classificar_texto(self, texto: str, prompt_sistema: str) -> RespostaModeracao:
        """
        Recebe o texto do usuário e o prompt do sistema.
        Deve retornar uma instância do esquema RespostaModeracao.
        """
        pass