"""Testes E2E das rotas HTTP com agente e banco isolados por mocks."""

import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "codigo"))

from api import ControladorModeracao
from esquemas import Acao, ComentarioSaidaBanco, NivelDaOfensa, RespostaModeracao


def resposta_moderacao() -> RespostaModeracao:
    return RespostaModeracao(
        eh_ofensivo=False,
        nivel_da_ofensa=NivelDaOfensa.nenhuma,
        eh_discurso_de_odio=False,
        justificativa="Comentário sem termos ofensivos.",
        acao=Acao.aprovar,
        modelo_de_llm="modelo-mock",
        provedor_llm="mock",
    )


@pytest.fixture
def dependencias_api():
    agente = Mock()
    agente.moderar_comentario.return_value = resposta_moderacao()
    banco = Mock()
    banco.inserir_comentario.return_value = 1
    banco.listar_historico.return_value = []

    app = FastAPI()
    app.include_router(ControladorModeracao(agente, banco).obter_roteador())
    return TestClient(app), agente, banco


def test_post_moderar_retorna_contrato_esperado(dependencias_api):
    cliente, agente, banco = dependencias_api

    resposta = cliente.post("/moderar", json={"texto": "Muito obrigado pelo conteúdo."})

    assert resposta.status_code == 200
    assert resposta.json() == {
        "eh_ofensivo": False,
        "nivel_da_ofensa": "nenhuma",
        "eh_discurso_de_odio": False,
        "justificativa": "Comentário sem termos ofensivos.",
        "acao": "Aprovar",
        "modelo_de_llm": "modelo-mock",
        "provedor_llm": "mock",
    }
    agente.moderar_comentario.assert_called_once_with("Muito obrigado pelo conteúdo.")
    banco.inserir_comentario.assert_called_once()


@pytest.mark.parametrize("payload", [{"texto": ""}, {"texto": "   "}, {}, "não é um objeto"])
def test_post_moderar_rejeita_payload_invalido(dependencias_api, payload):
    cliente, agente, banco = dependencias_api

    resposta = cliente.post("/moderar", json=payload)

    assert resposta.status_code == 422
    agente.moderar_comentario.assert_not_called()
    banco.inserir_comentario.assert_not_called()


def test_get_historico_retorna_lista_no_contrato(dependencias_api):
    cliente, _, banco = dependencias_api
    banco.listar_historico.return_value = [
        ComentarioSaidaBanco(
            id=1,
            texto="Comentário analisado",
            eh_ofensivo=True,
            nivel_da_ofensa=NivelDaOfensa.levemente,
            eh_discurso_de_odio=False,
            justificativa="O comentário contém um insulto.",
            acao=Acao.sinalizar,
            modelo_de_llm="modelo-mock",
            provedor_llm="mock",
            criado_em=datetime(2026, 7, 13, 18, 25, 31),
        )
    ]

    resposta = cliente.get("/historico")

    assert resposta.status_code == 200
    assert resposta.json() == [
        {
            "id": 1,
            "texto": "Comentário analisado",
            "eh_ofensivo": True,
            "nivel_da_ofensa": "levemente",
            "eh_discurso_de_odio": False,
            "justificativa": "O comentário contém um insulto.",
            "acao": "Sinalizar",
            "modelo_de_llm": "modelo-mock",
            "provedor_llm": "mock",
            "criado_em": "2026-07-13T18:25:31",
        }
    ]
    banco.listar_historico.assert_called_once_with()
