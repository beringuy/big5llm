
import pandas as pd
import numpy as np
import re
import os
import matplotlib.pyplot as plt

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def count_unique_first_elements(df, colname, i):
    # Extrai o primeiro elemento de cada lista (se existir)
    first_elements = df[colname].apply(lambda x: x[i] if isinstance(x, list) and len(x) > 0 else None)
    
    # Retorna a contagem de valores únicos (ignorando None)
    unique_values = first_elements.dropna().unique()
    return unique_values

# # # # # # # # # #

def score_ploter (score_df , inv_quest , pillar_list, info):
    
    new_df = score_df[["persona"]]    
    new_df["factor_list"] = new_df["persona"].apply(
        lambda x: [i.strip() for i in re.split(r",| and ", x)]
    )
    
    for pilar in pillar_list:
        print(pilar)
        tmp_df = score_df[ inv_quest[inv_quest["factor"] == pilar]["item"].to_list() ]
        new_df[pilar + "_score"] = tmp_df.sum(axis=1)
    new_df
    
    for i in range ( len(new_df["factor_list"][0]) ):        
        categorias = list(count_unique_first_elements(new_df , "factor_list", i))
        df_filtrado = new_df[new_df["factor_list"].apply(lambda lista: any(x in categorias for x in lista))]
        
        # Criar um dicionário com listas de valores de score por categoria
        dados = {
            cat: df_filtrado[df_filtrado["factor_list"].apply(lambda x: cat in x)][list(pillar_list.keys())[i]+"_score"]
            for cat in categorias
        }
        
        # ⚡️ Ordenar categorias pela média dos valores
        dados_ordenados = dict(
            sorted(dados.items(), key=lambda kv: np.nanmean(kv[1]), reverse=False)
        )
        # reverse=False → ordem crescente; reverse=True → decrescente
        
        # Gerar o boxplot
        plt.figure(figsize=(8, 5))
        plt.boxplot(dados_ordenados.values(), labels=dados_ordenados.keys(), patch_artist=True, showmeans=True)
        
        plt.title("Distribuição de score")
        plt.xlabel("Grau do fator")
        plt.xticks(rotation=45)
        plt.ylabel("Score")
        plt.grid(True, linestyle="--", alpha=0.5)
        
        os.makedirs("registry/" + info + "/vis/" , exist_ok=True)
        plt.savefig("registry/" + info + "/vis/boxplot_" + str(list(pillar_list.keys())[i]) + ".png", dpi=300, bbox_inches="tight")
        plt.close()
    
    return None