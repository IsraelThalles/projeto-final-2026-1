from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class NivelDaOfensa(str, Enum):
    nenhuma = "nenhuma"
    levemente = "levemente"
    moderadamente = "moderadamente"
    altamente = "altamente"


class Acao(str, Enum):
    aprovar = "Aprovar"
    sinalizar = "Sinalizar"
    bloquear = "Bloquear"


class ComentarioEntrada(BaseModel):
    texto: str = Field(..., description="O texto do comentário a ser moderado")


class ResultadoModeracao(BaseModel):
    eh_ofensivo: bool = Field(..., description="Indica se o comentário é ofensivo")
    nivel_da_ofensa: NivelDaOfensa = Field(..., description="O nível da ofensa do comentário")
    eh_discurso_de_odio: bool = Field(..., description="Indica se o comentário contém discurso de ódio")
    confianca: float = Field(..., description="O nível de confiança da análise")
    justificativa: str = Field(..., description="A justificativa para a classificação")
    acao: Acao = Field(..., description="A ação recomendada para o comentário")
    modelo_de_llm: Optional[str] = Field(None, description="O modelo de LLM utilizado para a moderação")
    provedor_llm: Optional[str] = Field(None, description="O provedor do LLM utilizado para a moderação")


class ComentarioSaidaBanco(ResultadoModeracao):
    id: int = Field(..., description="O ID único do comentário no banco de dados")
    texto: str = Field(..., description="O texto original do comentário")
    criado_em: Optional[datetime] = Field(None, description="O timestamp de criação do registro")
