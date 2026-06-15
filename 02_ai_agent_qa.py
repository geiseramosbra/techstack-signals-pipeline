import os
import json
import pandas as pd
from groq import Groq

def main():
    print("\n=== [STEP 1] Inicializando Agente de Validação de IA (Groq LLM QA - Gratuito) ===")
    
    # O código procura a chave no sistema operacional de forma segura
    if "GROQ_API_KEY" not in os.environ:
        print("=== [ERROR] Variável de ambiente GROQ_API_KEY não encontrada! ===")
        print("Por favor, execute o comando de injeção de chave no seu terminal antes de rodar.")
        return

    # Inicializa o cliente do Groq buscando a chave injetada automaticamente
    client = Groq()
    parquet_folder = "gold_market_intelligence_summary"

    try:
        # Lendo os dados consolidados pelo PySpark
        df = pd.read_parquet(parquet_folder)
        print(f"=== [STEP 2] Lendo dados consolidados de: {parquet_folder} ===")
        
        print("=== [STEP 3] Enviando métricas financeiras para análise do Agente de IA (Llama 3.3) ===")
        
        # Convertemos o dataframe em string para enviar ao modelo
        dados_financeiros = df.to_string(index=False)
        
        prompt_sistema = """
        Você é um Agente de IA especialista em Auditoria de Risco de Crédito Corporativo e Garantia de Qualidade (QA).
        Sua tarefa é analisar as métricas consolidadas de empresas (ROA médio, crescimento e net income ratio) agrupadas por status de falência (is_bankrupt: 1 para falidas, 0 para saudáveis).
        
        Para cada segmento encontrado, você deve gerar uma análise heurística de risco e retornar estritamente um objeto JSON contendo um array chamado 'relatorio' com a seguinte estrutura:
        {
            "relatorio": [
                {
                    "segmento": "Nome do Segmento (Falidas ou Saudáveis)",
                    "metricas_analisadas": {
                        "avg_roa": valor_float,
                        "avg_net_income_ratio": valor_float
                    },
                    "insight_ia": "Seu diagnóstico detalhado de risco de crédito baseado nos sinais financeiros",
                    "status_qa": "REJEITADO - Risco Elevado" ou "APROVADO - Sinais Estáveis"
                }
            ]
        }
        Certifique-se de retornar APENAS o JSON, sem nenhuma marcação de texto ou markdown antes ou depois.
        """

        # Chamada para a API do Groq usando o Llama 3.3
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            response_format={ "type": "json_object" }, # Força o modelo a responder em JSON estruturado
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": f"Aqui estão os dados agregados do Spark:\n{dados_financeiros}"}
            ],
            temperature=0.0 # Temperatura zero para garantir respostas exatas e sem alucinações
        )

        # Captura o retorno da IA e carrega como JSON nativo do Python
        resultado_json = json.loads(response.choices[0].message.content)

        print("\n=== [STEP 4] Relatório Final do Agente de IA (Formato JSON Corporativo Real - Gratuito) ===")
        print(json.dumps(resultado_json, indent=4, ensure_ascii=False))
        
        print("\n=== [SUCCESS] Framework de QA via LLM concluído com sucesso! ===\n")

    except FileNotFoundError:
        print(f"=== [ERROR] Diretório {parquet_folder} não encontrado. Execute o script 01 primeiro! ===")
    except Exception as e:
        print(f"=== [ERROR] Ocorreu um erro inesperado: {str(e)} ===")

if __name__ == "__main__":
    main()