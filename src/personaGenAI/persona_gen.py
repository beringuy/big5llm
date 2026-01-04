
import re

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def combine_dimensions(dimensions, tmp_persona=None, depth=0, persona_list=None):
    if persona_list is None:
        persona_list = []
    if tmp_persona is None:
        tmp_persona = []

    if depth == len(dimensions):
        if len(tmp_persona) > 1:
            formatted = ", ".join(tmp_persona[:-1]) + " and " + tmp_persona[-1]
        else:
            formatted = tmp_persona[0] if tmp_persona else ""
        persona_list.append(formatted)
        return persona_list
    for current_dimension in dimensions[list(dimensions.keys())[depth]]:
        combine_dimensions(dimensions, tmp_persona + [current_dimension], depth + 1, persona_list)

    return persona_list

# # # # # # # # # #

def level_personas (persona_list, levels=None):
    if levels == [] or levels == None:
        return persona_list

    leveled_personas = []
    for persona in persona_list:
        #print ("Persona:", persona)
        split_dimensions = re.split(r',\W|\Wand\W', persona)
        for i in range(len(split_dimensions)):
            for level in levels:
                #print ("Level:", level)
                #print ("Dimension:", i)
                aux_split_dimensions = split_dimensions.copy()
                aux_split_dimensions[i] = level + split_dimensions[i]
                if len (split_dimensions) > 1:
                    tmp = ", ".join(aux_split_dimensions[:-1]) + " and " + aux_split_dimensions[-1]                    
                else:
                    tmp = aux_split_dimensions[0] if aux_split_dimensions else ""
                leveled_personas.append(tmp)
                
    return leveled_personas

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
