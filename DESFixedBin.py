import numpy as np
import os, sys, time
from io import StringIO
from cobaya.yaml import yaml_load_file
from cobaya.run import run
from cobaya.post import post
from getdist.mcsamples import MCSamplesFromCobaya

ggsplit_yaml_file   = "./projects/des_y3/EXAMPLE_EVALUATE1.yaml"

info_lcdm = yaml_load_file("./projects/des_y3/EXAMPLE_EVALUATE1.yaml")

info_lcdm['params']['changer']['value'] = 2

kbins = 8
zbins = 5
### NOTE THE EDIT TO THE Z's to start at "1" and the relabeling of that as bin 0... to start itt up at 0.2 ###
for i in range(zbins-1): # prev 0, zbins -1
    bin_name = "zbin" + str(i) #-1 is addition if shifting off of first bin
    bin_value = "zvalue" + str(i)
    info_lcdm['likelihood']['des_y3.des_cosmic_shear']['print_datavector_file'] = "./projects/des_y3/data/DES_oneXi_real_newSmoothing_As199_Data/1.001" + bin_name + ".modelvector"
    info_lcdm["params"][bin_value]["value"] = 1.001
    updated_info, evaluate = run(info_lcdm, force=True)
    info_lcdm["params"][bin_value]["value"] = 1.

for i in range(zbins-1): #see above
    bin_name = "zbin" + str(i)
    bin_value = "zvalue" + str(i)
    info_lcdm['likelihood']['des_y3.des_cosmic_shear']['print_datavector_file'] = "./projects/des_y3/data/DES_oneXi_real_newSmoothing_As199_Data/0.999" + bin_name + ".modelvector"
    info_lcdm["params"][bin_value]["value"] = 0.999
    updated_info, evaluate = run(info_lcdm, force=True)
    info_lcdm["params"][bin_value]["value"] = 1.

for i in range(kbins-1):
    bin_name = "kbin" + str(i)
    bin_value = "kvalue" + str(i)
    info_lcdm['likelihood']['des_y3.des_cosmic_shear']['print_datavector_file'] = "./projects/des_y3/data/DES_oneXi_real_newSmoothing_As199_Data/1.001" + bin_name + ".modelvector"
    info_lcdm["params"][bin_value]["value"] = 1.001
    updated_info, evaluate = run(info_lcdm, force=True)
    info_lcdm["params"][bin_value]["value"] = 1.

for i in range(kbins-1):
    bin_name = "kbin" + str(i)
    bin_value = "kvalue" + str(i)
    info_lcdm['likelihood']['des_y3.des_cosmic_shear']['print_datavector_file'] = "./projects/des_y3/data/DES_oneXi_real_newSmoothing_As199_Data/0.999" + bin_name + ".modelvector"
    info_lcdm["params"][bin_value]["value"] = 0.999
    updated_info, evaluate = run(info_lcdm, force=True)
    info_lcdm["params"][bin_value]["value"] = 1.
