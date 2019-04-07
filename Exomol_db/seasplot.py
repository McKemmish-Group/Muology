#!/usr/bin/env python

import sys
import sqlalchemy
from SQLiteConnection import engine, Session
from ModelClasses import *
from sqlalchemy import or_, and_
import pandas as pd
import seaborn as sns 
import math
import matplotlib.pyplot as plt

session = Session()

cutoff = 2

dbsearch = session.query(Transition).join(Transition.isotopologue).filter(or_(Transition.K_mu > cutoff, Transition.K_mu < -cutoff)).all()

data_dict = {'molecule': [], 'exomol ID': [], 'wavenumber': [], 'intensity':[], 'log(intensity)': [], 'K_mu': [], 'upper J': []}

for entry in dbsearch:
	data_dict['molecule'].append(entry.isotopologue.name)
	data_dict['exomol ID'].append(entry.exomol_ID)
	data_dict['wavenumber'].append(entry.wavenumber)
	data_dict['intensity'].append(entry.intensity)
	data_dict['log(intensity)'].append(math.log10(entry.intensity))
	data_dict['K_mu'].append(entry.K_mu)
	data_dict['upper J'].append(entry.upper.J)
	
print(len(data_dict['molecule']))

data_df = pd.DataFrame(data=data_dict)
#print(data_df)

#plt.plot(data_df['wavenumber'], data_df['K_mu'], '.')





# from matplotlib.colors import LogNorm
# fig = sns.regplot(x="wavenumber", y="K_mu",
#             hue="intensity", style="choice",
#             hue_norm=LogNorm(), data=data_df);
            


sns.scatterplot(x='wavenumber', y = 'K_mu', hue='log(intensity)', style ='molecule', data = data_df, legend = 'brief')

plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.2)
#fig.savefig(f'intensity.pdf')

plt.show()


