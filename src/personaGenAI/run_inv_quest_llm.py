
import ollama
from groq import Groq
# pip install python-dotenv
from dotenv import load_dotenv

import pandas as pd
import time
import os
import re
from datetime import datetime

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

MODELS_WITH_THINK = {
    "gpt-oss:20b",
    #"qwen3:14b",
    #"deepseek-r1:14b",
}

# CRIAR ".env" com "GROQ_API_KEY=[groq_api_key]"
load_dotenv()

#groq_api_key = os.getenv("GROQ_API_KEY")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# histórico global
chat_history = []

def llm_chat(prompt, client, model, experiment_type, temperature=None):
    global chat_history
    
    # adiciona a nova mensagem do usuário ao histórico
    chat_history.append({"role": "user", "content": prompt})
    
    if experiment_type == "stateless":
        kwargs = {
            "model": model,        
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }
        
    if experiment_type == "statefull":
        kwargs = {
            "model": model,        
            "messages": chat_history,
        }
    
    
    if client == "ollama":
        if temperature is not None:
            kwargs["options"] = {"temperature": temperature}

        if model in MODELS_WITH_THINK:
            kwargs["think"] = "low"

        resposta = ollama.chat(**kwargs)
        
        # adiciona a resposta ao histórico
        chat_history.append({"role": "assistant", "content": resposta["message"]["content"]})
        print ("\n-- Chat History:", chat_history)
        
        return resposta["message"]["content"]
    
    elif client == "groq": # or client == "openai" (CONFERIR)
        if temperature is not None:
            kwargs["temperature"] = temperature

        response = Groq().chat.completions.create(**kwargs)
        #response = Groq(api_key=groq_api_key).chat.completions.create(**kwargs)
        
        # adiciona a resposta ao histórico
        chat_history.append({"role": "assistant", "content": response.choices[0].message.content})
        print ("\n-- Chat History:", chat_history)
        
        return response.choices[0].message.content

    else:
        print(">>> Warning! Invalid Client!!!")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def run_inv_quest_llm (persona_list, psych_domain_base_prompt, persona_list_prompt, inv_quest_df, base_prompt,
                                 psych_domain_cat, inv_quest_cat, experiment_type, inv_quest_answers_str,
                                 client = "ollama", model = "gemma3:12b", temperature = None):
    
    global chat_history
    
    tmp_df = pd.DataFrame(columns = ["persona"] + inv_quest_df["item"].tolist())
    tmp_df
    
    start = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    exp_base_name = start + "__" + client + "_" + model  + "__p_" + psych_domain_cat + "__i_" + inv_quest_cat + "__" + experiment_type
    exp_dir = "registry/" + exp_base_name + "/"
    os.makedirs(exp_dir , exist_ok=True)
    
    log_file = exp_dir + exp_base_name +  "_logfile.txt"
    
    persona_id = 0
    for current_persona, current_persona_prompt in zip(persona_list, persona_list_prompt):
        #print("-current_persona: ",current_persona)
        #print("-current_persona_prompt: ",current_persona_prompt)
        persona_start_time = time.time()
        tmp_persona_response = [current_persona]
        
        item_id = 0
        for statement in inv_quest_df["item"].tolist():
            #print (statement)
            
            if (item_id == 0 and experiment_type == "statefull") or experiment_type == "stateless":
                prompt = base_prompt.format(current_persona_prompt, inv_quest_answers_str, statement)
            elif experiment_type == "statefull":
                prompt = """ Statement: '{}'. 
 Response: """.format(statement)
            else:
                print(">>> Warning! Invalid experiment_type!!!")
    
            statement_start_time = time.time()
            
            resposta = llm_chat(prompt, client, model, experiment_type, temperature)
            resposta = re.sub(r"\.$", "", resposta.strip().lower())
            
            tmp_log_list = []
    
            tmp_log_list.append("\n=== === === === === ===")
            tmp_log_list.append("persona " + str(persona_id+1) + " / item " + str(item_id+1))
            tmp_log_list.append("Persona: " + current_persona)
            tmp_log_list.append("Statement: " + statement)
            tmp_log_list.append("Response: " + resposta)
            tmp_persona_response.append(resposta)
    
            tmp_log_list.append(">>> Runtime: %s seconds (statement) <<<" % (time.time() - statement_start_time))
            tmp_log_list.append("=== === === === === ===\n")
            
            item_id += 1
            
            print ("\n-- Prompt:")
            print (prompt, "\n")
            with open(log_file, "a") as f:  # "a" = append (adiciona ao final)
                for elem in tmp_log_list:
                    tmp = f.write(f"{elem}\n")
                    print (elem)
        
        tmp_df.loc[len(tmp_df)] = tmp_persona_response
        tmp_df.to_csv(exp_dir + exp_base_name + "_responses.csv", index=False)
    
        with open(log_file, "a") as f:  # "a" = append (adiciona ao final)
            tmp = f.write( ">>> Runtime: %s seconds (persona) <<<\n\n" % (time.time() - persona_start_time) )
            print (">>> Runtime: %s seconds (persona) <<<\n" % (time.time() - persona_start_time))
            
            tmp = f.write(str(chat_history))
            tmp = f.write("\n\n")
            tmp = f.write("<<< <<< <<< <<< <<< <<<")
            tmp = f.write("\n\n")
            
        chat_history = []
        persona_id += 1
        
        #print("--Check:")
        #print(exp_base_name)
        #print(tmp_df)
        #print(start)
        #print("\n")
        
    return exp_base_name, tmp_df, start

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
