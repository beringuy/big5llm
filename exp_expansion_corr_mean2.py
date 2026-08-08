
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches



cat = "morality" # "personality" / "morality" / "all"

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

def rename_labels(labels):
    new_labels = []

    for label in labels:
        # Remove "_score"
        label = label.replace("_score", "")

        # Moralidade
        label = label.replace("Harm_Care", "Care")

        label = label.replace("Fairness_Reciprocity", "Fairness")

        label = label.replace("In-group_Loyalty", "Loyalty")

        label = label.replace("Authority_Respect", "Authority")

        label = label.replace("Purity_Sanctity", "Sanctity")

        new_labels.append(label)

    return new_labels

#

# Empilha os valores
stack = np.stack([df.values for df in corr_list])

# Média
mean_df = pd.DataFrame(
    stack.mean(axis=0),
    index=corr_list[0].index,
    columns=corr_list[0].columns
)

# Desvio padrão
std_df = pd.DataFrame(
    stack.std(axis=0),
    index=corr_list[0].index,
    columns=corr_list[0].columns
)

# Menor valor
min_df = pd.DataFrame(
    stack.min(axis=0),
    index=corr_list[0].index,
    columns=corr_list[0].columns
)

# Maior valor
max_df = pd.DataFrame(
    stack.max(axis=0),
    index=corr_list[0].index,
    columns=corr_list[0].columns
)

#

for df in [mean_df, std_df, min_df, max_df]:
    df.index = rename_labels(df.index)
    df.columns = rename_labels(df.columns)

# ------------------------
# Texto que aparecerá nas células
# ------------------------
annot = mean_df.copy().astype(str)

for i in range(mean_df.shape[0]):
    for j in range(mean_df.shape[1]):
        annot.iloc[i, j] = (
            f"{mean_df.iloc[i, j]:.2f}\n"
            f"({min_df.iloc[i, j]:.2f}, {max_df.iloc[i, j]:.2f})"
        )

# ------------------------

mask = np.triu(np.ones_like(mean_df, dtype=bool))

plt.figure(figsize=(15, 12))

ax = sns.heatmap(
    mean_df,
    annot=annot,
    fmt="",
    linewidths=0.5,
    center=0,
    vmin=-1,
    vmax=1,
    mask=mask,
    cmap="RdBu_r",
    annot_kws={
        "fontsize":8,
        "ha":"center",
        "va":"center"
    }
)

# bloco principal
ax.add_patch(
    patches.Rectangle(
        (0, 5),
        5,
        5,
        fill=False,
        edgecolor="black",
        lw=8
    )
)

# Colocar em negrito apenas a média
for text in ax.texts:
    txt = text.get_text()

    try:
        media = float(txt.split("\n")[0])

        if abs(media) > 0.65:
            text.set_weight("bold")

    except ValueError:
        pass

plt.title("Mean - Correlation\nInducted - " + cat.upper())

plt.savefig(
    "corr/" + cat + "_mean_corr.pdf",
    dpi=300,
    bbox_inches="tight"
)

plt.close()