
import pandas as pd
import re
import matplotlib.pyplot as plt


df_new_scores_p = pd.read_csv("registry/20251025_143026_gemma3:4b_answersScores.csv")
df_new_scores_p

levels = ["highly ", "slightly "]

openn = ["open to experience", "closed to experience"]
consc = ["conscientious", "unconscientious"]
extra = ["extroverted", "introverted"]
agree = ["agreeable", "antagonistic"]
neuro = ["neurotic", "emotionally stable"]

factors = [openn,consc,extra,agree,neuro,]

def score_ploter (score_df , factors , levels):
    
    tmp_df = score_df.drop("persona", axis=1)
    
    for factor in range (len () ):
        pass
    
    return None



df_new_scores = df_new_scores_p.drop("persona", axis=1)
df_new_scores
df_new_scores.dtypes

# O - openness to experience
df_fac1 = df_new_scores.iloc[:, 4::5]
df_fac1["o_score"] = df_fac1.sum(axis=1)
df_fac1["persona"] = df_new_scores_p["persona"]
df_fac1
# E - extraversion
df_fac2 = df_new_scores.iloc[:, 0::5]
df_fac2["e_score"] = df_fac2.sum(axis=1)
df_fac2["persona"] = df_new_scores_p["persona"]
df_fac2
# A - agreeableness
df_fac3 = df_new_scores.iloc[:, 1::5]
df_fac3["a_score"] = df_fac3.sum(axis=1)
df_fac3["persona"] = df_new_scores_p["persona"]
df_fac3
# C - conscientiousness
df_fac4 = df_new_scores.iloc[:, 2::5]
df_fac4["c_score"] = df_fac4.sum(axis=1)
df_fac4["persona"] = df_new_scores_p["persona"]
df_fac4
# N - neuroticism
df_fac5 = df_new_scores.iloc[:, 3::5]
df_fac5["n_score"] = df_fac5.sum(axis=1)
df_fac5["persona"] = df_new_scores_p["persona"]
df_fac5

df_short = df_fac1[["persona", "o_score"]]
df_short["c_score"] = df_fac4["c_score"]
df_short["e_score"] = df_fac2["e_score"]
df_short["a_score"] = df_fac3["a_score"]
df_short["n_score"] = df_fac5["n_score"]

df_short["persona_list"] = df_short["persona"].apply(
    lambda x: [i.strip() for i in re.split(r",| and ", x)]
)

df_short
df_short["persona"].value_counts()
df_short.columns

#########################

for fator_n in range(len(factors)):
    print(fator_n)
    fator_alvo = factors[fator_n] # 0 - openn // 1 - consc // 2 - extra // 3 - agree // 4 - neuro
    print(fator_alvo)
    
    # o_score // c_score // e_score // a_score // n_score
    if fator_n == 0:
        score_alvo = "o_score"
    if fator_n == 1:
        score_alvo = "c_score"
    if fator_n == 2:
        score_alvo = "e_score"
    if fator_n == 3:
        score_alvo = "a_score"
    if fator_n == 4:
        score_alvo = "n_score"
    
    categorias = ["highly " + fator_alvo[0], fator_alvo[0], "slightly " + fator_alvo[0], "slightly " + fator_alvo[1], fator_alvo[1], "highly " + fator_alvo[1]]
    df_filtrado = df_short[df_short["persona_list"].apply(lambda lista: any(x in categorias for x in lista))]
    
    # Criar um dicionário com listas de valores de score por categoria
    dados = {
        cat: df_filtrado[df_filtrado["persona_list"].apply(lambda x: cat in x)][score_alvo]
        for cat in categorias
    }
    
    # Gerar o boxplot
    plt.figure(figsize=(8, 5))
    plt.boxplot(dados.values(), labels=dados.keys(), patch_artist=True, showmeans=True)
    
    plt.title("Distribuição de score: " + fator_alvo[0] + " e " + fator_alvo[1])
    plt.xlabel("Grau do fator")
    plt.xticks(rotation=45)
    plt.ylabel("Score")
    plt.grid(True, linestyle="--", alpha=0.5)
    
    
    plt.savefig("vis/boxplot_" + fator_alvo[0] + "_" + fator_alvo[1] + ".png", dpi=300, bbox_inches="tight")
    #plt.show()