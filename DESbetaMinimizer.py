import numpy as np
import os, sys, time
from io import StringIO
from cobaya.yaml import yaml_load_file
from cobaya.run import run
from cobaya.post import post
from getdist.mcsamples import MCSamplesFromCobaya
from scipy.optimize import minimize
from scipy.integrate import quad

# original file: EXAMPLE_EVALUATE1.yaml

ggsplit_yaml_file   = "./projects/des_y3/EXAMPLE_EVALUATE1.yaml"

info_lcdm = yaml_load_file("./projects/des_y3/EXAMPLE_EVALUATE1.yaml")

info_lcdm['params']['changer']['value'] = 2

# normally k, z are both 8, changing as needed

kbins = 8 # k will not be modified in this method
zbins = 5

#initial_guess = [0] * (kbins + zbins - 2) # -1 is another sk edit

initial_guess = [0]

def chi_square_model_beta_simple(beta_value):
    for i in range(zbins - 1):
        bin_value = "zvalue" + str(i)

        left_bin = "zbin" + str(i)
        right_bin = "zbin" + str(i+1)

        left = float(info_lcdm["params"][left_bin]["value"])
        right = float(info_lcdm["params"][right_bin]["value"])
        
        z = (left + right) / 2
        
        changed_alpha = beta_value[0] / (0.3 * (1 + z)**3 + 0.7)
        
        print('changed alpha', changed_alpha)

        info_lcdm["params"][bin_value]["value"] = 1 + changed_alpha

    updated_info, evaluate = run(info_lcdm, force=True)
    sample = evaluate.products()["sample"]
    sample_array = sample.to_numpy()
    chi_squared = sample_array[-1][-1]
    
    for i in range(zbins - 1):
        bin_value = "zvalue" + str(i)
        info_lcdm["params"][bin_value]["value"] = 1.
    
    if np.isnan(chi_squared):
        chi_squared = 1e10

    return chi_squared

def integrand(z):
    return 1 / (0.3 * (1 + z)**3 + 0.7)

def chi_square_model_beta_integral(beta_value):
    for i in range(zbins - 1):
        bin_value = "zvalue" + str(i)
        left_bin = "zbin" + str(i)
        right_bin = "zbin" + str(i+1)
        left = float(info_lcdm["params"][left_bin]["value"])
        right = float(info_lcdm["params"][right_bin]["value"])
        
        #def integrand(z):
        #    return beta_value[0] / (0.3 * (1 + z)**3 + 0.7)
        print(integrand)
        changed_alpha, error = quad(integrand, left, right)
        print(changed_alpha) 
        changed_alpha = changed_alpha * beta_value[0] / (right - left)

        print('changed alpha', changed_alpha)

        if changed_alpha < -0.98:
            chi_squared = 1e10
            return chi_squared

        info_lcdm["params"][bin_value]["value"] = 1 + changed_alpha
 
    updated_info, evaluate = run(info_lcdm, force=True)
    sample = evaluate.products()["sample"]
    sample_array = sample.to_numpy()
    chi_squared = sample_array[-1][-1]

    for i in range(zbins - 1):
        bin_value = "zvalue" + str(i)
        info_lcdm["params"][bin_value]["value"] = 1.

    if np.isnan(chi_squared):
        chi_squared = 1e10

    return chi_squared

def chi_square_model(params):
    #changer_vector = p0 * np.array(eigen0) + p1 * np.array(eigen1) + p2 * np.array(eigen2) + p3 * np.array(eigen3)

    #changer_vector = 0.001 * changer_vector

    for i in range(kbins+zbins - 2): # the 1 is an sk added change to see what occurs if I strip out the first z bin
        if i + 1 < kbins:
            bin_value = "kvalue" + str(i)
            info_lcdm["params"][bin_value]["value"] = 1 + float(params[i])
        else:
            idep = i - kbins + 1 # change here
            bin_value = "zvalue" + str(idep)
            info_lcdm["params"][bin_value]["value"] = 1 + float(params[i])

    
    updated_info, evaluate = run(info_lcdm, force=True)
    sample = evaluate.products()["sample"]
    sample_array = sample.to_numpy()
    chi_squared = sample_array[-1][-1]
    #if p1 > p0: # to make p2 less than p1
    #    chi_squared = 1000
    print("HELLO: PARAMS ARE:", params)
    for i in range(kbins+zbins - 2): # the same sk edit to remove first bin, can reasesss as needed
        if i + 1 < kbins:
            bin_value = "kvalue" + str(i)
            info_lcdm["params"][bin_value]["value"] = 1.
        else:
            idep = i - kbins + 1  # change here
            bin_value = "zvalue" + str(idep)
            info_lcdm["params"][bin_value]["value"] = 1.
    
    # We are gonna try the below if it is no good then we can take away
    if np.isnan(chi_squared):
        chi_squared = 1e10

    print('csq after mod is', chi_squared)

    return chi_squared

#options = {'ftol': 1e-10, 'gtol': 1e-8, 'maxiter': 10000}

result = minimize(chi_square_model_beta_integral, initial_guess, method = 'COBYLA')

optimal_params = result.x
min_chi_square = result.fun

print("Optimal Parameters:", optimal_params)
print("Minimum Chi-Square:", min_chi_square)

