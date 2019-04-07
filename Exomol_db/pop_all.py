#!/usr/bin/env python

import glob
from func_pop_db import pop_db
 

# files = glob.glob("../../Data_J20_1000K/*_e-0.states")
#files = ['../../Data_J20_1000K/27Al18O_J20_1000K_e-0.states', '../../Data_J20_1000K/51V16O_J20_1000K_e-0.states']

files = ['../../Data_J20_1000K/51V16O_J20_1000K_e-0.states', '../../Data_J20_1000K/26Al16O_J20_1000K_e-0.states', '../../Data_J20_1000K/27Al18O_J20_1000K_e-0.states', '../../Data_J20_1000K/27Al16O_J20_1000K_e-0.states']

for f in files:
	file_1 = f.split('.states')[0]
	file_2 = f.split('.states')[0].split('-')[0] + '-4'
	print(file_1)
	print(file_2)
	temp = 20
	cutoff = 1e-30
	pop_db(file_1, file_2, cutoff, temp)
	print('added')