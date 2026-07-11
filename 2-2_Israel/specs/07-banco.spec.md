---
name: banco
description: Banco de dados SQLite para armazenar comentários analisados e resultados de moderação.
targets:
  - /2-2_Israel/codigo/banco/sqlite.py
  - /2-2_Israel/codigo/banco/models.py
---

# Banco de Dados: SQLite

## Objetivo

Armazenar o histórico de análises do agente para exibição no frontend e auditoria/métricas offline.

## Tecnologia

- **Banco:** SQLite (arquivo local `moderacao.db`).

## Esquema de Tabelas

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

- **Consulta:** Listar histórico com filtros por eh_ofensivo e tipo de acao para alimentar o dashboard.