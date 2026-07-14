
import pandas as pd
import numpy as np
import re
import os

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # #

def experiment_corr (exp_id, cat, personali_path, moral_pt1_path, moral_pt2_path):

    personali_df = pd.read_csv(personali_path)
    moral_pt1_df = pd.read_csv(moral_pt1_path)
    moral_pt2_df = pd.read_csv(moral_pt2_path)

    moral_pt1_df = moral_pt1_df.rename(columns={'Harm_Care_score' : 'Harm_Care_pt1_score',
                                                'Fairness_Reciprocity_score' : 'Fairness_Reciprocity_pt1_score',
                                                'In-group_Loyalty_score' : 'In-group_Loyalty_pt1_score',
                                                'Authority_Respect_score' : 'Authority_Respect_pt1_score',
                                                'Purity_Sanctity_score' : 'Purity_Sanctity_pt1_score',
                                                })
    moral_pt2_df = moral_pt2_df.rename(columns={'Harm_Care_score' : 'Harm_Care_pt2_score',
                                                'Fairness_Reciprocity_score' : 'Fairness_Reciprocity_pt2_score',
                                                'In-group_Loyalty_score' : 'In-group_Loyalty_pt2_score',
                                                'Authority_Respect_score' : 'Authority_Respect_pt2_score',
                                                'Purity_Sanctity_score' : 'Purity_Sanctity_pt2_score',
                                                })

    # # # # #

    #result = pd.concat([personali_df, moral_pt1_df, moral_pt2_df], axis=1, join="inner")

    result = pd.merge(personali_df.drop("persona_dimension_list", axis=1), moral_pt1_df.drop("persona_dimension_list", axis=1), on="persona", how="inner")
    result = pd.merge(result, moral_pt2_df.drop("persona_dimension_list", axis=1), on="persona", how="inner")

    # # # # #

    result['Harm_Care_total_score'] = result['Harm_Care_pt1_score'] + result['Harm_Care_pt2_score']
    result['Fairness_Reciprocity_total_score'] = result['Fairness_Reciprocity_pt1_score'] + result['Fairness_Reciprocity_pt2_score']
    result['In-group_Loyalty_total_score'] = result['In-group_Loyalty_pt1_score'] + result['In-group_Loyalty_pt2_score']
    result['Authority_Respect_total_score'] = result['Authority_Respect_pt1_score'] + result['Authority_Respect_pt2_score']
    result['Purity_Sanctity_total_score'] = result['Purity_Sanctity_pt1_score'] + result['Purity_Sanctity_pt2_score']

    # # # # # # # # # # # # # # # # # #
    
    # # # # # # # # # # # # # # # # # #

    corr = result.corr(numeric_only=True)
    
    os.makedirs("corr" + "/" + exp_id, exist_ok=True)
    
    corr.to_csv("corr" + "/" + exp_id + "/" + exp_id + "_corr_values_csv.csv")
    corr.to_json("corr" + "/" + exp_id + "/" + exp_id + "_corr_values_json.json")
    
    # # # # #

    mask = np.triu(np.ones_like(corr, dtype=bool))

    plt.figure(figsize=(15, 12))
    ax = sns.heatmap(corr,
                annot=True,
                fmt=".2f",
                linewidths=0.5,            
                center=0,
                vmin=-1,
                vmax=1,
                mask = mask,
                cmap="RdBu" + "_r",
                )

    # # # # #
    
    edgecolor = "black"

    # bloco 1 (top-left)
    ax.add_patch(patches.Rectangle(
        (0, 1), # coluna, linha inicial
        4,      # largura (número de colunas)
        4,      # altura (número de linhas)
        fill=False, edgecolor=edgecolor, lw=4))

    # bloco 2 (meio-right)
    ax.add_patch(patches.Rectangle((5, 10), 5, 5, fill=False, edgecolor=edgecolor, lw=4))

    # bloco 3 (meio-left)
    ax.add_patch(patches.Rectangle((0, 15), 5, 5, fill=False, edgecolor=edgecolor, lw=4))

    # bloco 4 (bottom-right)
    ax.add_patch(patches.Rectangle((15, 16), 4, 4, fill=False, edgecolor=edgecolor, lw=4))

    ######################################

    # Aplicar negrito para valores > 0.65
    for text in ax.texts:
        try:
            value = float(text.get_text())
            if value > 0.65 or value < -0.65:
                text.set_weight('bold')
        except ValueError:
            pass  # ignora células mascaradas ou vazias

    #plt.xticks(rotation=45)
    #plt.yticks(rotation=0)
    plt.title(exp_id + "\nCorrelation Matrix - " + cat + " Induction")

    plt.savefig("corr" + "/" + exp_id + "/" + exp_id + "_correlation_plot_exp.pdf", dpi=300, bbox_inches="tight") # pdf / eps
    plt.close()

    # # # # # # # # # # # # # # # # # #
    
    # # # # # # # # # # # # # # # # # #
    
    result = result.drop(columns=['Harm_Care_pt1_score',
                                  'Harm_Care_pt2_score',
                                  'Fairness_Reciprocity_pt1_score',
                                  'Fairness_Reciprocity_pt2_score',
                                  'In-group_Loyalty_pt1_score',
                                  'In-group_Loyalty_pt2_score',
                                  'Authority_Respect_pt1_score',
                                  'Authority_Respect_pt2_score',
                                  'Purity_Sanctity_pt1_score',
                                  'Purity_Sanctity_pt2_score',
                                  ])
    
    corr = result.corr(numeric_only=True)
    
    # # # # #

    mask = np.triu(np.ones_like(corr, dtype=bool))

    plt.figure(figsize=(15, 12))
    ax = sns.heatmap(corr,
                annot=True,
                fmt=".2f",
                linewidths=0.5,            
                center=0,
                vmin=-1,
                vmax=1,
                mask = mask,
                cmap="RdBu" + "_r",
                )

    # # # # #

    # bloco principal
    ax.add_patch(patches.Rectangle(
        (0, 5), # coluna, linha inicial
        5,      # largura (número de colunas)
        5,      # altura (número de linhas)
        fill=False, edgecolor=edgecolor, lw=8))

    ######################################

    # Aplicar negrito para valores > 0.65
    for text in ax.texts:
        try:
            value = float(text.get_text())
            if value > 0.65 or value < -0.65:
                text.set_weight('bold')
        except ValueError:
            pass  # ignora células mascaradas ou vazias

    #plt.xticks(rotation=45)
    #plt.yticks(rotation=0)
    plt.title(exp_id + "\nCorrelation Matrix - " + cat + " Induction")

    plt.savefig("corr" + "/" + exp_id + "/" + exp_id + "_correlation_plot.pdf", dpi=300, bbox_inches="tight") # pdf / eps
    plt.close()
    
    
