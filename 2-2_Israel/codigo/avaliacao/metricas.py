import time
import argparse
import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score, f1_score, recall_score, confusion_matrix

from codigo.agente import AgenteClassificador


class AvaliadorMetricas:
    def __init__(self, caminho_csv: str):
        """
        Inicializa o avaliador carregando o dataset HateBRXplain.
        """
        caminho_arquivo = Path(caminho_csv)
        if not caminho_arquivo.exists():
            raise FileNotFoundError(f"Arquivo de dados não encontrado: {caminho_arquivo}")
        
        self.df = pd.read_csv(caminho_arquivo)
        self.agente = AgenteClassificador()

    def executar_avaliacao(self, limite_amostras: int, atraso_segundos: float):
        """
        Roda a inferência em lote utilizando amostragem aleatória estratificada.
        """
        # Garante que o limite não ultrapasse o tamanho do dataset
        limite_amostras = min(limite_amostras, len(self.df))
        
        # Amostragem Estratificada: Sorteia N linhas garantindo que as classes (0 e 1) 
        # mantenham a mesma proporção existente no dataset original.
        # random_state=42 garante que a aleatoriedade seja sempre a mesma em testes repetidos.
        df_lote = self.df.groupby('offensive_label', group_keys=False).apply(
            lambda x: x.sample(n=max(1, int(limite_amostras * len(x) / len(self.df))), random_state=42)
        )
        
        total = len(df_lote)
        y_true = df_lote['offensive_label'].tolist()
        y_pred = []
        
        print(f"\n🚀 Iniciando avaliação científica com {total} amostras (Aleatória Estratificada)...")
        if atraso_segundos > 0:
            print(f"⏳ Atraso configurado: {atraso_segundos}s entre requisições.")
        print("=" * 70)

        # Inferência em Lote
        for _, row in df_lote.iterrows():
            texto = row['comment']
            print(f"[{len(y_pred) + 1}/{total}] Analisando comentário...")
            
            try:
                resposta = self.agente.moderar_comentario(texto)
                # Converte booleano para inteiro (1 = ofensivo, 0 = inofensivo)
                predicao = 1 if resposta.eh_ofensivo else 0
                y_pred.append(predicao)
            except Exception as e:
                print(f"  [!] Falha ao analisar (Fallback aplicado para 0). Erro: {e}")
                # Em caso de falha, assumimos inofensivo para impactar as métricas negativamente e expor o erro
                y_pred.append(0) 
            
            if atraso_segundos > 0:
                time.sleep(atraso_segundos)

        # Cálculo de Métricas (scikit-learn)
        self._gerar_relatorio(y_true, y_pred)

    def _gerar_relatorio(self, y_true: list, y_pred: list):
        """
        Extrai a matriz de confusão e compara os resultados com os limiares de negócio.
        """
        acuracia = accuracy_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        
        # Extrai os quadrantes da Matriz de Confusão
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
        
        taxa_fp = fp / (fp + tn) if (fp + tn) > 0 else 0.0

        # Formatação do Relatório
        self._imprimir_relatorio(acuracia, f1, recall, tn, fp, fn, tp, taxa_fp)

    def _imprimir_relatorio(self, acuracia, f1, recall, tn, fp, fn, tp, taxa_fp):
        print("\n📊 RELATÓRIO DE DESEMPENHO DO MODELO")
        print("=" * 70)
        
        print("\nMatriz de Confusão:")
        print(f"  Verdadeiros Positivos (Acertou Ofensa)    : {tp}")
        print(f"  Verdadeiros Negativos (Acertou Inofensivo): {tn}")
        print(f"  Falsos Positivos (Bloqueio Injusto)       : {fp}")
        print(f"  Falsos Negativos (Deixou passar ofensa)   : {fn}")
        print("-" * 70)
        
        print("\nMétricas Científicas e Validação:")
        
        # MT04: Acurácia >= 85%
        status_acuracia = "✅" if acuracia >= 0.85 else "❌"
        print(f"  [MT04] Acurácia Geral  : {acuracia:.2%} {status_acuracia} (Meta: >= 85%)")
        
        # MT01: F1-Score >= 85%
        status_f1 = "✅" if f1 >= 0.85 else "❌"
        print(f"  [MT01] F1-Score        : {f1:.2%} {status_f1} (Meta: >= 85%)")
        
        # MT02: Recall >= 90%
        status_recall = "✅" if recall >= 0.90 else "❌"
        print(f"  [MT02] Recall          : {recall:.2%} {status_recall} (Meta: >= 90%)")
        
        # MT03: Taxa de Falsos Positivos <= 10%
        status_fp = "✅" if taxa_fp <= 0.10 else "❌"
        print(f"  [MT03] Falsos Positivos: {taxa_fp:.2%} {status_fp} (Meta: <= 10%)")
        print("=" * 70)


if __name__ == "__main__":
    # Configuração dos argumentos de linha de comando via argparse
    parser = argparse.ArgumentParser(description="Script de avaliação científica do Agente Classificador.")
    parser.add_argument(
        "--amostras", 
        type=int, 
        default=100, 
        help="Quantidade de amostras para testar (Padrão: 100)."
    )
    parser.add_argument(
        "--atraso", 
        type=float, 
        default=1.0, 
        help="Atraso em segundos entre as requisições. Use 0 para modelos locais (Padrão: 1.0)."
    )
    args = parser.parse_args()

    # Resolve o caminho do CSV na raiz do repositório
    CAMINHO_DATASET = Path(__file__).parent.parent.parent / "dados" / "HateBRXplain.csv"
    
    try:
        avaliador = AvaliadorMetricas(caminho_csv=str(CAMINHO_DATASET))
        avaliador.executar_avaliacao(limite_amostras=args.amostras, atraso_segundos=args.atraso)
        
    except Exception as erro:
        print(f"Erro fatal na execução da avaliação: {erro}")