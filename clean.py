#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 17:02:10 2018

@author: z5190046
"""
from func_csv import write_csv

def clean(data1, data2, intensity_cutoff, temp):

	from func_join_statestrans import join_statestrans
	from func_compare import compare
    
	g_ns_dict = {'31P16O':2, '31P32S':2, '14N32S':3, '32S1H':2, '45Sc1H':16,  '27Al16O': 6, '27Al18O': 6 , '26Al16O': 6, '14N16O': 2, '28Si1H': 2, '51V16O': 8}
    
	name1 = data1.split('/')    
	name2 = data2.split('/')
    
	#get the fractional change in mu from the second datafile name 
	frac_delta_mu = 10**float(name2[-1].split('e')[1])
	print (frac_delta_mu)
    
	# check if data1 and data2 are the same molecule 
	molecule1 = name1[-1].split('_')[0]
	molecule2 = name2[-1].split('_')[0]
	if molecule1 != molecule2:
		print("You're not comparing the same molecule data files")
	print(molecule1)
	print(molecule2)
	
	if molecule1 in g_ns_dict:
		g_ns = (g_ns_dict[molecule1])
	else: print('Molecule g_ns not in dictionary')
    
	data1_statestrans, Q_T = join_statestrans(data1, g_ns, temp)
    
	data2_statestrans, Q2T = join_statestrans(data2, g_ns, temp)

	print(len(data1_statestrans), Q_T)
	print(f'number 2 {len(data2_statestrans)}')
	data_compare = compare(data1_statestrans, data2_statestrans, frac_delta_mu, intensity_cutoff)
    
	print(len(data_compare))
	return data1_statestrans, data_compare, Q_T, frac_delta_mu
    
st, comp, qt, fracmu = clean('../couplings/27Al16O_J20_1000K_nodiag_e-0', '../couplings/27Al16O_J20_1000K_nodiag_e-4',1e-30, 1000)

count_half = 0
count1 = 0
count2 = 0
count10 = 0
count20 = 0
count100 = 0
count1000 = 0
for key in comp:
	if abs(comp[key][4]) >= 0.5:
		count_half+=1
	if abs(comp[key][4]) >= 1:
		count1+=1
	if abs(comp[key][4]) >= 2:
		count2+=1
	if abs(comp[key][4]) >= 10:
		count10+=1
	if abs(comp[key][4]) >= 20:
		count20+=1
	if abs(comp[key][4]) >= 100:
		count100+=1
	if abs(comp[key][4]) >= 1000:
		count1000+=1
		
print(f'|K|>0: {len(comp)}')
print(f'|K|>0.5: {count_half}')
print(f'|K|>1: {count1}')
print(f'|K|>2: {count2}')
print(f'|K|>10: {count10}')
print(f'|K|>20: {count20}')
print(f'|K|>100: {count100}')
print(f'|K|>1000: {count1000}')
	

write_csv(st, comp, '../couplings/out/AlO_nodiag.txt')

            
