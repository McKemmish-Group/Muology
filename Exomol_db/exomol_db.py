#!/usr/bin/env python
import sys
import sqlalchemy
from SQLiteConnection import engine, Session
from ModelClasses import *
from func_pop_db import pop_db
from func_search_db import search_db
from func_reg_init import initiate_inp


datapath = '../../Data_J20_1000K/' #location to where you have stored your data 
while exit != 'yes':

	task = input(f'What would you like to do? \n initialise input files (inp) \n run DUO (run) \n add to database (add) \n search database (search) \n')
	
	if task == 'inp':
		initiate_inp()
	
	
	elif task == 'run':
		print('DUO not yet set up run on raijin')


	
	elif task == 'add':
		f_1 = input('file 1: ')
		f_1 = datapath + f_1
		f_2 = input('file 2: ')
		f_2 = datapath + f_2
		in_co = float(input('Intensity cutoff for db: '))
		temp = float(input('Temperature: '))
		pop_db(f_1, f_2, in_co, temp)
		print(f'molecule added to db')
		
		
	elif task == 'search':
		search_db()
		
		
	exit = input('Are you finished? ')