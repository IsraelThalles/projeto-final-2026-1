import os
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from llm import FabricaProvedorLLM
from esquemas import Acao, NivelDaOfensa, RespostaModeracao


class AgenteClassificador:
    """Classe responsável por orquestrar a moderação de comentários usando LLMs e aplicar guardrails de segurança."""

    def __init__(self):
        self._prompt_sistema = self._ler_prompt_sistema()
        self._tempo_limite = float(os.getenv("TEMPO_LIMITE_INFERENCIA") or 5)
        
        if self._tempo_limite <= 0:
            raise ValueError("Configuração incorreta: A variável 'TEMPO_LIMITE_INFERENCIA' deve ser um número positivo.")


    def _ler_prompt_sistema(self) -> str:
        """Lê o prompt dinamicamente do arquivo Markdown."""
        caminho_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        caminho_arquivo = os.path.join(caminho_base, "llm", "prompts", "prompt_sistema.md")
        
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            return f.read()



    def _gerar_fallback_erro(self, motivo: str) -> RespostaModeracao:
        """Gera um payload de segurança quando o LLM falha."""
        fallback = RespostaModeracao(
            eh_ofensivo=True,
            nivel_da_ofensa=NivelDaOfensa.nenhuma,
            eh_discurso_de_odio=False,
            justificativa=motivo,
            acao=Acao.sinalizar,
            modelo_de_llm=None,
            provedor_llm=None
        )
        return fallback



    def moderar_comentario(self, texto: str) -> RespostaModeracao:
        """Orquestra a classificação e impõe o Guardrail de Timeout."""
        try:
            provedor = FabricaProvedorLLM.obter_provedor()
            
            with ThreadPoolExecutor(max_workers=1) as executor:
                futuro = executor.submit(provedor.classificar_texto, texto, self._prompt_sistema)
                resultado = futuro.result(timeout=self._tempo_limite)
                
            return resultado
            
        except TimeoutError:
            return self._gerar_fallback_erro(f"Indisponibilidade técnica: tempo limite de {self._tempo_limite} segundos excedido.")
        except Exception as erro:
            return self._gerar_fallback_erro(f"Indisponibilidade técnica: {str(erro)}")