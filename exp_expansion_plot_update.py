
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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

PSYCH_DOMAINS = {
    "personality_bigfive" : {
        "Openness" : [
            "open to experience",
            "closed to experience",
            ],
        "Conscientiousness" : [
            "conscientious",
            "unconscientious",
            ],
        "Extraversion" : [
            "extroverted",
            "introverted",
            ],
        "Agreeableness" : [
            "agreeable",
            "antagonistic",
            ],
        "Neuroticism" : [
            "neurotic",
            "emotionally stable",
            ],
        "BASE_PROMPT" : "You are a character who is {}.",
    },
    
    
    "personality_bigfive_mod" : {
        "Extraversion" : [
            "extroverted",
            "introverted",
            ],
        "Agreeableness" : [
            "agreeable",
            "antagonistic",
            ],
        "BASE_PROMPT" : "You are a character who is {}.",
    },
    
    
    
    "unspecified" : {
        "Unspecified" : [""],
        "BASE_PROMPT" : "",
    },
    
    
    
    "morality_mft_v1" : {
        "Harm_Care" : [
            "cares about the well-being of others",
            "is not concerned with the well-being of others",
            ],
        "Fairness_Reciprocity" : [
            "cares about reciprocity or fairness",
            "is not concerned with reciprocity or fairness",
            ],
        "In-group_Loyalty" : [
            "cares about loyalty to your group",
            "is not concerned with loyalty to your group",
            ],
        "Authority_Respect" : [
            "cares about respecting hierarchies or authority figures",
            "is not concerned with respecting hierarchies or authority figures",
            ],
        "Purity_Sanctity" : [
            "cares about moral purity or spiritual elevation",
            "is not concerned with moral purity or spiritual elevation",
            ],
        "BASE_PROMPT" : "You are a character who {}.",
    },
    
    
    "morality_mft_v2" : {
        "Harm_Care" : [
            "cares strongly about the well-being of others",
            "cares slightly about the well-being of others",
            "is not concerned with the well-being of others",
            ],
        "Fairness_Reciprocity" : [
            "cares strongly about reciprocity or fairness",
            "cares slightly about reciprocity or fairness",
            "is not concerned with reciprocity or fairness",
            ],
        "In-group_Loyalty" : [
            "cares strongly about loyalty to your group",
            "cares slightly about loyalty to your group",
            "is not concerned with loyalty to your group",
            ],
        "Authority_Respect" : [
            "cares strongly about respecting hierarchies or authority figures",
            "cares slightly about respecting hierarchies or authority figures",
            "is not concerned with respecting hierarchies or authority figures",
            ],
        "Purity_Sanctity" : [
            "cares strongly about moral purity or spiritual elevation",
            "cares slightly about moral purity or spiritual elevation",
            "is not concerned with moral purity or spiritual elevation",
            ],
        "BASE_PROMPT" : "You are a character who {}.",
    },
}

INV_QUEST = {
    "bfi44" : {
        "path" : "inventories_questionnaires/bfi44.csv",
        
        "base_prompt" : ''' {} 
 Answer using solely {}, indicating the extent to which you agree or disagree with the following statement based on your traits. 
 Answer concisely, objectively, and in the first person. 
 Do not justify or explain your answers. 
 
 Statement: 'Has opinions about various topics.' 
 Response: strongly agree 
 
 Statement: '{}'. 
 Response: ''',
            
        "answers" : {
            "strongly disagree": 1,
            "disagree": 2,
            "neither agree nor disagree": 3,
            "agree": 4,
            "strongly agree": 5,
            'REF_VALUE':6,
        },
    },
    
    
    
    "ipip50" : {
        "path" : "inventories_questionnaires/ipip50.csv",
        
        "base_prompt" : ''' {} 
 Answer using solely {}, indicating the extent to which you agree or disagree with the following statement based on your traits. 
 Answer concisely, objectively, and in the first person. 
 Do not justify or explain your answers. 
 
 Statement: 'Has opinions about various topics.' 
 Response: strongly agree 
 
 Statement: '{}'. 
 Response: ''',
            
        "answers" : {
            "strongly disagree": 1,
            "disagree": 2,
            "neither agree nor disagree": 3,
            "agree": 4,
            "strongly agree": 5,
            'REF_VALUE':6,
        },
    },
    
    
    
    "mfq30_pt1" : {
        "path" : "inventories_questionnaires/mfq30_pt1.csv",
        
        "base_prompt" : ''' {} 
 When you decide whether something is right or wrong, to what extent are the following consideration relevant to your thinking? 
 Answer using solely {}. 
 Answer concisely, objectively, and in the first person, based on your traits. 
 Do not justify or explain your answers. 

 Example:
 Consideration: 'Whether or not someone was good at math'. 
 Response: not at all relevant 
 
 Now answer the following consideration: 
 Consideration: '{}'. 
 Response: ''',
            
        "answers" : {
            'not at all relevant':0,
            'not very relevant':1,
            'slightly relevant':2,
            'somewhat relevant':3,
            'very relevant':4,
            'extremely relevant':5,
            'REF_VALUE':5,
        },
    },
    
    
    
    "mfq30_pt2" : {
        "path" : "inventories_questionnaires/mfq30_pt2.csv",
        
        "base_prompt" : ''' {} 
 Read the following sentence and indicate your agreement or disagreement. 
 Answer using solely {}. 
 Answer concisely, objectively, and in the first person, based on your traits. 
 Do not justify or explain your answers. 

 Example:
 Sentence: 'It is better to do good than to do bad.'. 
 Response: strongly agree 
 
 Now answer the following sentence: 
 Sentence: '{}'. 
 Response: ''',
            
        "answers" : {
            "strongly disagree": 0,
            "moderately disagree": 1,
            "slightly disagree": 2,
            "slightly agree": 3,
            "moderately agree": 4,
            "strongly agree": 5,
            'REF_VALUE':5,
        },
    },
    
    

}


PSYCH_DOMAINS = {
    "personality_bigfive" : {
        "Openness" : [
            "open to experience",
            "closed to experience",
            ],
        "Conscientiousness" : [
            "conscientious",
            "unconscientious",
            ],
        "Extraversion" : [
            "extroverted",
            "introverted",
            ],
        "Agreeableness" : [
            "agreeable",
            "antagonistic",
            ],
        "Neuroticism" : [
            "neurotic",
            "emotionally stable",
            ],
        "BASE_PROMPT" : "You are a character who is {}.",
    },
    
    
    "personality_bigfive_mod" : {
        "Extraversion" : [
            "extroverted",
            "introverted",
            ],
        "Agreeableness" : [
            "agreeable",
            "antagonistic",
            ],
        "BASE_PROMPT" : "You are a character who is {}.",
    },
    
    
    
    "unspecified" : {
        "Unspecified" : [""],
        "BASE_PROMPT" : "",
    },
    
    
    
    "morality_mft_v1" : {
        "Harm_Care" : [
            "cares about the well-being of others",
            "is not concerned with the well-being of others",
            ],
        "Fairness_Reciprocity" : [
            "cares about reciprocity or fairness",
            "is not concerned with reciprocity or fairness",
            ],
        "In-group_Loyalty" : [
            "cares about loyalty to your group",
            "is not concerned with loyalty to your group",
            ],
        "Authority_Respect" : [
            "cares about respecting hierarchies or authority figures",
            "is not concerned with respecting hierarchies or authority figures",
            ],
        "Purity_Sanctity" : [
            "cares about moral purity or spiritual elevation",
            "is not concerned with moral purity or spiritual elevation",
            ],
        "BASE_PROMPT" : "You are a character who {}.",
    },
    
    
    "morality_mft_v2" : {
        "Harm_Care" : [
            "cares strongly about the well-being of others",
            "cares slightly about the well-being of others",
            "is not concerned with the well-being of others",
            ],
        "Fairness_Reciprocity" : [
            "cares strongly about reciprocity or fairness",
            "cares slightly about reciprocity or fairness",
            "is not concerned with reciprocity or fairness",
            ],
        "In-group_Loyalty" : [
            "cares strongly about loyalty to your group",
            "cares slightly about loyalty to your group",
            "is not concerned with loyalty to your group",
            ],
        "Authority_Respect" : [
            "cares strongly about respecting hierarchies or authority figures",
            "cares slightly about respecting hierarchies or authority figures",
            "is not concerned with respecting hierarchies or authority figures",
            ],
        "Purity_Sanctity" : [
            "cares strongly about moral purity or spiritual elevation",
            "cares slightly about moral purity or spiritual elevation",
            "is not concerned with moral purity or spiritual elevation",
            ],
        "BASE_PROMPT" : "You are a character who {}.",
    },
}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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

#########################################################################################################


#########################################################################################################

import pandas as pd

data_df = pd.read_csv("registry/20260206_221713__ollama_gemma3:27b__p_personality_bigfive__i_ipip50__stateless/vis/20260206_221713__ollama_gemma3:27b__p_personality_bigfive__i_ipip50__stateless_sum.csv")
data_df

baseline_df = pd.read_csv("registry/20260206_135601__ollama_gemma3:27b__p_unspecified__i_ipip50__stateless/vis/20260206_135601__ollama_gemma3:27b__p_unspecified__i_ipip50__stateless_sum.csv")
baseline_df

info = "20260206_221713__ollama_gemma3:27b__p_personality_bigfive__i_ipip50__stateless"

inv_quest = pd.read_csv(INV_QUEST['ipip50']['path'])
inv_quest

psych_domain_dimensions = PSYCH_DOMAINS["personality_bigfive"]
psych_domain_dimensions.pop("BASE_PROMPT", None)
psych_domain_dimensions

inv_quest_dimension_list = inv_quest["dimension"].value_counts().index.tolist()
inv_quest_dimension_list

#########################################################################################################

#########################################################################################################
import ast # para converter string → lista real

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

# # # # #

baseline_por_classe = plot_df.groupby("classe")["score"].mean().reset_index()
baseline_por_classe

# # # # #

for i in constr:
    print(i[0])
    
    for index, row in baseline_por_classe.iterrows():
        #print(row['classe'])

        if i[0] in row['classe']:
            baseline_por_classe.loc[index, 'score'] = i[2]
            print ("MUDOU:", row)

baseline_por_classe
baseline_por_classe = baseline_por_classe.set_index("classe")["score"]

# # # # #

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

        plt.title("Experiment: " + info + "\n\nScore Distribution - " + current_inv_quest_dimension)
        plt.xlabel("Class(es)")
        plt.ylabel("Score")
        #plt.legend(title="Dimension") # checar: dimension referente ao quest ou ao response?
        plt.xticks(rotation=90) # 45 > 90
        plt.grid(True, linestyle="--", alpha=0.5)
        
        plt.savefig("teste" + info + "_" + str(current_inv_quest_dimension) + ".png",
                    dpi=300, bbox_inches="tight")
        plt.close()

