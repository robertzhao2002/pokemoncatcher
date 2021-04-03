import pokebase as pb
import math as ma

#Assume IVs are all 16, EVs are all 81 [AVERAGE VALUES]

IV = 16

EV = 81

BALLS = {'pokeball': 1, 'great ball': 1.5, 'ultra ball': 2}

STATUS = {'pbp': [1.5, 'poisoned/burned/paralyzed'], 'fs': [2.5, 'frozen/asleep']}

pokemon_name = input('Input a pokemon name: ')

status = input('pbp for poison/burn/paralysis, fs for frozen/asleep: ')

level = int(input('1-100 for the level of the pokemon: '))

ball = input('Input a pokeball: ')

#1.5x for poison/burn/paralysis, 2.5x for frozen/asleep

catch_rate = pb.APIResource('pokemon-species', pokemon_name).capture_rate
base_hp = pb.pokemon(pokemon_name).stats[0].base_stat

hp_level = ma.floor((2*base_hp+IV+(EV//4))*level/100)+level+10

hp = int(input('Enter an HP value between 1 and ' + str(hp_level) + ': '))

catch_value = (((3*hp_level-2*hp)*catch_rate*BALLS[ball])/(3*hp_level))*STATUS[status][0]

catch_prob = catch_value/255

print('The probability of catching a', str(hp), 'HP', STATUS[status][1], 'level', str(level), pokemon_name, 'with a(n)', ball, 'is', str(catch_prob*100), 'percent.')
print('You will need', str(1/catch_prob), ball+'(s) on average to capture it.')


# print(catch_rate)
# print(base_hp)
# print(hp_level)