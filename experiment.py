
# temperature, tok k, etc.

import pandas as pd

from src.personaGenAI.persona_gen import combine_dimensions, level_personas # OK <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
from src.personaGenAI.run_inv_quest_llm import run_inv_quest_llm
from src.personaGenAI.score_count import score_counter, extract_standard_responses
from src.personaGenAI.score_plot import score_ploter

###########################

# SETUP

MODEL = "gemma3:4b" # "gemma3:1b" ou "gemma3:4b" ou "gemma3:12b" ou "gemma3:27b" ou "gpt-oss:20b"
MODEL = "gpt-oss:20b"

TEMPERATURE = 0

LEVELS = [
    #"highly ",
    #"slightly "
    ]

PSYCH_DOMAIN_CAT = "personality_bigfive"

INV_QUEST_CAT = "bfi44"

###########################

###########################

PSYCH_DOMAINS = {
    "personality_bigfive" : {
        #"Openness" : ["open to experience", "closed to experience"],
        #"Conscientiousness" : ["conscientious", "unconscientious"],
        "Extraversion" : ["extroverted", "introverted"],
        "Agreeableness" : ["agreeable", "antagonistic"],
        #"Neuroticism" : ["neurotic", "emotionally stable"],
    }
}

INV_QUEST = {
    "bfi44" : {
        "path" : "inventories_questionnaires/bfi44.csv",
        
        "base_prompt" : ''' You are a character who is {}. 
 Answer using solely {}, indicating the extent to which you agree or disagree with the following statement based on your traits. 
 Answer concisely, objectively, and in the first person.
 Do not justify or explain your answers. 
 
 Statement: 'Acts as they believe they should.'
 Response: strongly agree
 
 Statement: '{}'. 
 Response: ''',
            
        "answers" : {
            "strongly disagree": 1,
            "disagree": 2,
            "neither agree nor disagree": 3,
            "agree": 4,
            "strongly agree": 5,
            'REF_VALUE':6,
        },
    },
}

###########################

# MODIFICAR:




##########################################################################################



##########################################################################################

class AIPsychExperiment:
    def __init__(self, model, temperature, psych_domain_cat, dimension_levels, inv_quest_cat, experiment_type = "stateless"):
        self.model = model
        self.temperature = temperature
        
        self.psych_domain_cat = psych_domain_cat
        self.psych_domain_dimensions = PSYCH_DOMAINS[self.psych_domain_cat]
        self.dimension_levels = dimension_levels
        self.persona_list = combine_dimensions(self.psych_domain_dimensions)
        self.leveled_persona_list = level_personas(self.persona_list, self.dimension_levels)
        
        self.inv_quest_cat = inv_quest_cat        
        self.inv_quest_path = INV_QUEST[self.inv_quest_cat]["path"]
        self.inv_quest = pd.read_csv(self.inv_quest_path)
        self.inv_quest_dimensions = list(self.inv_quest["dimension"].value_counts().keys())
        self.inv_quest_base_prompt = INV_QUEST[self.inv_quest_cat]["base_prompt"]        
        self.inv_quest_answers_score = INV_QUEST[self.inv_quest_cat]["answers"]
        self.inv_quest_answers_str = ", ".join(f"'{k}'" for k in list(self.inv_quest_answers_score.keys())[:-1])
        
        self.experiment_type = str(experiment_type).lower()
        self.experiment_info = None
        self.experiment_responses = None
        self.experiment_start_time = None
        
        self.experiment_std_responses = None
        self.experiment_score = None
        
    def run_experiment(self):
        if self.experiment_type == "stateless":
            self.experiment_info, self.experiment_responses, self.experiment_start_time = run_inv_quest_llm (self.leveled_persona_list,
                                                                                                             self.inv_quest,
                                                                                                             self.inv_quest_base_prompt,
                                                                                                             
                                                                                                             self.psych_domain_cat,
                                                                                                             self.inv_quest_cat,
                                                                                                             self.experiment_type,
                                                                                                             self.inv_quest_answers_str,
                                                                                                             
                                                                                                             self.model,
                                                                                                             self.temperature)
        elif self.experiment_type == "statefull":
            pass
        else:
            print("Invalid experiment_type. Try 'stateless' or 'statefull'!")
            
        '''
        self.experiment_std_responses = extract_standard_responses(self.experiment_responses,
                                                                   self.inv_quest_answers_str,
                                                                   self.experiment_info) # TALVEZ REMOVER ESSA ETAPA SE AS RESPOSTAS ESTÃO OKs
        
        self.experiment_score = score_counter (self.experiment_std_responses,
                                               self.inv_quest,
                                               self.inv_quest_answers_score,
                                               self.experiment_info)
        #'''
        
        self.experiment_score = score_counter (self.experiment_responses,
                                               self.inv_quest,
                                               self.inv_quest_answers_score,
                                               self.experiment_info)
    
    def plot_graphs(self):
        score_ploter (self.experiment_score,
                      self.inv_quest,
                      self.psych_domain_dimensions,
                      self.experiment_info)
        
    def run_all(self):
        self.run_experiment()
        self.plot_graphs()


##########################################################################################



##########################################################################################

exp1 = AIPsychExperiment(MODEL, TEMPERATURE, PSYCH_DOMAIN_CAT, LEVELS, INV_QUEST_CAT)

exp1.model
exp1.temperature
exp1.psych_domain_cat
exp1.psych_domain_dimensions
exp1.dimension_levels
exp1.persona_list
exp1.leveled_persona_list
exp1.inv_quest_cat
exp1.inv_quest_path
exp1.inv_quest
exp1.inv_quest_dimensions
exp1.inv_quest_base_prompt
exp1.inv_quest_answers_score
exp1.inv_quest_answers_str

exp1.experiment_type
print(exp1.experiment_info)
print(exp1.experiment_responses)
print(exp1.experiment_start_time)

print(exp1.experiment_std_responses)
print(exp1.experiment_score)

###########################

###########################

exp1.run_experiment()

exp1.experiment_info
exp1.experiment_responses
exp1.experiment_start_time

exp1.experiment_std_responses
exp1.experiment_score

exp1.plot_graphs()
