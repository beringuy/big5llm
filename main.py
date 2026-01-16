
from src.personaGenAI.experiment import AIPsychExperiment

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

# EXPERIMENT

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

exp1.run_experiment()

exp1.experiment_info
exp1.experiment_responses
exp1.experiment_start_time

exp1.experiment_std_responses
exp1.experiment_score

exp1.plot_graphs()

exp1.experiment_score_by_dimensions