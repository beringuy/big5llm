
import pandas as pd
import numpy as np
import re
import os
import matplotlib.pyplot as plt
import seaborn as sns
import ast # para converter string → lista real

from global_info import palette_classes
from global_info import ordered_classes
from global_info import PSYCH_DOMAINS
from global_info import INV_QUEST

#########################################################################################################



#########################################################################################################

source_id = "20260206_221713__ollama_gemma3:27b__p_personality_bigfive__i_ipip50__stateless"
baseline_id = "20260206_135601__ollama_gemma3:27b__p_unspecified__i_ipip50__stateless"

# # # # #

data_df = pd.read_csv("registry/" + source_id + "/vis/" + source_id + "_sum.csv")
data_df

baseline_df = pd.read_csv("registry/" + baseline_id + "/vis/" + baseline_id + "_sum.csv")
baseline_df

# # # # #

selected_inv_quest = re.search(r'(?<=__i_).*?(?=__)', source_id).group()
selected_inv_quest

selected_psych_domain = re.search(r'(?<=__p_).*?(?=__)', source_id).group()
selected_psych_domain

inv_quest = pd.read_csv(INV_QUEST[selected_inv_quest]['path'])
inv_quest

psych_domain_dimensions = PSYCH_DOMAINS[selected_psych_domain]
psych_domain_dimensions.pop("BASE_PROMPT", None)
psych_domain_dimensions

inv_quest_dimension_list = inv_quest["dimension"].value_counts().index.tolist()
inv_quest_dimension_list

#########################################################################################################



#########################################################################################################

current_base = baseline_df.drop(['persona','persona_dimension_list'], axis = 1)
current_base

baseline_list = []

for i in current_base:
    baseline_list.append([i[:-6], int(current_base[i][0])])

baseline_list

# # # # #

constr = []
for trait in psych_domain_dimensions:
    print(trait)
    for pole in psych_domain_dimensions[trait]:
        print(pole)
        constr.append([pole, trait])
constr

# # # # #

for i in baseline_list:
    #print(i)
    for j in constr:
        print(j)
        if i[0] == j[1]:
            j.append(i[1])

constr

# # # # # # # # # #

for current_inv_quest_dimension in inv_quest_dimension_list:
        plot_df = []
        for current_psydomdim_i in range(len(psych_domain_dimensions)):
            current_data = data_df[["persona_dimension_list", current_inv_quest_dimension+"_score"]].copy()
            current_data
            current_data["inv_quest_dimension"] = current_inv_quest_dimension
            current_data
            current_data["persona_dimension_list"] = current_data["persona_dimension_list"].apply(ast.literal_eval) # converte string → lista real
            current_data["classe"] = current_data["persona_dimension_list"].apply(lambda x: x[current_psydomdim_i])
            current_data

            plot_df.append(current_data[["classe", current_inv_quest_dimension+"_score", "inv_quest_dimension"]]
                           .rename(columns={current_inv_quest_dimension+"_score": "score"}))

        # junta tudo
        plot_df = pd.concat(plot_df)
        
        print("plot_df:")
        print(plot_df)
        
        # ordena as classes
        # manter apenas as classes que existem no dataframe
        ordem_classes_presentes = [c for c in ordered_classes if c in plot_df["classe"].unique()]
        ordem_classes_presentes

        plt.figure(figsize=(12,6))
        
        sns.boxplot(data=plot_df,
                    x="classe",
                    y="score",
                    palette=palette_classes,
                    #hue="inv_quest_dimension",
                    order=ordem_classes_presentes,
                    showmeans=True,
                    meanprops={
                        "marker": "o",
                        "markerfacecolor": "black",
                        "markeredgecolor": "black",
                        "markersize": 5
                        }
                    )
        #sns.violinplot(data=plot_df, x="classe", y="score", hue="inv_quest_dimension", split=False, inner="quartile", linewidth=1)
        
        ##############
        
        baseline_por_classe = plot_df.groupby("classe")["score"].mean().reset_index()
        baseline_por_classe

        for i in constr:
            print(i[0])

            for index, row in baseline_por_classe.iterrows():
                #print(row['classe'])

                if i[0] in row['classe']:
                    baseline_por_classe.loc[index, 'score'] = i[2]
                    print ("MUDOU:", row)

        baseline_por_classe
        baseline_por_classe = baseline_por_classe.set_index("classe")["score"]
        
        ##############
        
        ax = plt.gca()

        # exemplo: baseline por classe (ajuste conforme sua lógica)
        baseline_por_classe2 = plot_df.groupby("classe")["score"].mean()
        # ou use outra métrica (mediana, valor fixo, etc.)

        for i, classe in enumerate(ordem_classes_presentes):
            baseline = baseline_por_classe[classe]

            # desenha uma linha horizontal "curta" na posição da classe
            ax.hlines(
                y=baseline,
                #y=47,
                xmin=i - 0.3,
                xmax=i + 0.3,
                colors="red",
                linestyles="dashed",
                linewidth=2,
                zorder=10  # 🔥 garante que fique por cima
            )
        
        ##############

        plt.title("Experiment: " + source_id + "\n\nScore Distribution - " + current_inv_quest_dimension)
        plt.xlabel("Class(es)")
        plt.ylabel("Score")
        #plt.legend(title="Dimension") # checar: dimension referente ao quest ou ao response?
        plt.xticks(rotation=90) # 45 > 90
        plt.grid(True, linestyle="--", alpha=0.5)
        
        plt.savefig("teste1" + source_id + "_" + str(current_inv_quest_dimension) + ".png",
                    dpi=300, bbox_inches="tight")
        plt.close()

