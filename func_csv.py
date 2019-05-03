def write_csv(data1_statestrans, data_compare, filename):
	#open file and set coloumn headings 
	with open(filename, 'w') as f:
		f.write("Exomol_ID,wavenumber,K_mu,")
		f.write("Upper_energy,Upper_degen,Upper_J,Upper_Tparity,Upper_Rparity,")
		f.write("Upper_state,Upper_v,Upper_Lambda,Upper_Sigma,Upper_Omega,")
		f.write("Lower_energy,Lower_degen,Lower_J,Lower_Tparity,Lower_Rparity,")
		f.write("Lower_state,Lower_v,Lower_Lambda,Lower_Sigma,Lower_Omega\n")
    	
    	
#loop over keys in dictionary and write to file, keeping track of what is a string, float, or in scientific notation
		for key in data_compare:
			f.write(str(key) + ",")
			f.write("%.6e," % data1_statestrans[key][21])
			f.write("%.6e," % data_compare[key][4])
			#upper
			f.write("%6f," % data1_statestrans[key][0])
			f.write("%.1f," % data1_statestrans[key][1])
			f.write("%.1f," % data1_statestrans[key][2])
			f.write(str(data1_statestrans[key][3])+ ",")
			f.write(str(data1_statestrans[key][4])+ ",")
			f.write(str(data1_statestrans[key][5])+ ",")
			f.write("%.1f," % data1_statestrans[key][6])
			f.write("%.1f," % data1_statestrans[key][7])
			f.write("%.1f," % data1_statestrans[key][8])
			f.write("%.1f," % data1_statestrans[key][9])
			#lower
			f.write("%.6f," % data1_statestrans[key][10])
			f.write("%.1f," % data1_statestrans[key][11])
			f.write("%.1f," % data1_statestrans[key][12])
			f.write(str(data1_statestrans[key][13])+ ",")
			f.write(str(data1_statestrans[key][14])+ ",")
			f.write(str(data1_statestrans[key][15])+ ",")
			f.write("%.1f," % data1_statestrans[key][16])
			f.write("%.1f," % data1_statestrans[key][17])
			f.write("%.1f," % data1_statestrans[key][18])
			f.write("%.1f\n" % data1_statestrans[key][19])