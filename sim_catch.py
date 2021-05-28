import csv
from random import random, randint
from prob_catch import catch_prob
import pokemon_stat as stats

#CSV row format: pokedex_number,pokemon_name,pokemon_lvl,iv,ev,hp,total_pokemon_hp,ball,status,catch_probability,balls_used
#Example: 150,mewtwo,70,16,85,1,285,ultra ball,fs,0.1536,33

#Inputs
pokedex_no = randint(1,600)
pokemon_name = stats.get_pokemon(pokedex_no)
print('Pokemon:', pokemon_name)

IV = stats.RAND_IVS
EV = stats.rand_EVs()
print('IVs:', IV)
print('EVs:', EV)

BALL = 'pokeball'

STATUS_DICT = {'0': 'none', '1': 'pbp', '2': 'fs'} 
STATUS = STATUS_DICT[str(randint(0,2))]

LEVEL = randint(1, 100)
print('Level:', LEVEL)

h_or_p = random()
base_hp = stats.get_base(pokemon_name, 'hp')
total_hp = stats.get_hp(base_hp, LEVEL, IV[0], EV[0])
HP = (str(random()*100) + 'p') if h_or_p < 0.5 else (str(random()*total_hp) + 'h')

HP_VAL = str(float(HP[0:-1]) * total_hp/100) if (HP[-1] == 'p') else HP[0:-1]

try:
    #simulate
    prob = catch_prob(IV, EV, BALL, STATUS, HP, LEVEL, pokemon_name)
    print('Catch probability:', prob)
    balls_thrown = 1
    r = random()
    while(r > prob):
        r = random()
        balls_thrown+=1
    print('Balls thrown:', str(balls_thrown))

    #place into CSV
    fields=[pokedex_no,pokemon_name,LEVEL,IV[0],EV[0],HP_VAL,total_hp,BALL,STATUS,round(prob,4),balls_thrown]
    with open('catch_simulations.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
except:
    print('Invalid input')