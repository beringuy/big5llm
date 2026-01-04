
import pandas as pd
import numpy as np
import re
import os
import matplotlib.pyplot as plt
import seaborn as sns

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def count_unique_first_elements(df, colname, i):
    # Extrai o primeiro elemento de cada lista (se existir)
    first_elements = df[colname].apply(lambda x: x[i] if isinstance(x, list) and len(x) > 0 else None)
    
    # Retorna a contagem de valores únicos (ignorando None)
    unique_values = first_elements.dropna().unique()
    return unique_values

# # # # # # # # # #

def score_ploter (score_df , inv_quest , pillar_list, info):
    inv_quest_dimension_list = inv_quest["dimension"].value_counts().index.tolist()
    
    new_df = score_df[["persona"]]    
    new_df["dimension_list"] = new_df["persona"].apply(
        lambda x: [i.strip() for i in re.split(r",| and ", x)]
    )
    
    for inv_quest_dimension in inv_quest_dimension_list:
        print(inv_quest_dimension)
        tmp_df = score_df[ inv_quest[inv_quest["dimension"] == inv_quest_dimension]["item"].to_list() ]
        new_df[inv_quest_dimension + "_score"] = tmp_df.sum(axis=1)
    
    print ("--")
    print (new_df)
    
    os.makedirs("registry/" + info + "/vis/" , exist_ok=True)
    new_df.to_csv( "registry/" + info + "/vis/" + info + "_sum.csv" , index=False )
    
    ## ## ##
    
    for current_inv_quest_dimension in inv_quest_dimension_list:
        plot_df = []
        for pillar_i in range(len(pillar_list)):
            current_data = new_df[["dimension_list", current_inv_quest_dimension+"_score"]].copy()
            current_data["pillar"] = pillar_i
            current_data["fator"] = current_inv_quest_dimension
            current_data["classe"] = current_data["dimension_list"].apply(lambda x: x[pillar_i])

            plot_df.append(current_data[["classe", current_inv_quest_dimension+"_score", "fator"]]
                           .rename(columns={current_inv_quest_dimension+"_score": "score"}))

        # junta tudo
        plot_df = pd.concat(plot_df)

        plt.figure(figsize=(12,6))
        
        sns.boxplot(data=plot_df, x="classe", y="score", hue="fator", showmeans=True)
        #sns.violinplot(data=plot_df, x="classe", y="score", hue="fator", split=False, inner="quartile", linewidth=1)

        plt.title("Score Distribution - "+ current_inv_quest_dimension) # checar: dimension referente ao quest ou ao response?
        plt.xlabel("Classes")
        plt.ylabel("Score")
        plt.legend(title="Dimension") # checar: dimension referente ao quest ou ao response?
        plt.xticks(rotation=45)
        plt.grid(True, linestyle="--", alpha=0.5)
        
        plt.savefig("registry/" + info + "/vis/boxplot_" + str(current_inv_quest_dimension) + ".png",
                    dpi=300, bbox_inches="tight")
        plt.close()
        
        ## ## ##

    return None