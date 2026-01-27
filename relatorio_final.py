from fpdf import FPDF
import pandas as pd
import os


arq_benchmark = "grafico_benchmark_final.png" 
arq_risco     = "grafico_volatilidade.png"
arq_pares     = "grafico_comparativo.png"
arq_dados     = "relatorio_performance.csv"

# gerando o Cabeçalho e Rodapé
class PDF(FPDF):
    def header(self):
        # Título
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 0, 0) # Preto
        self.cell(0, 10, '3Q Asset Management | Relatório', 0, 1, 'L')
        
        # Subtítulo
        self.set_font('Arial', 'I', 10)
        self.set_text_color(100, 100, 100) # Cinza
        self.cell(0, 5, 'Análise de Performance Proprietária - Jan/2026', 0, 1, 'L')
        
        # Linha divisória grossa
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.5)
        self.line(10, 25, 200, 25)
        self.ln(7) # Espaço após a linha

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Página {self.page_no()} - Relatório Gerado via Python Engine', 0, 0, 'C')

# Leitura do arquivo CSV
try:
    df = pd.read_csv(arq_dados)
    # Tenta filtrar a linha da 3Q (ou pega a primeira se der erro)
    row = df[df.iloc[:,0].str.contains("3Q", case=False, na=False)]
    if row.empty: row = df.iloc[0] # Fallback
    else: row = row.iloc[0]

    val_retorno = f"{row['Retorno (%)']:.2f}%"
    val_vol     = f"{row['Volatilidade (%)']:.2f}%"
    val_sharpe  = f"{row['Sharpe (Eficiência)']:.2f}"
except:
    val_retorno, val_vol, val_sharpe = "N/D", "N/D", "N/D"

# Montagem do PDF 
pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=10)


# Pg 1 Resumo Visual

pdf.add_page()

# Título da Seção
# Configura o visual da Barra
# Azul Escuro (RGB aproximado da 3Q/BTG: 0, 40, 80)
pdf.set_fill_color(0, 40, 80) 
# Texto Branco (RGB: 255, 255, 255)
pdf.set_text_color(255, 255, 255) 
# Fonte Negrito
pdf.set_font("Arial", "B", 11)

# Desenha o retângulo com fundo azul e ativa o comando fill=True.
# O espaço "#" no começo do texto serve como margem esquerda
pdf.cell(0, 8, " Indicadores e Performance vs Mercado", 0, 1, 'L', fill=True)

# Reseta as cores para o padrão do arquivo e volta para o texto preto
pdf.set_text_color(0, 0, 0) 
pdf.set_fill_color(255, 255, 255) 

# Adiciona um pequeno espaço antes do texto de baixo
pdf.ln(2)
# Guarda a posição Y do topo para alinhar as colunas
y_topo_colunas = pdf.get_y()

# Tabela do retorno anualizado, volatilidade e Sharpe a esquerda

pdf.set_xy(10, y_topo_colunas) # Trava na esquerda
largura_esq = 75

# Cabeçalho da Tabela
pdf.set_font("Arial", "B", 10)
pdf.set_fill_color(240, 240, 240) # preenche de cinza claro
pdf.cell(largura_esq, 8, "Indicadores (12m)", 1, 1, 'L', fill=True) 

# Dados da Tabela
pdf.set_font("Arial", "", 9)
altura_linha = 8

pdf.cell(45, altura_linha, "Retorno Anualizado:", 1)
pdf.cell(30, altura_linha, val_retorno, 1, 1, 'C')

pdf.cell(45, altura_linha, "Volatilidade (Risco):", 1)
pdf.cell(30, altura_linha, val_vol, 1, 1, 'C')

pdf.cell(45, altura_linha, "Índice Sharpe:", 1)
pdf.cell(30, altura_linha, val_sharpe, 1, 1, 'C')

# Texto Explicativo
pdf.set_font("Arial", "", 8)

pdf.ln(3) # Um pequeno respiro após a tabela

pdf.set_font("Arial", "", 10)


# Usando largura_esq e set_x(10) para garantir que o texto comece na margem
pdf.set_x(10) 
texto_objetivo = (
    "Gerar retornos absolutos minimizando as perdas de forma sistematizada com o "
    "objetivo de longo prazo. A estratégia é composta por um shortlist investível "
    "com base em análise fundamentalista associada ao algoritmo de market timing."
)

pdf.multi_cell(largura_esq, 4, texto_objetivo, 0, 'J') 

y_fim_esq = pdf.get_y() # O PDF calcula onde a tabela terminou

# Gráfico de Benchmark

pdf.set_xy(90, y_topo_colunas) 

if os.path.exists(arq_benchmark):
    
    pdf.image(arq_benchmark, x=90, w=100, h=65) 
else:
    pdf.cell(90, 55, "[Gráfico não encontrado]", 1, 1, 'C')

y_fim_dir = pdf.get_y() # O PDF calcula onde a imagem terminou


# Reset do cursor para não encavalar
# Pega o maior Y entre a tabela e o gráfico e adiciona uma margem
pdf.set_y(max(y_fim_esq, 55 + y_topo_colunas) + 10)

# Gráfico de volatilidade móvel 21d 
# Configura o visual da Barra
# Azul Escuro (RGB aproximado da 3Q/BTG: 0, 40, 80)
pdf.ln(5)
pdf.set_fill_color(0, 40, 80) 
# Texto Branco (RGB: 255, 255, 255)
pdf.set_text_color(255, 255, 255) 
# Fonte Negrito
pdf.set_font("Arial", "B", 11)

# Desenha o retângulo com fundo azul e ativa o comando fill=True.
# O espaço "#" no começo do texto serve como margem esquerda

pdf.cell(0, 8, " Monitoramento de Risco (Volatilidade Móvel 21d)", 0, 1, 'L', fill=True)

# Reseta as cores para o padrão e volta para o texto preto
pdf.set_text_color(0, 0, 0) 
pdf.set_fill_color(255, 255, 255) 

# Adiciona um pequeno espaço antes do texto de baixo
pdf.ln(5)

if os.path.exists(arq_risco):
    # Altura menor para caber na página (h=65)
    pdf.image(arq_risco, x=10, w=190, h=85)
else:
    pdf.cell(190, 65, "[Gráfico Volatilidade não encontrado]", 1, 1, 'C')

# Pg 2: Gráfico comparativo de peers

pdf.add_page()
pdf.set_font("Arial", "B", 11)

# Título da Seção
# Configura o visual da Barra
# Azul Escuro (RGB aproximado da 3Q/BTG: 0, 40, 80)
pdf.set_fill_color(0, 40, 80) 
# Texto Branco (RGB: 255, 255, 255)
pdf.set_text_color(255, 255, 255) 
# Fonte Negrito
pdf.set_font("Arial", "", 11)

# Desenha o retângulo com fundo azul e ativa o comando fill=True.
# O espaço "#" no começo do texto serve como margem esquerda
pdf.cell(0, 8, " Retorno: 3Q FIA x Peers", 0, 1, 'L', fill=True)

# Reseta as cores para o padrão e volta para o texto preto
pdf.set_text_color(0, 0, 0) 
pdf.set_fill_color(255, 255, 255) 
pdf.ln(3)
pdf.multi_cell(0, 5, "Correlação de retorno acumulado  dos principais players do mercado como Alaska Black FIA, Dahlia FIA, Dynamo Cougar FIA, Trígono Flagship Small Caps e Velt FIA. Observe como o 3Q FIA se comporta em relação aos concorrentes em diferentes ciclos de mercado.", 0, 'L') #texto explicativo dos fundos selecionados e objetivo da análise
pdf.ln(5)

if os.path.exists(arq_pares):
    pdf.image(arq_pares, x=10, w=190, h=90)

# Critério de Seleção dos peers
pdf.ln(5)

# Configura a Cor do Fundo com Cinza bem claro
pdf.set_fill_color(245, 245, 245) 
pdf.set_font("Arial", "B", 10)

# Título
pdf.cell(0, 8, "  Critério de Seleção dos Peers", "LTR", 1, 'L', fill=True)

# Texto do Corpo
pdf.set_font("Arial", "", 9)
texto_criterio = (
    "A definição do Peer Group obedeceu a critérios rigorosos de elegibilidade, "
    "selecionando exclusivamente fundos 'Flagship' de gestoras com comprovado track record no mercado brasileiro "
    "(Alaska, Dynamo, Velt, Dahlia e Trígono). O objetivo é submeter a estratégia do 3Q FIA a um teste de estresse "
    "relativo, comparando geração de Alpha contra gestores consolidados na gestão ativa de ações. "
    "Essa abordagem valida a tese de que o modelo quantitativo proprietário é capaz de entregar performance superior "
    "mesmo diante dos concorrentes mais resilientes e com mais tempo no mercado."
)

# Border='LBR' (Left, Bottom, Right) fecha a caixa embaixo
pdf.multi_cell(0, 5, texto_criterio, "LBR", 'J', fill=True)

# Pg 3: Correlação Cross-Asset (matriz de correlação a partir de outro código))

pdf.add_page()

# Título da Seção (Estilo Barra Azul)
pdf.set_fill_color(0, 40, 80) 
pdf.set_text_color(255, 255, 255)
pdf.set_font("Arial", "B", 11)
pdf.cell(0, 8, "  Correlação e Diversificação (Cross-Asset)", 0, 1, 'L', fill=True)

# Reseta cores para texto normal
pdf.set_text_color(0, 0, 0)
pdf.set_fill_color(255, 255, 255)
pdf.ln(5)

# Texto Explicativo
pdf.set_font("Arial", "", 10)
pdf.multi_cell(0, 5, "A matriz abaixo exibe a correlação calculada entre os fundos. O objetivo é demonstrar como o 3Q se comporta em relação aos pares (diversificação).")
pdf.ln(10)

# Inserir o PNG do heatmap de correlação gerado em matriz_correlacao.py
arq_correlacao = "heatmap_correlacao.png"

if os.path.exists(arq_correlacao):
    # Centraliza a imagem na página
    pdf.image(arq_correlacao, x=25, w=160, h=130)
else:
    pdf.cell(0, 10, "[ERRO: O arquivo 'heatmap_correlacao.png' não está na pasta]", 1, 1, 'C')

# Argumento de venda com boxe destaque
pdf.ln(5)

# Título com fundo mais escuro 
pdf.set_fill_color(230, 230, 230) # Cinza médio
pdf.set_font("Arial", "B", 10)
pdf.cell(0, 8, "  Por que 3Q Asset?", 1, 1, 'L', fill=True)

# Corpo do texto com fundo claro
pdf.set_fill_color(250, 250, 250) # Cinza quase branco
pdf.set_font("Arial", "", 9)
texto_venda = (
    "A análise de correlação cruzada (Cross-Asset) revela o diferencial competitivo do 3Q FIA: sua descorrelação estrutural. "
    "Com um coeficiente de correlação médio de 0.5 contra o mercado, o fundo atua como um poderoso diversificador de risco. "
    "Enquanto a maioria dos fundos tradicionais possui alta sobreposição de teses (correlação > 0.8), o 3Q FIA otimiza a captura prêmios "
    "de risco idiossincráticos através de um algoritmo proprietário.\n\n"
    "A inclusão do 3Q FIA no portfólio não visa apenas o retorno absoluto, mas a otimização da Fronteira Eficiente. "
    "Matematicamente, adicionar um ativo descorrelacionado e com Sharpe elevado reduz a volatilidade global da carteira "
    "do cliente, entregando um retorno ajustado ao risco superior ao de uma alocação concentrada apenas em gestores tradicionais."
)

pdf.multi_cell(0, 5, texto_venda, 1, 'J', fill=True)

# SALVANDO
pdf.output("Lamina_3Q_Final.pdf")
print("\n Pdf gerado: 'Lamina_3Q_Final.pdf'")