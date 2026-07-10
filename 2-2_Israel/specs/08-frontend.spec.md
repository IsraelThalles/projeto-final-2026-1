---
name: frontend
description: Interface web (dashboard) que consome a API de moderação.
targets:
  - /2-2_Israel/codigo/frontend/
---

# Produto: Painel de Moderação de Comentários

## Funcionalidades

- Campo de texto para o analista colar um comentário suspeito.
- Botão "Analisar Toxicidade".
- Exibição de painel de resultados contendo:
  - Indicador visual de ação (Verde = Aprovado, Amarelo = Sinalizado, Vermelho = Bloqueado).
  - Tags visuais para o Nível da Ofensa (leve, moderada, alta) e um alerta se for discurso de ódio.
  - Justificativa do agente (*rationale*) detalhando a decisão lógica.
  - Confiança da classificação.
  - Horário da análise.
  - Botão para limpar o formulário.
- Histórico em formato de lista/tabela exibindo as últimas validações do banco de dados.

## UX

- Estado de carregamento explicativo avisando que a "IA está analisando o texto".
- Exibição de mensagem amigável caso ocorra timeout (*fallback* acionado aos 5 segundos).

[@test]: /2-2_Israel/testes/teste_api.py#L41-L60