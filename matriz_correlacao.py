import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carrega os dados
# Se o seu arquivo tiver outro nome, mude aqui.
try:
    df = pd.read_csv("dados_finais.csv", index_col=0, parse_dates=True)
    
    # Filtra apenas colunas numéricas (caso tenha alguma sujeira)
    df_returns = df.pct_change().dropna() # Variação diária (%)
    
    # Calcula a Correlação
    matriz_corr = df_returns.corr()
    
    # Salva os números em um CSV (para conferência)
    matriz_corr.to_csv("matriz_correlacao_calculada.csv")

    # Gera o Gráfico de heatmap
    plt.figure(figsize=(8, 6)) # Tamanho quadrado
    
    # Desenha o mapa de calor
    # annot=True (mostra os números), cmap='RdBu' (Azul=Positivo, Vermelho=Negativo)
    sns.heatmap(matriz_corr, annot=True, fmt=".2f", cmap='RdBu_r', vmin=-1, vmax=1, linewidths=0.5)
    
    plt.title("Matriz de Correlação (12 Meses)", fontsize=12, fontweight='bold')
    plt.tight_layout()
    
    # Salva a imagem
    plt.savefig("heatmap_correlacao.png", dpi=300)
    print(" 'heatmap_correlacao.png'")
    
except Exception as e:
    print(f"Erro ao ler os dados: {e}")
    print("Verifique se o arquivo 'dados_finais.csv' está na pasta.")