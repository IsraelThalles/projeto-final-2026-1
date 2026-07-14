"""Testes unitários para a seleção de provedores LLM."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "codigo"))

from llm import FabricaProvedorLLM
from llm.provedores import EstrategiaGemini, EstrategiaOllama, EstrategiaOpenAI


@pytest.mark.parametrize(
    ("nome", "tipo_esperado"),
    [
        ("openai", EstrategiaOpenAI),
        ("gemini", EstrategiaGemini),
        ("ollama", EstrategiaOllama),
    ],
)
def test_obter_provedor_retorna_estrategia_configurada(monkeypatch, nome, tipo_esperado):
    monkeypatch.setenv("PROVEDOR_LLM", nome)

    assert isinstance(FabricaProvedorLLM.obter_provedor(), tipo_esperado)


@pytest.mark.parametrize("nome", ["desconhecido", "", " proved or "])
def test_obter_provedor_rejeita_configuracao_invalida(monkeypatch, nome):
    monkeypatch.setenv("PROVEDOR_LLM", nome)

    with pytest.raises(ValueError, match="desconhecido ou não especificado"):
        FabricaProvedorLLM.obter_provedor()


def test_obter_provedor_rejeita_configuracao_ausente(monkeypatch):
    monkeypatch.delenv("PROVEDOR_LLM", raising=False)

    with pytest.raises(ValueError, match="desconhecido ou não especificado"):
        FabricaProvedorLLM.obter_provedor()
