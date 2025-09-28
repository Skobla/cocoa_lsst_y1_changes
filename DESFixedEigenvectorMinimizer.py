import numpy as np
import os, sys, time
from io import StringIO
from cobaya.yaml import yaml_load_file
from cobaya.run import run
from cobaya.post import post
from getdist.mcsamples import MCSamplesFromCobaya
from scipy.optimize import minimize

# original file: EXAMPLE_EVALUATE1.yaml

ggsplit_yaml_file   = "./projects/des_y3/EXAMPLE_EVALUATE1.yaml"

info_lcdm = yaml_load_file("./projects/des_y3/EXAMPLE_EVALUATE1.yaml")

info_lcdm['params']['changer']['value'] = 2

# normally k, z are both 8, changing as needed

kbins = 8
zbins = 5

#We are gonna try stripping the label 
#initial_guess = [0] * (kbins + zbins - 2) # -1 is another sk edit

#initial_guess = [-2.33563650e-01, -1.25103291e-01, -7.84774399e-02, -1.04305397e-01,
#         -7.47651072e-02, -5.20953274e-02, -9.87372998e-02,  2.54355465e-01,
#          -6.82993314e-04,  1.02476706e+00, -2.72571208e-01]

#initial_guess = np.array([ 0.05221488, -0.20385588, -0.10668704, -0.22836565, -0.99542944 * 0.95, -0.99945047 * 0.95,
#         -0.1398541,  -0.21281225,  0.64659549,  0.20044805,  0.0053682,  -0.00607865,
#          -0.00324256, -0.00135969])

initial_guess = [0] * 4

#initial_guess = [-0.12696726,  0.05636146, -0.17876376, -0.02112459]

#eigen0 = [-0.0433717 , -0.00709454, -0.21877118, -0.26430244, -0.27606507,
#               -0.08065701,  0.05519716, -0.88454813, -0.10684167, -0.02685973,
#                      -0.0050759 ]
#eigen1 = [-0.02691131,  0.55842457,  0.37753849,  0.47973727, -0.03552276,
#               -0.18652453, -0.42463804, -0.256144  ,  0.11135984,  0.13985639,
#                       0.02851863]
#eigen2 = [-0.10609147, -0.15547878,  0.00627422,  0.03634504, -0.18251537,
#               -0.33572085, -0.39287204,  0.15387664, -0.70462311, -0.37225676,
#                      -0.06399209]
#eigen3 = [ 0.17601045,  0.13717186,  0.41903056, -0.32621913, -0.52216661,
#               -0.46994369,  0.34601627,  0.19543551,  0.12776172,  0.02112527,
#                       0.00141277]

#eigen0 = [-0.0472897 ,  0.0575034 , -0.18539348, -0.19737185, -0.26886743,
#               -0.10420487, -0.04245742, -0.90270521, -0.13996228, -0.04068445,
#                      -0.0076362 ]
#eigen1 = [-0.06759282,  0.51496686,  0.38730975,  0.52378785, -0.01236148,
#               -0.22379907, -0.48736362, -0.10620192, -0.01790413,  0.07823287,
#                       0.01989687]
#eigen2 = [-0.04995212, -0.20953795, -0.01605916, -0.10815114, -0.21872597,
#               -0.35468299, -0.27144795,  0.25964353, -0.68706573, -0.38659056,
#                      -0.07343473]
#eigen3 = [ 0.17384293,  0.19458129,  0.42768427, -0.26344673, -0.54357758,
#               -0.39847213,  0.41197147,  0.12987867,  0.18296837,  0.07162313,
#                       0.01207692]


#These are A199, .1 percent difference eigenvectors
#eigen0 = [-0.08299766,  0.18006804,  0.25341219,  0.33872161,  0.1804131 ,
#                0.0440284 , -0.08751268,  0.85017532,  0.12341714,  0.03875271,
#                        0.00770214]
#eigen1 = [0.15788889,  0.0749676 ,  0.05920203, -0.02168068, -0.45122975,
#        0.29068264,  0.45159215,  0.01527027,  0.59538093,  0.33862947,
#                0.06367359]
#eigen2 = [ 0.25900441, -0.50035716, -0.38000472,  0.00716314,  0.456751  ,
#                0.55024887,  0.0819234 ,  0.12095527,  0.00226085,  0.07190026,
#                        0.01388737]
#eigen3 = [-0.39444229,  0.11313507, -0.00716091,  0.24039655,  0.41552998,
#                0.04608104, -0.33390288, -0.37095472,  0.57519254,  0.13619617,
#                        0.02215703]

#These are As199, 1 percent difference eigenvectors
#eigen0 = [ 0.01431059,  0.08306634,  0.21952175,  0.31150194,  0.29245626,
#                0.12376273, -0.03429627,  0.8569189 ,  0.10367477,  0.02387735,
#                        0.00438434]
#eigen1 = [ 0.02753176,  0.14406871,  0.33869913,  0.24815951, -0.24507947,
#               -0.53600991, -0.54270759, -0.00280285, -0.37333429, -0.14289504,
#                      -0.02187505]
#eigen2 = [-0.15755939, -0.33459038, -0.40598295, -0.15092957,  0.16430517,
#                0.12574982, -0.059763  ,  0.20868073, -0.66769539, -0.36828628,
#                       -0.06513103]
#eigen3 = [-0.03178798, -0.23852787, -0.20837459,  0.36976457,  0.56636195,
#                0.07645887, -0.53023172, -0.31150763,  0.20893367,  0.11432157,
#                        0.02076004]

#These are As199 using real DES Y3 and using teh .1 percent eigenvectors of that model
eigen0 = [-0.04183004,  0.15529298,  0.25523423,  0.34750339,  0.23067142,
                0.04318104, -0.13313056,  0.84020829,  0.09446738,  0.02320797,
                        0.00457235]
eigen1 = [ 0.16531077,  0.15650645,  0.13248099, -0.00084422, -0.50302953,
                0.2019547 ,  0.40522772,  0.05471494,  0.59752195,  0.33056485,
                        0.05738397]
eigen2 = [ 0.25721813, -0.49225604, -0.38607414, -0.0170751 ,  0.37324745,
                0.58357175,  0.18164468,  0.11404846,  0.06497172,  0.10824637,
                        0.01918179]
eigen3 = [-0.39364339,  0.31115546, -0.33662532, -0.50384304, -0.16451086,
                0.19986253,  0.31193729,  0.35064907, -0.24599628, -0.1787773 ,
                       -0.03617668]

def chi_square_model(params):
    p0, p1, p2, p3 = params[0], params[1], params[2], params[3]
    changer_vector = p0 * np.array(eigen0) + p1 * np.array(eigen1) + p2 * np.array(eigen2) + p3 * np.array(eigen3)

    #changer_vector = 0.001 * changer_vector
   
    #Let us see if this fixes the left log error on the lnPL because not a previous error with nonlinear
    if np.any(np.array(changer_vector) < -0.99):
        chi_squared = 1e10
        return chi_squared

    for i in range(kbins+zbins - 2): # the 1 is an sk added change to see what occurs if I strip out the first z bin
        if i + 1 < kbins:
            bin_value = "kvalue" + str(i)
            info_lcdm["params"][bin_value]["value"] = 1 + float(changer_vector[i])
        else:
            idep = i - kbins + 1 # change here
            bin_value = "zvalue" + str(idep)
            info_lcdm["params"][bin_value]["value"] = 1 + float(changer_vector[i])

    
    updated_info, evaluate = run(info_lcdm, force=True)
    sample = evaluate.products()["sample"]
    sample_array = sample.to_numpy()
    chi_squared = sample_array[-1][-1]
    #if p1 > p0: # to make p2 less than p1
    #    chi_squared = 1000
    print("HELLO: PARAMS ARE:", changer_vector)
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


options = {'ftol': 1e-10, 'gtol': 1e-8, 'maxiter': 10000}

#result = minimize(chi_square_model, initial_guess, method = 'L-BFGS-B')
result = minimize(chi_square_model, initial_guess, options = options, method = 'COBYLA')
optimal_params = result.x
min_chi_square = result.fun

print("Optimal Parameters:", optimal_params)
print("Minimum Chi-Square:", min_chi_square)

#z0_choices = np.arange(0.001, 0.005, 0.001).tolist()

#z0_changes_dict = dict()

#for first_bin in z0_choices:
#    for temp in range(zbins-1):
#        # so now we shift all the bins up as another test and if this doesn't work, I will try adding a quasi first bin normed out
#        # Next we will then try to shift up my epsilon and then have the minimizer IGNORE the value of the first epsilon shifted bin and see what happens :)
#        name = "zbin" + str(temp)
#        info_lcdm["params"][name]["value"] = first_bin + temp * 0.2
#    #info_lcdm["params"]["zbin0"]["value"] = first_bin
#    result = minimize(chi_square_model, initial_guess, method = 'L-BFGS-B')
#    optimal_params = result.x
#    min_chi_square = result.fun
#    z0_changes_dict[first_bin] = (optimal_params, min_chi_square)

#for temp in range(zbins-1):
#    name = "zbin" + str(temp)
#    info_lcdm["params"][name]["value"] = temp * 0.2

#print('Our results are', z0_changes_dict)


#sup_optimal_prev = [ 1.15894474e-01,  1.22880753e-02, -2.31989648e-01, -4.80285272e-01,
#         -2.53396506e-01, -3.52470496e-03,  1.34231430e-02, -9.62276863e-01,
#           4.96968428e-02,  2.10020282e-01,  5.34478856e-02,  8.34256225e-04,
#            -1.45527254e-03, -7.50745631e-04]


#sup_optimal = [ 0.08325332,  0.08125649, -0.04670897, -0.4266692,  -0.37071083,  0.02164983,
#          0.01074052, -0.99859535,  0.18658981,  0.2744198,   0.07674745,  0.00202307,
#           -0.00233337, -0.00125528]


#test_list = list()
#test_key = list()

#test_list.append(chi_square_model)
#test_key.append('sup_optimal')

#for i in range(1, 15):
#    holder = np.array(sup_optimal)
#    holder[7] = holder[7] + i * 0.1
#    test_list.append(chi_square_model(holder))
#    test_key.append('value of zbin0 is' + str(holder[7]))

#for x, y in zip(test_key, test_list):
#    print(x, y)

#for i in range(kbins + zbins - 2):
#    x = np.copy(sup_optimal)
#    x[i] = x[i] * 1.01 # 1.5 say
#    test_list.append(x)
#    test_key.append(str(i) + '_1.01')
#    x[i] = x[i] * 0.99 / 1.01
#    test_list.append(x)
#    test_key.append(str(i) + '_0.99')

#print('tysh sup_optimal', sup_optimal)
#baseline = chi_square_model(sup_optimal)

#print('tysh', baseline)

#results_dict = dict()

#results_dict['0'] = baseline

#results_dict['LCDM'] = chi_square_model([0] * (kbins + zbins - 2))

#for i in range(2*(kbins + zbins - 2)):
#    temp = chi_square_model(test_list[i])
#    results_dict[test_key[i]] = temp - baseline

#print('RESULTS ARE')
#print(results_dict)
