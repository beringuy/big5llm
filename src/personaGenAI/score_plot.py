
import pandas as pd
import numpy as np
import re
import os
import matplotlib.pyplot as plt
import seaborn as sns

# # # # # # # # # #

# ADICIONAR CORES PARA MORALIDADE

palette_classes = {
    "open to experience": "#27E0F5",
    "closed to experience": "#27E0F5",
    "conscientious": "#27F598",
    "unconscientious": "#27F598",
    "extroverted": "#F5BE27",
    "introverted": "#F5BE27",
    "agreeable": "#F5277D",
    "antagonistic": "#F5277D",
    "neurotic": "#F87C63",
    "emotionally stable": "#F87C63",
}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def count_unique_first_elements(df, colname, i):
    # Extrai o primeiro elemento de cada lista (se existir)
    first_elements = df[colname].apply(lambda x: x[i] if isinstance(x, list) and len(x) > 0 else None)
    
    # Retorna a contagem de valores únicos (ignorando None)
    unique_values = first_elements.dropna().unique()
    return unique_values

# # # # # # # # # #

def score_ploter (score_df , inv_quest , psych_domain_dimensions, info):
    inv_quest_dimension_list = inv_quest["dimension"].value_counts().index.tolist()
    
    new_df = score_df[["persona"]].copy()
    new_df["persona_dimension_list"] = new_df["persona"].apply(
        lambda x: [i.strip() for i in re.split(r",| and ", x)]
    )
    
    for inv_quest_dimension in inv_quest_dimension_list:
        print(inv_quest_dimension)
        tmp_df = score_df[ inv_quest[inv_quest["dimension"] == inv_quest_dimension]["item"].to_list() ]
        new_df[inv_quest_dimension + "_score"] = tmp_df.sum(axis=1)
    
    print ("\n--")
    print (new_df)
    print ("--\n")
    
    os.makedirs("registry/" + info + "/vis/" , exist_ok=True)
    new_df.to_csv( "registry/" + info + "/vis/" + info + "_sum.csv" , index=False )
    
    ## ## ##
    
    for current_inv_quest_dimension in inv_quest_dimension_list:
        plot_df = []
        for current_psydomdim_i in range(len(psych_domain_dimensions)):
            current_data = new_df[["persona_dimension_list", current_inv_quest_dimension+"_score"]].copy()
            current_data["inv_quest_dimension"] = current_inv_quest_dimension
            current_data["classe"] = current_data["persona_dimension_list"].apply(lambda x: x[current_psydomdim_i])

            plot_df.append(current_data[["classe", current_inv_quest_dimension+"_score", "inv_quest_dimension"]]
                           .rename(columns={current_inv_quest_dimension+"_score": "score"}))

        # junta tudo
        plot_df = pd.concat(plot_df)
        
        print("plot_df:")
        print(plot_df)

        plt.figure(figsize=(12,6))
        
        sns.boxplot(data=plot_df,
                    x="classe",
                    y="score",
                    palette=palette_classes,
                    #hue="inv_quest_dimension",
                    showmeans=True)
        #sns.violinplot(data=plot_df, x="classe", y="score", hue="inv_quest_dimension", split=False, inner="quartile", linewidth=1)

        plt.title("Score Distribution - "+ current_inv_quest_dimension)
        plt.xlabel("Class(es)")
        plt.ylabel("Score")
        plt.legend(title="Dimension") # checar: dimension referente ao quest ou ao response?
        plt.xticks(rotation=45)
        plt.grid(True, linestyle="--", alpha=0.5)
        
        plt.savefig("registry/" + info + "/vis/boxplot_" + str(current_inv_quest_dimension) + ".png",
                    dpi=300, bbox_inches="tight")
        plt.close()
        
        ## ## ##

    return new_df