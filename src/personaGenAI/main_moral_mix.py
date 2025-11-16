
import pandas as pd

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# SETUP:
# - LEVELS
LEVELS = [""]

# - PILLAR_LIST
PILLAR_LIST = {
    "Openness" : ["open to experience", "closed to experience"],
    #"Conscientiousness" : ["conscientious", "unconscientious"],
    "Extraversion" : ["extroverted", "introverted"],
    #"Agreeableness" : ["agreeable", "antagonistic"],
    #"Neuroticism" : ["neurotic", "emotionally stable"],
    }

# - INV_QUEST
INV_QUEST_1 = pd.read_csv("inventories_questionnaires/mfq30_pt1.csv")
INV_QUEST_2 = pd.read_csv("inventories_questionnaires/mfq30_pt2.csv")
# INV_QUEST

# - ANSWERS
# Mapeamento base das respostas
ANSWERS_1 = {
    'Not at all relevant.':0,
    'Not very relevant.':1,
    'Slightly relevant.':2,
    'Somewhat relevant.':3,
    'Very relevant.':4,
    'Extremely relevant.':5,
    'Not at all relevant':0,
    'Not very relevant':1,
    'Slightly relevant':2,
    'Somewhat relevant':3,
    'Very relevant':4,
    'Extremely relevant':5,
    'REF_VALUE':5,
}

ANSWERS_2 = {
    'Strongly disagree.':0,
    'Moderately disagree.':1,
    'Slightly disagree.':2,
    'Slightly agree.':3,
    'Moderately agree.':4,
    'Strongly agree.':5,
    'Strongly disagree':0,
    'Moderately disagree':1,
    'Slightly disagree':2,
    'Slightly agree':3,
    'Moderately agree':4,
    'Strongly agree':5,
    'REF_VALUE':5,
}

# - MODELO
MODELO = "gemma3:12b" # "gemma3:1b" ou "gemma3:4b" ou "gemma3:12b" ou "gemma3:27b" ou "gpt-oss:20b"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

try:
    from src.personaGenAI.persona_gen import combine_factors, level_personas
except:
    from persona_gen import combine_factors, level_personas

# PERSONAS: 

persona_list = combine_factors(PILLAR_LIST)
print ("-- persona_list length" , len (persona_list))

leveled_personalities_list = level_personas (persona_list, LEVELS) # <<<<<<< PQ DÀ ERRADO?
print ("-- leveled_personalities_list length" , len (leveled_personalities_list))

main_personalities_list = persona_list
for i in main_personalities_list:
    print (i)
print (len(main_personalities_list))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

try:
    from src.personaGenAI.run_inv_quest_llm import run_inv_quest_llm_moral_pt1 , run_inv_quest_llm_moral_pt2
except:
    from run_inv_quest_llm import run_inv_quest_llm_moral_pt1 , run_inv_quest_llm_moral_pt2

# LARGE LANGUAGE MODEL:

# ETAPA 1:
#"""
answers_df_1 , start_time_1 = run_inv_quest_llm_moral_pt1 (main_personalities_list , INV_QUEST_1 , MODELO)
answers_df_1
start_time_1
#"""

# ETAPA 2:

answers_df_2 , start_time_2 = run_inv_quest_llm_moral_pt2 (main_personalities_list , INV_QUEST_2 , MODELO)
answers_df_2
start_time_2

#BREAK

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

try:
    from src.personaGenAI.score_count import score_counter, extract_standard_responses
except:
    from score_count import score_counter, extract_standard_responses

# SCORES:

# ETAPA 1:

score_df_1 = score_counter (answers_df_1 , INV_QUEST_1 , ANSWERS_1 , start_time_1 + "_" + MODELO)
#score_df_1 = pd.read_csv("registry/20251104_223516_gemma3:12b/20251104_223516_gemma3:12b_answersScores.csv")
score_df_1

# ETAPA 2:

score_df_2 = score_counter (answers_df_2 , INV_QUEST_2 , ANSWERS_2 , start_time_2 + "_" + MODELO)
#score_df_2 = pd.read_csv("registry/20251104_225248_gemma3:12b/20251104_225248_gemma3:12b_answersScores.csv")
score_df_2

"""
# MERGE:
score_df = pd.merge(score_df_1, score_df_2, on='persona', how='inner')
score_df.columns
score_df

try:
    from src.personaGenAI.aux import multi_value_counts
except:
    from aux import multi_value_counts

multi_value_counts(score_df.drop(columns="persona"))
#"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

try:
    from src.personaGenAI.score_plot import score_ploter
except:
    from score_plot import score_ploter

# PLOT:

score_ploter (score_df_1 , INV_QUEST_1, PILLAR_LIST, str(start_time_1) + "_" + MODELO)
score_ploter (score_df_2 , INV_QUEST_2, PILLAR_LIST, str(start_time_2) + "_" + MODELO)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #







import pandas as pd

PILLAR_LIST = {
    "Openness" : ["open to experience", "closed to experience"],
    #"Conscientiousness" : ["conscientious", "unconscientious"],
    "Extraversion" : ["extroverted", "introverted"],
    #"Agreeableness" : ["agreeable", "antagonistic"],
    #"Neuroticism" : ["neurotic", "emotionally stable"],
    }

INV_QUEST_1 = pd.read_csv("inventories_questionnaires/mfq30_pt1.csv")
INV_QUEST_2 = pd.read_csv("inventories_questionnaires/mfq30_pt2.csv")

MODELO = "gemma3:4b"

try:
    from src.personaGenAI.score_plot import score_ploter
except:
    from score_plot import score_ploter

score_df_1 = pd.read_csv("registry/20251116_110834_gemma3:4b/20251116_110834_gemma3:4b_answersScores.csv")
score_df_2 = pd.read_csv("registry/20251116_110846_gemma3:4b/20251116_110846_gemma3:4b_answersScores.csv")

# PLOT:

score_ploter (score_df_1 , INV_QUEST_1, PILLAR_LIST, '20251116_110834' + "_" + MODELO)
score_ploter (score_df_2 , INV_QUEST_2, PILLAR_LIST, '20251116_110846' + "_" + MODELO)