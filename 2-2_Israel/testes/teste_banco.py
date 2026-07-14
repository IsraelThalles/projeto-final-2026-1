"""Testes de integração do repositório SQLite em banco temporário."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "codigo"))

from banco import GerenciadorBancoDados
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


@pytest.fixture
def banco_temporario(monkeypatch, tmp_path):
    monkeypatch.setattr(GerenciadorBancoDados, "_instancia", None)
    monkeypatch.setattr(GerenciadorBancoDados, "_caminho_banco", tmp_path / "moderacao.db")
    return GerenciadorBancoDados()


def test_insere_e_lista_comentarios_no_banco_temporario(banco_temporario):
    primeiro_id = banco_temporario.inserir_comentario("Obrigado pelo conteúdo.", resposta())
    segundo_id = banco_temporario.inserir_comentario(
        "Você é incompetente.",
        resposta(
            eh_ofensivo=True,
            nivel_da_ofensa=NivelDaOfensa.levemente,
            justificativa="O comentário contém um insulto.",
            acao=Acao.sinalizar,
        ),
    )

    historico = banco_temporario.listar_historico()

    assert (primeiro_id, segundo_id) == (1, 2)
    assert [comentario.texto for comentario in historico] == [
        "Obrigado pelo conteúdo.",
        "Você é incompetente.",
    ]
    assert historico[1].acao is Acao.sinalizar
    assert historico[1].criado_em is not None


def test_lista_historico_aplica_filtros(banco_temporario):
    banco_temporario.inserir_comentario("Texto seguro", resposta())
    banco_temporario.inserir_comentario(
        "Texto ofensivo",
        resposta(
            eh_ofensivo=True,
            nivel_da_ofensa=NivelDaOfensa.altamente,
            eh_discurso_de_odio=True,
            justificativa="O comentário ataca um grupo protegido.",
            acao=Acao.bloquear,
        ),
    )

    ofensivos = banco_temporario.listar_historico(eh_ofensivo=True)
    bloqueados = banco_temporario.listar_historico(acao=Acao.bloquear)

    assert [comentario.texto for comentario in ofensivos] == ["Texto ofensivo"]
    assert [comentario.texto for comentario in bloqueados] == ["Texto ofensivo"]
