import pandas as pd
import requests
from io import BytesIO
from datetime import datetime, timedelta

# CONFIGURAÇÃO
fundos_alvo = {
    "3Q_FIA": "53625021000169",      
    "Dynamo": "73232530000139",      
    "Alaska": "12987743000186",      
    
    # Os CNPJs dos peers que faltaram
    "Trigono": "29177013000112",     # Trígono Flagship Small Caps FIC FIA
    "Dahlia": "30858733000122",      # Dahlia Ações FIC FIA
    "Velt": "08940189000104"         # Velt FIF Cotas FIA
}

def obter_meses_analise():
    """Gera a lista de datas (YYYYMM) dos últimos 13 meses."""
    hoje = datetime.now()
    datas = []
    for i in range(13): 
        data_passada = hoje - timedelta(days=30 * i)
        datas.append(data_passada.strftime('%Y%m'))
    return sorted(list(set(datas)))

def coletar_dados_cvm():
    meses = obter_meses_analise()
    lista_dfs = []
    
    print(f"--- Iniciando Coleta de dados ({len(meses)} meses) ---")
    
    for mes in meses:
        url = f"http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{mes}.zip"
        print(f"> Processando {mes}...", end=" ")
        
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                with BytesIO(response.content) as arquivo_zip:
                    # Lê o CSV
                    df = pd.read_csv(arquivo_zip, compression='zip', sep=';', encoding='ISO-8859-1')
                    
                    # Padroniza colunas com maiúsculo e sem espaços
                    df.columns = df.columns.str.strip().str.upper()
                    
                    # Garante que temos a coluna certa (CNPJ_FUNDO_CLASSE)
                    # O Python tenta achar a coluna nova. Se não achar, tenta a antiga dado que as colunas mudaram recentemente de nomenclatura.
                    coluna_cnpj = 'CNPJ_FUNDO_CLASSE' if 'CNPJ_FUNDO_CLASSE' in df.columns else 'CNPJ_FUNDO'
                
                # Limpeza do CNPJ usando a coluna certa detectada
                df['CNPJ_LIMPO'] = df[coluna_cnpj].str.replace(r'[./-]', '', regex=True)
                
                # Filtro para os fundos alvo
                df_filtrado = df[df['CNPJ_LIMPO'].isin(fundos_alvo.values())].copy()
                
                if not df_filtrado.empty:
                    # Seleciona só o necessário (Data, ID Limpo, Valor da Cota)
                    df_filtrado = df_filtrado[['DT_COMPTC', 'CNPJ_LIMPO', 'VL_QUOTA']]
                    lista_dfs.append(df_filtrado)
                    print(f"OK! ({len(df_filtrado)} registros)")
                else:
                    print("Sem dados dos alvos.")
            else:
                print(f"Arquivo não disponível (Erro {response.status_code}).")
                
        except Exception as e:
            print(f"Erro: {e}")

    # Consolida todos os dados coletados
    if lista_dfs:
        print("\nConsolidando dados coletados...")
        df_final = pd.concat(lista_dfs)
        df_final['DT_COMPTC'] = pd.to_datetime(df_final['DT_COMPTC'])
        
        # Troca o CNPJ pelo Nome do Fundo
        mapa_nomes = {v: k for k, v in fundos_alvo.items()}
        df_final['FUNDO'] = df_final['CNPJ_LIMPO'].map(mapa_nomes)
        
        # Pivot (Linhas=Datas, Colunas=Fundos)
        df_pivot = df_final.pivot(index='DT_COMPTC', columns='FUNDO', values='VL_QUOTA')
        
        # Remove dias vazios
        df_pivot = df_pivot.ffill().dropna()
        
        return df_pivot
    else:
        return pd.DataFrame()

# Executa a coleta de dados
if __name__ == "__main__":
    df_resultado = coletar_dados_cvm()
    
    if not df_resultado.empty:
        print("\n Coleta concluida")
        print(df_resultado.tail())
        df_resultado.to_csv("dados_finais.csv")
        print("\n'dados_finais.csv'")
    else:
        print("Falha na coleta.")