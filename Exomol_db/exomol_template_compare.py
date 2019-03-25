#!/usr/bin/env python

import sys
import sqlalchemy
from SQLiteConnection import engine, Session
from ModelClasses import *
from clean import clean

temperature = 100
name = '32S1H'
g_ns_dict = {'31P16O':2, '31P32S':2, '14N32S':3, '32S1H':2, '45Sc1H':16,  '27Al16O': 6, '27Al18O': 6 , '26Al16O': 6}
#statestrans, compare, Q_T, change_mu = clean('Data_14N32S/14N32S_J10_100K_e-0', 'Data_14N32S/14N32S_J10_100K_e-4',10**-30, temperature)
statestrans, compare, Q_T, change_mu = clean('Data_32S1H/32S1H_J10_100K_e-0', 'Data_32S1H/32S1H_J10_100K_e-4',10**-30, temperature)


print(len(compare))

# filename = 'student_data.txt'
# or use argparse

# data = open(filename)

session = Session(autoflush=False)



for key in compare:
	try:
		new_trans = session.query(Transition).filter(Transition.exomol_ID==key).filter(Transition.wavenumber==statestrans[key][21]).one()
	except sqlalchemy.orm.exc.NoResultFound:
	#not in db, add
		new_trans = Transition()
		new_trans.exomol_ID = key
		new_trans.einstien_A = statestrans[key][20]
		new_trans.intensity = statestrans[key][22]
		new_trans.wavenumber = statestrans[key][21]
		new_trans.change_mu = change_mu
		new_trans.change_nu = compare[key][2]
		new_trans.change_I = compare[key][3]
		new_trans.K_mu = compare[key][4]
		new_trans.K_I = compare[key][5]
	except sqlalchemy.orm.exc.MultipleResultsFound:
		raise Exception("Too many in db - FIX!")
	
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
	new_trans.isotopologue = trans_iso.id
	#print(trans_iso.id)
	
	try:
		upper_el = session.query(EnergyLevel).filter(EnergyLevel.exomol_ID==key.split(' - ')[0]).filter(EnergyLevel.isotopologue==trans_iso.id).one()
	except sqlalchemy.orm.exc.NoResultFound:
	#not in db, add
		upper_el = EnergyLevel()
		upper_el.exomol_ID = key.split(' - ')[0]
		
		upper_el.isotopologue = trans_iso.id
		
		upper_el.energy = statestrans[key][0]
		upper_el.J = statestrans[key][1]
		upper_el.Tparity = statestrans[key][2]
		upper_el.Rparity = statestrans[key][3]
		upper_el.state = statestrans[key][4]
		upper_el.v = statestrans[key][5]
		upper_el.Lambda = statestrans[key][6]
		upper_el.Sigma = statestrans[key][7]
		upper_el.Omega = statestrans[key][8]
		session.add(upper_el)
		session.flush()
	except sqlalchemy.orm.exc.MultipleResultsFound:
		raise Exception("Too many in db - FIX!")
	new_trans.upper = upper_el.id
	
	
	try:
		lower_el = session.query(EnergyLevel).filter(EnergyLevel.exomol_ID==key.split(' - ')[1]).filter(EnergyLevel.isotopologue==trans_iso.id).one()
	except sqlalchemy.orm.exc.NoResultFound:
	#not in db, add
		lower_el = EnergyLevel()
		lower_el.exomol_ID = key.split(' - ')[1]
		
		lower_el.isotopologue = trans_iso.id
		
		lower_el.energy = statestrans[key][10]
		lower_el.J = statestrans[key][11]
		lower_el.Tparity = statestrans[key][12]
		lower_el.Rparity = statestrans[key][13]
		lower_el.state = statestrans[key][14]
		lower_el.v = statestrans[key][15]
		lower_el.Lambda = statestrans[key][16]
		lower_el.Sigma = statestrans[key][17]
		lower_el.Omega = statestrans[key][18]
		session.add(lower_el)
		session.flush()
	except sqlalchemy.orm.exc.MultipleResultsFound:
		raise Exception("Too many in db - FIX!")
	new_trans.lower = lower_el.id

	session.flush()
	session.add(new_trans)
	
print('done loop')	



session.commit()

engine.dispose() # cleanly disconnect from the database
sys.exit(0)
