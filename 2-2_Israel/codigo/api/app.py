from fastapi import FastAPI
from api import ControladorModeracao
from agente import AgenteClassificador
from banco import GerenciadorBancoDados



class AgenteModeracaoAPI:
    def __init__(self):
        # 1. Instancia o app nativo
        self.app = FastAPI(
            title="API do Agente de Moderação",
            description="API REST orientada a objetos que expõe o agente de moderação para detectar toxicidade.",
            version="1.0.0",
        )
        
        # 2. Instancia as dependências (Injeção)
        self.agente = AgenteClassificador()
        self.banco = GerenciadorBancoDados()
        self.controlador = ControladorModeracao(self.agente, self.banco)
        
        # 3. Executa a configuração
        self._configurar_rotas()

    def _configurar_rotas(self):
        """Registra o roteador do controlador na aplicação principal."""
        self.app.include_router(self.controlador.obter_roteador())

        # Rota de healthcheck padrão
        @self.app.get("/", include_in_schema=False)
        def raiz():
            return {
                "status": "online",
                "mensagem": "Bem-vindo à API do Agente de Moderação! Acesse /docs para a documentação."
            }

    def obter_app(self) -> FastAPI:
        """Retorna a instância configurada do FastAPI."""
        return self.app


# Ponto de entrada exportado para o servidor ASGI (Uvicorn)
app = AgenteModeracaoAPI().obter_app()