import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados 
# index_col=0: Diz que a primeira coluna (Datas) é o índice (Eixo X)
# parse_dates=True: Mantém datas e não texto
df = pd.read_csv("dados_finais.csv", index_col=0, parse_dates=True)

# Normalização (Base 100)
# Divide a tabela inteira pela primeira linha e multiplica por 100. Isso normaliza tudo.
df_normalizado = (df / df.iloc[0]) * 100

# Plotagem do Gráfico
plt.figure(figsize=(12, 6)) # Tamanho da imagem (12 de largura, 6 de altura)

# Desenha as linhas
for coluna in df_normalizado.columns:
    # Destaca a 3Q destacando para o cliente
    if "3Q" in coluna:
        plt.plot(df_normalizado.index, df_normalizado[coluna], label=coluna, linewidth=3, color='black')
    else:
        # Os outros ficam com linhas mais suaves
        plt.plot(df_normalizado.index, df_normalizado[coluna], label=coluna, linewidth=1.5, alpha=0.7)

# Estética do Gráfico
plt.title("Rentabilidade Acumulada", fontsize=14, fontweight='bold')
plt.xlabel("Data")
plt.ylabel("Retorno Acumulado (Base 100)")
plt.legend() # Mostra a legenda com os nomes
plt.grid(True, linestyle='--', alpha=0.5) # Coloca uma grade suave no fundo

# Salvar e Mostrar
plt.tight_layout()
plt.savefig("grafico_comparativo.png", dpi=300) # Salva em alta resolução
print("'grafico_comparativo.png'")
plt.show() # Abre a janela pra você ver