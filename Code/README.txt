This folder contains the code used to re-run two of the simulations from the article. 

"Probability of Divergence" were tried reproduced using the POD.py
	Run the method pod_simulation with True/False as parameter  wheter to write the result in json lines format to file
	
"Performance Comparison With Other Algorithms" were tried reproduced using the WEP.py
	Run the method wep_simulation with distribution type (enum from GMCC.py) and True/False wheter the result in json lines format should be written to file


GMCC.py contains the GMCC algorithm and the distribution type enum used in WEP.py

Plot-Result.py is used to plot the results

WriteJSON.py is used to write the results in json lines format to file