
from src.personaGenAI.experiment import AIPsychExperiment

###########################
# SETUP OPTIONS

CLIENT = [
    "ollama", # 0
    "groq",   # 1
    ]

MODEL = [
    # ollama:
    "gemma3:1b",       # 0 # OLLAMA
    "gemma3:4b",       # 1 # OLLAMA
    "gemma3:12b",      # 2 # OLLAMA
    "gemma3:27b",      # 3 # OLLAMA
    "gpt-oss:20b",     # 4 # OLLAMA
    "qwen3:14b",       # 5 # OLLAMA
    "deepseek-r1:14b", # 6 # OLLAMA
    "llama-3.1-8b-instant", # 7 # GROQ
    "openai/gpt-oss-120b",   # 8 # GROQ
    "qwen2.5:14b"      # 9 # OLLAMA
    ]

TEMPERATURE = 0

PSYCH_DOMAIN_CAT = [
    "personality_bigfive", # 0
    "unspecified",         # 1
    "morality_mft_v1",   # 2
    "morality_mft_v2",   # 3
    "personality_bigfive_mod" # 4
    ]

LEVELS = [
    [""],                     # 0
    ["highly ", "slightly "], # 1
    ]

INV_QUEST_CAT = [
    "bfi44",     # 0
    "ipip50",    # 1
    "mfq30_pt1", # 2
    "mfq30_pt2", # 3
    ]

EXP_TYPE = [
    "stateless", # 0
    "statefull", # 1
    ]

###########################
# EXPERIMENT RUN

# Models [service, model]:
models = {
    "ollama - gemma3:27b" : [0, 3],
    "ollama - gpt-oss:20b" : [0, 4],
    #"ollama - qwen3:14b" : [0, 5],
    #"ollama - deepseek-r1:14b" : [0, 6],
    "groq - openai/gpt-oss-120b" : [1, 8],
    "ollama - qwen2.5:14b" : [0, 9],
    #"openai - " : [,],
    #"gemini - " : [,],
    }

# for each model [temperature, psych domain, levels, inv/quest, experiment type]:
exps = {
    "A1 - unspecified x personality ipip50 - stateless" : [0, 1, 0, 1, 0],
    "A2 - unspecified x personality ipip50 - statefull" : [0, 1, 0, 1, 1],
    "B1 - leveled Big5 x personality ipip50 - stateless" : [0, 0, 1, 1, 0],
    #"B2 - leveled Big5 x personality ipip50 - statefull" : [0, 0, 1, 1, 1],
    "C1 - unspecified x morality pt1 - stateless" : [0, 1, 0, 2, 0],    
    "C2 - unspecified x morality pt2 - stateless" : [0, 1, 0, 3, 0],
    "C3 - unspecified x morality pt1 - statefull" : [0, 1, 0, 2, 1],
    "C4 - unspecified x morality pt2 - statefull" : [0, 1, 0, 3, 1],
    #"D1a - MFT x morality pt1 - stateless" : [0, 2, 0, 2, 0],
    "D1b - leveled MFT x morality pt1 - stateless" : [0, 3, 0, 2, 0],
    #"D2a - MFT x morality pt2 - stateless" : [0, 2, 0, 3, 0],
    "D2b - leveled MFT x morality pt2 - stateless" : [0, 3, 0, 3, 0],
    #"D3 - MFT x morality pt1 - statefull" : [0, 2, 0, 2, 1],
    #"D4 - MFT x morality pt2 - statefull" : [0, 2, 0, 3, 1],
    #"E1a - leveled Big5 x morality pt1 - stateless" : [0, 0, 1, 2, 0],
    "E1b - Big5 x morality pt1 - stateless" : [0, 0, 0, 2, 0],
    #"E2a - leveled Big5 x morality pt2 - stateless" : [0, 0, 1, 3, 0],
    "E2b - Big5 x morality pt2 - stateless" : [0, 0, 0, 3, 0],
    #"E3 - leveled Big5 x morality pt1 - statefull" : [0, 0, 1, 2, 1],
    #"E4 - leveled Big5 x morality pt2 - statefull" : [0, 0, 1, 3, 1],
    "F1 - MFT x personality ipip50 - stateless" : [0, 2, 0, 1, 0],    
    }


# # # # #

#'''
# SELECTED RUN
models = {
    "ollama - qwen2.5:14b" : [0, 9],
    }
'''
exps = {
    "A0 - leveled Big5 x personality ipip50 - stateless" : [0, 0, 0, 0, 0],
    }
# SELECTED RUN
#'''

# # # # #

for model_selection_setup in models:
    for exp_setup in exps:
        current_setup = models[model_selection_setup] + exps[exp_setup]
        print ("-- Current Setup:",current_setup)
        print ("Client:", CLIENT[current_setup[0]])
        print ("Model:", MODEL[current_setup[1]])
        print ("Temperature:", TEMPERATURE)
        print ("Psy Domain:", PSYCH_DOMAIN_CAT[current_setup[3]])
        print ("Levels", LEVELS[current_setup[4]])
        print ("Inv/Quest:", INV_QUEST_CAT[current_setup[5]])
        print ("Experiment Type:", EXP_TYPE[current_setup[6]])
        
        current_experiment = AIPsychExperiment(CLIENT[current_setup[0]], # service
                                               MODEL[current_setup[1]], # model
                                               TEMPERATURE, # temperature
                                               PSYCH_DOMAIN_CAT[current_setup[3]], # psych domain
                                               LEVELS[current_setup[4]], # levels
                                               INV_QUEST_CAT[current_setup[5]], # inv/quest
                                               EXP_TYPE[current_setup[6]], # experiment type
                                               )
        current_experiment.run_experiment()
        current_experiment.plot_graphs()
