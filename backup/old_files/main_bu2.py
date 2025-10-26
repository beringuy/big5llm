
import ollama
import time
import pandas as pd

############################### ###############################

def basic_chat(prompt, modelo):
    
    resposta = ollama.chat(
        model=modelo,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    #print(resposta["message"]["content"])    
    return (resposta["message"]["content"])

modelo = "gemma3:27b" # "gemma3:4b" ou "gemma3:12b" ou "gemma3:27b" ou "gpt-oss:20b"

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
'''
all_conbinations = []

for current_factor_1 in factors[0]:
    for current_factor_2 in factors[1]:
        for current_factor_3 in factors[2]:
            for current_factor_4 in factors[3]:
                for current_factor_5 in factors[4]:
                    all_conbinations.append (current_factor_1+", "+current_factor_2+", "+current_factor_3+", "+current_factor_4+" e "+current_factor_5)

all_conbinations
len(all_conbinations)
'''
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
Answer using only 'Strongly disagree', 'Disagree', 'Neither agree nor disagree', 'Agree', 'Strongly agree', indicating the extent to which you agree or disagree with the following statement: {}
Answer concisely, objectively, and in the first person.
'''

base_prompt = base_prompt_2
#statement = "I love spending my free time at home."

###############################

main_df = pd.DataFrame(columns = ["persona"] + ipip50df["item"].tolist())
main_df

i = 0 # remover <<< <<< <<<
for current_persona in main_personalities_list:
    persona_start_time = time.time()
    tmp_persona_answer = [current_persona]
    for statement in ipip50df["item"].tolist():
        #print (statement)

        prompt = base_prompt.format(current_persona, statement)

        statement_start_time = time.time()
        resposta = basic_chat(prompt, modelo)

        print ("=== === === === === ===")
        print ("Persona: " + current_persona)
        print ("Statement: " + statement)
        print ("Resposta: " + resposta.strip())
        tmp_persona_answer.append(resposta.strip())

        print (">>> TEMPO: %s segundos (statement) <<<" % (time.time() - statement_start_time))
        print ("=== === === === === ===\n")

    main_df.loc[len(main_df)] = tmp_persona_answer
    print (">>> TEMPO: %s segundos (persona) <<<\n" % (time.time() - persona_start_time))
    
    if i == 3: # remover <<< <<< <<<
        break # remover <<< <<< <<<
    i += 1

main_df

###############################

score_df = pd.DataFrame(columns = ["persona"] + ipip50df["item"].tolist())
score_df

for current_row_number in range(len(main_df)):    
    tmp_persona_score = [main_df.iloc[current_row_number]["persona"]]
    
    i = 0
    for item in range(len(main_df.columns.tolist())):
        if int(i) == 0:            
            pass
        else:
            if ipip50df.iloc[int(i) - 1]["asc_dsc"] == "+":
                if main_df.iloc[current_row_number][int(i)] == "Strongly disagree.":
                    tmp_persona_score.append(1)
                elif main_df.iloc[current_row_number][int(i)] == "Disagree.":
                    tmp_persona_score.append(2)
                elif main_df.iloc[current_row_number][int(i)] == "Neither agree nor disagree.":
                    tmp_persona_score.append(3)
                elif main_df.iloc[current_row_number][int(i)] == "Agree.":
                    tmp_persona_score.append(4)
                elif main_df.iloc[current_row_number][int(i)] == "Strongly agree.":
                    tmp_persona_score.append(5)
                else:
                    print ("Warning!")
                    
            elif ipip50df.iloc[int(i) - 1]["asc_dsc"] == "-":
                if main_df.iloc[current_row_number][int(i)] == "Strongly disagree.":
                    tmp_persona_score.append(5)
                elif main_df.iloc[current_row_number][int(i)] == "Disagree.":
                    tmp_persona_score.append(4)
                elif main_df.iloc[current_row_number][int(i)] == "Neither agree nor disagree.":
                    tmp_persona_score.append(3)
                elif main_df.iloc[current_row_number][int(i)] == "Agree.":
                    tmp_persona_score.append(2)
                elif main_df.iloc[current_row_number][int(i)] == "Strongly agree.":
                    tmp_persona_score.append(1)
                else:
                    print ("Warning!")
                
            else:
                print ("Warning!")
            
        i = int(i) + 1
            
    print ('tmp_persona_score:', tmp_persona_score)    
    score_df.loc[len(score_df)] = tmp_persona_score
    #break

score_df

###############################

for i in ipip50df["item"].tolist():
    print(i)


main_df
score_df

ipip50df

ipip50df.iloc[ 0 ]["asc_dsc"]

main_df[main_df.columns.tolist()[int(0)]]

main_df[main_df.columns.tolist()[0]]

main_df.iloc[row][0]
main_df.iloc[row]['persona']

main_df.iloc[current_row_number][1] 