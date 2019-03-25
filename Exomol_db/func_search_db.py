#!/usr/bin/env python
import sys
import sqlalchemy
from SQLiteConnection import engine, Session
from ModelClasses import *
from sqlalchemy import func
from sqlalchemy import or_, and_
from sqlalchemy import func
from func_pop_db import pop_db
from func_plotpdf import plot_K, plot_SQL


#a function used to search through the exomol_K db - can be used as a stand alone script 
def search_db():

	#initiate db session 
	session = Session()
	
	
	#options to only search specific molecules, wavenumber ranges, and intensities 
	#is none are selected - search through db and grab all options
	set_mol = input('Choose specific molecules? ')
	
	dbmol = session.query(Isotopologue.name).all()
	mol = []
	[mol.append(item[0]) for item in dbmol]
	
	if set_mol =='yes':
		molecule = input('molecule input: ')
		molecule = molecule.split(' ')
	else:
		molecule = mol
	
	
	#check if molecule in db - if not option to func_pop_db
	for item in molecule:
		if item not in mol:
			add = input(f'{item} not in database, add? ')
			if add =='yes':
				f_1 = input('file 1: ')
				f_2 = input('file 2: ')
				in_co = float(input('Intensity cutoff for db: '))
				temp = float(input('Temperature: '))
				pop_db(f_1, f_2, in_co, temp)
				print(f'{item} added to db')
			else:
				print('Exiting')
				sys.exit(0)
				
	print(f'Searching {molecule}')		
	#[print(name[0]) for name in iso if name[0] in molecule]
	

	set_range = input('Set transition wavenumber range? ')
	if set_range =='yes':
		rangelow = input('From: ')
		rangeup = input('To: ')
	else:
		rangelow = session.query(func.min(Transition.wavenumber)).one()[0]
		rangeup = session.query(func.max(Transition.wavenumber)).one()[0]
		
	print(f'Wavenumber range {rangelow, rangeup}')
	
	
	set_intense = input('Set transition intensity cutoff?(y/n) ')

	if set_intense == 'yes':
		intensity_cutoff = float(input('Search for number of transitions with intensity greater than: '))
	else:
		intensity_cutoff = float(session.query(func.min(Transition.intensity)).one()[0])
		
	print(f'Intensity cutoff {intensity_cutoff}')


	#loop over search options for given initial conditions 

	exit = str()
	while exit != 'yes':
		task = input('What would you like to do out of the following; K values, count transitions, column headings, raw SQL? ' )
	

		#option 1 - get table and column headings from db

		if task =='column headings':
			con = engine.connect()
			print(f'tables in database are:\n {engine.table_names()}')
			usrinpt = input('table name for column headings: ')
			try:
				testlist = con.execute(f'select * from {usrinpt}').keys()
				[print(row) for row in testlist]
			except sqlalchemy.exc.OperationalError:
				print("Invalid search terms")
	

		#option 2 is a raw SQL search - works best with simple queries 

		elif task == 'raw SQL':
			con = engine.connect()
			usrinpt = input('raw SQL comands: ')
			try:
				rawSQL = con.execute(usrinpt)
				#[print(row) for row in testlist]					
			except sqlalchemy.exc.OperationalError:
				print("Invalid search terms")
				
			#save output to memory as list	
			raw_outpt = []
			for row in rawSQL:
				raw_outpt.append(row)
				print(row)
			
			#save to csv file 
			save_raw = input('save output as csv? ')
			if save_raw =='yes':
				filename = input('filename? ')
				with open(f'{filename}.txt', 'w') as file:
					[file.write(f'{row}\n') for row in raw_outpt]
						
			#create pdf plot 				
			plot_raw = input('plot raw SQL output? ')
			if plot_raw == 'yes':
				plot_SQL(raw_outpt)
	
	
	
		#option 3 count the number of transitions - separates by temp, and molecule
		#also counts the number of electronic states involved
		elif task == 'count':
			
			tally = session.query(Transition).join(Transition.isotopologue).filter(Isotopologue.name.in_(molecule)).filter(and_(Transition.wavenumber >= rangelow, Transition.wavenumber<= rangeup)).filter(Transition.intensity > intensity_cutoff).all()
			
			isos = set()
			[isos.add(item.isotopologue) for item in tally]
			isos = list(isos)
			
			temps = set()
			[temps.add(item.isotopologue.temperature) for item in tally]
			temps = list(temps)
			for temp in temps:
				print(f'T = {temp}')

				for i in range(len(isos)):
					count = 0
					el_states = set()
					for item in tally:
						if item.isotopologue.name == isos[i].name:
							count+=1
							el_states.add(item.upper.state)
							el_states.add(item.lower.state)
					print(f'There are {count} {isos[i].name} transitions with intensity greater than {intensity_cutoff} between {rangelow, rangeup}')
					print(f'there are {len(el_states)} electronic states for {isos[i].name}')
			
		
		#option 4 - goes one further with filter and has a |K| condition of. the db search 
		# splits on temp and molecule	
		elif task == 'K values':
			cutoff =float(input('Search for |K| greater than: '))
			K = session.query(Transition).join(Transition.isotopologue).filter(Isotopologue.name.in_(molecule)).filter(and_(Transition.wavenumber >= rangelow, Transition.wavenumber<= rangeup)).filter(Transition.intensity > intensity_cutoff).filter(or_(Transition.K_mu > cutoff, Transition.K_mu < -cutoff)).order_by(Transition.wavenumber).all()

			
			print(f'There are {len(K)} transitions that match that criteria')
			isos = set()
			[isos.add(item.isotopologue) for item in K]
			isos = list(isos)
			
			temps = set()
			[temps.add(item.isotopologue.temperature) for item in K]
			temps = list(temps)
			for temp in temps:
				print(f'T = {temp}')
				
				for i in range(len(isos)):
					count = 0
					for item in K:
						if item.isotopologue.name == isos[i].name:
							count+=1
					print(f'{count} are from {isos[i].name}')
			
			#print to screen - can change what is printed - only have name, ID, and K atm 
			K_print=input('Would you like to print the exomol IDs? ')
			[print(item.isotopologue.name, item.exomol_ID, item.K_mu) for item in K if K_print=='yes']
			
			#save to csv - same ability as above
			save_K = input('save output as csv? ')
			if save_K =='yes':
				filename = input('filename? ')
# 				outpt = [['isotopologue.name', 'exomol_ID', 'K_mu']]
# 				[outpt.append([item.isotopologue.name, item.exomol_ID, item.K_mu]) for item in K]

				outpt = [['isotopologue.name', 'exomol_ID', 'wavenumber', 'K_mu', 'upper.energy', 'degeneracy', 'J', 'Tparity', 'Rparity', 'state', 'v', 'Lambda', 'Sigma', 'Omega', 'lower.energy', 'degeneracy', 'J', 'Tparity', 'Rparity', 'state', 'v', 'Lambda', 'Sigma', 'Omega']]
				[outpt.append([item.isotopologue.name, item.exomol_ID, item.wavenumber, item.K_mu, item.upper.energy, item.upper.degeneracy, item.upper.J, item.upper.Tparity, item.upper.Rparity, item.upper.state, item.upper.v, item.upper.Lambda, item.upper.Sigma, item.upper.Omega, item.lower.energy, item.lower.degeneracy, item.lower.J, item.lower.Tparity, item.lower.Rparity, item.lower.state, item.lower.v, item.lower.Lambda, item.lower.Sigma, item.lower.Omega]) for item in K
				]
				with open(f'{filename}.txt', 'w') as file:
					[file.write(f'{row}\n') for row in outpt]
		
			#create pdf plot - one for each molecule - plus one for all
			input_plot = input('Would you like to plot these? ')
			if input_plot == 'yes':
				plot_K(K, cutoff)
		
		
		exit = input('Are you finished searching? ')


	engine.dispose() # cleanly disconnect from the database
	
search_db()
