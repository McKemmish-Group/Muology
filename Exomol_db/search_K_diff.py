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


session = Session()

dbisos = session.query(Isotopologue.name).distinct()
dbtemps = session.query(Isotopologue.temperature).distinct()

temps = []
isos=[]
[temps.append(item[0]) for item in dbtemps]
[isos.append(item[0]) for item in dbisos]



K_diff = {}

# for temp in temps:
# 	for iso in isos:
# 		max = session.query(func.max(Transition.K_mu)).join(Transition.isotopologue).filter(Isotopologue.name==iso).filter(Isotopologue.temperature==temp).one()[0]
# 		min = session.query(func.min(Transition.K_mu)).join(Transition.isotopologue).filter(Isotopologue.name==iso).filter(Isotopologue.temperature==temp).one()[0]
# 		
# 		maxtrans = session.query(Transition).filter(Transition.K_mu==max).one()
# 		mintrans = session.query(Transition).filter(Transition.K_mu==min).one()
# 
# 		print(iso)
# 		print(maxtrans.exomol_ID, maxtrans.upper.state, maxtrans.lower.state, max, maxtrans.wavenumber, maxtrans.intensity)
# 		print(mintrans.exomol_ID, mintrans.upper.state, mintrans.lower.state, min, mintrans.wavenumber, mintrans.intensity)
# 
# 		K_diff[f'{iso}_{temp}K']= max - min
		
#print(K_diff)


delta_K = session.query(Transition, func.max(Transition.K_mu), func.min(Transition.K_mu)).group_by(Transition.isotopologue_id).all()

[K_diff.update({f'{item[0].isotopologue.name}':(item[1]-item[2])}) for item in delta_K]
print(K_diff)

[print(item[0].K_mu)for item in delta_K]


engine.dispose()