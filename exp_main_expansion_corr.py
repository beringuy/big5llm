
from exp_expansion_corr import experiment_corr
import re

######################################

######################################

# SETUP:

experiments = {
    "ollama_gemma3:27b__p_personality_bigfive" : [
        "20260206_221713__ollama_gemma3:27b__p_personality_bigfive__i_ipip50__stateless",
        "20260304_230355__ollama_gemma3:27b__p_personality_bigfive__i_mfq30_pt1__stateless",
        "20260305_030012__ollama_gemma3:27b__p_personality_bigfive__i_mfq30_pt2__stateless",
        "ollama - gemma3:27b",
        ],
    
    "ollama_gemma3:27b__p_morality_mft_v2" : [
        "20260305_065212__ollama_gemma3:27b__p_morality_mft_v2__i_ipip50__stateless",
        "20260207_123247__ollama_gemma3:27b__p_morality_mft_v2__i_mfq30_pt1__stateless",
        "20260207_153524__ollama_gemma3:27b__p_morality_mft_v2__i_mfq30_pt2__stateless",
        "ollama - gemma3:27b",
        ],
    
    #
    
    "ollama_gpt-oss:20b__p_personality_bigfive" : [
        "20260203_211502__ollama_gpt-oss:20b__p_personality_bigfive__i_ipip50__stateless",
        "20260519_224143__ollama_gpt-oss:20b__p_personality_bigfive__i_mfq30_pt1__stateless",
        "20260530_221204__ollama_gpt-oss:20b__p_personality_bigfive__i_mfq30_pt2__stateless",
        "ollama - gpt-oss:20b",
        ],
    
    "ollama_gpt-oss:20b__p_morality_mft_v2" : [
        "20260531_100136__ollama_gpt-oss:20b__p_morality_mft_v2__i_ipip50__stateless",
        "20260205_040724__ollama_gpt-oss:20b__p_morality_mft_v2__i_mfq30_pt1__stateless",
        "20260205_161608__ollama_gpt-oss:20b__p_morality_mft_v2__i_mfq30_pt2__stateless",
        "ollama - gpt-oss:20b",
        ],
    
    #
    
    "groq_openaigpt-oss-120b__p_personality_bigfive" : [
        "20260209_234824__groq_openaigpt-oss-120b__p_personality_bigfive__i_ipip50__stateless",
        "20260601_210033__groq_openaigpt-oss-120b__p_personality_bigfive__i_mfq30_pt1__stateless",
        "20260601_221113__groq_openaigpt-oss-120b__p_personality_bigfive__i_mfq30_pt2__stateless",
        "groq - openai gpt-oss-120b",
        ],
    
    "groq_openaigpt-oss-120b__p_morality_mft_v2" : [
        "20260602_092034__groq_openaigpt-oss-120b__p_morality_mft_v2__i_ipip50__stateless",
        "20260209_141958__groq_openaigpt-oss-120b__p_morality_mft_v2__i_mfq30_pt1__stateless",
        "20260209_152341__groq_openaigpt-oss-120b__p_morality_mft_v2__i_mfq30_pt2__stateless",
        "groq - openai gpt-oss-120b",
        ],
    
    #
    
    "ollama_qwen2.5:14b__p_personality_bigfive" : [
        "20260206_105934__ollama_qwen2.5:14b__p_personality_bigfive__i_ipip50__stateless",
        "20260308_001053__ollama_qwen2.5:14b__p_personality_bigfive__i_mfq30_pt1__stateless",
        "20260308_002735__ollama_qwen2.5:14b__p_personality_bigfive__i_mfq30_pt2__stateless",
        "ollama - qwen2.5:14b",
        ],
    
    "ollama_qwen2.5:14b__p_morality_mft_v2" : [
        "20260308_004401__ollama_qwen2.5:14b__p_morality_mft_v2__i_ipip50__stateless",
        "20260206_114253__ollama_qwen2.5:14b__p_morality_mft_v2__i_mfq30_pt1__stateless",
        "20260206_115548__ollama_qwen2.5:14b__p_morality_mft_v2__i_mfq30_pt2__stateless",
        "ollama - qwen2.5:14b",
        ],
    
    }

for experiment in experiments:
    print (experiment)

    ######################################

    exp_id = experiment

    selected_experiment = experiments[exp_id]
    cat = re.search(r'(?<=__p_).*?(?=_)', exp_id).group().capitalize()

    ######################################

    ######################################

    personali_path = "EXPERIMENTS BIG5LLM/" + selected_experiment[3] + "/" + selected_experiment[0] + "/vis/" + selected_experiment[0] + "_sum.csv"
    moral_pt1_path = "EXPERIMENTS BIG5LLM/" + selected_experiment[3] + "/" + selected_experiment[1] + "/vis/" + selected_experiment[1] + "_sum.csv"
    moral_pt2_path = "EXPERIMENTS BIG5LLM/" + selected_experiment[3] + "/" + selected_experiment[2] + "/vis/" + selected_experiment[2] + "_sum.csv"

    experiment_corr (exp_id, cat, personali_path, moral_pt1_path, moral_pt2_path)
