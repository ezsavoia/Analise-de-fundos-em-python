import pandas as pd
import numpy as np

# Carrega os dados
df = pd.read_csv("dados_finais.csv", index_col=0, parse_dates=True)
retornos_diarios = df.pct_change().dropna()

# Calcula KPIs de performance
retorno_anual = (1 + retornos_diarios.mean()) ** 252 - 1
volatilidade_anual = retornos_diarios.std() * np.sqrt(252)
sharpe_ratio = retorno_anual / volatilidade_anual

tabela_kpis = pd.DataFrame({
    "Retorno (%)": retorno_anual * 100,
    "Volatilidade (%)": volatilidade_anual * 100,
    "Sharpe": sharpe_ratio
})

tabela_kpis = tabela_kpis.sort_values(by="Sharpe", ascending=False).round(2)

# Calcula Correlação 
matriz_correlacao = retornos_diarios.corr()

# Salvando a tabela de NOTAS (KPIs)
tabela_kpis.to_csv("relatorio_performance.csv")
print("KPIs salvos em 'relatorio_performance.csv'")

# Salva a tabela de Correlação
matriz_correlacao.to_csv("matriz_correlacao.csv")
print("Correlação salva em 'matriz_correlacao.csv'")

print(tabela_kpis)