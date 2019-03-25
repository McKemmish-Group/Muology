#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 16:05:19 2018

@author: z5190046
"""
# function to join the states and trans file from DUO output and calculate the intensitives of all the transitions - output as a dictionary with teh transition as the key
# taskes input of the file name without extention, dictionary name, and the nuclear statistical weight factor for that molecule (g_ns)
def join_statestrans(data, statestrans, g_ns):
    
    import math
    
    statesdict = {}
    states = data + '.states'
    x = open(states, 'r')
    
    f = x.readline()
    #while loop to read through states file and split each line on the spaces 
    # store in a dictionary with the key as the ID and the whole line as a list as the value 
    # ID, states energy in cm^-1, state degeneracy , Total angular momentum J, Total parity, rotationless parity, state label, vibrational quantum number, projection of the electronic angular momentum, projection of the electronic spin, projection of the total angular momentum
    while f:
        g = f.split()
        #print(g)
        statesdict[int(g[0])] = g[:]
        f = x.readline()
    x.close()
    
    #T = 100 #K - set manually 
    #grab the temperature from the data file name 
    names = data.split('_')
    temp = names[-2].split('K') 
    T = float(temp[0])
    #constants 
    c2 = 1.43877736 #cm K from CODATA
    c = 29979245800.00 #cm/s
       
    #calculating Partition funciton - split equation up to make more clear for calculation 
    # Q(T) = g_ns \Sigma_i (2J_i + 1)exp(-c_2 * \bar{E_i} / T), c_2 = h c/k_B, \bar{E_i} = E_i/hc (in cm^-1 taken from .states file)
    q_T = 0
    for key in statesdict:
        first = (2 * float(statesdict[key][3])) + 1
        second = math.exp((-c2 * float(statesdict[key][1]))/T)
        q_T += first*second 
    Q_T = g_ns * q_T
    
    #open trans file to add Einstien A and frequency (\bar{\nu}) (cm^-1) and calculate intensity (unitless?)
    trans = data + '.trans'
    x = open(trans, 'r')
    f = x.readline()
    g = f.split()
    
    #
    while f: 
        g = f.split()
        #calculate the intensity of the transition - broken up into three steps
        #I = g_ns (2J_f + 1) A_fi / (8 pi c \bar{\nu}^2) exp(-c_2 * \bar{E_i} / T) (1 - exp(-c_2 * \bar{\nu_if} / T))/ Q_T
        one = g_ns * (2 * float(statesdict[int(g[0])][3]) + 1) * float(g[2]) /(8 * math.pi * c * (float(g[3]))**2)
        two = math.exp((-c2 * float(statesdict[int(g[1])][1]))/T)
        three = (1 - math.exp((-c2 * float(g[3]))/T))
        intensity = one * (two * three)/Q_T
        #create dictionary - key is transition as state_ID - state_ID
        # value for each key is a list of all the information from the states file for each states then, Einstien A, frequency (\bar{\nu}) (cm^-1), intensity 
        statestrans[statesdict[int(g[0])][0] + " - " + statesdict[int(g[1])][0]] = [float(statesdict[int(g[0])][1]),int(statesdict[int(g[0])][2]), float(statesdict[int(g[0])][3]), statesdict[int(g[0])][4],  statesdict[int(g[0])][5], statesdict[int(g[0])][6] + statesdict[int(g[0])][7] ,int(statesdict[int(g[0])][8]) ,int(statesdict[int(g[0])][9]), float(statesdict[int(g[0])][10]), float(statesdict[int(g[0])][11]), float(statesdict[int(g[1])][1]),int(statesdict[int(g[1])][2]), float(statesdict[int(g[1])][3]), statesdict[int(g[1])][4],  statesdict[int(g[1])][5], statesdict[int(g[1])][6] + statesdict[int(g[1])][7] ,int(statesdict[int(g[1])][8]), int(statesdict[int(g[1])][9]), float(statesdict[int(g[1])][10]), float(statesdict[int(g[1])][11]), float(g[2]), float(g[3]), intensity]
        f = x.readline()
        
    x.close()
    
    return statestrans


statestrans = {}
PO_g_ns = 2 #calc from .inp file 
join_statestrans('Data_31P16O_CURVES/31P16O_CURVES_J10_100K_e-0', statestrans, PO_g_ns)
print (statestrans['69 - 1'])

print(len(statestrans))

#pattern match 