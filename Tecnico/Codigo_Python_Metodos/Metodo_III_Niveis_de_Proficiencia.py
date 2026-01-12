import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Dados ---
dados = {
    "Momento": ["Momento Inicial Intv", "Momento Final Intv",
                "Momento Inicial Ctrl", "Momento Final Ctrl"],
    "Excelente": ["0%", "0%", "0%", "0%"],
    "Muito Bom": ["0%", "18.182%", "7.692%", "7.692%"],
    "Bom": ["6.061%", "39.394%", "38.462%", "53.846%"],
    "Regular": ["72.727%", "42.424%", "38.462%", "30.769%"],
    "Insuficiente": ["21.212%", "0%", "15.385%", "7.692%"]
}

df = pd.DataFrame(dados)
for col in ["Excelente", "Muito Bom", "Bom", "Regular", "Insuficiente"]:
    df[col] = df[col].str.replace('%', '').astype(float)

# --- Ordem das menções ---
mencoes = ["Excelente", "Muito Bom", "Bom", "Regular", "Insuficiente"]

# --- Cores fixas ---
cores = {
    "Excelente": "blue",
    "Muito Bom": "green",
    "Bom": "orange",
    "Regular": "purple",
    "Insuficiente": "red"
}

# --- Configuração do gráfico ---
x = np.arange(len(df["Momento"]))  # eixo x = momentos
largura = 0.15  # largura das barras

fig, ax = plt.subplots(figsize=(11, 6))

# --- Deslocamento para cada menção ---
for i, mencao in enumerate(mencoes):
    ax.bar(x + (i - 2) * largura, df[mencao], largura,
           label=mencao, color=cores[mencao], alpha=0.9)
    # Rótulos nas barras
    for j, val in enumerate(df[mencao]):
        ax.text(x[j] + (i - 2) * largura, val + 1, f"{val:.0f}%",
                ha='center', va='bottom', fontsize=8)

# --- Traçar linhas de evolução entre momentos iniciais e finais ---
pares = [(0, 1), (2, 3)]
for mencao in mencoes:
    cor = cores[mencao]
    for (ini, fim) in pares:
        x_ini = x[ini] + (mencoes.index(mencao) - 2) * largura
        x_fim = x[fim] + (mencoes.index(mencao) - 2) * largura
        y_ini = df.loc[ini, mencao]
        y_fim = df.loc[fim, mencao]
        ax.plot([x_ini, x_fim], [y_ini, y_fim],
                color=cor, linestyle='--', linewidth=1.5, alpha=0.8)

# --- Configuração do eixo X ---
ax.set_xticks(x)
ax.set_xticklabels([
    "Intv - Inicial", "Intv - Final",
    "Ctrl - Inicial", "Ctrl - Final"
], ha='center', fontsize=10)

# Adiciona linhas verticais para separar grupos
ax.axvline(1.5, color='gray', linestyle=':', alpha=0.5)
ax.text(0.5, 103, "Intervenção", ha='center', va='bottom', fontsize=11, fontweight='bold')
ax.text(2.5, 103, "Controle", ha='center', va='bottom', fontsize=11, fontweight='bold')

# --- Ajustes finais ---
ax.set_ylim(0, 110)
ax.set_ylabel("Percentual (%)")
#ax.set_title("Níveis de Proficiência por Momento e Grupo")
ax.grid(True, linestyle='--', alpha=0.3)
ax.legend(title="Menções", bbox_to_anchor=(1.02, 1), loc='upper left', frameon=False)

plt.tight_layout()
plt.savefig("redessgt24_autoaperfeicoamento.png", dpi=300, bbox_inches='tight')
plt.show()
