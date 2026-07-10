---
name: testes
description: Estratégia de testes do sistema de moderação.
targets:
  - /2-2_Israel/testes/
---

# Estratégia de Testes

## Tipos de Teste

- **Testes unitários:** lógica do agente, formatação de resposta, *guardrails* de entrada e saída.
- **Testes de integração:** API + agente, persistência no banco SQLite.
- **Testes de aceitação:** cenários de moderação realistas baseados em exemplos do HateBRXplain.

## Cobertura Esperada

- ≥ 80% de cobertura de código para `/2-2_Israel/codigo/agente/` e `/2-2_Israel/codigo/api/`.
- Testes para casos de borda: ironia leve, falsos positivos comuns e tentativas de injeção de *prompt*.
- Testes de limite de tempo (*timeout*) para verificar se o *fallback* de 5 segundos está sendo acionado corretamente.

[@test]: /2-2_Israel/testes/teste_agente.py
[@test]: /2-2_Israel/testes/teste_classificador.py
[@test]: /2-2_Israel/testes/teste_api.py