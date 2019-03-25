import sys
import sqlalchemy
from SQLiteConnection import engine, Session
from ModelClasses import *
from sqlalchemy import func
from sqlalchemy import or_, and_

import matplotlib.pyplot as plt 


#function to create basic pdf plot of K transitions
# takes input of list of Transition objects returned from db query and cutoff 
def plot_K(transitions, cutoff):
	#list of the molecules
	isos = set()
	[isos.add(item.isotopologue) for item in transitions]
	isos = list(isos)
	
	#list of the temperatures
	temps = set()
	[temps.add(item.isotopologue.temperature) for item in transitions]
	temps = list(temps)
	
	#loop over molecules and temperature - to get individual plots for each molecule
	#plots K_mu vs wavenumber - temperature as legend
	for i in range(len(isos)):
		fig = plt.figure(figsize=(12,6))
		for temp in temps:
			x = []
			y = []
			print(f'plotting {isos[i].name} transitions')
			for item in transitions:
				if item.isotopologue.name==isos[i].name and item.isotopologue.temperature==temp:
					x.append(item.wavenumber)
					y.append(item.K_mu)
	
			
			plt.plot(x, y, 'x', label= f'T = {temp}K')
		plt.legend(loc='best')
		plt.xlabel(f'Wavenumber ($cm^-1$)')
		plt.ylabel(f'$K_\mu$')
		plt.title(f'{isos[i].name} transitions with |$K_\mu$| > {cutoff}')

		fig.savefig(f'{isos[i].name}_K{int(cutoff)}_plot.pdf')



	#plots all on one plot - legend as molecule and temp
	fig = plt.figure(figsize=(12,6))
	for temp in temps:	
		for i in range(len(isos)):
			x = []
			y = []
			#print(isos[i].name)
			for item in transitions:
				if item.isotopologue.name==isos[i].name and item.isotopologue.temperature==temp:
					x.append(item.wavenumber)
					y.append(item.K_mu)
	
			plt.plot(x, y, 'x', label = f'{isos[i].name} at T = {temp}K')
			#plt.xlim(0, 1000)
	plt.xlabel('wavenumber')
	plt.ylabel(f'$K_\mu$')
	plt.title(f'Transitions with |$K_\mu$| > {cutoff}')
	plt.legend(loc='best')
	fig.savefig(f'plot_K{int(cutoff)}.pdf')
	
	
#function for simple plot of raw SQL output - takes input of list returned by search	
def plot_SQL(list):
	#user input of columns to plot - as well as axis labels and filename
	ref_x = int(input('which column on x axis (interger starting at 0)? '))
	ref_y = int(input('which column on y axis (interger starting at 0)? '))
	
	xlab = input('label on x axis: ')
	ylab = input('label on y axis: ')
	filename = input('filename: ')

	x = []
	y = []
	for row in list:
		x.append(row[ref_x])
		y.append(row[ref_y])
	
	fig = plt.figure(figsize=(12,6))
	plt.plot(x, y, 'x')
	plt.xlabel(xlab)
	plt.ylabel(ylab)
	fig.savefig(f'{filename}.pdf')