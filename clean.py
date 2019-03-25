#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 17:02:10 2018

@author: z5190046
"""

def clean(data1, data2, intensity_cutoff):
    
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
    
    data1_statestrans = join_statestrans(data1, g_ns)
    
    data2_statestrans = join_statestrans(data2, g_ns)

    data_compare = {}
    compare(data1_statestrans, data2_statestrans, frac_delta_mu, data_compare, intensity_cutoff)
#    print(len(data1_statestrans))
#    print(len(data2_statestrans))
#    print(len(data_compare))
    
    csv_filename = data2 + '.csv'
#    print(csv_filename)
    
    write_csv(data1_statestrans, data_compare, frac_delta_mu, csv_filename)
#    write_csv_all(data1_statestrans, data2_statestrans, data_compare, frac_delta_mu, csv_filename)

    return True


# function to join the states and trans file from DUO output and calculate the intensitives of all the transitions - output as a dictionary with teh transition as the key
# taskes input of the file name without extention, dictionary name, and the nuclear statistical weight factor for that molecule (g_ns)
def join_statestrans(data, g_ns):
    
    import math
    
    statesdict = {}
    statestrans = {}
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
    
    def min_energy(statesdict):
        min_energy = float(statesdict[1][1])
        for i in range(1,len(statesdict)):
            if float(statesdict[i][1]) < min_energy:
    #            print(float(statesdict[i][1]))
                min_energy = float(statesdict[i][1])
#        print(min_energy)
        return min_energy
    
    min_energy = min_energy(statesdict)
    
    #calculating Partition funciton - split equation up to make more clear for calculation 
    # Q(T) = g_ns \Sigma_i (2J_i + 1)exp(-c_2 * (\bar{E_i}- E_min) / T), c_2 = h c/k_B, \bar{E_i} = E_i/hc (in cm^-1 taken from .states file), E_min = correcting for ZPE
    q_T = 0
    for key in statesdict:
        first = (2 * float(statesdict[key][3])) + 1
        second = math.exp((-c2 * (float(statesdict[key][1]))- min_energy)/T)
        q_T += first*second 
    Q_T = g_ns * q_T
    
    #A small fuction to calculate the minimium energy from the states dictionary
    
    
#    print(len(statesdict))
#    print(len(statesdict[1]))
#    print(statesdict[1])
     
        
#    print(Q_T)
    
    #open trans file to add Einstien A and frequency (\bar{\nu}) (cm^-1) and calculate intensity (unitless?)
    trans = data + '.trans'
    x = open(trans, 'r')
    f = x.readline()
    g = f.split()
    
    
    ##
    while f: 
        g = f.split()
#        print (g)
        #calculate the intensity of the transition - broken up into three steps
        #I = g_ns (2J_f + 1) A_fi / (8 pi c \bar{\nu}^2) exp(-c_2 * \bar{E_i} / T) (1 - exp(-c_2 * \bar{\nu_if} / T))/ Q_T
        one = g_ns * (2 * float(statesdict[int(g[0])][3]) + 1) * float(g[2]) /(8 * math.pi * c * (float(g[3]))**2)
#        print(float(statesdict[int(g[1])][1]))
        two = math.exp((-c2 * (float(statesdict[int(g[1])][1]))-min_energy)/T)
        three = (1 - math.exp((-c2 * float(g[3]))/T))
        intensity = one * (two * three)/Q_T
        #create dictionary - key is transition as state_ID - state_ID
        if len(statesdict[1]) == 12:
            statestrans[statesdict[int(g[0])][0] + " - " + statesdict[int(g[1])][0]] = [float(statesdict[int(g[0])][1]),int(statesdict[int(g[0])][2]), float(statesdict[int(g[0])][3]), statesdict[int(g[0])][4],  statesdict[int(g[0])][5], statesdict[int(g[0])][6] + statesdict[int(g[0])][7] ,int(statesdict[int(g[0])][8]) ,int(statesdict[int(g[0])][9]), float(statesdict[int(g[0])][10]), float(statesdict[int(g[0])][11]), float(statesdict[int(g[1])][1]),int(statesdict[int(g[1])][2]), float(statesdict[int(g[1])][3]), statesdict[int(g[1])][4],  statesdict[int(g[1])][5], statesdict[int(g[1])][6] + statesdict[int(g[1])][7] ,int(statesdict[int(g[1])][8]), int(statesdict[int(g[1])][9]), float(statesdict[int(g[1])][10]), float(statesdict[int(g[1])][11]), float(g[2]), float(g[3]), intensity]
        elif len(statesdict[1]) == 11:
            statestrans[statesdict[int(g[0])][0] + " - " + statesdict[int(g[1])][0]] = [float(statesdict[int(g[0])][1]),int(statesdict[int(g[0])][2]), float(statesdict[int(g[0])][3]), statesdict[int(g[0])][4],  statesdict[int(g[0])][5], statesdict[int(g[0])][6] ,int(statesdict[int(g[0])][7]) ,int(statesdict[int(g[0])][8]), float(statesdict[int(g[0])][9]), float(statesdict[int(g[0])][10]), float(statesdict[int(g[1])][1]),int(statesdict[int(g[1])][2]), float(statesdict[int(g[1])][3]), statesdict[int(g[1])][4],  statesdict[int(g[1])][5], statesdict[int(g[1])][6] ,int(statesdict[int(g[1])][7]), int(statesdict[int(g[1])][8]), float(statesdict[int(g[1])][9]), float(statesdict[int(g[1])][10]), float(g[2]), float(g[3]), intensity]

        # value for each key is a list of all the information from the states file for each states then, Einstien A, frequency (\bar{\nu}) (cm^-1), intensity 
#        statestrans[statesdict[int(g[0])][0] + " - " + statesdict[int(g[1])][0]] = [float(statesdict[int(g[0])][1]),int(statesdict[int(g[0])][2]), float(statesdict[int(g[0])][3]), statesdict[int(g[0])][4],  statesdict[int(g[0])][5], statesdict[int(g[0])][6] + statesdict[int(g[0])][7] ,int(statesdict[int(g[0])][8]) ,int(statesdict[int(g[0])][9]), float(statesdict[int(g[0])][10]), float(statesdict[int(g[0])][11]), float(statesdict[int(g[1])][1]),int(statesdict[int(g[1])][2]), float(statesdict[int(g[1])][3]), statesdict[int(g[1])][4],  statesdict[int(g[1])][5], statesdict[int(g[1])][6] + statesdict[int(g[1])][7] ,int(statesdict[int(g[1])][8]), int(statesdict[int(g[1])][9]), float(statesdict[int(g[1])][10]), float(statesdict[int(g[1])][11]), float(g[2]), float(g[3]), intensity]
        f = x.readline()

    x.close()
    
    return statestrans



#function to compare to statestrans dictionaries and calculate the fractional change in frequency and intensity as well as the sensitivity coefficient for both 
#output to a new dictionary. Takes input of the names of the two dictionaries, the fractional change in mass between the two dictionaries, output dictionary, and an intensity cutoff
def compare(original_mass, changed_mass, frac_delta_mu, compare_dict, intensity_cutoff):
    
    #loops over the first dictionary ###
    for trans_og in original_mass:
        #loops over the second dictionary ###
        for trans_ch in changed_mass:
            #check if the key of the dictionaries match 
            if trans_og == trans_ch:
                # Calculate the fractional change in frequency and intensity; \Delta \nu /\nu = (\nu_change - nu_original\)/\nu_original 
                deltav = float(changed_mass[trans_ch][21]) - float(original_mass[trans_og][21])
                frac_changev = deltav/float(original_mass[trans_og][21])
                deltaI = float(changed_mass[trans_ch][22]) - float(original_mass[trans_og][22])
                frac_changeI = deltaI/float(original_mass[trans_og][22])
                #only outputs values for transitions with intensities greater than the input cutoff
                if original_mass[trans_og][22] > intensity_cutoff:                    
                    #Create a dictionary entry for each key with values of the original transition frequency, original intensity, fractional change in frequency, fractional change in intensity, K_\mu, K_I; K = fractional change / fractional change in mass 
                    compare_dict[trans_og] = [original_mass[trans_ch][21], original_mass[trans_ch][22], frac_changev,frac_changeI,frac_changev/frac_delta_mu, frac_changeI/frac_delta_mu]

    return compare_dict

#function to write dictionary out to a csv file to use with pandas package 
def write_csv(original_mass, compare_dict, frac_delta_mu, filename):
    #open file and set coloumn headings 
    y = open(filename, 'w')
    y.write("Transition_ID,Upper_energy,Upper_degen,Upper_J,Upper_Tparity,Upper_Rparity,Upper_state,Upper_v,Upper_Lambda,Upper_Sigma,Upper_Omega,")
    y.write("Lower_energy,Lower_degen,Lower_J,Lower_Tparity,Lower_Rparity,Lower_state,Lower_v,Lower_Lambda,Lower_Sigma,Lower_Omega,")
    y.write("Einstien_A,Intensity,wavenumber,")
    y.write("frac_v,frac_I,K_v,K_I,frac_mu\n")

    #loop over keys in dictionary and write to file, keeping track of what is a string, float, or in scientific notation
    for key in compare_dict:
        
        y.write(key + ",") 
        y.write("%6f," % original_mass[key][0])
        y.write("%.1f," % original_mass[key][1])
        y.write("%.1f," % original_mass[key][2])
        y.write(str(original_mass[key][3])+ ",")
        y.write(str(original_mass[key][4])+ ",")
        y.write(str(original_mass[key][5])+ ",")
        y.write("%.1f," % original_mass[key][6])
        y.write("%.1f," % original_mass[key][7])
        y.write("%.1f," % original_mass[key][8])
        y.write("%.1f," % original_mass[key][9])
        y.write("%.6f," % original_mass[key][10])
        y.write("%.1f," % original_mass[key][11])
        y.write("%.1f," % original_mass[key][12])
        y.write(str(original_mass[key][13])+ ",")
        y.write(str(original_mass[key][14])+ ",")
        y.write(str(original_mass[key][15])+ ",")
        y.write("%.1f," % original_mass[key][16])
        y.write("%.1f," % original_mass[key][17])
        y.write("%.1f," % original_mass[key][18])
        y.write("%.1f," % original_mass[key][19])
        y.write("%.6e," % original_mass[key][20])
        y.write("%.6e," % original_mass[key][22])
        y.write("%.6e," % original_mass[key][21])
        y.write("%.6e," % compare_dict[key][2])
        y.write("%.6e," % compare_dict[key][3])
        y.write("%.6e," % compare_dict[key][4])
        y.write("%.6e," % compare_dict[key][5])
        y.write("%.6e\n" % frac_delta_mu)
    y.close()
    
#function to write dictionary out to a csv file to use with pandas package 
def write_csv_all(original_mass, changed_mass, compare_dict, frac_delta_mu, filename):
    #open file and set coloumn headings 
    y = open(filename, 'w')
    y.write("Transition_ID,Upper_energy,Upper_degen,Upper_J,Upper_Tparity,Upper_Rparity,Upper_state,Upper_v,Upper_Lambda,Upper_Sigma,Upper_Omega,")
    y.write("Lower_energy,Lower_degen,Lower_J,Lower_Tparity,Lower_Rparity,Lower_state,Lower_v,Lower_Lambda,Lower_Sigma,Lower_Omega,")
    y.write("Einstien_A,Intensity,wavenumber,")
    y.write("ch_Upper_energy,ch_Upper_degen,ch_Upper_J,ch_Upper_Tparity,ch_Upper_Rparity,ch_Upper_state,ch_Upper_v,ch_Upper_Lambda,ch_Upper_Sigma,ch_Upper_Omega,")
    y.write("ch_Lower_energy,ch_Lower_degen,ch_Lower_J,ch_Lower_Tparity,ch_Lower_Rparity,ch_Lower_state,ch_Lower_v,ch_Lower_Lambda,ch_Lower_Sigma,ch_Lower_Omega,")
    y.write("ch_Einstien_A,ch_Intensity,ch_wavenumber,")
    y.write("frac_v,frac_I,K_v,K_I,frac_mu\n")

    #loop over keys in dictionary and write to file, keeping track of what is a string, float, or in scientific notation
    for key in compare_dict:
        
        y.write(key + ",") 
        y.write("%6f," % original_mass[key][0])
        y.write("%.1f," % original_mass[key][1])
        y.write("%.1f," % original_mass[key][2])
        y.write(str(original_mass[key][3])+ ",")
        y.write(str(original_mass[key][4])+ ",")
        y.write(str(original_mass[key][5])+ ",")
        y.write("%.1f," % original_mass[key][6])
        y.write("%.1f," % original_mass[key][7])
        y.write("%.1f," % original_mass[key][8])
        y.write("%.1f," % original_mass[key][9])
        y.write("%.6f," % original_mass[key][10])
        y.write("%.1f," % original_mass[key][11])
        y.write("%.1f," % original_mass[key][12])
        y.write(str(original_mass[key][13])+ ",")
        y.write(str(original_mass[key][14])+ ",")
        y.write(str(original_mass[key][15])+ ",")
        y.write("%.1f," % original_mass[key][16])
        y.write("%.1f," % original_mass[key][17])
        y.write("%.1f," % original_mass[key][18])
        y.write("%.1f," % original_mass[key][19])
        y.write("%.6e," % original_mass[key][20])
        y.write("%.6e," % original_mass[key][22])
        y.write("%.6e," % original_mass[key][21])
        y.write("%.6f," % changed_mass[key][0])
        y.write("%.1f," % changed_mass[key][1])
        y.write("%.1f," % changed_mass[key][2])
        y.write(str(changed_mass[key][3])+ ",")
        y.write(str(changed_mass[key][4])+ ",")
        y.write(str(changed_mass[key][5])+ ",")
        y.write("%.1f," % changed_mass[key][6])
        y.write("%.1f," % changed_mass[key][7])
        y.write("%.1f," % changed_mass[key][8])
        y.write("%.1f," % changed_mass[key][9])
        y.write("%.6f," % changed_mass[key][10])
        y.write("%.1f," % changed_mass[key][11])
        y.write("%.1f," % changed_mass[key][12])
        y.write(str(changed_mass[key][13])+ ",")
        y.write(str(changed_mass[key][14])+ ",")
        y.write(str(changed_mass[key][15])+ ",")
        y.write("%.1f," % changed_mass[key][16])
        y.write("%.1f," % changed_mass[key][17])
        y.write("%.1f," % changed_mass[key][18])
        y.write("%.1f," % changed_mass[key][19])
        y.write("%.6e," % changed_mass[key][20])
        y.write("%.6e," % changed_mass[key][22])
        y.write("%.6e," % changed_mass[key][21])
        y.write("%.6e," % compare_dict[key][2])
        y.write("%.6e," % compare_dict[key][3])
        y.write("%.6e," % compare_dict[key][4])
        y.write("%.6e," % compare_dict[key][5])
        y.write("%.6e\n" % frac_delta_mu)
    y.close()
    


#clean('Data_31P32S_CURVES/31P32S_CURVES_J10_100K_e-0', 'Data_31P32S_CURVES/31P32S_CURVES_J10_100K_e-5', 0)
#clean('Data_31P16O_CURVES/31P16O_CURVES_J10_100K_e-0', 'Data_31P16O_CURVES/31P16O_CURVES_J10_100K_e-3', 0)
#clean('Data_14N32S/14N32S_J10_100K_e-0', 'Data_14N32S/14N32S_J10_100K_e-5', 0)
#clean('Data_31P32S_CURVES/31P32S_CURVES_J20_100K_e-0', 'Data_31P32S_CURVES/31P32S_CURVES_J20_100K_e-3', 0)
#clean('Data_32S1H/32S1H_J10_100K_e-0', 'Data_32S1H/32S1H_J10_100K_e-8', 0)
#clean('Data_45Sc1H/45Sc1H_J10_100K_e-0', 'Data_45Sc1H/45Sc1H_J10_100K_e-4', 0)
#clean('Data_27Al16O/27Al16O_J10_100K_e-0', 'Data_27Al16O/27Al16O_J10_100K_e-4', 0)
#clean('Data_27Al18O/27Al18O_J10_100K_e-0', 'Data_27Al18O/27Al18O_J10_100K_e-4', 0)


#for i in range(1,9):
#    clean('Data_26Al16O/26Al16O_J10_100K_e-0', 'Data_26Al16O/26Al16O_J10_100K_e-'+ str(i), 0)
    
molecules = ['14N32S', '32S1H', '31P16O_CURVES', '31P32S_CURVES', '45Sc1H', '27Al16O', '27Al18O', '26Al16O']

def clean_all(molecules, start, stop):
    for molecule in molecules:
        for i in range(start, stop+1):
            clean('Data_' + molecule + '/' + molecule + '_J10_100K_e-0', 'Data_' + molecule + '/' + molecule + '_J10_100K_e-'+ str(i), 0)



            
