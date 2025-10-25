
import pandas as pd

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from _01_persona_gen import combine_factors, level_personas

# PERSONAS: 

levels = ["highly", "slightly"]

pillar_list = {
    "openness" : ["open to experience", "closed to experience"],
    "conscientiousness" : ["conscientious", "unconscientious"],
    "extraversion" : ["extroverted", "introverted"],
    "agreeableness" : ["agreeable", "antagonistic"],
    "neuroticism" : ["neurotic", "emotionally stable"],
    }

persona_list = combine_factors(pillar_list)
for i in persona_list:
    print (i)
len (persona_list)

leveled_personalities_list = level_personas (persona_list, levels)
for i in leveled_personalities_list:
    print (i)
len (leveled_personalities_list)



main_personalities_list = leveled_personalities_list
for i in main_personalities_list:
    print (i)

# # # # # # # # # #

# INVENTORIE / QUESTIONNAIRE:

ipip50df = pd.read_csv("inventories_questionnaires/ipip50.csv")
#ipip50df = ipip50df[0:5]
ipip50df

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from _02_runner import inv_quest_runner

# Large Language Model:

modelo = "gemma3:4b" # "gemma3:1b" ou "gemma3:4b" ou "gemma3:12b" ou "gemma3:27b" ou "gpt-oss:20b"

base_prompt = '''
You are a character who is {}.
Answer concisely, objectively, and in the first person, using only 'Strongly disagree', 'Disagree', 'Neither agree nor disagree', 'Agree', 'Strongly agree', indicating the extent to which you agree or disagree with the following statement.
Statement: '{}'.
'''

answers_df , start_time = inv_quest_runner (main_personalities_list , ipip50df , base_prompt , modelo)
answers_df
start_time

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from _03_score_count import score_counter, extract_standard_responses

form_answers_df = extract_standard_responses(answers_df , start_time + "_" + modelo)
form_answers_df

score_df = score_counter (form_answers_df , ipip50df , start_time + "_" + modelo)
score_df

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #




