
import ollama

##########################################################

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