#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#function to compare to statestrans dictionaries and calculate the fractional change in frequency and intensity as well as the sensitivity coefficient for both 
#output to a new dictionary. Takes input of the names of the two dictionaries, the fractional change in mass between the two dictionaries, output dictionary, and an intensity cutoff
def compare(original_mass, changed_mass, frac_delta_mu, intensity_cutoff):
    #print('compare')
    compare_dict = {}
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
                #print('calcs')
                if original_mass[trans_og][22] > intensity_cutoff:                    
                    #Create a dictionary entry for each key with values of the original transition frequency, original intensity, fractional change in frequency, fractional change in intensity, K_\mu, K_I; K = fractional change / fractional change in mass 
                    compare_dict[trans_og] = [original_mass[trans_ch][21], original_mass[trans_ch][22], frac_changev,frac_changeI,frac_changev/frac_delta_mu, frac_changeI/frac_delta_mu]
                    #print('adding')
    #print(len(compare_dict))
    return compare_dict