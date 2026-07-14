
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches



cat = "all" # "personality" / "morality" / "all"

if cat == "personality":
    corr_list = [ # personality
        pd.read_csv("corr/groq_openaigpt-oss-120b__p_personality_bigfive/groq_openaigpt-oss-120b__p_personality_bigfive_corr_values_csv.csv", index_col="Unnamed: 0"),
        pd.read_csv("corr/ollama_gemma3:27b__p_personality_bigfive/ollama_gemma3:27b__p_personality_bigfive_corr_values_csv.csv", index_col="Unnamed: 0"),
        pd.read_csv("corr/ollama_gpt-oss:20b__p_personality_bigfive/ollama_gpt-oss:20b__p_personality_bigfive_corr_values_csv.csv", index_col="Unnamed: 0"),
        pd.read_csv("corr/ollama_qwen2.5:14b__p_personality_bigfive/ollama_qwen2.5:14b__p_personality_bigfive_corr_values_csv.csv", index_col="Unnamed: 0"),    
        ]
elif cat == "morality":
    corr_list = [ # morality
        pd.read_csv("corr/groq_openaigpt-oss-120b__p_morality_mft_v2/groq_openaigpt-oss-120b__p_morality_mft_v2_corr_values_csv.csv", index_col="Unnamed: 0"),
        pd.read_csv("corr/ollama_gemma3:27b__p_morality_mft_v2/ollama_gemma3:27b__p_morality_mft_v2_corr_values_csv.csv", index_col="Unnamed: 0"),
        pd.read_csv("corr/ollama_gpt-oss:20b__p_morality_mft_v2/ollama_gpt-oss:20b__p_morality_mft_v2_corr_values_csv.csv", index_col="Unnamed: 0"),
        pd.read_csv("corr/ollama_qwen2.5:14b__p_morality_mft_v2/ollama_qwen2.5:14b__p_morality_mft_v2_corr_values_csv.csv", index_col="Unnamed: 0"),    
        ]
elif cat == "all":
    corr_list = [ # all
        pd.read_csv("corr/groq_openaigpt-oss-120b__p_personality_bigfive/groq_openaigpt-oss-120b__p_personality_bigfive_corr_values_csv.csv", index_col="Unnamed: 0"),
        pd.read_csv("corr/ollama_gemma3:27b__p_personality_bigfive/ollama_gemma3:27b__p_personality_bigfive_corr_values_csv.csv", index_col="Unnamed: 0"),
        pd.read_csv("corr/ollama_gpt-oss:20b__p_personality_bigfive/ollama_gpt-oss:20b__p_personality_bigfive_corr_values_csv.csv", index_col="Unnamed: 0"),
        pd.read_csv("corr/ollama_qwen2.5:14b__p_personality_bigfive/ollama_qwen2.5:14b__p_personality_bigfive_corr_values_csv.csv", index_col="Unnamed: 0"),    
        pd.read_csv("corr/groq_openaigpt-oss-120b__p_morality_mft_v2/groq_openaigpt-oss-120b__p_morality_mft_v2_corr_values_csv.csv", index_col="Unnamed: 0"),
        pd.read_csv("corr/ollama_gemma3:27b__p_morality_mft_v2/ollama_gemma3:27b__p_morality_mft_v2_corr_values_csv.csv", index_col="Unnamed: 0"),
        pd.read_csv("corr/ollama_gpt-oss:20b__p_morality_mft_v2/ollama_gpt-oss:20b__p_morality_mft_v2_corr_values_csv.csv", index_col="Unnamed: 0"),
        pd.read_csv("corr/ollama_qwen2.5:14b__p_morality_mft_v2/ollama_qwen2.5:14b__p_morality_mft_v2_corr_values_csv.csv", index_col="Unnamed: 0"),    
        ]
else:
    print("Erro!!!")

corr_list



#

cols_to_drop = [
    'Harm_Care_pt1_score',
    'Harm_Care_pt2_score',
    'Fairness_Reciprocity_pt1_score',
    'Fairness_Reciprocity_pt2_score',
    'In-group_Loyalty_pt1_score',
    'In-group_Loyalty_pt2_score',
    'Authority_Respect_pt1_score',
    'Authority_Respect_pt2_score',
    'Purity_Sanctity_pt1_score',
    'Purity_Sanctity_pt2_score',
]

corr_list = [
    df.drop(index=cols_to_drop, columns=cols_to_drop)
    for df in corr_list
]

#

# Empilha os valores (3, linhas, colunas)
stack = np.stack([df.values for df in corr_list])

# Média célula a célula
mean_df = pd.DataFrame(stack.mean(axis=0), index=corr_list[0].index, columns=corr_list[0].columns)

# Desvio padrão célula a célula
std_df = pd.DataFrame(stack.std(axis=0), index=corr_list[0].index, columns=corr_list[0].columns)


# # # # #

mask = np.triu(np.ones_like(mean_df, dtype=bool))

plt.figure(figsize=(15, 12))
ax = sns.heatmap(mean_df,
            annot=True,
            fmt=".2f",
            linewidths=0.5,            
            center=0,
            vmin=-1,
            vmax=1,
            mask = mask,
            cmap="RdBu" + "_r",
            )

# bloco principal
ax.add_patch(patches.Rectangle(
    (0, 5), # coluna, linha inicial
    5,      # largura (número de colunas)
    5,      # altura (número de linhas)
    fill=False,
    edgecolor="black",
    lw=8))

# Aplicar negrito para valores > 0.65
for text in ax.texts:
    try:
        value = float(text.get_text())
        if value > 0.65 or value < -0.65:
            text.set_weight('bold')
    except ValueError:
        pass  # ignora células mascaradas ou vazias

plt.title("Mean - Correlation\nInducted - " + cat.upper())

plt.savefig("corr/" + cat + "_mean_corr.pdf", dpi=300, bbox_inches="tight")
plt.close()

# # # # #

plt.figure(figsize=(15, 12))
ax = sns.heatmap(std_df,
            annot=True,
            fmt=".2f",
            linewidths=0.5,            
            #center=0.5,
            vmin=std_df.values.min(),
            vmax=std_df.values.max(),
            mask = mask,
            cmap="RdYlGn" + "_r",
            )

# bloco principal
ax.add_patch(patches.Rectangle(
    (0, 5), # coluna, linha inicial
    5,      # largura (número de colunas)
    5,      # altura (número de linhas)
    fill=False, edgecolor="black", lw=8))

# Aplicar negrito para valores < 0.1
for text in ax.texts:
    try:
        value = float(text.get_text())
        if value < 0.06:
            text.set_weight('bold')
    except ValueError:
        pass  # ignora células mascaradas ou vazias

plt.title("Standard Deviation - Correlation\nInducted - " + cat.upper())

plt.savefig("corr/" + cat + "_stf_dev_corr.pdf", dpi=300, bbox_inches="tight")
plt.close()