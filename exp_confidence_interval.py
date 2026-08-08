
import pandas as pd
import ast
import scipy.stats as stats
import numpy as np

# # # # # # # # # # # # # # # # # #

paths = {"gemma3:27b":
            {"ipip50" : "EXPERIMENTS BIG5LLM/ollama - gemma3:27b/20260206_221713__ollama_gemma3:27b__p_personality_bigfive__i_ipip50__stateless/vis/20260206_221713__ollama_gemma3:27b__p_personality_bigfive__i_ipip50__stateless_sum.csv",
            "mfq30_pt1" : "EXPERIMENTS BIG5LLM/ollama - gemma3:27b/20260207_123247__ollama_gemma3:27b__p_morality_mft_v2__i_mfq30_pt1__stateless/vis/20260207_123247__ollama_gemma3:27b__p_morality_mft_v2__i_mfq30_pt1__stateless_sum.csv",
            "mfq30_pt2" : "EXPERIMENTS BIG5LLM/ollama - gemma3:27b/20260207_153524__ollama_gemma3:27b__p_morality_mft_v2__i_mfq30_pt2__stateless/vis/20260207_153524__ollama_gemma3:27b__p_morality_mft_v2__i_mfq30_pt2__stateless_sum.csv"},
         "qwen2.5:14b":
             {"ipip50" : "EXPERIMENTS BIG5LLM/ollama - qwen2.5:14b/20260206_105934__ollama_qwen2.5:14b__p_personality_bigfive__i_ipip50__stateless/vis/20260206_105934__ollama_qwen2.5:14b__p_personality_bigfive__i_ipip50__stateless_sum.csv",
             "mfq30_pt1" : "EXPERIMENTS BIG5LLM/ollama - qwen2.5:14b/20260206_114253__ollama_qwen2.5:14b__p_morality_mft_v2__i_mfq30_pt1__stateless/vis/20260206_114253__ollama_qwen2.5:14b__p_morality_mft_v2__i_mfq30_pt1__stateless_sum.csv",
             "mfq30_pt2" : "EXPERIMENTS BIG5LLM/ollama - qwen2.5:14b/20260206_115548__ollama_qwen2.5:14b__p_morality_mft_v2__i_mfq30_pt2__stateless/vis/20260206_115548__ollama_qwen2.5:14b__p_morality_mft_v2__i_mfq30_pt2__stateless_sum.csv"},
         "gpt-oss:20b":
              {"ipip50" : "EXPERIMENTS BIG5LLM/ollama - gpt-oss:20b/20260203_211502__ollama_gpt-oss:20b__p_personality_bigfive__i_ipip50__stateless/vis/20260203_211502__ollama_gpt-oss:20b__p_personality_bigfive__i_ipip50__stateless_sum.csv",
              "mfq30_pt1" : "EXPERIMENTS BIG5LLM/ollama - gpt-oss:20b/20260205_040724__ollama_gpt-oss:20b__p_morality_mft_v2__i_mfq30_pt1__stateless/vis/20260205_040724__ollama_gpt-oss:20b__p_morality_mft_v2__i_mfq30_pt1__stateless_sum.csv",
              "mfq30_pt2" : "EXPERIMENTS BIG5LLM/ollama - gpt-oss:20b/20260205_161608__ollama_gpt-oss:20b__p_morality_mft_v2__i_mfq30_pt2__stateless/vis/20260205_161608__ollama_gpt-oss:20b__p_morality_mft_v2__i_mfq30_pt2__stateless_sum.csv"},
         "gpt-oss::120b":
              {"ipip50" : "EXPERIMENTS BIG5LLM/groq - openai gpt-oss-120b/20260209_234824__groq_openaigpt-oss-120b__p_personality_bigfive__i_ipip50__stateless/vis/20260209_234824__groq_openaigpt-oss-120b__p_personality_bigfive__i_ipip50__stateless_sum.csv",
              "mfq30_pt1" : "EXPERIMENTS BIG5LLM/groq - openai gpt-oss-120b/20260209_141958__groq_openaigpt-oss-120b__p_morality_mft_v2__i_mfq30_pt1__stateless/vis/20260209_141958__groq_openaigpt-oss-120b__p_morality_mft_v2__i_mfq30_pt1__stateless_sum.csv",
              "mfq30_pt2" : "EXPERIMENTS BIG5LLM/groq - openai gpt-oss-120b/20260209_152341__groq_openaigpt-oss-120b__p_morality_mft_v2__i_mfq30_pt2__stateless/vis/20260209_152341__groq_openaigpt-oss-120b__p_morality_mft_v2__i_mfq30_pt2__stateless_sum.csv"}
         }

# # # # # # # # # # # # # # # # # #

perso_traits = [
    ["open to experience", "Openness"],
    ["closed to experience", "Openness"],
    ["highly open to experience", "Openness"],
    ["highly closed to experience", "Openness"],
    ["slightly open to experience", "Openness"],
    ["slightly closed to experience", "Openness"],
    ["conscientious", "Conscientiousness"],
    ["unconscientious", "Conscientiousness"],
    ["highly conscientious", "Conscientiousness"],
    ["highly unconscientious", "Conscientiousness"],
    ["slightly conscientious", "Conscientiousness"],
    ["slightly unconscientious", "Conscientiousness"],
    ["extroverted", "Extraversion"],
    ["introverted", "Extraversion"],
    ["highly extroverted", "Extraversion"],
    ["highly introverted", "Extraversion"],
    ["slightly extroverted", "Extraversion"],
    ["slightly introverted", "Extraversion"],
    ["agreeable", "Agreeableness"],
    ["antagonistic", "Agreeableness"],
    ["highly agreeable", "Agreeableness"],
    ["highly antagonistic", "Agreeableness"],
    ["slightly agreeable", "Agreeableness"],
    ["slightly antagonistic", "Agreeableness"],
    ["neurotic", "Neuroticism"],
    ["emotionally stable", "Neuroticism"],
    ["highly neurotic", "Neuroticism"],
    ["highly emotionally stable", "Neuroticism"],
    ["slightly neurotic", "Neuroticism"],
    ["slightly emotionally stable", "Neuroticism"],
]

perso_score_cols_titles = [
    "Extraversion_score",
    "Agreeableness_score",
    "Conscientiousness_score",
    "Neuroticism_score",
    "Openness_score",
]

perso_score_cols = {
    "Extraversion": "Extraversion_score",
    "Agreeableness": "Agreeableness_score",
    "Conscientiousness": "Conscientiousness_score",
    "Neuroticism": "Neuroticism_score",
    "Openness": "Openness_score",
}

# # # # # # #

moral_traits = [
    ["cares strongly about the well-being of others", "Harm_Care"],
    ["cares slightly about the well-being of others", "Harm_Care"],
    ["is not concerned with the well-being of others", "Harm_Care"],
    ["cares strongly about reciprocity or fairness", "Fairness_Reciprocity"],
    ["cares slightly about reciprocity or fairness", "Fairness_Reciprocity"],
    ["is not concerned with reciprocity or fairness", "Fairness_Reciprocity"],
    ["cares strongly about loyalty to your group", "In-group_Loyalty"],
    ["cares slightly about loyalty to your group", "In-group_Loyalty"],
    ["is not concerned with loyalty to your group", "In-group_Loyalty"],
    ["cares strongly about respecting hierarchies or authority figures", "Authority_Respect"],
    ["cares slightly about respecting hierarchies or authority figures", "Authority_Respect"],
    ["is not concerned with respecting hierarchies or authority figures", "Authority_Respect"],
    ["cares strongly about moral purity or spiritual elevation", "Purity_Sanctity"],
    ["cares slightly about moral purity or spiritual elevation", "Purity_Sanctity"],
    ["is not concerned with moral purity or spiritual elevation", "Purity_Sanctity"],
    ]

moral_score_cols_titles = [
    "Harm_Care_score",
    "Fairness_Reciprocity_score",
    "In-group_Loyalty_score",
    "Authority_Respect_score",
    "Purity_Sanctity_score",
]

moral_score_cols = {
    "Harm_Care": "Harm_Care_score",
    "Fairness_Reciprocity": "Fairness_Reciprocity_score",
    "In-group_Loyalty": "In-group_Loyalty_score",
    "Authority_Respect": "Authority_Respect_score",
    "Purity_Sanctity": "Purity_Sanctity_score",
}

# # # # # # # # # # # # # # # # # #

for model in paths:
    print ("Model:", model)
    for target_quest in paths[model]:
        print ("Quest.", target_quest)
        
        #print (paths[model][target_quest])

        data_source = pd.read_csv(paths[model][target_quest])
        #data_source
        
        if target_quest == "ipip50":
            target = perso_traits
            score_cols = perso_score_cols
            score_cols_titles = perso_score_cols_titles
        else:
            target = moral_traits
            score_cols = moral_score_cols
            score_cols_titles = moral_score_cols_titles
            
        for trait in target:
            target_trait = trait[0]
            #print ("--Trait:", target_trait)
            target_dimension = trait[1]
            #print ("--Dimension:", target_dimension)

            target_col = f"{target_dimension}_score"
            #print ("target_col:", target_col)

            df_filter = data_source[data_source["persona_dimension_list"].apply(lambda x: target_trait in ast.literal_eval(x))]
            df_filter = df_filter.drop("persona_dimension_list", axis=1)
            df_filter['dimension'] = target_dimension

            # # # # # # # # # # # # # # # # # #

            # Cópia do dataframe
            df = df_filter.copy()

            # Calcula a média dos 5 scores
            df["total_mean"] = df[list(score_cols.values())].mean(axis=1)

            # Média das outras quatro dimensões
            df["Others_average_score"] = (df["total_mean"] * 5 - df[target_col]) / 4

            # Mantém apenas as colunas desejadas
            resultado = df[["persona", "dimension",  target_col, "Others_average_score"]]

            # # # # # # # # # # # # # # # # # #

            # Scores
            scores = resultado[target_col]

            # Estatísticas
            media = scores.mean()
            #media
            desvio_padrao = round(scores.std(ddof=1),2)  # desvio padrão amostral
            #desvio_padrao
            n = len(scores)
            #n
            erro_padrao = stats.sem(scores)  # desvio padrão / sqrt(n)
            #erro_padrao

            # IC de 95%
            ic = stats.t.interval(
                confidence=0.95,
                df=n-1,
                loc=media,
                scale=erro_padrao
            )

            # # # # # # # # # # # # # # # # # #
            
            main_text = "Modelo: {} \n - Quest.: {} \n - Dimension: {} \n - Trait: {} \n - Média: {} \n - StD: {} \n - n: {} \n - IC95: ({}, {}) \n ---------- \n".format(model,
                                                                                                                                           target_quest,
                                                                                                                                           target_dimension,
                                                                                                                                           target_trait,
                                                                                                                                           round(media,2),
                                                                                                                                           desvio_padrao,
                                                                                                                                           n,
                                                                                                                                           round(ic[0],2),
                                                                                                                                           round(ic[1],2),
                                                                                                                                           )
            
            with open("z_main_data.txt", "a", encoding="utf-8") as arquivo:
                arquivo.write(main_text)

            print(f"\nModelo: {model}","\n",
                  f"Quest.: {target_quest}","\n",
                  f"Dimension: {target_dimension}","\n",
                  f"Trait: {target_trait}","\n",
                  f"Média: {media:.2f}","\n",
                  f"StD: {desvio_padrao}","\n",
                  f"n: {n}","\n",
                  f">>> IC95%: ({ic[0]:.2f}, {ic[1]:.2f})","\n\n------------------------------------------------------------")

        # # # # # # # # # # # # # # # # # #
            
        # OTHERS / ALL:
        
        for dimension in score_cols_titles:

            test_target = dimension
            #test_target
            test_score = data_source[test_target]

            # Estatísticas
            test_mean = round(test_score.mean(),2)
            #test_mean
            test_std = round(test_score.std(ddof=1),2)  # desvio padrão amostral
            #test_std
            
            others_text = "Modelo: {} \n - Quest.: {} \n - Dimension: {} \n - Média: {} \n - StD: {} \n ---------- \n".format(model,
                                                                                                                          target_quest,
                                                                                                                          test_target,
                                                                                                                          round(test_mean, 2),
                                                                                                                          test_std,
                                                                                                                          )
            
            with open("z_others_data.txt", "a", encoding="utf-8") as arquivo:
                arquivo.write(others_text)
            
            print(f"\nModelo: {model}","\n",
                  f"Quest.: {target_quest}","\n",
                  f"Dimension: {test_target}","\n",
                  f"Média: {test_mean:.2f}","\n",
                  f"StD: {test_std}","\n\n------------------------------------------------------------")
    
    
    