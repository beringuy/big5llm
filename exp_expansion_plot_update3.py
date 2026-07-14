
import pandas as pd
import numpy as np
import re
import os
import matplotlib.pyplot as plt
import seaborn as sns
import ast # para converter string → lista real

from exp_global_info import palette_classes
from exp_global_info import ordered_classes
from exp_global_info import PSYCH_DOMAINS
from exp_global_info import INV_QUEST


#########################################################################################################

def experiment_plot(exp_id, source_id, baseline_id, exp_path):

    data_df = pd.read_csv(exp_path + source_id + "/vis/" + source_id + "_sum.csv")
    #data_df
    print("\ndata_df:")
    print(data_df)

    baseline_df = pd.read_csv(exp_path + baseline_id + "/vis/" + baseline_id + "_sum.csv")
    #baseline_df

    # # # # #

    selected_inv_quest = re.search(r'(?<=__i_).*?(?=__)', source_id).group()
    #selected_inv_quest

    selected_psych_domain = re.search(r'(?<=__p_).*?(?=__)', source_id).group()
    #selected_psych_domain

    inv_quest = pd.read_csv(INV_QUEST[selected_inv_quest]['path'])
    #inv_quest
    #print("\ninv_quest:")
    #print(inv_quest)

    psych_domain_dimensions = PSYCH_DOMAINS[selected_psych_domain]
    psych_domain_dimensions.pop("BASE_PROMPT", None)
    #psych_domain_dimensions

    inv_quest_dimension_list = inv_quest["dimension"].value_counts().index.tolist()
    #inv_quest_dimension_list
    #print("\ninv_quest_dimension_list:")
    #print(inv_quest_dimension_list)

    # # # # # # # # # #

    current_base = baseline_df.drop(['persona','persona_dimension_list'], axis = 1)
    #current_base

    baseline_list = {}

    for i in current_base:
        baseline_list[i[:-6]] = int(current_base[i][0])    

    print("\nbaseline_list:")
    print(baseline_list)

    # # # # #

    constr = []
    for trait in psych_domain_dimensions:
        #print("trait:", trait)
        for pole in psych_domain_dimensions[trait]:
            #print("pole:", pole)
            constr.append([pole, trait])
    #constr

    # # # # #

    for i in baseline_list:
        #print(i)
        for j in constr:
            #print("j:", j)
            if i[0] == j[1]:
                j.append(i[1])

    #constr

    # # # # # # # # # #
    
    os.makedirs("EXP_PLOTS", exist_ok=True)
    os.makedirs("EXP_MEANST", exist_ok=True)

    for current_inv_quest_dimension in inv_quest_dimension_list:
    
        AQUI =  baseline_list[current_inv_quest_dimension]
    
        plot_df = []
        for current_psydomdim_i in range(len(psych_domain_dimensions)):
            current_data = data_df[["persona_dimension_list", current_inv_quest_dimension+"_score"]].copy()
            #current_data
            current_data["inv_quest_dimension"] = current_inv_quest_dimension
            #current_data
            current_data["persona_dimension_list"] = current_data["persona_dimension_list"].apply(ast.literal_eval) # converte string → lista real
            current_data["classe"] = current_data["persona_dimension_list"].apply(lambda x: x[current_psydomdim_i])
            #current_data
            #print("\ncurrent_data['classe']:")
            #print(current_data['classe'])

            plot_df.append(current_data[["classe", current_inv_quest_dimension+"_score", "inv_quest_dimension"]]
                           .rename(columns={current_inv_quest_dimension+"_score": "score"}))
            
            #print("\ninner plot_df:")
            #print(plot_df)

        # junta tudo
        plot_df = pd.concat(plot_df)
        
        print("\nplot_df:")
        print(plot_df)
        
        # # # #
        
        # ordena as classes
        # manter apenas as classes que existem no dataframe
        ordem_classes_presentes = [c for c in ordered_classes if c in plot_df["classe"].unique()]
        #ordem_classes_presentes

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
        
        ax = plt.gca()
        
        ##############

        for i, classe in enumerate(ordem_classes_presentes):

            # desenha uma linha horizontal "curta" na posição da classe
            ax.hlines(
                y=AQUI,
                #y=47,
                xmin=i - 0.3,
                xmax=i + 0.3,
                colors="darkred",
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
        
        plt.savefig("EXP_PLOTS/exp_" + source_id + "_" + str(current_inv_quest_dimension) + ".pdf",
                    dpi=300, bbox_inches="tight")
        plt.close()
        
        ############################
        
        ############################
        
        # ONE VS ALL:
        
        df_one_vs_all = plot_df.copy()
        
        print("\ncurrent_inv_quest_dimension:")
        print(current_inv_quest_dimension)
        
        if current_inv_quest_dimension == "Extraversion":
            not_others = ['highly extroverted',
                          'extroverted',
                          'slightly extroverted',
                          'highly introverted',
                          'introverted',
                          'slightly introverted',
                          ]
        if current_inv_quest_dimension == "Agreeableness":
            not_others = ['highly agreeable',
                          'agreeable',
                          'slightly agreeable',
                          'highly antagonistic',
                          'antagonistic',
                          'slightly antagonistic',
                          ]
        if current_inv_quest_dimension == "Conscientiousness":
            not_others = ['highly conscientious',
                          'conscientious',
                          'slightly conscientious',
                          'highly unconscientious',
                          'unconscientious',
                          'slightly unconscientious',
                          ]
        if current_inv_quest_dimension == "Neuroticism":
            not_others = ['highly emotionally stable',
                          'emotionally stable',
                          'slightly emotionally stable',
                          'highly neurotic',
                          'neurotic',
                          'slightly neurotic',
                          ]
        if current_inv_quest_dimension == "Openness":
            not_others = ['highly open to experience',
                          'open to experience',
                          'slightly open to experience',
                          'highly closed to experience',
                          'closed to experience',
                          'slightly closed to experience',
                          ]
            # # #
        if current_inv_quest_dimension == "Harm_Care":
            not_others = ['cares strongly about the well-being of others',
                          'cares slightly about the well-being of others',
                          'is not concerned with the well-being of others',
                          ]
        if current_inv_quest_dimension == "Fairness_Reciprocity":
            not_others = ['cares strongly about reciprocity or fairness',
                          'cares slightly about reciprocity or fairness',
                          'is not concerned with reciprocity or fairness',
                          ]
        if current_inv_quest_dimension == "In-group_Loyalty":
            not_others = ['cares strongly about loyalty to your group',
                          'cares slightly about loyalty to your group',
                          'is not concerned with loyalty to your group',
                          ]
        if current_inv_quest_dimension == "Authority_Respect":
            not_others = ['cares strongly about respecting hierarchies or authority figures',
                          'cares slightly about respecting hierarchies or authority figures',
                          'is not concerned with respecting hierarchies or authority figures',
                          ]
        if current_inv_quest_dimension == "Purity_Sanctity":
            not_others = ['cares strongly about moral purity or spiritual elevation',
                          'cares slightly about moral purity or spiritual elevation',
                          'is not concerned with moral purity or spiritual elevation',
                          ]
        
        mask = (
            (df_one_vs_all['inv_quest_dimension'] == current_inv_quest_dimension) &
            (~df_one_vs_all['classe'].isin(not_others))
            )        
        df_one_vs_all.loc[mask, 'classe'] = 'Others'
        
        #print("\ndf_one_vs_all:")
        #print(df_one_vs_all)
        
        ##############
        
        mean_table = (
            df_one_vs_all
            .groupby('classe')['score']
            .agg(
                mean='mean',
                std='std'
            )
            .reset_index()
            .round(2)
        )
        
        df_one_vs_all.to_csv("EXP_MEANST/oneVAll_" + source_id + "_" + current_inv_quest_dimension + ".csv", index=False)
        mean_table.to_csv("EXP_MEANST/meanSt_" + source_id + "_" + current_inv_quest_dimension + ".csv", index=False)

        print('\nmean_table:')
        print(mean_table)
        
        ##############
        
        # # # #
        
        ##############
        
        plt.figure(figsize=(12,6))
        
        sns.boxplot(data=df_one_vs_all,
                    x="classe",
                    y="score",
                    palette=palette_classes,
                    #hue="inv_quest_dimension",
                    order=ordem_classes_presentes.append("Others"),
                    showmeans=True,
                    meanprops={
                        "marker": "o",
                        "markerfacecolor": "black",
                        "markeredgecolor": "black",
                        "markersize": 5
                        }
                    )
                
        ##############
        
        ax = plt.gca()
        
        ##############

        for i, classe in enumerate(ordem_classes_presentes):

            # desenha uma linha horizontal "curta" na posição da classe
            ax.hlines(
                y=AQUI,
                #y=47,
                xmin=i - 0.3,
                xmax=i + 0.3,
                colors="darkred",
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
        
        plt.savefig("EXP_PLOTS/exp_1vsAll_" + source_id + "_" + str(current_inv_quest_dimension) + ".pdf",
                    dpi=300, bbox_inches="tight")
        plt.close()

