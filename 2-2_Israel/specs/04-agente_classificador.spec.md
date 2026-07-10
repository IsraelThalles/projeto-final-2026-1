---
name: agente_classificador
description: Agente de IA agnóstico que detecta toxicidade em comentários em português e explica o raciocínio.
targets:
  - /2-2_Israel/codigo/agente/agente_classificador.py
  - /2-2_Israel/codigo/agente/provedores.py
---

# Agente Classificador de Toxicidade (Moderação)

## Capacidades

- Receber um comentário de rede social em português e classificar sua toxicidade.
- **Classificação Binária Principal:** Determinar se é Ofensivo ou Não Ofensivo.
- **Inferência de Nível:** Determinar o nível de ofensa (altamente, moderadamente, levemente) baseado na quantidade e peso dos termos pejorativos, seguindo a árvore de decisão estruturada do HateBR.
- **Inferência de Ódio:** Identificar se a ofensa se enquadra como discurso de ódio (booleano).
- Justificar a classificação em linguagem natural baseada no texto.
- Sugerir ação de moderação (Aprovar, Sinalizar ou Bloquear).

## Arquitetura de Provedores (Estratégia/Fábrica)

- O sistema deve implementar uma interface comum (ex: `ProvedorLLM`) para suportar múltiplos modelos (ex: `EstratégiaOllama`, `EstratégiaGemini`, `EstratégiaOpenAI`).
- A escolha do provedor será resolvida dinamicamente via `FábricaProvedorLLM`, lendo o arquivo `.env`.
- O *prompt* do sistema será idêntico para todos os provedores, roteirizando a árvore de decisão do *dataset* HateBRXplain.
- **Guardrails de formatação:** Garantir que a saída do modelo, independente do provedor, seja sempre o JSON estruturado esperado.

## Fallback

- Se o provedor configurado estiver indisponível, falhar na autenticação ou a latência ultrapassar o limite de 5 segundos > interromper a chamada, acionar log de erro e devolver ação "Sinalizar" com aviso de indisponibilidade técnica para encaminhar à fila manual.

[@test]: /2-2_Israel/testes/teste_agente.py#L21-L50
[@test]: /2-2_Israel/testes/teste_classificador.py#L31-L60