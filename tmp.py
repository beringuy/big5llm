
import pandas as pd

def multi_value_counts(df, cols=None):
    """
    Conta a frequência total de cada valor em múltiplas colunas de um DataFrame.
    Retorna uma Series parecida com o resultado de value_counts().
    
    Parâmetros:
    - df: DataFrame
    - cols: lista de colunas a considerar (se None, usa todas as colunas)
    """
    if cols is None:
        cols = df.columns

    return df[cols].melt(value_name='value')['value'].value_counts()



tmp_df_1 = pd.read_csv("registry/20251102_003254_gemma3:27b/20251102_003254_gemma3:27b_answers.csv")
tmp_df_1
tmp_df_1.drop(columns="persona")
multi_value_counts(tmp_df_1.drop(columns="persona"))

tmp_df_2 = pd.read_csv("registry/20251102_032942_gemma3:27b/20251102_032942_gemma3:27b_answers.csv")
tmp_df_2
tmp_df_2.drop(columns="persona")
multi_value_counts(tmp_df_2.drop(columns="persona"))

##########################################################


##########################################################

import ollama

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

resposta = basic_chat(prompt, modelo)
resposta

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import ollama

# histórico global
chat_history = []

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
    
    print (chat_history)

    return content

prompt = ""
while prompt != "sair":
    prompt = input("Diga algo ('sair' para encerrar):")
    resposta = chat_with_memory(prompt, "gemma3:4b")
    print(resposta)

##########################################################

import pandas as pd

score_df = pd.read_csv("registry/20251115_202419_gemma3:4b/20251115_202419_gemma3:4b_answersScores.csv")

inv_quest = pd.read_csv("inventories_questionnaires/mfq30_pt2.csv")

pillar_list = {
    "Openness" : ["open to experience", "closed to experience"],
    "Conscientiousness" : ["conscientious", "unconscientious"],
    "Extraversion" : ["extroverted", "introverted"],
    #"Agreeableness" : ["agreeable", "antagonistic"],
    #"Neuroticism" : ["neurotic", "emotionally stable"],
    }


score_df[ inv_quest[inv_quest["factor"] == pilar]["item"].to_list() ]

for pilar in pillar_list:
    print(pilar)
    tmp_df = score_df[ inv_quest[inv_quest["factor"] == pilar]["item"].to_list() ]
    new_df[pilar + "_score"] = tmp_df.sum(axis=1)
    
    
inv_quest[inv_quest["factor"] == "Harm_Care"]["item"].to_list()

##########################################################

import ollama
import pandas as pd
import time
import os
import re
from datetime import datetime

# # # # # # # # # # # # # # #

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


prompt = """
You are a character who is extroverted and agreeable. 
 Answer using solely 'strongly disagree', 'disagree', 'neither agree nor disagree', 'agree', 'strongly agree', indicating the extent to which you agree or disagree with the following statement based on your traits. 
 Answer concisely, objectively, and in the first person.
 Do not justify or explain your answers. 
 Statement: 'Acts as they believe they should.'
 Response: strongly agree
 Statement: 'Usually trusts people.'. 
 Response:
"""


resposta = basic_chat(prompt, "gemma3:12b", 0)
print(resposta)
