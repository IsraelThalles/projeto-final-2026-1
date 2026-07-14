# Relatório Final: Shield IA - Moderação de Conteúdo

## Cabeçalho
* **Aplicação:** "Execução Local"
* **Repositório:** https://github.com/IsraelThalles/projeto-final-2026-1
* **Equipe:** Israel Thalles

## Definição do Problema
O projeto visa resolver a proliferação de toxicidade e discurso de ódio em plataformas digitais, automatizando a triagem primária de comentários suspeitos por meio de IA. 
* **A dor e sua importância:** A moderação manual é lenta, psicologicamente exaustiva para os revisores e cara para as empresas. A ausência de filtros rápidos permite que ambientes online se tornem hostis.
* **Stakeholders:** Equipes de moderação (redução de carga de trabalho), usuários finais (ambiente mais seguro) e administradores da plataforma (redução de riscos legais e melhora na retenção de usuários).
* **Métricas de Sucesso:** 
  * *Negócio:* Redução do tempo médio de análise de um comentário e diminuição do volume de reports ignorados por falta de equipe.
  * *Técnica:* Latência da resposta (inferência em poucos segundos) e confiabilidade do fallback (o sistema não deve travar se a IA demorar a responder).

## Como o sistema é montado
* **Arquitetura:** O sistema segue um fluxo linear e isolado (Microsserviços). A **Entrada** ocorre via interface Streamlit (Frontend), que faz uma requisição HTTP REST para a **API** (FastAPI). A API repassa o texto ao **Agente** (que aplica o padrão Strategy para escolher o provedor de LLM). A **Resposta** é padronizada via Pydantic, gravada no **Banco de Dados** (SQLite) e devolvida ao **Produto** (Frontend) para exibição do cartão de classificação e atualização do histórico.
* **Exploração de Modelos (Agent Exploration):** A estratégia inicial foi desenvolver localmente para evitar custos de nuvem. Foram testados:
  * *Qwen2.5-coder (1.5b e 7b):* Falharam ao tentar executar chamadas de ferramentas (tool calling).
  * *Qwen3 (1.7b e 4b):* Realizaram a chamada de ferramentas, mas perderam contexto da moderação e geraram baixa qualidade.
  * *Gemma4 (4b e 12b):* Causaram timeout de requisição na integração com o Roo Code.
  * *Decisão final:* Utilizar o padrão de projeto Factory/Strategy para alternar entre provedores locais (Ollama) e nuvem (Gemini/OpenAI) via `.env`.
* **Deployment:** O agente foi empacotado como uma API FastAPI conteinerizada (junto ao Streamlit) usando Docker e docker-compose. 
* **Confiabilidade e Fallback:** O sistema possui um guardrail de tempo limite estrito (timeout de 5 segundos). Caso o LLM falhe ou demore a responder, a API intercepta a falha e aciona o fallback, gerando uma resposta padrão segura (Ação: "Sinalizar" / "Erro técnico") para que a moderação humana seja alertada sem travar a interface do usuário.

## Descrição do Agente
* **Modelo e Ferramentas:** Utilizamos um padrão agnóstico a modelos para a extração estruturada de dados. O agente processa a entrada e deve devolver obrigatoriamente um objeto JSON com variáveis de toxicidade (ofensivo, nível da ofensa, discurso de ódio) e uma recomendação de ação (Aprovar, Sinalizar, Bloquear).
* **Dados e Contexto:** O input principal são os comentários dos usuários injetados em tempo real na interface. O histórico de decisões é gravado em um banco de dados relacional (SQLite) para auditoria.
* **Guardrails:** 
  * *Entrada:* O FastAPI utiliza Pydantic para barrar payloads inválidos (textos vazios ou strings malformadas) antes de gastar processamento de IA. 
  * *Saída:* A resposta do modelo é estritamente validada; enums garantem que a IA não invente níveis de ofensa fora do padrão.

## Avaliação do Sistema
* **Performance:** A confiabilidade é garantida por uma suíte de testes automatizados (pytest). O critério técnico de sucesso é manter uma cobertura de código superior a 80%. Para evitar custos e poluição de dados, implementamos Mocks e um banco de dados em memória (`:memory:`) nos testes End-to-End.
* **UX:** O painel em Streamlit é responsivo e claro. O usuário recebe feedback visual imediato (cores semânticas: verde para aprovar, amarelo para sinalizar, vermelho para bloquear) e alertas de erro amigáveis caso ocorram problemas de rede.

## Demonstração
<img width="1366" height="768" alt="Capturar_20260714001256" src="https://github.com/user-attachments/assets/30e1332a-e8bf-4a03-96f3-b9506d1faed8" />

## Reflexão sobre o que aprenderam
O grande aprendizado técnico e metodológico residiu no uso do **Spec-Driven Development (SDD)** utilizando o framework Tessl. A dinâmica de criar especificações, iterar e gerar lotes de código trouxe percepções valiosas:
* **O que funcionou bem:** A modularização da arquitetura (separando API e Frontend) e o estabelecimento de contratos rigorosos de software (esquemas Pydantic).
* **Limitações enfrentadas:** O hardware local (Samsung Book x40, i5 10ª Gen, GPU MX110, 16GB RAM) impôs severas barreiras. Mesmo com o Ollama transferindo camadas para a GPU, o ganho de performance foi marginal, inviabilizando modelos pesados. 
* **Reflexão sobre a IA como parceira de código:** O ciclo inicial de SDD foi frustrante. O código gerado muitas vezes carecia de qualidade, obrigando revisões constantes na spec. A curva de aprendizado revelou que, ao entender como a IA "pensa", bastava padronizar as especificações. Paradoxalmente, a sensação final é que a codificação manual direta (sem SDD) poderia ter sido mais rápida em diversos módulos, visto a exaustiva necessidade de revisar documentos técnicos.

## Impactos e Ética
* **Riscos de Viés:** Sistemas de moderação correm o risco crítico de silenciar minorias devido à incapacidade da IA de entender dialetos locais, ironias ou apropriação linguística de determinados grupos sociais, marcando essas falas como "discurso de ódio" ou "ofensivas" (falsos positivos).
* **Mitigação Adotada:** O sistema não tem autonomia punitiva final. Ele atua como um sistema de suporte à decisão. A ação primária de incerteza do agente (e de falhas sistêmicas) é "Sinalizar", enviando o caso para a fila de revisão humana, garantindo que o contexto social não seja apagado pela automação pura.

## Referências
* Tessl Framework (SDD).
* HateBRXplain (Referência de dataset e cenários para testes em pt-br).
* FastAPI e Pydantic para APIs robustas.
* Streamlit para construção rápida de painéis de dados.
* Ollama para testes locais de Modelos de Linguagem de Grande Escala.
