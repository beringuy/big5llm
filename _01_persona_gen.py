
import re

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def combine_factors(factors, tmp_persona=None, level=0, persona_list=None):
    if persona_list is None:
        persona_list = []
    if tmp_persona is None:
        tmp_persona = []

    if level == len(factors):
        if len(tmp_persona) > 1:
            formatted = ", ".join(tmp_persona[:-1]) + " and " + tmp_persona[-1]
        else:
            formatted = tmp_persona[0] if tmp_persona else ""
        persona_list.append(formatted)
        return persona_list
    for current_factor in factors[list(factors.keys())[level]]:
        combine_factors(factors, tmp_persona + [current_factor], level + 1, persona_list)

    return persona_list

# # # # # # # # # #

def level_personas (persona_list, levels):

    leveled_personas = []
    for persona in persona_list:
        #print ("Persona:", persona)
        split_factors = re.split(r',\W|\Wand\W', persona)
        for i in range(len(split_factors)):
            #print ("Factor:", i)
            for level in levels:
                #print ("Level:", level)
                aux_split_factors = split_factors.copy()
                aux_split_factors[i] = level + " " + split_factors[i]
                leveled_personas.append(", ".join(aux_split_factors[:-1]) + " and " + aux_split_factors[-1])
                
    return leveled_personas

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
