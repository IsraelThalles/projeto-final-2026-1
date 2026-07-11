---
name: banco
description: Banco de dados SQLite para armazenar comentários analisados e resultados de moderação.
targets:
  - /2-2_Israel/codigo/banco/banco.py
  - /2-2_Israel/codigo/banco/ddl.sql
  - /2-2_Israel/codigo/esquemas/esquemas.py
---

# Banco de Dados: SQLite

## Objetivo

Criar uma classe usando o padrão de projeto *Singleton* em `/2-2_Israel/codigo/banco/banco.py` responsável por:

- Conectar ao arquivo local `/2-2_Israel/moderacao.db`.
- Salvar o esquema de tabelas em um arquivo `ddl.sql`.
- Executar o esquema salvo em `ddl.sql` para criar as tabelas na inicialização (não deve executar um *script* de criação de tabelas definido estaticamente no código python).
- Criar um método inserir_comentario(…).
- Criar um método listar_historico(…).
- Armazenar o histórico de análises do agente para exibição no frontend e auditoria/métricas offline.

## Regra de Arquitetura

- **Modelos de Dados:** Crie ou utilize estritamente os contratos já definidos em `/2-2_Israel/codigo/esquemas/esquemas.py`.

## Tecnologia

- **Banco:** SQLite (arquivo local `moderacao.db`).

## Esquema de Tabelas

As tabelas devem ser salvas no arquivo `/2-2_Israel/codigo/banco/ddl.sql`

### Tabela `comentarios`

```sql
CREATE TABLE comentarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    texto TEXT NOT NULL,
    eh_ofensivo BOOLEAN NOT NULL,
    nivel_da_ofensa TEXT CHECK (nivel_da_ofensa IN ('nenhuma', 'levemente', 'moderadamente', 'altamente')),
    eh_discurso_de_odio BOOLEAN NOT NULL,
    confianca REAL,
    justificativa TEXT,
    acao TEXT CHECK (acao IN ('Aprovar', 'Sinalizar', 'Bloquear')),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modelo_de_llm TEXT,
    provedor_llm TEXT
);
```

## Operações Principais

- **Inserção:** Salvar o payload completo gerado pelo agente na API.

- **Consulta:** Listar histórico com filtros por eh_ofensivo ou tipo de acao para alimentar o dashboard.