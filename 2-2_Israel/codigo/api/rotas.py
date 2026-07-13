from fastapi import APIRouter, HTTPException, status
from esquemas import ComentarioEntrada, RespostaModeracao
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agente import AgenteClassificador
    from banco import GerenciadorBancoDados



class ControladorModeracao:
    def __init__(self, agente: "AgenteClassificador", banco: "GerenciadorBancoDados"):
        self.agente = agente
        self.banco = banco
        self.roteador = APIRouter()
        
        # Mapeia o método da classe para a rota POST de forma nativa no FastAPI
        self.roteador.add_api_route(
            path="/moderar",
            endpoint=self.moderar,
            methods=["POST"],
            response_model=RespostaModeracao,
            status_code=status.HTTP_200_OK,
            summary="Classificar Comentário",
            description="Analisa um texto e retorna a classificação de toxicidade e discurso de ódio."
        )

    def moderar(self, comentario: ComentarioEntrada) -> RespostaModeracao:
        """
        Recebe o payload validado, repassa ao agente de IA e devolve a resposta.
        Definido de forma síncrona para que o FastAPI rode a requisição 
        em uma thread separada, evitando bloqueio do event loop.
        """
        try:
            # Chama o orquestrador exatamente com a assinatura especificada
            resposta_validada = self.agente.moderar_comentario(comentario.texto)

            self.banco.inserir_comentario(comentario.texto, resposta_validada)

            return resposta_validada
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Erro interno ao processar a moderação: {str(e)}"
            )

    def obter_roteador(self) -> APIRouter:
        """Retorna o roteador configurado."""
        return self.roteador