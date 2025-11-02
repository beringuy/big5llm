
import ollama
import pandas as pd
import time
import os
from datetime import datetime

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def basic_chat(prompt, modelo):
    
    resposta = ollama.chat(
        model = modelo,
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        #think = "low" # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< para o gpt-oss:20b" <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    )

    #print(resposta["message"]["content"])    
    return (resposta["message"]["content"])

# # # # # # # # # #

# GPT MOD:
# histórico global
chat_history = [] # Como resetar a cada nova persona?

def chat_with_memory(prompt, modelo):
    global chat_history

    # adiciona a nova mensagem do usuário
    chat_history.append({"role": "user", "content": prompt})

    # envia TODO o histórico ao modelo
    resposta = ollama.chat(
        model=modelo,
        messages=chat_history
    )

    # extrai a resposta
    content = resposta["message"]["content"]

    # adiciona a resposta ao histórico
    chat_history.append({"role": "assistant", "content": content})
    
    print ("\n-- Chat History:", chat_history)

    return content

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def run_inv_quest_llm_pt1 (persona_list , inv_quest_df ,  modelo = "gemma3:12b"):
    tmp_df = pd.DataFrame(columns = ["persona"] + inv_quest_df["item"].tolist())
    tmp_df
    
    start = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("registry/" + start + "_" + modelo + "/" , exist_ok=True)
    log_file = "registry/" + start + "_" + modelo + "/" + start + "_" + modelo +  "_logfile.txt"
    
    i = 0 # remover <<< <<< <<<
    for current_persona in persona_list[i:]:
        #print(current_persona)
        persona_start_time = time.time()
        tmp_persona_answer = [current_persona]
        j = 0
        for statement in inv_quest_df["item"].tolist():
            #print (statement)
    
            base_prompt = '''
You are a character who is {}.
Answer using solely 'Strongly disagree', 'Disagree', 'Neither agree nor disagree', 'Agree' or 'Strongly agree', indicating the extent to which you agree or disagree with the following statement based on your traits.
Answer concisely, objectively, and in the first person. Do not justify or explain your answers.
Statement: '{}'.
            '''
            prompt = base_prompt.format(current_persona, statement)
    
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
            
            print ("\n-- Prompt:", prompt, "\n")
            with open(log_file, "a") as f:  # "a" = append (adiciona ao final)
                for elem in tmp_log_list:
                    garbage = f.write(f"{elem}\n")
                    print (elem)
        
        tmp_df.loc[len(tmp_df)] = tmp_persona_answer
        tmp_df.to_csv("registry/" + start + "_" + modelo + "/" + start + "_" + modelo + "_answers.csv", index=False)
    
        with open(log_file, "a") as f:  # "a" = append (adiciona ao final)
            garbage = f.write( ">>> TEMPO: %s segundos (persona) <<<\n\n" % (time.time() - persona_start_time) )
            print (">>> TEMPO: %s segundos (persona) <<<\n" % (time.time() - persona_start_time))
        
        if i == 1: # remover <<< <<< <<<
            #break # remover <<< <<< <<<
            pass # remover <<< <<< <<<
        i += 1 # remover <<< <<< <<<
        
    return tmp_df , start

# # # # # # # # # #

# # # # # # # # # #

def run_inv_quest_llm_pt2 (persona_list , inv_quest_df ,  modelo = "gemma3:12b"):
    global chat_history
    
    tmp_df = pd.DataFrame(columns = ["persona"] + inv_quest_df["item"].tolist())
    tmp_df
    
    start = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("registry/" + start + "_" + modelo + "/" , exist_ok=True)
    log_file = "registry/" + start + "_" + modelo + "/" + start + "_" + modelo +  "_logfile.txt"
    
    i = 0 # remover <<< <<< <<<
    for current_persona in persona_list[i:]:
        #print(current_persona)
        persona_start_time = time.time()
        tmp_persona_answer = [current_persona]
        
        base_prompt = '''
You are a character who is {}.
Answer using solely 'Strongly disagree', 'Disagree', 'Neither agree nor disagree', 'Agree' or 'Strongly agree', indicating the extent to which you agree or disagree with the following statement based on your traits.
Answer concisely, objectively, and in the first person. Do not justify or explain your answers.
            '''
        prompt = base_prompt.format(current_persona)
        print ("\n-- Prompt:", prompt)
        resposta = chat_with_memory(prompt, modelo)
        
        j = 0
        for statement in inv_quest_df["item"].tolist():
            #print (statement)
    
            prompt = "Statement: '{}'.".format(statement)
    
            statement_start_time = time.time()
            resposta = chat_with_memory(prompt, modelo)
            
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
            
            print ("\n-- Prompt:", prompt, "\n")
            with open(log_file, "a") as f:  # "a" = append (adiciona ao final)
                for elem in tmp_log_list:
                    garbage = f.write(f"{elem}\n")
                    print (elem)
        chat_history = []
        
        tmp_df.loc[len(tmp_df)] = tmp_persona_answer
        tmp_df.to_csv("registry/" + start + "_" + modelo + "/" + start + "_" + modelo + "_answers.csv", index=False)
    
        with open(log_file, "a") as f:  # "a" = append (adiciona ao final)
            garbage = f.write( ">>> TEMPO: %s segundos (persona) <<<\n\n" % (time.time() - persona_start_time) )
            print (">>> TEMPO: %s segundos (persona) <<<\n" % (time.time() - persona_start_time))
        
        if i == 1: # remover <<< <<< <<<
            #break # remover <<< <<< <<<
            pass # remover <<< <<< <<<
        i += 1 # remover <<< <<< <<<
        
    return tmp_df , start

# # # # # # # # # #

# # # # # # # # # #

def run_inv_quest_llm_pt3 (persona_list , inv_quest_df ,  modelo = "gemma3:12b"):
    return None

# # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # #

def run_inv_quest_llm_moral_pt1 (persona_list , inv_quest_df ,  modelo = "gemma3:12b"):
    tmp_df = pd.DataFrame(columns = ["persona"] + inv_quest_df["item"].tolist())
    tmp_df
    
    start = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("registry/" + start + "_" + modelo + "/" , exist_ok=True)
    log_file = "registry/" + start + "_" + modelo + "/" + start + "_" + modelo +  "_logfile.txt"
    
    i = 0 # remover <<< <<< <<<
    for current_persona in persona_list[i:]:
        #print(current_persona)
        persona_start_time = time.time()
        tmp_persona_answer = [current_persona]
        j = 0
        for statement in inv_quest_df["item"].tolist():
            #print (statement)
    
            base_prompt = '''
You are a character who {}.
Answer concisely, objectively, and in the first person, based on your traits. Do not justify or explain your answers.
When you decide whether something is right or wrong, to what extent are the following considerations relevant to your thinking?
Answer using solely 'Not at all relevant', 'Not very relevant', 'Slightly relevant', 'Somewhat relevant', 'Very relevant' or 'Extremely relevant'.
Consideration: '{}'.
            '''
            prompt = base_prompt.format(current_persona, statement)
    
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
            
            print ("\n-- Prompt:", prompt, "\n")
            with open(log_file, "a") as f:  # "a" = append (adiciona ao final)
                for elem in tmp_log_list:
                    garbage = f.write(f"{elem}\n")
                    print (elem)
        
        tmp_df.loc[len(tmp_df)] = tmp_persona_answer
        tmp_df.to_csv("registry/" + start + "_" + modelo + "/" + start + "_" + modelo + "_answers.csv", index=False)
    
        with open(log_file, "a") as f:  # "a" = append (adiciona ao final)
            garbage = f.write( ">>> TEMPO: %s segundos (persona) <<<\n\n" % (time.time() - persona_start_time) )
            print (">>> TEMPO: %s segundos (persona) <<<\n" % (time.time() - persona_start_time))
        
        if i == 1: # remover <<< <<< <<<
            #break # remover <<< <<< <<<
            pass # remover <<< <<< <<<
        i += 1 # remover <<< <<< <<<
        
    return tmp_df , start

# # # # # # # # # #

def run_inv_quest_llm_moral_pt2 (persona_list , inv_quest_df ,  modelo = "gemma3:12b"):
    tmp_df = pd.DataFrame(columns = ["persona"] + inv_quest_df["item"].tolist())
    tmp_df
    
    start = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("registry/" + start + "_" + modelo + "/" , exist_ok=True)
    log_file = "registry/" + start + "_" + modelo + "/" + start + "_" + modelo +  "_logfile.txt"
    
    i = 0 # remover <<< <<< <<<
    for current_persona in persona_list[i:]:
        #print(current_persona)
        persona_start_time = time.time()
        tmp_persona_answer = [current_persona]
        j = 0
        for statement in inv_quest_df["item"].tolist():
            #print (statement)
    
            base_prompt = '''
You are a character who {}.
Answer concisely, objectively, and in the first person, based on your traits. Do not justify or explain your answers.
Please read the following sentences and indicate your agreement or disagreement.
Answer using solely 'Strongly disagree', 'Moderately disagree', 'Slightly disagree', 'Slightly agree', 'Moderately agree' or 'Strongly agree'.
Sentence: '{}'.
            '''
            prompt = base_prompt.format(current_persona, statement)
    
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
            
            print ("\n-- Prompt:", prompt, "\n")
            with open(log_file, "a") as f:  # "a" = append (adiciona ao final)
                for elem in tmp_log_list:
                    garbage = f.write(f"{elem}\n")
                    print (elem)
        
        tmp_df.loc[len(tmp_df)] = tmp_persona_answer
        tmp_df.to_csv("registry/" + start + "_" + modelo + "/" + start + "_" + modelo + "_answers.csv", index=False)
    
        with open(log_file, "a") as f:  # "a" = append (adiciona ao final)
            garbage = f.write( ">>> TEMPO: %s segundos (persona) <<<\n\n" % (time.time() - persona_start_time) )
            print (">>> TEMPO: %s segundos (persona) <<<\n" % (time.time() - persona_start_time))
        
        if i == 1: # remover <<< <<< <<<
            #break # remover <<< <<< <<<
            pass # remover <<< <<< <<<
        i += 1 # remover <<< <<< <<<
        
    return tmp_df , start

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
