import math as ma
import pokebase as pb
from random import randint, shuffle

stats_dict = {'hp': 0, 'attack': 1, 'defense': 2, 'special attack': 3, 'special defense': 4, 'speed': 5}

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

#returns the HP of a pokemon with the given level, hp iv, and hp ev
def get_hp(base_hp, level, iv=16, ev=85):
    assert iv >= 0 and iv <= 31
    assert ev >= 0 and ev <= 252
    return ma.floor((2*base_hp+iv+(ev//4))*level/100)+level+10

#Attack
#Defense
#Sp. Attack
#Sp. Defense
#Speed

#Get Pokemon name from dex number
def get_pokemon(dex_no):
    name = pb.APIResource('pokemon-species', dex_no).name
    return name