from fastapi import APIRouter, HTTPException, status
from esquemas import ComentarioEntrada, RespostaModeracao, ComentarioSaidaBanco
from typing import TYPE_CHECKING, Literal
from collections.abc import Callable

if TYPE_CHECKING:
    from agente import AgenteClassificador
    from banco import GerenciadorBancoDados



class ControladorModeracao:
    """Controlador responsável por expor as rotas da API de moderação, delegando a lógica para o agente e o banco de dados."""
    
    def __init__(self, agente: "AgenteClassificador", banco: "GerenciadorBancoDados"):
        self.agente = agente
        self.banco = banco
        self.roteador = APIRouter()
        
        # Mapeia o método da classe para a rota POST de forma nativa no FastAPI
        self._adicionar_rotas("/moderar", self.moderar, "POST", RespostaModeracao, "Classificar Comentário", "Analisa um texto e retorna a classificação de toxicidade e discurso de ódio.")

        self._adicionar_rotas("/historico", self.listar_historico, "GET", list[ComentarioSaidaBanco], "Histórico de Moderação", "Retorna os comentários analisados, ordenados do mais recente para o mais antigo.")



    def _adicionar_rotas(self, caminho: str, endpoint: Callable[..., object], metodo: Literal["GET", "POST"], modelo_de_resposta, sumario: str, descricao: str):
        """Método auxiliar para adicionar rotas ao APIRouter."""
        self.roteador.add_api_route(
            path=caminho,
            endpoint=endpoint,
            methods=[metodo],
            response_model=modelo_de_resposta,
            status_code=status.HTTP_200_OK,
            summary=sumario,
            description=descricao
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



    def listar_historico(self) -> list[ComentarioSaidaBanco]:
        """
        Retorna o histórico de comentários analisados.
        """
        try:
            return self.banco.listar_historico()

        except Exception as erro:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno ao consultar o histórico: {erro}",
            )



    def obter_roteador(self) -> APIRouter:
        """Retorna o roteador configurado."""
        return self.roteador