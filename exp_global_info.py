
PSYCH_DOMAINS = {
    "personality_bigfive" : {
        "Openness" : [
            "open to experience",
            "closed to experience",
            ],
        "Conscientiousness" : [
            "conscientious",
            "unconscientious",
            ],
        "Extraversion" : [
            "extroverted",
            "introverted",
            ],
        "Agreeableness" : [
            "agreeable",
            "antagonistic",
            ],
        "Neuroticism" : [
            "neurotic",
            "emotionally stable",
            ],
        "BASE_PROMPT" : "You are a character who is {}.",
    },
    
    
    "personality_bigfive_mod" : {
        "Extraversion" : [
            "extroverted",
            "introverted",
            ],
        "Agreeableness" : [
            "agreeable",
            "antagonistic",
            ],
        "BASE_PROMPT" : "You are a character who is {}.",
    },
    
    
    
    "unspecified" : {
        "Unspecified" : [""],
        "BASE_PROMPT" : "",
    },
    
    
    
    "morality_mft_v1" : {
        "Harm_Care" : [
            "cares about the well-being of others",
            "is not concerned with the well-being of others",
            ],
        "Fairness_Reciprocity" : [
            "cares about reciprocity or fairness",
            "is not concerned with reciprocity or fairness",
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
    
    
    "morality_mft_v2" : {
        "Harm_Care" : [
            "cares strongly about the well-being of others",
            "cares slightly about the well-being of others",
            "is not concerned with the well-being of others",
            ],
        "Fairness_Reciprocity" : [
            "cares strongly about reciprocity or fairness",
            "cares slightly about reciprocity or fairness",
            "is not concerned with reciprocity or fairness",
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
 
 Statement: 'Has opinions about various topics.' 
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
 
 Statement: 'Has opinions about various topics.' 
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
 When you decide whether something is right or wrong, to what extent are the following consideration relevant to your thinking? 
 Answer using solely {}. 
 Answer concisely, objectively, and in the first person, based on your traits. 
 Do not justify or explain your answers. 

 Example:
 Consideration: 'Whether or not someone was good at math'. 
 Response: not at all relevant 
 
 Now answer the following consideration: 
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
    
    
    
    "mfq30_pt2" : {
        "path" : "inventories_questionnaires/mfq30_pt2.csv",
        
        "base_prompt" : ''' {} 
 Read the following sentence and indicate your agreement or disagreement. 
 Answer using solely {}. 
 Answer concisely, objectively, and in the first person, based on your traits. 
 Do not justify or explain your answers. 

 Example:
 Sentence: 'It is better to do good than to do bad.'. 
 Response: strongly agree 
 
 Now answer the following sentence: 
 Sentence: '{}'. 
 Response: ''',
            
        "answers" : {
            "strongly disagree": 0,
            "moderately disagree": 1,
            "slightly disagree": 2,
            "slightly agree": 3,
            "moderately agree": 4,
            "strongly agree": 5,
            'REF_VALUE':5,
        },
    },
    
}

###################################################################

palette_classes = {
    "open to experience": "#27E0F5",
    "closed to experience": "#27E0F5",
    "highly open to experience": "#27E0F5",
    "highly closed to experience": "#27E0F5",
    "slightly open to experience": "#27E0F5",
    "slightly closed to experience": "#27E0F5",
    
    "conscientious": "#27F598",
    "unconscientious": "#27F598",
    "highly conscientious": "#27F598",
    "highly unconscientious": "#27F598",
    "slightly conscientious": "#27F598",
    "slightly unconscientious": "#27F598",
    
    "extroverted": "#F5BE27",
    "introverted": "#F5BE27",
    "highly extroverted": "#F5BE27",
    "highly introverted": "#F5BE27",
    "slightly extroverted": "#F5BE27",
    "slightly introverted": "#F5BE27",
    
    "agreeable": "#F5277D",
    "antagonistic": "#F5277D",
    "highly agreeable": "#F5277D",
    "highly antagonistic": "#F5277D",
    "slightly agreeable": "#F5277D",
    "slightly antagonistic": "#F5277D",
    
    "neurotic": "#F87C63",
    "emotionally stable": "#F87C63",
    "highly neurotic": "#F87C63",
    "highly emotionally stable": "#F87C63",
    "slightly neurotic": "#F87C63",
    "slightly emotionally stable": "#F87C63",
    
    
    
    "Others": "grey",
    
    
    
    "cares strongly about the well-being of others": "#F5277D",
    "cares about the well-being of others": "#F5277D",
    "cares slightly about the well-being of others": "#F5277D",
    "is not concerned with the well-being of others": "#F5277D",
    
    "cares strongly about reciprocity or fairness": "#27F598",
    "cares about reciprocity or fairness": "#27F598",
    "cares slightly about reciprocity or fairness": "#27F598",
    "is not concerned with reciprocity or fairness": "#27F598",
    
    "cares strongly about loyalty to your group": "#F87C63",
    "cares about loyalty to your group": "#F87C63",
    "cares slightly about loyalty to your group": "#F87C63",
    "is not concerned with loyalty to your group": "#F87C63",
    
    "cares strongly about respecting hierarchies or authority figures": "#F5BE27",
    "cares about respecting hierarchies or authority figures": "#F5BE27",
    "cares slightly about respecting hierarchies or authority figures": "#F5BE27",
    "is not concerned with respecting hierarchies or authority figures": "#F5BE27",
    
    "cares strongly about moral purity or spiritual elevation": "#27E0F5",
    "cares about moral purity or spiritual elevation": "#27E0F5",
    "cares slightly about moral purity or spiritual elevation": "#27E0F5",
    "is not concerned with moral purity or spiritual elevation": "#27E0F5",
}

ordered_classes = [
        "",
        " ",
    
        "highly open to experience",
        "open to experience",
        "slightly open to experience",
        "slightly closed to experience",
        "closed to experience",
        "highly closed to experience",
        
        "highly conscientious",
        "conscientious",
        "slightly conscientious",
        "slightly unconscientious",
        "unconscientious",
        "highly unconscientious",
        
        "highly extroverted",
        "extroverted",
        "slightly extroverted",
        "slightly introverted",
        "introverted",
        "highly introverted",
                
        "highly agreeable",
        "agreeable",
        "slightly agreeable",
        "slightly antagonistic",
        "antagonistic",
        "highly antagonistic",
        
        "highly neurotic",
        "neurotic",
        "slightly neurotic",
        "slightly emotionally stable",
        "emotionally stable",
        "highly emotionally stable",
        
        
        "cares strongly about the well-being of others",
        "cares about the well-being of others",
        "cares slightly about the well-being of others",
        "is not concerned with the well-being of others",
    
        "cares strongly about reciprocity or fairness",
        "cares about reciprocity or fairness",
        "cares slightly about reciprocity or fairness",
        "is not concerned with reciprocity or fairness",
    
        "cares strongly about loyalty to your group",
        "cares about loyalty to your group",
        "cares slightly about loyalty to your group",
        "is not concerned with loyalty to your group",
    
        "cares strongly about respecting hierarchies or authority figures",
        "cares about respecting hierarchies or authority figures",
        "cares slightly about respecting hierarchies or authority figures",
        "is not concerned with respecting hierarchies or authority figures",
    
        "cares strongly about moral purity or spiritual elevation",
        "cares about moral purity or spiritual elevation",
        "cares slightly about moral purity or spiritual elevation",
        "is not concerned with moral purity or spiritual elevation",
        ]

###################################################################

CLIENT = [
    "ollama", # 0
    "groq",   # 1
    "openai", # 2
    "google", # 3
    ]

MODEL = [
    # ollama:
    "gemma3:1b",               #  0 # OLLAMA
    "gemma3:4b",               #  1 # OLLAMA
    "gemma3:12b",              #  2 # OLLAMA
    "gemma3:27b",              #  3 # OLLAMA
    "gpt-oss:20b",             #  4 # OLLAMA
    "qwen3:14b",               #  5 # OLLAMA
    "deepseek-r1:14b",         #  6 # OLLAMA
    "llama-3.1-8b-instant",    #  7 # GROQ
    "openai/gpt-oss-120b",     #  8 # GROQ
    "qwen2.5:14b",             #  9 # OLLAMA
    "llama-3.3-70b-versatile", # 10 # GROQ
    "gpt-4o-mini",             # 11 # OPENAI
    "gemini-2.5-flash",        # 12 # GOOGLE
    ]

TEMPERATURE = 0

PSYCH_DOMAIN_CAT = [
    "personality_bigfive",    # 0
    "unspecified",            # 1
    "morality_mft_v1",        # 2
    "morality_mft_v2",        # 3
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

###################################################################
