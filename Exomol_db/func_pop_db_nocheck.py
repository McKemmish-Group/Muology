#!/usr/bin/env python

import sys
import sqlalchemy
from SQLiteConnection import engine, Session
from ModelClasses import *

def pop_db(file1, file2, intensity_cutoff, temperature):
	'''A function to populate that database ExoMol_K.db with output files from DUO. 
	Needed are the .states and .trans files of an isotopologue without mass perturbation
	and with perturbation. functions will join the states and trans files as well as 
	calculate the intensity. a function will then compare every transition frequency and 
	calculate the K_mu and K_I. The db will have all of the states and trans information
	of the non perturbative mass of the isotopologue as well as the fractional change in 
	mass, intensity, and frequency, K_mu and K_I'''

	from func_join_statestrans import join_statestrans
	from func_compare import compare
    
	'''dictionary of nuclear statistical weight factor for each isotopologue'''

	g_ns_dict = {'31P16O':2, '31P32S':2, '14N32S':3, '32S1H':2, '45Sc1H':16,  '27Al16O': 6, '27Al18O': 6 , '26Al16O': 6, '14N16O': 2, '28Si1H': 2, '51V16O': 8}

# 	print(file1)
	name1 = file1.split('/')    
	name2 = file2.split('/')

    
    #get the fractional change in mu from the second datafile name 
	try:
		frac_delta_mu = 10**float(name2[-1].split('e')[1])
# 		print (frac_delta_mu)
	except ValueError:
		print(f'filenames not set up to have change in mu before extension, fix and try again')
		sys.exit(0)
    
    # check if data1 and data2 are the same molecule 

	molecule1 = name1[-1].split('_')[0]
	molecule2 = name2[-1].split('_')[0]
	if molecule1 != molecule2:
	    print("You're not comparing the same molecule data files")
	print(molecule1)

#    print(molecule2)
    
	'''set g_ns; add to dictionary if not present'''
	try:
		g_ns = (g_ns_dict[molecule1])
	except KeyError:
		g_ns_dict[molecule1] = input(f'g_ns for {molecule1} not in dictionary, add now: ')	
#	 if molecule1 in g_ns_dict:
# 	    g_ns = (g_ns_dict[molecule1])
# 	else: print('Molecule g_ns not in dictionary')
		g_ns = (g_ns_dict[molecule1])
    
	'''join states and trans files for molecule, calculate intensity'''
	data1_statestrans, Q_T = join_statestrans(file1, g_ns, temperature)
    
	data2_statestrans, Q2T = join_statestrans(file2, g_ns, temperature)

	print('comparing')
	
	'''compare statestrans for two data files, calculate K ect for each transition'''
	data_compare = compare(data1_statestrans, data2_statestrans, frac_delta_mu, intensity_cutoff)

	name = molecule1
# 	print(frac_delta_mu)
	
	count = 0
	print('opening db')

	'''open session to db'''
	session = Session(autoflush=False)
	
	'''check if isotopologue in db, if not; add. create relationship between 
		isotopologue and transition'''
	try:
		trans_iso = session.query(Isotopologue).filter(Isotopologue.name==name).filter(Isotopologue.temperature==temperature).one()
		#print('try')
	except sqlalchemy.orm.exc.NoResultFound:
	#not in db, add
		#print('add')
		trans_iso = Isotopologue()
		trans_iso.name = name
		trans_iso.temperature = temperature
		trans_iso.g_ns = g_ns_dict[name]
		trans_iso.Q_T = Q_T
			
		session.add(trans_iso)
		session.flush()		
	except sqlalchemy.orm.exc.MultipleResultsFound:
		raise Exception("Too many in db - FIX!")

	'''loop through all transitions check if in db, if not; add'''
	for key in data_compare:
		#try:
			#new_trans = session.query(Transition).filter(Transition.exomol_ID==key).filter(Transition.wavenumber==data1_statestrans[key][21]).one()
		#except sqlalchemy.orm.exc.NoResultFound:
		#not in db, add
		new_trans = Transition()
		new_trans.exomol_ID = key
		new_trans.einstien_A = data1_statestrans[key][20]
		new_trans.intensity = data1_statestrans[key][22]
		new_trans.wavenumber = data1_statestrans[key][21]
		new_trans.change_mu = frac_delta_mu
		new_trans.change_nu = data_compare[key][2]
		new_trans.change_I = data_compare[key][3]
		new_trans.K_mu = data_compare[key][4]
		new_trans.K_I = data_compare[key][5]
			'''link to isotopologue'''
		new_trans.isotopologue_id = trans_iso.id
		#except sqlalchemy.orm.exc.MultipleResultsFound:
			#raise Exception("Too many in db - FIX!")
# 		print('search for iso')


		'''check if energylevels in db, if not; add. create relationship between 
		energylevels and transition'''
		try:
			upper_el = session.query(EnergyLevel).filter(EnergyLevel.exomol_ID==key.split(' - ')[0]).filter(EnergyLevel.isotopologue_id==trans_iso.id).one()
		except sqlalchemy.orm.exc.NoResultFound:
		#not in db, add
			upper_el = EnergyLevel()
			upper_el.exomol_ID = key.split(' - ')[0]
# 			print('link up energylevel to iso')
			upper_el.isotopologue_id = trans_iso.id
# 			print('linked')
			upper_el.energy = data1_statestrans[key][0]
			upper_el.degeneracy = data1_statestrans[key][1]
			upper_el.J = data1_statestrans[key][2]
			upper_el.Tparity = data1_statestrans[key][3]
			upper_el.Rparity = data1_statestrans[key][4]
			upper_el.state = data1_statestrans[key][5]
			upper_el.v = data1_statestrans[key][6]
			upper_el.Lambda = data1_statestrans[key][7]
			upper_el.Sigma = data1_statestrans[key][8]
			upper_el.Omega = data1_statestrans[key][9]

			session.add(upper_el)
			session.flush()
		except sqlalchemy.orm.exc.MultipleResultsFound:
			raise Exception("Too many in db - FIX!")
# 		print('here')
		new_trans.upper_id = upper_el.id
	
		try:
			lower_el = session.query(EnergyLevel).filter(EnergyLevel.exomol_ID==key.split(' - ')[1]).filter(EnergyLevel.isotopologue_id==trans_iso.id).one()
		except sqlalchemy.orm.exc.NoResultFound:
		#not in db, add
			lower_el = EnergyLevel()
			lower_el.exomol_ID = key.split(' - ')[1]
# 			print('link low energylevel to iso')
			lower_el.isotopologue_id = trans_iso.id
# 			print('linked')		
			lower_el.energy = data1_statestrans[key][10]
			lower_el.degeneracy = data1_statestrans[key][11]
			lower_el.J = data1_statestrans[key][12]
			lower_el.Tparity = data1_statestrans[key][13]
			lower_el.Rparity = data1_statestrans[key][14]
			lower_el.state = data1_statestrans[key][15]
			lower_el.v = data1_statestrans[key][16]
			lower_el.Lambda = data1_statestrans[key][17]
			lower_el.Sigma = data1_statestrans[key][18]
			lower_el.Omega = data1_statestrans[key][19]
			
			session.add(lower_el)
			session.flush()
		except sqlalchemy.orm.exc.MultipleResultsFound:
			raise Exception("Too many in db - FIX!")
		new_trans.lower_id = lower_el.id
		
		session.add(new_trans)
		session.flush()
		
		count+=1
		print(count)
	print('closing db')	


	'''commit new additions to db'''
	session.commit()

	engine.dispose() # cleanly disconnect from the database


pop_db('../../Data_J20_1000K/51V16O_J20_1000K_e-0', '../../Data_J20_1000K/51V16O_J20_1000K_e-4',1e-30, 1000)

# pop_db('Data_14N32S/14N32S_J10_100K_e-0', 'Data_14N32S/14N32S_J10_100K_e-4',0, 10)




