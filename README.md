# Muology
Any important files for the Muology project 

The func_join_statestrans.py program is the bare bones of the junction that joins the .states and .trans output files from Duo. 
It also calculates the intensity for each transition and outputs to a dictionary with the key being the transitions ID. 

The compare.py program extends on the above by including an other function to compare two statestrans dictionaries. 
It takes input of the two dictionaries, the fractional change in mass between the two dictionaries, an output dictionary and an intensity cutoff. 
The output is a dictionary that has the transition ID as the key and the values are the original frequency, original intensity, fractional change in frequency, fractional change in intensity, the sensitivity coefficient for frequency, and the sensitivity coefficient intensity
