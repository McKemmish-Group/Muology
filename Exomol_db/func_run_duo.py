#!/usr/bin/env python

import re
import subprocess
import glob

def run_duo():
	files = glob.glob('run/*.inp')
# 	print(files)

	for file in files:
		subprocess.call(["chmod", "666", file])
		outputfl = file.split('.')[0]+'.out'
		inpt = open(file)
		outpt = open(outputfl, 'w')
		p = subprocess.Popen('./j-duo_fast.x', stdin = inpt, stdout=outpt)
		p.wait()
		outpt.flush()
