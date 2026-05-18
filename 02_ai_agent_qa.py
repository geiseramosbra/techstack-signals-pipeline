import pandas as pd
import json

def main():
    print("\n=== [STEP 1] Inicializando Agente de Validação de IA (Framework QA) ===")
    
    csv_file = "market_intelligence_summary.csv"
    
    try:
        
        df = pd.read_csv(csv_file)
        print(f"=== [STEP 2] Lendo dados consolidados de: {csv_file} ===")
        
        
        print("=== [STEP 3] Executando Regras de Validação de Sinais Financeiros ===")
        
        relatorio_qa = []
        
        for index, row in df.iterrows():
            status_falencia = "Falidas (Bankrupt)" if row['is_bankrupt'] == 1 else "Saudáveis (Solvent)"
            roa = row['avg_roa']
            net_income_ratio = row['avg_net_income_ratio']
            
            
            if row['is_bankrupt'] == 1 and roa < 0.45:
                alerta = f"CRÍTICO: Empresas {status_falencia} apresentam ROA médio preocupante de {roa:.4f}."
                resultado_validacao = "REJEITADO - Risco de Crédito Elevado"
            else:
                alerta = f"NORMAL: Métricas para empresas {status_falencia} operando dentro dos limites estatísticos."
                resultado_validacao = "APROVADO - Padrão de Estabilidade Mapeado"
                
            relatorio_qa.append({
                "segmento": status_falencia,
                "metricas_analisadas": {
                    "avg_roa": roa,
                    "avg_net_income_ratio": net_income_ratio
                },
                "insight_ia": alerta,
                "status_qa": resultado_validacao
            })
            
        print("\n=== [STEP 4] Relatório Final do Agente de IA (Formato JSON Corporativo) ===")
        print(json.dumps(relatorio_qa, indent=4, ensure_ascii=False))
        
        print("\n=== [SUCCESS] Framework de QA concluído com 100% de cobertura! ===\n")
        
    except FileNotFoundError:
        print(f"=== [ERROR] Arquivo {csv_file} não encontrado. Execute o script 01 primeiro! ===")

if __name__ == "__main__":
    main()