#!/usr/bin/env python

import re
import subprocess
import glob


def initiate_inp():
	flnms = glob.glob('../../original_inpfiles/*.inp')
	print(flnms)

	#filename = "inpt_files/14N32S.inp"

	for filename in flnms:
		subprocess.call(["chmod", "666", filename])

		with open(filename, 'r') as file:
			molecule = filename.split('/')[-1].split('.')[0]
			print(molecule)

			txt = str(file.read())
		
			x = re.split('intensity',txt, flags=re.I)[1]
			x = re.split('end', x, flags= re.I)[0]
			#x = x[0]
			#print(x)
		
	# 		y = re.search('intensity.*end', txt, re.I| re.S).group(0)

	
			common = f'''\n  absorption
  thresh_intes  1e-30
  thresh_coeff 1e-30
  thresh_dipole 1e-30
  temperature   1000.0
  J,  0.5,20.5
  zpe  0.0
  linelist {molecule}_J20_1000K_e-0\n'''

	
		#Keep setting that are unique? to molecule
	
			srch = re.search('.*nspin.*\n', txt)
			if srch is not None:
				common = common + srch.group()
		
			srch = re.search('.*gns.*\n', txt)
			if srch is not None:
				common = common + srch.group()
		
			srch = re.search('.*freq-window.*\n', txt)
			if srch is not None:
				common = common + srch.group()
		
			srch = re.search('.*energy low.*\n', txt)
			if srch is not None:
				common = common + srch.group()
		
			srch = re.search('.*selection.*\n', txt)
			if srch is not None:
				common = common + srch.group()
	
			#print(common)


	# 	Get rid of lande and qstat in the intensity section 
	# 		srch = re.search('lande.*\n\s*', txt)
	# 		print(srch)
	# 		if srch is not None:
	# 			print(srch.group())
	# 			upx = re.sub(srch.group(), ' ', upx)
	# 				
	# 		srch = re.search('qstat.*\n\s*', txt)
	# 		print(srch)
	# 		if srch is not None:
	# 			print(srch.group())
	# 			upx = re.sub(srch.group(), ' ', upx)
	# 		print(x)
	# 		print(upx)
	# 		txt = re.sub(x, upx, txt)

		#update 

			txt = txt.replace(x, common)
			#print(txt)
	
		with open(f'../../run/{molecule}_e-0.inp', 'w') as file:
			file.write(txt)
		
		with open(f'../../run/{molecule}_e-0.inp', 'r') as file:
			txt = str(file.read())
			deltam = 1+ 10**(-4)
		
		
			molmass = txt.split('masses')[1].split('\n')[0]
			print(molmass)
			mass1 = float(molmass.split()[0])
			mass2 = float(molmass.split()[1])
		
			mass1_up = mass1*deltam
			mass2_up = mass2*deltam
			print(f' {mass1_up} {mass2_up}')
			
			srch = re.search('linelist.*\n\s*', txt)
			if srch is not None:
				print(srch.group())
				txt = re.sub(srch.group(), f'linelist {molecule}_J20_1000K_e-4 \n  ', txt)
			print(re.search('linelist.*\n\s*', txt).group())	
				
			
			txt = txt.replace(molmass, f' {mass1_up} {mass2_up}')
		
		with open(f'../../run/{molecule}_e-4.inp', 'w') as file:
			file.write(txt)


#initiate_inp()

		
		
		
		
		
