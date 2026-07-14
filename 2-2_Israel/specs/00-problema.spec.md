---
name: problema
description: Contexto do problema de moderação de toxicidade em comentários em português.
targets:
  - README.md
  - /2-2_Israel/dados/data_card.md
---

# Problema: Moderação e Detecção de Toxicidade em Comentários

## Contexto

Plataformas de redes sociais recebem um alto volume de comentários, muitos deles tóxicos. A equipe de moderação não consegue escalar a análise manualmente, e os usuários relatam demora na resposta a denúncias.

## Stakeholders

- **Usuários da plataforma:** que precisam de um ambiente seguro e livre de toxicidade.
- **Equipe de moderação:** que precisa automatizar a triagem de um alto volume de comentários.
- **Produto/Comunidade:** responsável por manter e aplicar as diretrizes de convivência.

## Objetivo Geral

Construir um agente de IA (baseado no *dataset* HateBRXplain) que atue como um "copiloto" para a equipe de moderação. Ele deve identificar rapidamente comentários ofensivos (classificação binária) e gerar uma justificativa explicável, sugerindo ações para reduzir o tempo de triagem manual.

## Escopo

- O sistema destina-se exclusivamente à análise de comentários escritos em português.
- A detecção foca em uma classificação binária: Ofensivo vs. Não Ofensivo.
- O sistema não realiza bloqueios automáticos irrevogáveis; a decisão final e a auditoria permanecem com o moderador humano.
