import sqlite3
from typing import Optional, List
from pathlib import Path
from datetime import datetime

from esquemas import RespostaModeracao, ComentarioSaidaBanco, Acao, NivelDaOfensa


class GerenciadorBancoDados:
    _instancia = None
    _caminho_banco = Path(__file__).parent / "moderacao.db"
    _caminho_ddl = Path(__file__).parent / "ddl.sql"

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(GerenciadorBancoDados, cls).__new__(cls)
            cls._instancia._inicializar_banco()
        return cls._instancia

    def _inicializar_banco(self):
        self._criar_tabelas()

    def _conectar(self):
        return sqlite3.connect(self._caminho_banco)

    def _criar_tabelas(self):
        with self._conectar() as conexao:
            cursor = conexao.cursor()
            with open(self._caminho_ddl, 'r', encoding='utf-8') as f:
                ddl_script = f.read()
            cursor.executescript(ddl_script)
            conexao.commit()

    def inserir_comentario(self, texto: str, resultado: RespostaModeracao) -> int:
        with self._conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                """INSERT INTO comentarios (
                    texto, eh_ofensivo, nivel_da_ofensa, eh_discurso_de_odio,
                    justificativa, acao, modelo_de_llm, provedor_llm
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    texto,
                    resultado.eh_ofensivo,
                    resultado.nivel_da_ofensa.value,
                    resultado.eh_discurso_de_odio,
                    resultado.justificativa,
                    resultado.acao.value,
                    resultado.modelo_de_llm,
                    resultado.provedor_llm,
                ),
            )
            conexao.commit()
            return int(cursor.lastrowid) if cursor.lastrowid is not None else -1 # Retorna -1 ou lança erro se a inserção falhar e não retornar ID

    def listar_historico(self, eh_ofensivo: Optional[bool] = None, acao: Optional[Acao] = None) -> List[ComentarioSaidaBanco]:
        with self._conectar() as conexao:
            conexao.row_factory = sqlite3.Row  # Para acessar colunas por nome
            cursor = conexao.cursor()

            consulta = "SELECT * FROM comentarios WHERE 1=1"
            parametros = []

            if eh_ofensivo is not None:
                consulta += " AND eh_ofensivo = ?"
                parametros.append(1 if eh_ofensivo else 0)
            if acao is not None:
                consulta += " AND acao = ?"
                parametros.append(acao.value)

            cursor.execute(consulta, parametros)
            resultados = cursor.fetchall()

            lista_comentarios = []
            for row in resultados:
                lista_comentarios.append(
                    ComentarioSaidaBanco(
                        id=row['id'],
                        texto=row['texto'],
                        eh_ofensivo=bool(row['eh_ofensivo']),
                        nivel_da_ofensa=NivelDaOfensa(row['nivel_da_ofensa']),
                        eh_discurso_de_odio=bool(row['eh_discurso_de_odio']),
                        justificativa=row['justificativa'],
                        acao=Acao(row['acao']),
                        criado_em=datetime.fromisoformat(row['criado_em']) if row['criado_em'] else None,
                        modelo_de_llm=row['modelo_de_llm'],
                        provedor_llm=row['provedor_llm'],
                    )
                )
            return lista_comentarios

