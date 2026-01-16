
# fazer chat statefull

# ATUALIZAR REQUIREMENTS

import pandas as pd

from src.personaGenAI.persona_gen import combine_dimensions, level_personas
from src.personaGenAI.run_inv_quest_llm import run_inv_quest_llm_stateless, run_inv_quest_llm_statefull
from src.personaGenAI.score_count import score_counter, extract_standard_responses
from src.personaGenAI.score_plot import score_ploter

###########################

# SETUP

CLIENT = [
    "ollama", # 0
    "groq",   # 1
    ][0]

if CLIENT == "ollama":
    MODEL = [
        # ollama:
        "gemma3:1b",       # 0
        "gemma3:4b",       # 1
        "gemma3:12b",      # 2
        "gemma3:27b",      # 3
        "gpt-oss:20b",     # 4
        "qwen3:14b",       # 5
        "deepseek-r1:14b", # 6
        ][0]
if CLIENT == "groq":
    MODEL = [
        # groq:
        "llama-3.1-8b-instant", # 0
        "openai/gpt-oss-20b",   # 1
        ][0]

TEMPERATURE = 0

LEVELS = [
    [""],                     # 0
    ["highly ", "slightly "], # 1
    ][0]

PSYCH_DOMAIN_CAT = [
    "personality_bigfive", # 0
    "unspecified",         # 1
    "morality_mft_tmp1",   # 2
    "morality_mft_tmp2",   # 3
    ][0]

INV_QUEST_CAT = [
    "bfi44",     # 0
    "ipip50",    # 1
    "mfq30_pt1", # 2
    "mfq30_pt2", # 3
    ][0]

EXP_TYPE = [
    "stateless", # 0
    "statefull", # 1
    ][0]

###########################

###########################

PSYCH_DOMAINS = {
    "personality_bigfive" : {
        #"Openness" : [
        #    "open to experience",
        #    "closed to experience",
        #    ],
        #"Conscientiousness" : [
        #    "conscientious",
        #    "unconscientious",
        #    ],
        "Extraversion" : [
            "extroverted",
            "introverted",
            ],
        "Agreeableness" : [
            "agreeable",
            "antagonistic",
            ],
        #"Neuroticism" : [
        #    "neurotic",
        #    "emotionally stable",
        #    ],
        "BASE_PROMPT" : "You are a character who is {}.",
    },
    
    "unspecified" : {
        "Unspecified" : [""],
        "BASE_PROMPT" : "",
    },
    
    "morality_mft_tmp1" : {
        "Harm_Care" : [
            "cares about the well-being of others",
            "is not concerned with the well-being of others",
            ],
        "Fairness_Reciprocity" : [
            "cares about reciprocity",
            "is not concerned with reciprocity",
            ],
        "In-group_Loyalty" : [
            "cares about loyalty to your group",
            "is not concerned with loyalty to your group",
            ],
        "Authority_Respect" : [
            "cares about respecting hierarchies or authority figures",
            "is not concerned with respecting hierarchies or authority figures",
            ],
        "Purity_Sanctity" : [
            "cares about moral purity or spiritual elevation",
            "is not concerned with moral purity or spiritual elevation",
            ],
        "BASE_PROMPT" : "You are a character who {}.",
    },
    
    "morality_mft_tmp2" : {
        "Harm_Care" : [
            "cares strongly about the well-being of others",
            "cares slightly about the well-being of others",
            "is not concerned with the well-being of others",
            ],
        "Fairness_Reciprocity" : [
            "cares strongly about reciprocity",
            "cares slightly about reciprocity",
            "is not concerned with reciprocity",
            ],
        "In-group_Loyalty" : [
            "cares strongly about loyalty to your group",
            "cares slightly about loyalty to your group",
            "is not concerned with loyalty to your group",
            ],
        "Authority_Respect" : [
            "cares strongly about respecting hierarchies or authority figures",
            "cares slightly about respecting hierarchies or authority figures",
            "is not concerned with respecting hierarchies or authority figures",
            ],
        "Purity_Sanctity" : [
            "cares strongly about moral purity or spiritual elevation",
            "cares slightly about moral purity or spiritual elevation",
            "is not concerned with moral purity or spiritual elevation",
            ],
        "BASE_PROMPT" : "You are a character who {}.",
    },
}

INV_QUEST = {
    "bfi44" : {
        "path" : "inventories_questionnaires/bfi44.csv",
        
        "base_prompt" : ''' {} 
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
    
    
    
    "ipip50" : {
        "path" : "inventories_questionnaires/ipip50.csv",
        
        "base_prompt" : ''' {} 
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
    
    
    
    "mfq30_pt1" : {
        "path" : "inventories_questionnaires/mfq30_pt1.csv",
        
        "base_prompt" : ''' {} 
 Answer concisely, objectively, and in the first person, based on your traits. Do not justify or explain your answers. 
 When you decide whether something is right or wrong, to what extent are the following considerations relevant to your thinking? 
 Answer using solely {}. 
 
 Consideration: '{}'. 
 Response: ''',
            
        "answers" : {
            'not at all relevant':0,
            'not very relevant':1,
            'slightly relevant':2,
            'somewhat relevant':3,
            'very relevant':4,
            'extremely relevant':5,
            'REF_VALUE':5,
        },
    },
}

##########################################################################################



##########################################################################################

class AIPsychExperiment:
    def __init__(self, client, model, temperature, psych_domain_cat, dimension_levels, inv_quest_cat, experiment_type = "stateless"):
        self.client = client
        self.model = model
        self.temperature = temperature
        
        self.psych_domain_cat = psych_domain_cat
        self.psych_domain_dimensions = PSYCH_DOMAINS[self.psych_domain_cat].copy()
        self.psych_domain_dimensions.pop("BASE_PROMPT", None)
        self.psych_domain_base_prompt = PSYCH_DOMAINS[self.psych_domain_cat]["BASE_PROMPT"]
        self.dimension_levels = dimension_levels        
        self.persona_list = combine_dimensions(self.psych_domain_dimensions)
        self.leveled_persona_list = level_personas(self.persona_list, self.dimension_levels)
        self.leveled_persona_list_prompt = [PSYCH_DOMAINS[self.psych_domain_cat]["BASE_PROMPT"].format(i) for i in self.leveled_persona_list]
        
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
        
        self.experiment_score_by_dimensions = None
        
    def run_experiment(self):
        if self.experiment_type == "stateless":
            self.experiment_info, self.experiment_responses, self.experiment_start_time = run_inv_quest_llm_stateless (self.leveled_persona_list,
                                                                                                                       self.psych_domain_base_prompt,
                                                                                                                       self.leveled_persona_list_prompt,
                                                                                                                       self.inv_quest,
                                                                                                                       self.inv_quest_base_prompt,
                                                                                                                       
                                                                                                                       self.psych_domain_cat,
                                                                                                                       self.inv_quest_cat,
                                                                                                                       self.experiment_type,
                                                                                                                       self.inv_quest_answers_str,
                                                                                                                       
                                                                                                                       self.client,
                                                                                                                       self.model,
                                                                                                                       self.temperature)
        elif self.experiment_type == "statefull":
            self.experiment_info, self.experiment_responses, self.experiment_start_time = run_inv_quest_llm_statefull (self.leveled_persona_list,
                                                                                                                       self.psych_domain_base_prompt,
                                                                                                                       self.leveled_persona_list_prompt,
                                                                                                                       self.inv_quest,
                                                                                                                       self.inv_quest_base_prompt,
                                                                                                                       
                                                                                                                       self.psych_domain_cat,
                                                                                                                       self.inv_quest_cat,
                                                                                                                       self.experiment_type,
                                                                                                                       self.inv_quest_answers_str,
                                                                                                                       
                                                                                                                       self.client,
                                                                                                                       self.model,
                                                                                                                       self.temperature)
        else:
            print(">>> Invalid experiment_type. Try 'stateless' or 'statefull'!")
            
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
        self.experiment_score_by_dimensions = score_ploter (self.experiment_score,
                                                            self.inv_quest,
                                                            self.psych_domain_dimensions,
                                                            self.experiment_info)
        
    def run_all(self):
        self.run_experiment()
        self.plot_graphs()


##########################################################################################



##########################################################################################

exp1 = AIPsychExperiment(CLIENT, MODEL, TEMPERATURE, PSYCH_DOMAIN_CAT, LEVELS, INV_QUEST_CAT, EXP_TYPE)

exp1.client
exp1.model
exp1.temperature
exp1.psych_domain_cat
exp1.psych_domain_dimensions
exp1.psych_domain_base_prompt
exp1.dimension_levels
exp1.persona_list
exp1.leveled_persona_list
exp1.leveled_persona_list_prompt
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

print(exp1.experiment_score_by_dimensions)

###########################

###########################

exp1.run_experiment()

exp1.experiment_info
exp1.experiment_responses
exp1.experiment_start_time

exp1.experiment_std_responses
exp1.experiment_score

exp1.plot_graphs()

exp1.experiment_score_by_dimensions

