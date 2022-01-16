import math as ma
import pokebase as pb
from list_operators import find_max_indexes, find_min_indexes
from random import randint, shuffle

stats_dict = {'hp': 0, 'attack': 1, 'defense': 2, 'special attack': 3, 'special defense': 4, 'speed': 5}

stats_list = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed'] # Follows Pokebase naming convention
offensive_stats_list = ['attack', 'special-attack', 'speed']
defensive_stats_list = ['defense', 'special-defense']

EV_TOTAL = 510

#Random IV Generator
RAND_IVS = (randint(0, 31), randint(0, 31), randint(0, 31), randint(0, 31), randint(0, 31), randint(0, 31))

#Random EV Generator
def rand_EVs():
    total = EV_TOTAL
    EV_list = [0]*6
    stats_index_list = list(stats_dict.values())
    shuffle(stats_index_list)
    i = 0
    while(total >= 0 and i < len(stats_index_list)):
        EV_list[stats_index_list[i]] = randint(0, total) if(total < 252) else randint(0, 252)
        total -= EV_list[stats_index_list[i]]
        i+=1
    return tuple(EV_list)

#Returns the given base stat
def get_base(pokemon_name, stat):
    return pb.pokemon(pokemon_name).stats[stats_dict[stat]].base_stat

# returns the HP of a pokemon with the given level, hp iv, and hp ev
def get_hp(base_hp, level, iv=16, ev=85):
    assert iv >= 0 and iv <= 31
    assert ev >= 0 and ev <= 252
    return ma.floor((2*base_hp+iv+(ev//4))*level/100)+level+10

# returns the attack, defense, special attack, special defense, and speed of a pokemon with the given level, iv, and ev
def get_other_stat(base_value, level, nature_string, stat_name, iv=16, ev=85):
    assert iv >= 0 and iv <= 31
    assert ev >= 0 and ev <= 252
    nature = 1
    if pb.nature(nature_string).increased_stat.name == stat_name: 
        nature = 1.1 
    elif pb.nature(nature_string).decreased_stat.name == stat_name: 
        nature = 0.9
    return ma.floor((ma.floor((2*base_value+iv+(ev//4))*level/100)+5)*nature)

# returns the name of the nature with the given raised and lowered stats
def get_nature(raised_stat, lowered_stat):
    for i in range(1, 26):
        nature = pb.nature(i)
        if nature.increased_stat != None and nature.decreased_stat != None and nature.increased_stat.name == raised_stat and nature.decreased_stat.name == lowered_stat:
            return nature.name
    return None

# returns the name of the best nature for the pokemon with the given name and the purpose (offensive or defensive)
# offensive takes into account the attacking stats, along with speed
# defensive takes into account the defending stats, along with hp
# if hp is the best stat, a not will be added that this pokemon should be used as an hp tank
def get_optimal_natures(pokemon_name, offensive=True):
    natures = {'name': pokemon_name}
    
    attack_stat = get_base(pokemon_name, "attack") 
    defense_stat = get_base(pokemon_name, "defense") 
    sp_attack_stat = get_base(pokemon_name, "special attack")
    sp_defense_stat = get_base(pokemon_name, "special defense")
    speed_stat = get_base(pokemon_name, "speed") 
     
    
    all_stats = [attack_stat, defense_stat, sp_attack_stat, sp_defense_stat, speed_stat]
    all_stats_list = stats_list[1:]
    offensive_stats = [attack_stat, sp_attack_stat, speed_stat]
    defensive_stats = [defense_stat, sp_defense_stat]
    
    #using the pokemon as an attacker (speed will be accounted for)
    if offensive: 
        largest_offensive_stats = find_max_indexes(offensive_stats)
        lowest_stats = find_min_indexes(all_stats)
        lowest_defensive_stats = find_min_indexes(defensive_stats)

        for i in largest_offensive_stats:
            stat_name = offensive_stats_list[i]

            if stat_name == 'speed':
                natures["speedster"] = []
                for j in lowest_defensive_stats:
                    lower_stat_name = defensive_stats_list[j]
                    nature = get_nature(raised_stat=stat_name, lowered_stat=lower_stat_name)
                    natures["speedster"].append(nature)
            else: 
                if stat_name == 'attack': natures['physical attacker'] = [] 
                elif stat_name == 'special-attack': natures['special attacker'] = []
                for j in lowest_stats: 
                    lower_stat_name = all_stats_list[j]
                    if stat_name != lower_stat_name: 
                        nature = get_nature(raised_stat=stat_name, lowered_stat=lower_stat_name)
                        if stat_name == 'attack':
                            natures['physical attacker'].append(nature)
                        elif stat_name == 'special-attack':
                            natures['special attacker'].append(nature)

    #using the pokemon as a defender (hp will be accounted for)
    else: 
        hp_stat = get_base(pokemon_name, 'hp') 
        largest_defensive_stats = find_max_indexes(defensive_stats)
        lowest_offensive_stats = find_min_indexes(offensive_stats)
        
        for i in largest_defensive_stats:
            raise_stat_name = defensive_stats_list[i]

            if raise_stat_name == 'defense': natures['physical tank'] = [] 
            elif raise_stat_name == 'special-defense': natures['special tank'] = []
            for j in lowest_offensive_stats:
                lower_stat_name = offensive_stats_list[j]
                nature = get_nature(raised_stat=raise_stat_name, lowered_stat=lower_stat_name)
                if raise_stat_name == 'defense':
                    natures['physical tank'].append(nature)
                elif raise_stat_name == 'special-defense':
                    natures['special tank'].append(nature)

        if hp_stat > largest_defensive_stats[0]: natures['hp tank'] = True

    return natures

# Get Pokemon name from dex number
def get_pokemon(dex_no):
    name = pb.APIResource('pokemon-species', dex_no).name
    return name