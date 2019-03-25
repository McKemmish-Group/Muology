#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 17:02:10 2018

@author: z5190046
"""

def clean(data1, data2, intensity_cutoff, temp):

    from func_join_statestrans import join_statestrans
    from func_compare import compare
    
    g_ns_dict = {'31P16O':2, '31P32S':2, '14N32S':3, '32S1H':2, '45Sc1H':16,  '27Al16O': 6, '27Al18O': 6 , '26Al16O': 6}
    
    name1 = data1.split('_')    
    name2 = data2.split('_')
    
    #get the fractional change in mu from the second datafile name 
    frac_delta_mu = 10**float(name2[-1].split('e')[1])
    print (frac_delta_mu)
    
    # check if data1 and data2 are the same molecule 
    molecule1 = name1[1].split('/')[0]
    molecule2 = name2[1].split('/')[0]
    if molecule1 != molecule2:
        print("You're not comparing the same molecule data files")
#    print(molecule1)
#    print(molecule2)
    
    if molecule1 in g_ns_dict:
        g_ns = (g_ns_dict[molecule1])
    else: print('Molecule g_ns not in dictionary')
    
    data1_statestrans, Q_T = join_statestrans(data1, g_ns, temp)
    
    data2_statestrans, Q2T = join_statestrans(data2, g_ns, temp)

    #print(len(data1_statestrans), Q_T)
    #print(f'number 2 {len(data2_statestrans)}')
    data_compare = compare(data1_statestrans, data2_statestrans, frac_delta_mu, intensity_cutoff)
    

    return data1_statestrans, data_compare, Q_T, frac_delta_mu



            
