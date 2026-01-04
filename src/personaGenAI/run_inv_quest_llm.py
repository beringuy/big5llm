
import ollama
import pandas as pd
import time
import os
import re
from datetime import datetime

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

MODELS_WITH_THINK = {
    "gpt-oss:20b",
}

def basic_chat(prompt, model, temperature=None):

    kwargs = {
        "model": model,        
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    if temperature is not None:
        kwargs["options"] = {"temperature": temperature}
    
    if model in MODELS_WITH_THINK:
        kwargs["think"] = "low"

    resposta = ollama.chat(**kwargs)
    return resposta["message"]["content"]

# # # # # # # # # #

# GPT MOD:
# histórico global
chat_history = [] # Como resetar a cada nova persona?

def chat_with_memory(prompt, model):
    global chat_history

    # adiciona a nova mensagem do usuário
    chat_history.append({"role": "user", "content": prompt})

    # envia TODO o histórico ao model
    resposta = ollama.chat(
        model=model,
        messages=chat_history
    )

    # extrai a resposta
    content = resposta["message"]["content"]

    # adiciona a resposta ao histórico
    chat_history.append({"role": "assistant", "content": content})
    
    print ("\n-- Chat History:", chat_history)

    return content

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def run_inv_quest_llm (persona_list, inv_quest_df, base_prompt,
                       psych_domain_cat, inv_quest_cat, experiment_type, inv_quest_answers_str,
                       model = "gemma3:12b", temperature = None):
    
    tmp_df = pd.DataFrame(columns = ["persona"] + inv_quest_df["item"].tolist())
    tmp_df
    
    start = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    exp_base_name = start + "__" + model  + "__p_" + psych_domain_cat + "__i_" + inv_quest_cat + "__" + experiment_type
    exp_dir = "registry/" + exp_base_name + "/"
    os.makedirs(exp_dir , exist_ok=True)
    
    log_file = exp_dir + exp_base_name +  "_logfile.txt"
    
    persona_id = 0
    for current_persona in persona_list:
        #print(current_persona)
        persona_start_time = time.time()
        tmp_persona_response = [current_persona]
        item_id = 0
        for statement in inv_quest_df["item"].tolist():
            #print (statement)
            
            prompt = base_prompt.format(current_persona, inv_quest_answers_str, statement)
    
            statement_start_time = time.time()
            resposta = basic_chat(prompt, model, temperature)
            resposta = re.sub(r"\.$", "", resposta.strip().lower())
            
            tmp_log_list = []
    
            tmp_log_list.append("=== === === === === ===")
            tmp_log_list.append("persona " + str(persona_id+1) + " / item " + str(item_id+1))
            tmp_log_list.append("Persona: " + current_persona)
            tmp_log_list.append("Statement: " + statement)
            tmp_log_list.append("Response: " + resposta)
            tmp_persona_response.append(resposta)
    
            tmp_log_list.append(">>> Runtime: %s seconds (statement) <<<" % (time.time() - statement_start_time))
            tmp_log_list.append("=== === === === === ===\n")
            
            item_id += 1
            
            print ("\n-- Prompt:", prompt, "\n")
            with open(log_file, "a") as f:  # "a" = append (adiciona ao final)
                for elem in tmp_log_list:
                    tmp = f.write(f"{elem}\n")
                    print (elem)
        
        tmp_df.loc[len(tmp_df)] = tmp_persona_response
        tmp_df.to_csv(exp_dir + exp_base_name + "_responses.csv", index=False)
    
        with open(log_file, "a") as f:  # "a" = append (adiciona ao final)
            tmp = f.write( ">>> Runtime: %s seconds (persona) <<<\n\n" % (time.time() - persona_start_time) )
            print (">>> Runtime: %s seconds (persona) <<<\n" % (time.time() - persona_start_time))
            
        persona_id += 1
        
    return exp_base_name, tmp_df, start

# # # # # # # # # #

# # # # # # # # # #

def run_inv_quest_llm_pt2 (persona_list , inv_quest_df ,  model = "gemma3:12b"):
    global chat_history
    
    tmp_df = pd.DataFrame(columns = ["persona"] + inv_quest_df["item"].tolist())
    tmp_df
    
    start = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("registry/" + start + "_" + model + "/" , exist_ok=True)
    log_file = "registry/" + start + "_" + model + "/" + start + "_" + model +  "_logfile.txt"
    
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
        resposta = chat_with_memory(prompt, model)
        
        j = 0
        for statement in inv_quest_df["item"].tolist():
            #print (statement)
    
            prompt = "Statement: '{}'.".format(statement)
    
            statement_start_time = time.time()
            resposta = chat_with_memory(prompt, model)
            
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
                    tmp = f.write(f"{elem}\n")
                    print (elem)
        chat_history = []
        
        tmp_df.loc[len(tmp_df)] = tmp_persona_answer
        tmp_df.to_csv("registry/" + start + "_" + model + "/" + start + "_" + model + "_answers.csv", index=False)
    
        with open(log_file, "a") as f:  # "a" = append (adiciona ao final)
            tmp = f.write( ">>> TEMPO: %s segundos (persona) <<<\n\n" % (time.time() - persona_start_time) )
            print (">>> TEMPO: %s segundos (persona) <<<\n" % (time.time() - persona_start_time))
        
        if i == 1: # remover <<< <<< <<<
            #break # remover <<< <<< <<<
            pass # remover <<< <<< <<<
        i += 1 # remover <<< <<< <<<
        
    return tmp_df , start

# # # # # # # # # #

# # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
