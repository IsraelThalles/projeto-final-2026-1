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