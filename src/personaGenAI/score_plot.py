
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
    inv_factor_list = inv_quest["factor"].value_counts().index.tolist()
    
    new_df = score_df[["persona"]]    
    new_df["factor_list"] = new_df["persona"].apply(
        lambda x: [i.strip() for i in re.split(r",| and ", x)]
    )
    
    for inv_factor in inv_factor_list:
        print(inv_factor)
        tmp_df = score_df[ inv_quest[inv_quest["factor"] == inv_factor]["item"].to_list() ]
        new_df[inv_factor + "_score"] = tmp_df.sum(axis=1)
    
    print ("--")
    print (new_df)
    
    os.makedirs("registry/" + info + "/vis/" , exist_ok=True)
    new_df.to_csv( "registry/" + info + "/vis/" + info + "_sum.csv" , index=False )
    
    ## ## ##
    
    for current_inv_factor in inv_factor_list:
        plot_df = []
        for pillar_i in range(len(pillar_list)):
            current_data = new_df[["factor_list", current_inv_factor+"_score"]].copy()
            current_data["pillar"] = pillar_i
            current_data["fator"] = current_inv_factor
            current_data["classe"] = current_data["factor_list"].apply(lambda x: x[pillar_i])

            plot_df.append(current_data[["classe", current_inv_factor+"_score", "fator"]]
                           .rename(columns={current_inv_factor+"_score": "score"}))

        # junta tudo
        plot_df = pd.concat(plot_df)

        plt.figure(figsize=(12,6))
        sns.boxplot(data=plot_df, x="classe", y="score", hue="fator", showmeans=True)
        plt.title("Distribuição de score")
        plt.xlabel("Classes")
        plt.ylabel("Score")
        plt.legend(title="Fator")
        plt.xticks(rotation=45)
        plt.grid(True, linestyle="--", alpha=0.5)
        
        plt.savefig("registry/" + info + "/vis/boxplot_" + str(current_inv_factor) + ".png",
                    dpi=300, bbox_inches="tight")
        plt.close()
        
        ## ## ##

    return None