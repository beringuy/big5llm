
import ollama
import time
from datetime import datetime
import pandas as pd
import os
import re

import matplotlib.pyplot as plt


############################### ###############################

def basic_chat(prompt, modelo):
    
    resposta = ollama.chat(
        model=modelo,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        #think= "low" # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< para o gpt-oss:20b" <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    )

    #print(resposta["message"]["content"])    
    return (resposta["message"]["content"])

modelo = "gemma3:4b" # "gemma3:1b" ou "gemma3:4b" ou "gemma3:12b" ou "gemma3:27b" ou "gpt-oss:20b"

############################### ###############################

ipip50df = pd.read_csv("ipip50.csv")

###############################

levels = ["highly ", "slightly "]

openn = ["open to experience", "closed to experience"]
consc = ["conscientious", "unconscientious"]
extra = ["extroverted", "introverted"]
agree = ["agreeable", "antagonistic"]
neuro = ["neurotic", "emotionally stable"]

factors = [openn,consc,extra,agree,neuro,]

###############################

main_personalities_list = []

for i in range (len(factors)):
    for level in levels:
        tmp_list = ["","","","","",]
        tmp_list[i] = level
        for current_factor_1 in factors[0]:
            for current_factor_2 in factors[1]:
                for current_factor_3 in factors[2]:
                    for current_factor_4 in factors[3]:
                        for current_factor_5 in factors[4]:
                            main_personalities_list.append (f"{tmp_list[0]}{current_factor_1}, {tmp_list[1]}{current_factor_2}, {tmp_list[2]}{current_factor_3}, {tmp_list[3]}{current_factor_4} and {tmp_list[4]}{current_factor_5}")

for tmp in main_personalities_list:
    print (tmp)
len(main_personalities_list)

############################### ###############################

base_prompt_1 = '''
You are a character who is {}. Answer concisely, objectively, and in the first person.
'''

base_prompt_2 = '''
You are a character who is {}.
Answer using only 'Strongly disagree', 'Disagree', 'Neither agree nor disagree', 'Agree', 'Strongly agree', indicating the extent to which you agree or disagree with the following statement: '{}'.
Answer concisely, objectively, and in the first person.
'''

base_prompt = base_prompt_2
#statement = "I love spending my free time at home."

###############################

main_df = pd.DataFrame(columns = ["persona"] + ipip50df["item"].tolist())
main_df

start = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = "registry/" + start + "_" + modelo +  "_logfile.txt"

i = 0 # remover <<< <<< <<<
for current_persona in main_personalities_list[i:]:
    #print(current_persona)
    persona_start_time = time.time()
    tmp_persona_answer = [current_persona]
    j = 0
    for statement in ipip50df["item"].tolist():
        #print (statement)

        prompt = base_prompt.format(current_persona, statement)
        print ("\n--prompt:", prompt)

        statement_start_time = time.time()
        resposta = basic_chat(prompt, modelo)
        
        tmp_log_list = []

        tmp_log_list.append("=== === === === === ===")
        tmp_log_list.append("persona " + str(i+1) + " e item " + str(j+1))
        tmp_log_list.append("Persona: " + current_persona)
        tmp_log_list.append("Statement: " + statement)
        tmp_log_list.append("Resposta: " + resposta.strip())
        tmp_persona_answer.append(resposta.strip())

        tmp_log_list.append(">>> TEMPO: %s segundos (statement) <<<" % (time.time() - statement_start_time))
        tmp_log_list.append("=== === === === === ===\n")
        
        j += 1
        
        with open(log_file, "a") as f:  # "a" = append (adiciona ao final)
            for elem in tmp_log_list:
                garbage = f.write(f"{elem}\n")
                print (elem)

    main_df.loc[len(main_df)] = tmp_persona_answer
    main_df.to_csv("registry/" + start + "_" + modelo + "_answers.csv", index=False)

    with open(log_file, "a") as f:  # "a" = append (adiciona ao final)
        garbage = f.write( ">>> TEMPO: %s segundos (persona) <<<\n\n" % (time.time() - persona_start_time) )
        print (">>> TEMPO: %s segundos (persona) <<<\n" % (time.time() - persona_start_time))
    
    if i == 1: # remover <<< <<< <<<
        #break # remover <<< <<< <<<
        pass # remover <<< <<< <<<
    i += 1

main_df

###############################

score_df = pd.DataFrame(columns = ["persona"] + ipip50df["item"].tolist())
score_df


# Mapeamento base das respostas
response_map = {
    "Strongly disagree.": 1,
    "Strongly disagree": 1,
    "I Strongly disagree.": 1,
    "I Strongly disagree": 1,
    "Disagree.": 2,
    "Disagree": 2,
    "I Disagree.": 2,
    "I Disagree": 2,
    "Neither agree nor disagree.": 3,
    "Neither agree nor disagree": 3,
    "I Neither agree nor disagree.": 3,
    "I Neither agree nor disagree": 3,
    "Agree.": 4,
    "Agree": 4,
    "I Agree.": 4,
    "I Agree": 4,
    "Strongly agree.": 5,
    "Strongly agree": 5,
    "I Strongly agree.": 5,
    "I Strongly agree": 5,
}


for current_row_number in range(len(main_df)):    
    tmp_persona_score = [main_df.iloc[current_row_number]["persona"]]
    
    for i in range(1, len(main_df.columns)):
        asc_dsc = ipip50df.iloc[i - 1]["asc_dsc"]
        response = main_df.iloc[current_row_number][i]

        if response not in response_map:
            print(f"Warning! Resposta inválida: {response}")
            tmp_persona_score.append(None)
            continue

        score = response_map[response]

        if asc_dsc == "-":
            score = 6 - score
        elif asc_dsc != "+":
            print(f"Warning! Valor de asc_dsc inválido: {asc_dsc}")

        tmp_persona_score.append(score)
            
    print("tmp_persona_score:", tmp_persona_score)
    score_df.loc[len(score_df)] = tmp_persona_score

    #break

score_df

###############################

score_df.to_csv("registry/" + start + "_" + modelo + "_answersScores.csv", index=False)

###############################



###############################

import ollama
import time
from datetime import datetime
import pandas as pd
import os
import re

import matplotlib.pyplot as plt



levels = ["highly ", "slightly "]

openn = ["open to experience", "closed to experience"]
consc = ["conscientious", "unconscientious"]
extra = ["extroverted", "introverted"]
agree = ["agreeable", "antagonistic"]
neuro = ["neurotic", "emotionally stable"]

factors = [openn,consc,extra,agree,neuro,]

df_new_scores_p = pd.read_csv("registry/20251021_111630answersScores.csv")

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
df_short.columns()


# re.split(r",| and ", df_new_scores_p["persona"][0])
# [i.strip() for i in re.split(r",| and ", df_new_scores_p["persona"])]

# "extroverted" in [i.strip() for i in re.split(r",| and ", df_new_scores_p["persona"][0])]
# "introverted" in [i.strip() for i in re.split(r",| and ", df_new_scores_p["persona"][0])]
# "open to experience" in [i.strip() for i in re.split(r",| and ", df_new_scores_p["persona"][0])]

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





###############################
'''
for i in ipip50df["item"].tolist():
    print(i)


main_df
score_df


for persona in main_df["persona"]:
    print (persona)
    
tmp_item = 

main_df[["persona", "Feel little concern for others."]]
score_df[["persona", "Feel little concern for others."]]



ipip50df

ipip50df.iloc[ 0 ]["asc_dsc"]

main_df[main_df.columns.tolist()[int(0)]]

main_df[main_df.columns.tolist()[0]]

main_df.iloc[row][0]
main_df.iloc[row]['persona']

main_df.iloc[current_row_number][1]
'''