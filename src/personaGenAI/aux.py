
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