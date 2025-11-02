
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

##########################################################

prompt = ""
while prompt != "sair":
    prompt = input("Diga algo ('sair' para encerrar):")
    resposta = chat_with_memory(prompt, "gemma3:4b")
    print(resposta)