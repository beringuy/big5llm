
import pandas as pd
import re
import os

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def score_counter (answers_df , inv_quest_df , info):
    score_df = pd.DataFrame(columns = ["persona"] + inv_quest_df["item"].tolist())

    for current_row_number in range(len(answers_df)):    
        tmp_persona_score = [answers_df.iloc[current_row_number]["persona"]]

        for i in range(1, len(answers_df.columns)):
            asc_dsc = inv_quest_df.iloc[i - 1]["asc_dsc"]
            response = answers_df.iloc[current_row_number][i]

            if response not in response_map:
                print(f"Warning! Resposta inválida: {response}")
                tmp_persona_score.append(None)
                continue

            score = response_map[response]

            if asc_dsc == "-":
                score = 6 - score # <<<<<<<<<< tem que ser de acordo com a quantiodade de opções e não 6 <<<<<<<<<<
            elif asc_dsc != "+":
                print(f"Warning! Valor de asc_dsc inválido: {asc_dsc}")

            tmp_persona_score.append(score)

        print("tmp_persona_score:", tmp_persona_score)
        score_df.loc[len(score_df)] = tmp_persona_score

    os.makedirs("registry/" + info + "/" , exist_ok=True)
    score_df.to_csv("registry/" + info + "/" + info + "_answersScores.csv", index=False)
    return score_df

# # # # # # # # # #

# MADE IN GPT:
def extract_standard_responses(df: pd.DataFrame , info) -> pd.DataFrame:
    valid_responses = [
        "Strongly disagree",
        "Strongly agree",
        "Neither agree nor disagree",
        "Disagree",
        "Agree"
    ]

    # Cria um único regex pattern para busca
    pattern = re.compile(
        r"\b(" + "|".join(re.escape(resp.lower()) for resp in valid_responses) + r")\b",
        flags=re.IGNORECASE
    )

    df_clean = df.copy()

    # Para cada coluna (exceto a primeira)
    for col in df.columns[1:]:
        df_clean[col] = (
            df[col]
            .astype(str)
            .apply(lambda text: _extract_match(text, pattern, valid_responses))
        )

    df_clean.to_csv("registry/" + info + "/" + info + "_answersStd.csv", index=False)
    return df_clean

def _extract_match(text, pattern, valid_responses):
    match = pattern.search(text.lower())
    if match:
        found = match.group(1)
        # Garante capitalização idêntica à da lista original
        for resp in valid_responses:
            if found.lower() == resp.lower():
                return resp
    return None

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
