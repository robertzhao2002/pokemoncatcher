import pokebase as pb
import re
from list_operators import total, none_greater
import pokemon_stat as stats

#Constants for average value
#(HP, ATK, DEF, SP. ATK, SP. DEF, SPD)
IV = (16, 16, 16, 16, 16, 16) #Average IVs

EV = (85, 85, 85, 85, 85, 85) #Average EVs

BALLS = {'pokeball': 1, 'great ball': 1.5, 'ultra ball': 2}

STATUS = {'none': [1, 'no status'], 'pbp': [1.5, 'poisoned/burned/paralyzed'], 'fs': [2.5, 'frozen/asleep']} #1.5x for poison/burn/paralysis, 2.5x for frozen/asleep

#Returns the catch probability.
#Input: iv and ev are both tuples of length 6 (HP, ATK, DEF, SP. ATK, SP. DEF, SPD)
#ivs must be smaller than or equal to 31
#evs must be smaller than or equal to 252
#ball, status, and level will be used with the constant dictionaries for their respective values
#hp as a string can be inputted as the value directly followed by an 'h' or a percentage followed by a 'p'
def catch_prob(iv, ev, ball, status, hp, level, pokemon_name):
    #Obtain regular expression for HP input
    hp_regex = re.compile(r"(^\d+)(\.\d+)?(h|p){1}$") #integer or decimal followed by exactly one 'h' or 'p'
    match = hp_regex.search(hp)

    #Make sure inputs are all valid
    assert none_greater(iv, 31)
    assert none_greater(ev, 252)
    assert total(ev) <= 510
    assert level >= 1 and level <= 100 #Pokemon must be between level 1 and 100
    assert ball in BALLS #Check that inputted Pokeball exists
    assert status in STATUS #Check that inputted status exists
    assert match != None #Make sure hp input matches the HP regular expressions

    #obtain HP value
    hp_type = hp[-1]
    hp = float(hp[0:-1]) 
    if hp_type == 'p': assert hp <= 100 and hp > 0 #Make sure percentage hp is greater than 0 and doesn't exceed 100

    catch_rate = pb.APIResource('pokemon-species', pokemon_name).capture_rate
    base_hp = stats.get_base(pokemon_name, 'hp')
    hp_level = stats.get_hp(base_hp, level, iv[0], ev[0])
    if hp_type == 'h': assert hp <= hp_level #Make sure input HP is not greater than the calculated full HP for this level, IV, and EV
    
    if hp_type == 'p': hp = hp*hp_level/100 #If percentage, convert to HP
    catch_value = (((3*hp_level-2*hp)*catch_rate*BALLS[ball])/(3*hp_level))*STATUS[status][0]

    catch_prob = (catch_value/255)**0.75
    # print(catch_rate)
    # print(base_hp)
    # print(hp_level)

    return catch_prob

print(catch_prob((16, 16), (85, 16), 'pokeball', 'none', '100p', 50, 'mewtwo'))


