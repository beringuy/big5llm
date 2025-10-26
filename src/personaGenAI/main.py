
import pandas as pd

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# SETUP:
# - LEVELS
LEVELS = ["highly", "slightly"]

# - PILLAR_LIST
PILLAR_LIST = {
    "Openness" : ["open to experience", "closed to experience"],
    "Conscientiousness" : ["conscientious", "unconscientious"],
    "Extraversion" : ["extroverted", "introverted"],
    "Agreeableness" : ["agreeable", "antagonistic"],
    "Neuroticism" : ["neurotic", "emotionally stable"],
    }

# - INV_QUEST
INV_QUEST = pd.read_csv("inventories_questionnaires/ipip50.csv")
# INV_QUEST

# - ANSWERS
# Mapeamento base das respostas
ANSWERS = {
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

# - MODELO
MODELO = "gemma3:12b" # "gemma3:1b" ou "gemma3:4b" ou "gemma3:12b" ou "gemma3:27b" ou "gpt-oss:20b"

# - BASE_PROMPT
BASE_PROMPT = '''
You are a character who is {}.
Answer using solely 'Strongly disagree', 'Disagree', 'Neither agree nor disagree', 'Agree' or 'Strongly agree', indicating the extent to which you agree or disagree with the following statement based on your traits.
Answer concisely, objectively, and in the first person. Do not justify or explain your answers.
Statement: '{}'.
'''

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from src.personaGenAI.persona_gen import combine_factors, level_personas

# PERSONAS: 

persona_list = combine_factors(PILLAR_LIST)
print ("-- persona_list length" , len (persona_list))

leveled_personalities_list = level_personas (persona_list, LEVELS)
print ("-- leveled_personalities_list length" , len (leveled_personalities_list))

main_personalities_list = leveled_personalities_list
for i in main_personalities_list:
    print (i)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from src.personaGenAI.run_inv_quest_llm import run_inv_quest_llm_1

# LARGE LANGUAGE MODEL:

answers_df , start_time = run_inv_quest_llm_1 (main_personalities_list , INV_QUEST , BASE_PROMPT , MODELO)
answers_df
start_time

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from src.personaGenAI.score_count import score_counter, extract_standard_responses

# SCORES:

form_answers_df = extract_standard_responses(answers_df , start_time + "_" + MODELO) # ver: valid_responses
form_answers_df

score_df = score_counter (form_answers_df , INV_QUEST , ANSWERS , start_time + "_" + MODELO)
score_df

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from src.personaGenAI.score_plot import score_ploter

# PLOT:

score_ploter (score_df , INV_QUEST , PILLAR_LIST, str(start_time) + "_" + MODELO)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
