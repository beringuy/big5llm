
import pandas as pd
import re
import os
import ast

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def score_counter (answers_df , inv_quest_df , response_map, experiment_info):
    score_df = pd.DataFrame(columns = ["persona"] + inv_quest_df["item"].tolist())

    invalid_response_counter = 0
    
    for current_row_number in range(len(answers_df)):    
        tmp_persona_score = [answers_df.iloc[current_row_number]["persona"]]

        for i in range(1, len(answers_df.columns)):
            asc_dsc = inv_quest_df.iloc[i - 1]["asc_dsc"]
            response = answers_df.iloc[current_row_number, i]
            
            if response not in response_map:
                print("Warning! Invalid response:")
                print(">>>")
                print(response)
                print("<<<\n")
                print("persona", current_row_number+1, "/ item",i)                
                invalid_response_counter += 1
                tmp_persona_score.append(None)
                continue

            score = response_map[response]

            if asc_dsc == "-":
                score = response_map['REF_VALUE'] - score
            elif asc_dsc != "+":
                print(f"Warning! Invalid value for asc_dsc: {asc_dsc}")

            tmp_persona_score.append(score)

        print("tmp_persona_score:", tmp_persona_score)
        score_df.loc[len(score_df)] = tmp_persona_score

    print("\n")
    print(">>> Invalid responses (total):", invalid_response_counter)
    print("\n")

    os.makedirs("registry/" + experiment_info + "/" , exist_ok=True)
    score_df.to_csv("registry/" + experiment_info + "/" + experiment_info + "_answersScores.csv", index=False)
    return score_df
