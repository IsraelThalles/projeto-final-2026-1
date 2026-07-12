import os
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from llm import FabricaProvedorLLM
from esquemas import Acao, NivelDaOfensa, RespostaModeracao



def _ler_prompt_sistema() -> str:
    """Lê o prompt dinamicamente do arquivo Markdown."""
    caminho_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_arquivo = os.path.join(caminho_base, "llm", "prompts", "prompt_sistema.md")
    
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        return f.read()



def _gerar_fallback_erro(motivo: str) -> RespostaModeracao:
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



def classificar_toxicidade(texto: str) -> RespostaModeracao:
    """Orquestra a classificação e impõe o Guardrail de Timeout (5s)."""
    try:
        prompt = _ler_prompt_sistema()
        provedor = FabricaProvedorLLM.obter_provedor()
        
        with ThreadPoolExecutor(max_workers=1) as executor:
            futuro = executor.submit(provedor.classificar_texto, texto, prompt)
            resultado = futuro.result(timeout=5.0)
            
        return resultado
        
    except TimeoutError:
        return _gerar_fallback_erro("Indisponibilidade técnica: Timeout de 5 segundos excedido.")
    except Exception as erro:
        return _gerar_fallback_erro(f"Indisponibilidade técnica: {str(erro)}")