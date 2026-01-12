import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import nltk
import warnings
import numpy as np
from wordcloud import WordCloud
from nltk.corpus import stopwords



# Inibir warnings futuros
warnings.filterwarnings("ignore", category=FutureWarning)

# 1. Carregar dados
df = pd.read_excel("dados_idt_bio_imp_dig.xlsx")
comentarios = df["avaliacao"].dropna().tolist()

# 2. Gerar representações semânticas (embeddings).-  transformar frases em vetores numéricos (chamados embeddings).
#O SentenceTransformer pega texto e transforma em números que representam o sentido do texto.
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
embeddings = model.encode(comentarios)

# 3. Agrupamento com KMeans- Pega os vetores (embeddings) e tenta dividir em k grupos (clusters).C
num_clusters =2
kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
labels = kmeans.fit_predict(embeddings)

df.loc[df["avaliacao"].notna(), "cluster"] = labels

# 4. Gerar nomes automáticos para clusters usando TF-IDF
nltk.download("stopwords")
stopwords_pt = nltk.corpus.stopwords.words("portuguese")

vectorizer = TfidfVectorizer(stop_words=stopwords_pt)
X = vectorizer.fit_transform(df["avaliacao"].dropna())
termos = vectorizer.get_feature_names_out()

cluster_names = {}
print("\n=== Nomes automáticos dos clusters ===")
for i in range(num_clusters):
    indices = df[df["cluster"] == i].index
    cluster_tfidf = X[indices].mean(axis=0)
    top = cluster_tfidf.A1.argsort()[-3:][::-1]  # top 3 termos
    palavras_chave = [termos[t] for t in top]
    nome_cluster = " / ".join(palavras_chave)
    cluster_names[i] = nome_cluster
    print(f"{nome_cluster}")

    exemplos = df[df["cluster"] == i]["avaliacao"].head(3).tolist()
    print("Exemplos:")
    for e in exemplos:
        print("-", e)
    print()

# 5. Adicionar nomes automáticos ao DataFrame
df["cluster_nome"] = df["cluster"].map(cluster_names)


# 6. Substituir tags automáticas por rótulos personalizados - Rótulação e Tags
tags_personalizadas = {
    0: "Elogio_Usabilidade_Relevância_Utilidade",
    2: "Sugestões_Melhorias"
    }
df["cluster_tag"] = df["cluster"].map(tags_personalizadas)



# 6b. Ajustes automáticos com base em palavras-chave
# Exemplo: se o comentário contém "erro", "bug" ou "travou", força para "Problemas_Técnicos"
#df.loc[df["avaliacao"].str.contains("não consegui utilizar|mozilla|não apareceu|Não abre|não funciona|não consegui|vpn|infelizmente|erro|bug|travou|problemas técnicos|não funcionou", case=False, na=False), "cluster_tag"] = "Problemas_Técnicos"

# Outro exemplos...: se contém "sugestão" ou "poderia melhorar", força para "Sugestões"
df.loc[df["avaliacao"].str.contains("intranet|Interação|Designe|aprimorado|acesso na internet|disponibilizar na internet|Poderia|poderia|Apresentar|agrupamento melhor|deve ser melhor|melhor avaliada|deveridt_bio_imp_dig ser|poderia ter|integração|acredito|poderia ser|Orientar|sugestao|poderia melhorar|melhoria|layout|orientar", case=False, na=False), "cluster_tag"] = "Sugestões_Melhorias"

df.loc[df["avaliacao"].str.contains("Muito útil|Facilidade|muito interessante|bons|Muito bom|CHA|Muito boa|muito úteis|excelente|ótimo|auxiliar|esclareceu|excelente", case=False, na=False), "cluster_tag"] = "Elogio_Usabilidade_Relevância_Utilidade"


#df.loc[df["avaliacao"].str.contains("incoerente|não condizente|não entendi|não constou", case=False, na=False), "cluster_tag"] = "Duvidas_Clareza_Feedback"

#df.loc[df["avaliacao"].str.contains("mais tempo|período maior|nada a declarar", case=False, na=False), "cluster_tag"] = "Neutro"

print(df["cluster_tag"])

# ============================
# 7. NUVEM DE PALAVRAS GERAL
# ============================
# Junta todos os comentários em uma única string
texto_todos = " ".join(df["avaliacao"].dropna().tolist())

# Stopwords em português
stopwords_wc = set(stopwords_pt)

stopwords_wc = set(stopwords.words("portuguese"))
stopwords_wc.update([
    "pois", "porque", "porém", "entretanto", "assim", 
    "também", "ainda", "além", "ser", "estar"
])


# Gerar nuvem
wordcloud = WordCloud(
    width=1200,
    height=600,
    background_color="white",
    stopwords=stopwords_wc,
    collocations=True
).generate(texto_todos)

# Plotar
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Nuvem de Palavras - Comentários dos Alunos", fontsize=16)
plt.tight_layout()
# ===== SALVAR =====
plt.savefig("nuvem_palavras_comentarios_idtbioimpdig.png", dpi=300, bbox_inches="tight")
plt.show()




#7. Análise quantitativa: distribuição dos clusters
print("\n=== Distribuição de Comentários por Categoria ===")
distribuicao = df["cluster_tag"].value_counts()
#print(distribuicao)

# Calcular percentual
percentual = (distribuicao / 11) * 100
print("\n=== Percentual de Comentários por Categoria ===")
print(percentual.round(2))  # arredonda para 2 casas decimais
soma = percentual.sum()
restante = 100 - soma
percentual["Sem_Comentários"] = restante

# 8. Visualização: gráfico de barras com percentuais
#plt.figure(figsize=(8, 5))
#percentual.plot(kind="bar", color="skyblue")
#plt.title("Distribuição de Comentários por Categoria (%)")
#plt.xlabel("Categoria")
#plt.ylabel("Percentual de Comentários")

# Rotaciona os rótulos do eixo X para diagonal
#plt.xticks(rotation=45, ha="right")  # 45 graus e alinhados à direita

#plt.tight_layout()

# Adicionar os valores percentuais acima das barras
#for i, v in enumerate(percentual):
 #   plt.text(i, v + 0.5, f"{v:.1f}%", ha="center", fontsize=9)

#plt.savefig("grafico_percentual_clusters.png")
#plt.show()

plt.figure(figsize=(8, 5))

# Importante: capturar o objeto do gráfico
ax = percentual.plot(kind="bar", color="skyblue")

plt.title("Distribuição de Comentários por Categoria (%)")
plt.xlabel("Categoria")
plt.ylabel("Percentual de Comentários")

# --- Construção dos rótulos ---
novos_rotulos = []
for idx in percentual.index:
    if isinstance(idx, int):  # índice numérico
        novos_rotulos.append(tags_personalizadas.get(idx, str(idx)))
    else:
        novos_rotulos.append(str(idx))

plt.xticks(
    ticks=range(len(percentual)),
    labels=novos_rotulos,
    rotation=45,
    ha="right"
)

# --- Remover moldura superior e direita ---
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# --- Adicionar valores nas barras ---
for i, v in enumerate(percentual):
    ax.text(i, v + 0.5, f"{v:.1f}%", ha="center", va="bottom", fontsize=10)

plt.tight_layout()
# ===== SALVAR =====
plt.savefig("grafico_percentual_clusters_idtbioimpdig.png", dpi=300, bbox_inches="tight")
plt.show()
plt.show()

# 8. Visualização: gráfico de barras
#plt.figure(figsize=(8, 5))
#distribuicao.plot(kind="bar", color="skyblue")
#plt.title("Distribuição de Comentários por Categoria")
#plt.xlabel("Categoria")
#plt.ylabel("Quantidade de Comentários")
#plt.xticks(rotation=0)
#plt.tight_layout()
#plt.savefig("grafico_distribuicao_clusters.png")
#plt.show()

# 9. Salvar resultados finais
df.to_excel("dados_com_clusters_embeddings_idt_bio_imp_dig.xlsx", index=False)


#--------------------Geração do texto Interpretativo------------------------

# 1. Abrir o arquivo Excel já gerado
df = pd.read_excel("dados_com_clusters_embeddings_idt_bio_imp_dig.xlsx")

# 2. Calcular distribuição e percentuais
distribuicao = df["cluster_tag"].value_counts()
percentual = (distribuicao / 11) * 100

#texto_final = "\n=== Relatório Final de Interpretação Qualitativa Indutiva ===\n"
#texto_final += "A análise qualitativa dos comentários dos alunos permitiu identificar categorias distintas, cada uma com seu peso percentual e significado qualitativo.\n"

# 3. Gerar texto encadeado
texto_final = "=== Relatório Final de Interpretação Qualitativa Indutiva ===\n\n"
texto_final += "A análise dos comentários dos alunos revelou diferentes dimensões da experiência com a ferramenta. "


"""
if "Elogio_Usabilidade_Relevância_Utilidade" in percentual.index:
    texto_final += f"{percentual['Elogio_Usabilidade_Relevância_Utilidade']:.1f}% dos comentários destacaram aspectos positivos, "
    texto_final += "como facilidade de uso e relevância, mostrando uma boa impressão do EBTutor.\n"
    exemplos = df[df["cluster_tag"] == "Elogio_Usabilidade_Relevância_Utilidade"]["avaliacao"].head(3).tolist()
    texto_final += "Exemplos: " + " | ".join(exemplos) + "\n"

if "Problemas_Técnicos" in percentual.index:
    texto_final += f"Por outro lado, {percentual['Problemas_Técnicos']:.1f}% dos alunos relataram falhas técnicas, "
    texto_final += "indicando barreiras de acesso que dificultaram a experiência.\n"
    exemplos = df[df["cluster_tag"] == "Problemas_Técnicos"]["avaliacao"].head(3).tolist()
    texto_final += "Exemplos: " + " | ".join(exemplos) + "\n"

if "Sugestões_Melhorias" in percentual.index:
    texto_final += f"Além disso, {percentual['Sugestões_Melhorias']:.1f}% dos comentários trouxeram sugestões de melhorias, "
    texto_final += "o que demonstra disposição para contribuir com o desenvolvimento da ferramenta.\n"
    exemplos = df[df["cluster_tag"] == "Sugestões_Melhorias"]["avaliacao"].head(3).tolist()
    texto_final += "Exemplos: " + " | ".join(exemplos) + "\n"

if "Questionamento_Feedbacks" in percentual.index:
    texto_final += f"Já {percentual['Questionamento_Feedbacks']:.1f}% dos alunos apresentaram dúvidas ou pedidos de esclarecimento, "
    texto_final += "apontando um espaço para refinamento.\n"
    exemplos = df[df["cluster_tag"] == "Questionamento_Feedbacks"]["avaliacao"].head(3).tolist()
    texto_final += "Exemplos: " + " | ".join(exemplos) + "\n"

if "Neutro" in percentual.index:
    texto_final += f"Por fim, {percentual['Neutro']:.1f}% dos comentários foram neutros, "
    texto_final += "sem carga emocional ou crítica.\n"
    exemplos = df[df["cluster_tag"] == "Neutro"]["avaliacao"].head(3).tolist()
    texto_final += "Exemplos: " + " | ".join(exemplos) + "\n"
texto_final += "\n\nEm síntese, os resultados revelam uma boa impressão da ferramenta, assim como as dificuldades técnicas de acesso, encontradas pelos alunos, tendo em vista o EBTutor estar hospedado na intranet do EB."
texto_final += "Além de sugestões construtivas e dúvidas que apontam para oportunidades de refinamento e melhoria contínua."


# 3. Relatório qualitativo indutivo com exemplos
"""
texto_final = "=== Relatório Final de Interpretação Qualitativa Indutiva ===\n\n"
texto_final += "A análise dos comentários dos alunos revelou diferentes dimensões da experiência com a ferramenta. "



for categoria, perc in percentual.items():
    texto_final += f"\n{perc:.1f}% dos comentários foram classificados como '{categoria}'. "
    
    # Breve interpretação
    if categoria == "Problemas_Técnicos":
        texto_final += "Os alunos relataram falhas técnicas que dificultaram a experiência, indicando barreiras de acesso. "
    elif categoria == "Sugestões_Melhorias":
        texto_final += "Os alunos propuseram melhorias, revelando disposição para contribuir com o desenvolvimento. "
    elif categoria == "Elogio_Usabilidade_Relevância_Utilidade":
        texto_final += "Os alunos destacaram aspectos positivos como facilidade de uso e relevância, reforçando percepção de valor. "
    elif categoria == "Questionamento_Feedbacks":
        texto_final += "Foram registradas dúvidas e pedidos de esclarecimento, apontando necessidade de refinamento da ferramenta. "
    elif categoria == "Neutro":
        texto_final += "Comentários sem carga emocional ou crítica, refletindo menor envolvimento. "
    
    # Exemplos representativos
    exemplos = df[df["cluster_tag"] == categoria]["avaliacao"].head(3).tolist()
    texto_final += "Exemplos: " + " | ".join(exemplos) + "\n"

texto_final += "\n\nEm síntese, os resultados revelam uma boa impressão da ferramenta."
texto_final += "Além do mais fornecem sugestões construtivas para expandir as funcionalidades da ferramenta e dúvidas, que apontam para oportunidades de refinamento e melhoria contínua."



# 4. Mostrar no console
print(texto_final)

# 5. (Opcional) Salvar em arquivo TXT
with open("relatorio_final_interpretacao_idt_bio_imp_dig.txt", "w", encoding="utf-8") as f:
    f.write(texto_final)




