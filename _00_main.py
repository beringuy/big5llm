
import pandas as pd

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# SETUP:
# - LEVELS
# - PILLAR_LIST
# - INV_QUEST
# - MODELO
# - BASE_PROMPT

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from _01_persona_gen import combine_factors, level_personas

# PERSONAS: 

LEVELS = ["highly", "slightly"]

PILLAR_LIST = {
    "Openness" : ["open to experience", "closed to experience"],
    "Conscientiousness" : ["conscientious", "unconscientious"],
    "Extraversion" : ["extroverted", "introverted"],
    "Agreeableness" : ["agreeable", "antagonistic"],
    "Neuroticism" : ["neurotic", "emotionally stable"],
    }

persona_list = combine_factors(PILLAR_LIST)
for i in persona_list:
    print (i)
len (persona_list)

leveled_personalities_list = level_personas (persona_list, LEVELS)
for i in leveled_personalities_list:
    print (i)
len (leveled_personalities_list)



main_personalities_list = leveled_personalities_list
for i in main_personalities_list:
    print (i)

# # # # # # # # # #

# INVENTORIE / QUESTIONNAIRE:

INV_QUEST = pd.read_csv("inventories_questionnaires/ipip50.csv")
#print(INV_QUEST)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from _02_runner import inv_quest_runner

# Large Language Model:

MODELO = "gemma3:4b" # "gemma3:1b" ou "gemma3:4b" ou "gemma3:12b" ou "gemma3:27b" ou "gpt-oss:20b"

BASE_PROMPT = '''
You are a character who is {}.
Answer using solely and exclusively 'Strongly disagree', 'Disagree', 'Neither agree nor disagree', 'Agree' or 'Strongly agree', indicating the extent to which you agree or disagree with the following statement, according to your traits.
Answer concisely, objectively, and in the first person.
Statement: '{}'.
'''

answers_df , start_time = inv_quest_runner (main_personalities_list , INV_QUEST , BASE_PROMPT , MODELO)
answers_df
start_time

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from _03_score_count import score_counter, extract_standard_responses

form_answers_df = extract_standard_responses(answers_df , start_time + "_" + MODELO)
form_answers_df

score_df = score_counter (form_answers_df , INV_QUEST , start_time + "_" + MODELO)
score_df

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from _04_score_plot import score_ploter

score_ploter (score_df , INV_QUEST , PILLAR_LIST, str(start_time) + "_" + MODELO)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
