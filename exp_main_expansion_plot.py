
from exp_expansion_plot_update3 import experiment_plot

######################################

######################################

# SETUP:

experiments = {
    "ollama_gemma3:27b__p_personality_bigfive" : [
        "20260206_221713__ollama_gemma3:27b__p_personality_bigfive__i_ipip50__stateless",
        "20260206_135601__ollama_gemma3:27b__p_unspecified__i_ipip50__stateless",
        "ollama - gemma3:27b",
        ],
    
    "ollama_gemma3:27b__p_morality_mft_v2_pt1" : [
        "20260207_123247__ollama_gemma3:27b__p_morality_mft_v2__i_mfq30_pt1__stateless",
        "20260206_182826__ollama_gemma3:27b__p_unspecified__i_mfq30_pt1__stateless",
        "ollama - gemma3:27b",
        ],
    
    "ollama_gemma3:27b__p_morality_mft_v2_pt2" : [
        "20260207_153524__ollama_gemma3:27b__p_morality_mft_v2__i_mfq30_pt2__stateless",
        "20260206_183017__ollama_gemma3:27b__p_unspecified__i_mfq30_pt2__stateless",
        "ollama - gemma3:27b",
        ],
    
    #
    
    "ollama_gpt-oss:20b__p_personality_bigfive" : [
        "20260203_211502__ollama_gpt-oss:20b__p_personality_bigfive__i_ipip50__stateless",
        "20260203_205517__ollama_gpt-oss:20b__p_unspecified__i_ipip50__stateless",
        "ollama - gpt-oss:20b",
        ],
    
    "ollama_gpt-oss:20b__p_morality_mft_v2_pt1" : [
        "20260205_040724__ollama_gpt-oss:20b__p_morality_mft_v2__i_mfq30_pt1__stateless",
        "20260205_040115__ollama_gpt-oss:20b__p_unspecified__i_mfq30_pt1__stateless",
        "ollama - gpt-oss:20b",
        ],
    
    "ollama_gpt-oss:20b__p_morality_mft_v2_pt2" : [
        "20260205_161608__ollama_gpt-oss:20b__p_morality_mft_v2__i_mfq30_pt2__stateless",
        "20260205_040230__ollama_gpt-oss:20b__p_unspecified__i_mfq30_pt2__stateless",
        "ollama - gpt-oss:20b",
        ],
    
    #
    
    "ollama_qwen2.5:14b__p_personality_bigfive" : [
        "20260206_105934__ollama_qwen2.5:14b__p_personality_bigfive__i_ipip50__stateless",
        "20260206_105704__ollama_qwen2.5:14b__p_unspecified__i_ipip50__stateless",
        "ollama - qwen2.5:14b",
        ],
    
    "ollama_qwen2.5:14b__p_morality_mft_v2_pt1" : [
        "20260206_114253__ollama_qwen2.5:14b__p_morality_mft_v2__i_mfq30_pt1__stateless",
        "20260206_114225__ollama_qwen2.5:14b__p_unspecified__i_mfq30_pt1__stateless",
        "ollama - qwen2.5:14b",
        ],
    
    "ollama_qwen2.5:14b__p_morality_mft_v2_pt2" : [
        "20260206_115548__ollama_qwen2.5:14b__p_morality_mft_v2__i_mfq30_pt2__stateless",
        "20260206_114229__ollama_qwen2.5:14b__p_unspecified__i_mfq30_pt2__stateless",
        "ollama - qwen2.5:14b",
        ],
    
    #
    
    "groq_openaigpt-oss-120b__p_personality_bigfive" : [
        "20260209_234824__groq_openaigpt-oss-120b__p_personality_bigfive__i_ipip50__stateless",
        "20260208_233917__groq_openaigpt-oss-120b__p_unspecified__i_ipip50__stateless",
        "groq - openai gpt-oss-120b",
        ],
    
    "groq_openaigpt-oss-120b__p_morality_mft_v2_pt1" : [
        "20260209_141958__groq_openaigpt-oss-120b__p_morality_mft_v2__i_mfq30_pt1__stateless",
        "20260209_000957__groq_openaigpt-oss-120b__p_unspecified__i_mfq30_pt1__stateless",
        "groq - openai gpt-oss-120b",
        ],
    
    "groq_openaigpt-oss-120b__p_morality_mft_v2_pt2" : [
        "20260209_152341__groq_openaigpt-oss-120b__p_morality_mft_v2__i_mfq30_pt2__stateless",
        "20260209_001015__groq_openaigpt-oss-120b__p_unspecified__i_mfq30_pt2__stateless",
        "groq - openai gpt-oss-120b",
        ],
    
    }


######################################

######################################

for i in experiments:
    print (i)
    exp_id = i

    source_id = experiments[exp_id][0]
    baseline_id = experiments[exp_id][1]
    exp_path = "EXPERIMENTS BIG5LLM/" + experiments[exp_id][2] + "/"

    experiment_plot(exp_id, source_id, baseline_id, exp_path)