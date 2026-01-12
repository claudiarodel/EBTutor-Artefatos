import pandas as pd
import numpy as np

# Caminho do arquivo
caminho_arquivo = "C:/Users/User/Documents/PYTHON/CODIGOS_EXERCICIOS/EBTutor/Avaliacao_IAMSgtTotal.csv"

# --- Leitura do CSV ---
data = pd.read_csv(caminho_arquivo)

# Limpar a coluna 'aspecto' para evitar espaços extras ou caracteres estranhos
data['aspecto'] = data['aspecto'].astype(str).str.strip()

# --- Mapeamento da escala Likert ---
escala = {
    'ConcordoFortemente': 5,
    'ConcordoParcialmente': 4,
    'Neutro': 3,
    'DiscordoParcialmente': 2,
    'DiscordoFortemente': 1
}

# Converter valores das colunas da escala para float
for col in escala.keys():
    data[col] = data[col].astype(str).str.replace(',', '.')
    data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)  # Substituir NaN por 0

# --- Média ponderada por pergunta ---
# Considerando que os valores estão em porcentagem (0 a 100)
total = sum(data[col] for col in escala.keys())  # Total por linha
data['media'] = sum(data[col] * valor for col, valor in escala.items()) / total

# --- Desvio padrão ponderado por pergunta ---
def desvio_padrao_likert(row):
    total_linha = sum(row[col] for col in escala.keys())
    if total_linha == 0:
        return 0
    return np.sqrt(sum((valor - row['media'])**2 * (row[col]/total_linha) for col, valor in escala.items()))

data['desvio'] = data.apply(desvio_padrao_likert, axis=1)

# --- Mediana ponderada por pergunta ---
def mediana_likert(row):
    total_linha = sum(row[col] for col in escala.keys())
    acumulado = 0
    for col, valor in sorted(escala.items(), key=lambda x: x[1]):
        acumulado += row[col]
        if acumulado >= total_linha / 2:
            return valor
    return 5

data['mediana'] = data.apply(mediana_likert, axis=1)

# --- Métricas agregadas por aspecto ---
resumo_aspecto = data.groupby('aspecto').agg(
    media_aspecto=('media', 'mean'),
    desvio_aspecto=('desvio', 'mean'),
    mediana_aspecto=('mediana', 'median')
).reset_index()

# Garantir que 'aspecto' seja string
resumo_aspecto['aspecto'] = resumo_aspecto['aspecto'].astype(str).str.strip()

# Merge com o DataFrame original
data = data.merge(resumo_aspecto, on='aspecto', how='left')

print(data[data['aspecto']=='utilidade'][['ConcordoFortemente','ConcordoParcialmente','Neutro','DiscordoParcialmente','DiscordoFortemente']])

# Exibir resultado final
print(data[['aspecto','media','desvio','mediana','media_aspecto','desvio_aspecto','mediana_aspecto']])

# Sobrescrever o mesmo arquivo CSV
data.to_csv(caminho_arquivo, index=False)
