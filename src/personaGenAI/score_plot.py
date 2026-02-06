
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
    "highly open to experience": "#27E0F5",
    "highly closed to experience": "#27E0F5",
    "slightly open to experience": "#27E0F5",
    "slightly closed to experience": "#27E0F5",
    
    "conscientious": "#27F598",
    "unconscientious": "#27F598",
    "highly conscientious": "#27F598",
    "highly unconscientious": "#27F598",
    "slightly conscientious": "#27F598",
    "slightly unconscientious": "#27F598",
    
    "extroverted": "#F5BE27",
    "introverted": "#F5BE27",
    "highly extroverted": "#F5BE27",
    "highly introverted": "#F5BE27",
    "slightly extroverted": "#F5BE27",
    "slightly introverted": "#F5BE27",
    
    "agreeable": "#F5277D",
    "antagonistic": "#F5277D",
    "highly agreeable": "#F5277D",
    "highly antagonistic": "#F5277D",
    "slightly agreeable": "#F5277D",
    "slightly antagonistic": "#F5277D",
    
    "neurotic": "#F87C63",
    "emotionally stable": "#F87C63",
    "highly neurotic": "#F87C63",
    "highly emotionally stable": "#F87C63",
    "slightly neurotic": "#F87C63",
    "slightly emotionally stable": "#F87C63",
    
    
    
    "cares strongly about the well-being of others": "#F5277D",
    "cares about the well-being of others": "#F5277D",
    "cares slightly about the well-being of others": "#F5277D",
    "is not concerned with the well-being of others": "#F5277D",
    
    "cares strongly about reciprocity or fairness": "#27F598",
    "cares about reciprocity or fairness": "#27F598",
    "cares slightly about reciprocity or fairness": "#27F598",
    "is not concerned with reciprocity or fairness": "#27F598",
    
    "cares strongly about loyalty to your group": "#F87C63",
    "cares about loyalty to your group": "#F87C63",
    "cares slightly about loyalty to your group": "#F87C63",
    "is not concerned with loyalty to your group": "#F87C63",
    
    "cares strongly about respecting hierarchies or authority figures": "#F5BE27",
    "cares about respecting hierarchies or authority figures": "#F5BE27",
    "cares slightly about respecting hierarchies or authority figures": "#F5BE27",
    "is not concerned with respecting hierarchies or authority figures": "#F5BE27",
    
    "cares strongly about moral purity or spiritual elevation": "#27E0F5",
    "cares about moral purity or spiritual elevation": "#27E0F5",
    "cares slightly about moral purity or spiritual elevation": "#27E0F5",
    "is not concerned with moral purity or spiritual elevation": "#27E0F5",
}

ordered_classes = [
        "",
        " ",
    
        "highly open to experience",
        "open to experience",
        "slightly open to experience",
        "slightly closed to experience",
        "closed to experience",
        "highly closed to experience",
        
        "highly conscientious",
        "conscientious",
        "slightly conscientious",
        "slightly unconscientious",
        "unconscientious",
        "highly unconscientious",
        
        "highly extroverted",
        "extroverted",
        "slightly extroverted",
        "slightly introverted",
        "introverted",
        "highly introverted",
                
        "highly agreeable",
        "agreeable",
        "slightly agreeable",
        "slightly antagonistic",
        "antagonistic",
        "highly antagonistic",
        
        "highly neurotic",
        "neurotic",
        "slightly neurotic",
        "slightly emotionally stable",
        "emotionally stable",
        "highly emotionally stable",
        
        
        "cares strongly about the well-being of others",
        "cares about the well-being of others",
        "cares slightly about the well-being of others",
        "is not concerned with the well-being of others",
    
        "cares strongly about reciprocity or fairness",
        "cares about reciprocity or fairness",
        "cares slightly about reciprocity or fairness",
        "is not concerned with reciprocity or fairness",
    
        "cares strongly about loyalty to your group",
        "cares about loyalty to your group",
        "cares slightly about loyalty to your group",
        "is not concerned with loyalty to your group",
    
        "cares strongly about respecting hierarchies or authority figures",
        "cares about respecting hierarchies or authority figures",
        "cares slightly about respecting hierarchies or authority figures",
        "is not concerned with respecting hierarchies or authority figures",
    
        "cares strongly about moral purity or spiritual elevation",
        "cares about moral purity or spiritual elevation",
        "cares slightly about moral purity or spiritual elevation",
        "is not concerned with moral purity or spiritual elevation",
        ]


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
        
        # ordena as classes
        # manter apenas as classes que existem no dataframe
        ordem_classes_presentes = [c for c in ordered_classes if c in plot_df["classe"].unique()]

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

        plt.title("Experiment: " + info + "\n\nScore Distribution - " + current_inv_quest_dimension)
        plt.xlabel("Class(es)")
        plt.ylabel("Score")
        #plt.legend(title="Dimension") # checar: dimension referente ao quest ou ao response?
        plt.xticks(rotation=90) # 45 > 90
        plt.grid(True, linestyle="--", alpha=0.5)
        
        plt.savefig("registry/" + info + "/vis/boxplot_" + str(current_inv_quest_dimension) + ".png",
                    dpi=300, bbox_inches="tight")
        plt.close()
        
        ## ## ##

    return new_df