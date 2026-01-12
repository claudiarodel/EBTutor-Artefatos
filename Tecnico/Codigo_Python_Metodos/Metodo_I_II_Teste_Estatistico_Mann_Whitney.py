import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.utils import resample
import itertools


# -------------------------
# Hipóteses
# -------------------------
# H₀: Não é possível dizer que valores observados no grupo "Intervenção" são maiores que os valores observados no grupo "Controle". Em outras palavras, a hipótese nula é de que não há evidência estatística de que o grupo de intervenção obteve resultados maiores que aqueles do grupo Controle.
# H₁: Há evidência estatística de que o grupo de intervenção obteve resultados maiores que aqueles do grupo Controle.
# -------------------------
# Caminho do arquivo Excel
# -------------------------
caminho_arquivo = 'C:/Users/User/Documents/PYTHON/CODIGOS_EXERCICIOS/EBTutor/Avaliacao_Conhecimento_Habilidades_ADJCMDSgt_ST25_Total_Par_Aluno_Questionario_Todos_1.xlsx'

# -------------------------
# Ler os dados
# -------------------------
df = pd.read_excel(caminho_arquivo)

# -------------------------
# Separar variáveis por grupo
# -------------------------
ganho_eb = df["Ganho Normalizado EB"].dropna()   # Grupo Intervenção (Grupo que usou o EBTutor)
ganho_neb = df["Ganho Normalizado NEB"].dropna() # Grupo Controle
print(ganho_eb)
print(ganho_neb)
# Imprimir a quantidade de linhas
print("Quantidade de linhas - Grupo Intervenção:", len(ganho_eb))
print("Quantidade de linhas - Grupo Controle:", len(ganho_neb))

# -------------------------
# Médias por grupo
# -------------------------
media_eb = np.mean(ganho_eb)
mediana_eb=np.median(ganho_eb)
media_neb = np.mean(ganho_neb)
mediana_neb=np.median(ganho_neb)
dp_eb=np.std(ganho_eb, ddof=1) 
dp_neb=np.std(ganho_neb, ddof=1) 
print(f"Média do Ganho Normalizado - Grupo Intervenção: {media_eb:.3f}")
print(f"Média do Ganho Normalizado - Grupo Controle: {media_neb:.3f}\n")
#A Mediana é o valor central de uma conjunto de dados. Ela divide os dados em duas parte iguais:50% dos valores estão abaixo da mediana e 50% dos  valores estão acima da mediana
print(f"Mediana do Ganho Normalizado - Grupo Intervenção: {mediana_eb:.3f}")
print(f"Mediana do Ganho Normalizado - Grupo Controle: {mediana_neb:.3f}\n")
#print(f"Metade dos alunos do Grupo Intervenção obteve ganho até: {mediana_eb:.3f} , metade acima de: {mediana_eb:.3f}.")
#print(f"Metade dos alunos do Grupo Controle obteve ganho até: {mediana_neb:.3f} , metade acima de: {mediana_neb:.3f}.")
print(f"O desvio padrão do Ganho Normalizado - Grupo Intervenção: {dp_eb:.3f}")
print(f"O desvio padrão do Ganho Normalizado - Grupo Controle: {dp_neb:.3f}\n")

# Valores individuais
valores_eb = ganho_eb.values
valores_neb = ganho_neb.values

# Posicionamento no eixo X para cada ponto
x_eb = np.ones_like(valores_eb) * 1  # Grupo Intervenção
x_neb = np.ones_like(valores_neb) * 2  # Grupo Controle

# Medianas
mediana_eb = np.median(valores_eb)
mediana_neb = np.median(valores_neb)

plt.figure(figsize=(8,5))

# Plot dos pontos individuais
#plt.plot(x_eb, valores_eb, 'o', color='blue', alpha=0.6, label='Intervenção')
#plt.plot(x_neb, valores_neb, 'o', color='orange', alpha=0.6, label='Controle')

# Linhas conectando medianas
#plt.plot([1, 2], [mediana_eb, mediana_neb], linestyle='-', color='red', linewidth=2, label='Medianas')

# Destacar medianas
#plt.scatter([1, 2], [mediana_eb, mediana_neb], color='red', s=100, zorder=5)

# Configurações do gráfico
#plt.xticks([1, 2], ['Intervenção', 'Controle'])
#plt.ylabel('Ganho Normalizado')
#plt.title('Ganho Normalizado por Grupo com Medianas')
#plt.grid(alpha=0.3)
#plt.legend()
#plt.show()

#As distribuições são normais?
# -------------------------
# Teste de normalidade (Shapiro-Wilk)
# -------------------------
#shapiro_eb = stats.shapiro(ganho_eb)
#shapiro_neb = stats.shapiro(ganho_neb)
#print("Teste de normalidade (Shapiro-Wilk):")
#print(f"Ganho Normalizado EB: estatística={shapiro_eb[0]:.3f}, p={shapiro_eb[1]:.3f}")
#print(f"Ganho Normalizado NEB: estatística={shapiro_neb[0]:.3f}, p={shapiro_neb[1]:.3f}\n")

#if shapiro_eb[1] < 0.05 or shapiro_neb[1] < 0.05:
 # Pelo menos um dos grupos não é normal
 # -------------------------
 # Teste estatístico Mann-Whitney (p-valor exato)
 # -------------------------
#print("A distribuição de pelo menos um dos grupos não é normal: aplicar os testes não paramétricos\n")
stat, p_val = stats.mannwhitneyu(ganho_eb,ganho_neb, alternative="greater", method='exact')
teste_usado = "Mann-Whitney U (p-valor exato)"
  #magnitude da diferença entre os grupos (independente de significância estatística).
  # -------------------------
  # Tamanho do efeito r
  # -------------------------
  #Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences (2nd ed.). Hillsdale, NJ: Lawrence Erlbaum.
  #Cohen (1988) sugere critérios de 0,10, 0,30 e 0,50 como indicativos, respectivamente, de efeitos pequenos, médios e grandes.
  #n1 = len(ganho_eb)
  #n2 = len(ganho_neb)
  #N = n1 + n2
  #mean_U = n1 * n2 / 2
  #std_U = np.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
  #Z = (stat - mean_U) / std_U
  #r = abs(Z / np.sqrt(N))  # sempre positivo

  #if r < 0.1:
    #interpretacao = "desprezível"
  #elif r < 0.3:
    #interpretacao = "pequeno"
  #elif r < 0.5:
    #interpretacao = "médio"
  #else:
    #interpretacao = "grande"

  
  # -------------------------
  # Resultados
  # -------------------------
print(f"{teste_usado}: estatística={stat:.3f}, p-valor exato={p_val:.5f} ,p-valor exato={p_val*100:.2f}%")
  #print(f"Tamanho do efeito r = {r:.3f} ({interpretacao})")
  # -------------------------
  # Conclusão sobre as hipóteses
  # -------------------------
if p_val <= 0.05:
  print("✅ Rejeitamos H₀, portanto há evidência estatística de que o grupo de intervenção obteve resultados maiores que aqueles do grupo Controle.")
elif 0.05 < p_val < 0.10:
  print("⚠️ P-valor próximo de 0,05 (tendência/marginal). Interpretar com cautela.")
else:
  print("❌ Não rejeitamos H₀: Não há evidência estatística de que o grupo de intervenção obteve resultados maiores que aqueles do grupo Controle.")

 
