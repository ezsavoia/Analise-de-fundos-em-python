import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carrega os dados
df = pd.read_csv("dados_finais.csv", index_col=0, parse_dates=True)

# Risco
# A. Calcula retornos diários
retornos = df.pct_change()

# B. Calcula o Desvio Padrão Móvel (Janela de 21 dias)
# C. Anualiza o risco (* raiz de 252)
vol_movel = retornos.rolling(window=21).std() * np.sqrt(252)

# Multiplica por 100 para virar porcentagem
vol_movel = vol_movel * 100

# Remove os primeiros 21 dias (que ficam vazios/NaN no cálculo)
vol_movel = vol_movel.dropna()

# Plotagem
plt.figure(figsize=(12, 6))

# A. Desenha os Concorrentes (Linhas finas)
for coluna in vol_movel.columns:
    if "3Q" not in coluna:
        # Se for o Alaska, deixa ele pontilhado ou mais suave para não poluir
        estilo = '--' if "Alaska" in coluna else '-'
        plt.plot(vol_movel.index, vol_movel[coluna], 
                 label=coluna, linewidth=1.5, alpha=0.6, linestyle=estilo)

# B. Desenha a 3Q Asset em destaque
if "3Q_FIA" in vol_movel.columns:
    plt.plot(vol_movel.index, vol_movel["3Q_FIA"], 
             label="3Q Asset", color='black', linewidth=3)

# Finalização do Gráfico
plt.title("Volatilidade (Rolling 21d)", fontsize=14, fontweight='bold')
plt.ylabel("Volatilidade Anualizada (%)")
plt.xlabel("Data")
plt.legend(loc='upper left') # Legenda no canto para não atrapalhar
plt.grid(True, linestyle=':', alpha=0.5)

plt.tight_layout()
plt.savefig("grafico_volatilidade.png", dpi=300)
print("\n 'grafico_volatilidade.png'")
plt.show()