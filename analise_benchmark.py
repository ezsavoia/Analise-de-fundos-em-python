import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Carrega os dados locais
try:
    df_fundos = pd.read_csv("dados_finais.csv", index_col=0, parse_dates=True)
    data_inicio = df_fundos.index.min().strftime('%Y-%m-%d')
    data_fim = df_fundos.index.max().strftime('%Y-%m-%d')
except Exception as e:
    print(f" Erro ao ler CSV: {e}")
    exit()

# Download Individual dos Ativos de Mercado
dados_mercado = {}
ativos = {
    "^BVSP": "IBOVESPA",
    "SMAL11.SA": "SMALL CAPS (B3)"
}

print("Baixando dados")

for simbolo, nome_bonito in ativos.items(): # A variável 'simbolo' pega a chave, 'nome_bonito' pega o valor.
    try:
        ativo = yf.Ticker(simbolo)
        historico = ativo.history(start=data_inicio, end=data_fim)
        
        if not historico.empty:
            # Remove fuso horário
            historico.index = historico.index.tz_localize(None)
            dados_mercado[nome_bonito] = historico['Close']
    except:
        pass

# Consolidação
if dados_mercado:
    df_mercado = pd.DataFrame(dados_mercado).ffill()
    df_completo = df_fundos.join(df_mercado, how='inner').dropna()
    df_normalizado = (df_completo / df_completo.iloc[0]) * 100
    
    # Mudança de cores
    plt.figure(figsize=(12, 6))
    
    # IBOVESPA 
    if 'IBOVESPA' in df_normalizado.columns:
        plt.plot(df_normalizado.index, df_normalizado['IBOVESPA'], 
                 label='IBOVESPA', color='#0000FF', linestyle='-', linewidth=2, alpha=0.8)

    # SMALL CAPS B3
    # Cor: Vermelho para diferenciar do Ibov
    if 'SMALL CAPS (B3)' in df_normalizado.columns:
        plt.plot(df_normalizado.index, df_normalizado['SMALL CAPS (B3)'], 
                 label='SMALL CAPS (B3)', color='red', linestyle='-', linewidth=1.5, alpha=0.9)
    
    # 3Q FIA
    # Cor: Preto | Estilo: Sólido | Espessura: Grossa (3)
    if '3Q_FIA' in df_normalizado.columns:
        plt.plot(df_normalizado.index, df_normalizado['3Q_FIA'], 
                 label='3Q Asset', color='black', linewidth=3)
        
    plt.title("3Q FIA x Benchmarks", fontsize=14, fontweight='bold')
    plt.ylabel("Retorno Acumulado")
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.tight_layout()
    
    plt.savefig("grafico_benchmark_final.png", dpi=300)
    print("\n 'grafico_benchmark_final.png'")
    plt.show()

else:
    print("Erro.")