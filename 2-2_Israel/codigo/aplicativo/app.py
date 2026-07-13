import os
from dotenv import load_dotenv
import requests
import pandas as pd
import streamlit as st

load_dotenv()

# Configuração da URL da API conforme variável de ambiente ou fallback local
API_URL = os.getenv("API_URL", "http://localhost:8000")
TEMPO_LIMITE_INFERENCIA = float(os.getenv("TEMPO_LIMITE_INFERENCIA") or 5)

if TEMPO_LIMITE_INFERENCIA <= 0:
    raise ValueError("Configuração incorreta: A variável 'TEMPO_LIMITE_INFERENCIA' deve ser um número positivo.")

# 1. Configuração da Página e UX
st.set_page_config(
    page_title="Shield IA - Moderação",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ Shield IA - Moderação de Conteúdo")
st.markdown("Colete, analise e gerencie comentários tóxicos utilizando Inteligência Artificial.")

st.divider()

# 2. Área de Inferência (Tempo Real)
st.subheader("Análise Rápida")
texto_entrada = st.text_area(
    "Comentário Suspeito",
    placeholder="Cole ou digite o comentário suspeito aqui...",
    height=120,
    label_visibility="collapsed"
)

if st.button("Analisar Toxicidade", type="primary"):
    if not texto_entrada.strip():
        st.warning("Por favor, digite um comentário antes de analisar.")
    else:
        # Estado de Carregamento
        with st.spinner("A IA está analisando o texto..."):
            try:
                # Requisição POST para a API
                resposta = requests.post(
                    f"{API_URL}/moderar",
                    json={"texto": texto_entrada},
                    timeout=TEMPO_LIMITE_INFERENCIA+1.0  # Timeout levemente superior para exibir erro da rede caso a API caia
                )
                resposta.raise_for_status()
                resultado = resposta.json()

                # 3. Painel de Resultados (Card de Resposta)
                st.markdown("### Resultado da Classificação")
                
                acao = resultado.get("acao", "")
                
                # Indicador de Ação
                if acao == "Aprovar":
                    st.success(f"**Ação Recomendada:** {acao} ✅")
                elif acao == "Sinalizar":
                    st.warning(f"**Ação Recomendada:** {acao} ⚠️")
                elif acao == "Bloquear":
                    st.error(f"**Ação Recomendada:** {acao} ⛔")

                # Informações da Classificação (Duas Colunas)
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        label="Nível da Ofensa", 
                        value=str(resultado.get("nivel_da_ofensa", "Desconhecido")).title()
                    )
                with col2:
                    eh_odio = "Sim 🚨" if resultado.get("eh_discurso_de_odio") else "Não"
                    st.metric(
                        label="Discurso de Ódio", 
                        value=eh_odio
                    )

                # Justificativa
                st.info(f"**Justificativa da IA:** {resultado.get('justificativa', '')}")

            except requests.exceptions.Timeout:
                st.error(f"⏳ Timeout: A API demorou mais de {TEMPO_LIMITE_INFERENCIA} segundos para responder.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Erro de Conexão: O servidor da API parece estar offline.")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Falha ao processar a requisição: {str(e)}")

st.divider()

# 4. Histórico de Análises
st.subheader("Últimas Análises")

try:
    # Requisição GET para buscar os registros no banco via API
    resposta_historico = requests.get(f"{API_URL}/historico", timeout=TEMPO_LIMITE_INFERENCIA+1.0)
    
    if resposta_historico.status_code == 200:
        dados_historico = resposta_historico.json()
        
        if dados_historico:
            # Converte a resposta em DataFrame do Pandas
            df = pd.DataFrame(dados_historico)
            
            # Formatação e Tradução das colunas
            df["criado_em"] = (
                pd.to_datetime(df["criado_em"])
                .dt.tz_localize("UTC")
                .dt.tz_convert("America/Sao_Paulo")
                .dt.strftime("%d/%m/%Y %H:%M:%S")
            )
            df["eh_ofensivo"] = df["eh_ofensivo"].apply(lambda x: "Sim" if x else "Não")
            df["eh_discurso_de_odio"] = df["eh_discurso_de_odio"].apply(lambda x: "Sim" if x else "Não")
            
            # Renomeia para as colunas exigidas na especificação
            df_visual = df.rename(columns={
                "criado_em": "Data/Hora",
                "texto": "Comentário",
                "eh_ofensivo": "Ofensivo",
                "nivel_da_ofensa": "Nível da Ofensa",
                "eh_discurso_de_odio": "Discurso de Ódio",
                "acao": "Ação"
            })
            
            # Filtra apenas as colunas que importam para o usuário
            colunas_exibidas = ["Data/Hora", "Comentário", "Ofensivo", "Nível da Ofensa", "Discurso de Ódio", "Ação"]
            df_visual = df_visual[colunas_exibidas]
            
            # Renderiza no Streamlit permitindo ordenação e filtros interativos nativos
            st.dataframe(
                df_visual.sort_values(by="Data/Hora", ascending=False), 
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Nenhuma análise encontrada no histórico.")
    else:
        st.error(f"Falha ao carregar histórico: HTTP {resposta_historico.status_code}")
except requests.exceptions.RequestException:
    st.warning("Não foi possível carregar o histórico de análises. Verifique a conexão com a API.")