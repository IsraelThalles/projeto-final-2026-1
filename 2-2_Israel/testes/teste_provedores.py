"""Testes unitários dos provedores LLM com clientes externos mockados."""

import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "codigo"))

from esquemas import Acao, NivelDaOfensa
from llm.provedores import EstrategiaGemini, EstrategiaOllama, EstrategiaOpenAI


def resposta_json(**sobrescritas) -> str:
    dados = {
        "eh_ofensivo": False,
        "nivel_da_ofensa": "nenhuma",
        "eh_discurso_de_odio": False,
        "justificativa": "Comentário sem termos ofensivos.",
        "acao": "Aprovar",
    }
    dados.update(sobrescritas)
    return json.dumps(dados)


def test_openai_converte_resposta_json_sem_chamada_real(monkeypatch):
    monkeypatch.setenv("CHAVE_DA_API", "chave-de-teste")
    monkeypatch.setenv("TEMPO_LIMITE_INFERENCIA", "2")
    resposta_api = Mock()
    resposta_api.choices = [Mock(message=Mock(content=resposta_json()))]

    with patch("llm.provedores.openai.OpenAI") as classe_cliente:
        classe_cliente.return_value.chat.completions.create.return_value = resposta_api
        resultado = EstrategiaOpenAI().classificar_texto("Comentário", "Prompt")

    assert resultado.acao is Acao.aprovar
    assert resultado.nivel_da_ofensa is NivelDaOfensa.nenhuma
    classe_cliente.assert_called_once_with(api_key="chave-de-teste")


@pytest.mark.parametrize(
    ("chave", "tempo", "mensagem"),
    [(None, "1", "CHAVE_DA_API"), ("chave", "0", "TEMPO_LIMITE_INFERENCIA")],
)
def test_openai_rejeita_configuracao_invalida(monkeypatch, chave, tempo, mensagem):
    if chave is None:
        monkeypatch.delenv("CHAVE_DA_API", raising=False)
    else:
        monkeypatch.setenv("CHAVE_DA_API", chave)
    monkeypatch.setenv("TEMPO_LIMITE_INFERENCIA", tempo)

    with pytest.raises(ValueError, match=mensagem):
        EstrategiaOpenAI().classificar_texto("Comentário", "Prompt")


def test_openai_rejeita_resposta_vazia(monkeypatch):
    monkeypatch.setenv("CHAVE_DA_API", "chave-de-teste")
    resposta_api = Mock()
    resposta_api.choices = [Mock(message=Mock(content=None))]

    with patch("llm.provedores.openai.OpenAI") as classe_cliente:
        classe_cliente.return_value.chat.completions.create.return_value = resposta_api
        with pytest.raises(ValueError, match="nenhum conteúdo"):
            EstrategiaOpenAI().classificar_texto("Comentário", "Prompt")


def test_gemini_converte_resposta_json_sem_chamada_real(monkeypatch):
    monkeypatch.setenv("CHAVE_DA_API", "chave-de-teste")
    modelo = Mock()
    modelo.generate_content.return_value = Mock(text=resposta_json())

    with patch("llm.provedores.gemini.genai") as genai:
        genai.GenerativeModel.return_value = modelo
        resultado = EstrategiaGemini().classificar_texto("Comentário", "Prompt")

    assert resultado.acao is Acao.aprovar
    genai.configure.assert_called_once_with(api_key="chave-de-teste")
    modelo.generate_content.assert_called_once()


def test_gemini_rejeita_chave_ausente(monkeypatch):
    monkeypatch.delenv("CHAVE_DA_API", raising=False)

    with pytest.raises(ValueError, match="CHAVE_DA_API"):
        EstrategiaGemini().classificar_texto("Comentário", "Prompt")


def test_ollama_converte_resposta_json_sem_chamada_real(monkeypatch):
    monkeypatch.setenv("OLLAMA_URL", "http://ollama-teste")
    monkeypatch.setenv("MODELO_LLM", "modelo-teste")
    monkeypatch.setenv("TEMPO_LIMITE_INFERENCIA", "2")
    resposta_http = Mock()
    resposta_http.json.return_value = {"message": {"content": resposta_json()}}

    with patch("llm.provedores.ollama.requests.post", return_value=resposta_http) as post:
        resultado = EstrategiaOllama().classificar_texto("Comentário", "Prompt")

    assert resultado.acao is Acao.aprovar
    resposta_http.raise_for_status.assert_called_once_with()
    post.assert_called_once()


@pytest.mark.parametrize(
    ("variavel", "valor", "mensagem"),
    [
        ("OLLAMA_URL", "", "OLLAMA_URL"),
        ("MODELO_LLM", "", "MODELO_LLM"),
        ("TEMPO_LIMITE_INFERENCIA", "0", "TEMPO_LIMITE_INFERENCIA"),
    ],
)
def test_ollama_rejeita_configuracao_invalida(monkeypatch, variavel, valor, mensagem):
    monkeypatch.setenv("OLLAMA_URL", "http://ollama-teste")
    monkeypatch.setenv("MODELO_LLM", "modelo-teste")
    monkeypatch.setenv("TEMPO_LIMITE_INFERENCIA", "1")
    monkeypatch.setenv(variavel, valor)

    with pytest.raises(ValueError, match=mensagem):
        EstrategiaOllama().classificar_texto("Comentário", "Prompt")
