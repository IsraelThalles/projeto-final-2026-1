"""Testes de integração do orquestrador de moderação com um LLM mockado."""

import sys
import time
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "codigo"))

from agente import AgenteClassificador
from esquemas import Acao, NivelDaOfensa, RespostaModeracao


def resposta(**sobrescritas) -> RespostaModeracao:
    dados = {
        "eh_ofensivo": False,
        "nivel_da_ofensa": NivelDaOfensa.nenhuma,
        "eh_discurso_de_odio": False,
        "justificativa": "Comentário sem termos ofensivos.",
        "acao": Acao.aprovar,
        "modelo_de_llm": "modelo-mock",
        "provedor_llm": "mock",
    }
    dados.update(sobrescritas)
    return RespostaModeracao(**dados)


@pytest.mark.parametrize(
    ("texto", "resposta_llm"),
    [
        (
            "Você é incompetente.",
            resposta(
                eh_ofensivo=True,
                nivel_da_ofensa=NivelDaOfensa.levemente,
                justificativa="O comentário contém um insulto.",
                acao=Acao.sinalizar,
            ),
        ),
        ("Obrigado pela explicação.", resposta()),
        (
            "Esse grupo não deveria existir.",
            resposta(
                eh_ofensivo=True,
                nivel_da_ofensa=NivelDaOfensa.altamente,
                eh_discurso_de_odio=True,
                justificativa="O comentário ataca um grupo protegido.",
                acao=Acao.bloquear,
            ),
        ),
    ],
)
def test_agente_retorna_resposta_moderacao_do_provedor(monkeypatch, texto, resposta_llm):
    monkeypatch.setenv("TEMPO_LIMITE_INFERENCIA", "1")
    provedor = Mock()
    provedor.classificar_texto.return_value = resposta_llm

    with patch(
        "agente.agente_classificador.FabricaProvedorLLM.obter_provedor",
        return_value=provedor,
    ):
        agente = AgenteClassificador()
        resultado = agente.moderar_comentario(texto)

    assert resultado == resposta_llm
    assert isinstance(resultado, RespostaModeracao)
    provedor.classificar_texto.assert_called_once_with(texto, agente._prompt_sistema)


def test_agente_aplica_fallback_quando_resposta_do_modelo_e_invalida(monkeypatch):
    monkeypatch.setenv("TEMPO_LIMITE_INFERENCIA", "1")
    provedor = Mock()
    provedor.classificar_texto.side_effect = ValueError("JSON de resposta inválido")

    with patch(
        "agente.agente_classificador.FabricaProvedorLLM.obter_provedor",
        return_value=provedor,
    ):
        resultado = AgenteClassificador().moderar_comentario("Texto de teste")

    assert resultado.acao is Acao.sinalizar
    assert resultado.eh_ofensivo is True
    assert "JSON de resposta inválido" in resultado.justificativa


def test_agente_aplica_fallback_em_erro_de_comunicacao(monkeypatch):
    monkeypatch.setenv("TEMPO_LIMITE_INFERENCIA", "1")
    provedor = Mock()
    provedor.classificar_texto.side_effect = ConnectionError("provedor indisponível")

    with patch(
        "agente.agente_classificador.FabricaProvedorLLM.obter_provedor",
        return_value=provedor,
    ):
        resultado = AgenteClassificador().moderar_comentario("Texto de teste")

    assert resultado.acao is Acao.sinalizar
    assert "Indisponibilidade técnica" in resultado.justificativa
    assert "provedor indisponível" in resultado.justificativa


def test_agente_aplica_fallback_quando_inferencia_excede_tempo_limite(monkeypatch):
    monkeypatch.setenv("TEMPO_LIMITE_INFERENCIA", "0.01")
    provedor = Mock()
    provedor.classificar_texto.side_effect = lambda *_: time.sleep(0.05)

    with patch(
        "agente.agente_classificador.FabricaProvedorLLM.obter_provedor",
        return_value=provedor,
    ):
        resultado = AgenteClassificador().moderar_comentario("Texto de teste")

    assert resultado.acao is Acao.sinalizar
    assert "tempo limite de 0.01 segundos excedido" in resultado.justificativa
