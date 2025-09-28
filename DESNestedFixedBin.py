import numpy as np
import os, sys, time
from io import StringIO
from cobaya.yaml import yaml_load_file
from cobaya.run import run
from cobaya.post import post
from getdist.mcsamples import MCSamplesFromCobaya

ggsplit_yaml_file   = "./projects/des_y3/EXAMPLE_EVALUATE1.yaml"

info_lcdm = yaml_load_file("./projects/des_y3/EXAMPLE_EVALUATE1.yaml")

info_lcdm['params']['changer']['value'] = 3

kbins = 6
zbins = 6

for i in range(zbins - 1):
    for j in range(kbins - 1):
        bin_name = "zbin" + str(i) + "kbin" + str(j)
        bin_value1 = "zvalue" + str(i)
        bin_value2 = "kvalue" + str(j)
        info_lcdm['likelihood']['des_y3.des_cosmic_shear']['print_datavector_file'] = "./projects/des_y3/data/DES25_oneXi_intAc2_z0to1_k0.025to0.8_Data/1.001" + bin_name + ".modelvector"
        info_lcdm["params"][bin_value1]["value"] = 1.001
        info_lcdm["params"][bin_value2]["value"] = 1.001
        updated_info, evaluate = run(info_lcdm, force=True)
        info_lcdm["params"][bin_value1]["value"] = 1.
        info_lcdm["params"][bin_value2]["value"] = 1.

for i in range(zbins - 1):
    for j in range(kbins - 1):
        bin_name = "zbin" + str(i) + "kbin" + str(j)
        bin_value1 = "zvalue" + str(i)
        bin_value2 = "kvalue" + str(j)
        info_lcdm['likelihood']['des_y3.des_cosmic_shear']['print_datavector_file'] = "./projects/des_y3/data/DES25_oneXi_intAc2_z0to1_k0.025to0.8_Data/0.999" + bin_name + ".modelvector"
        info_lcdm["params"][bin_value1]["value"] = 0.999
        info_lcdm["params"][bin_value2]["value"] = 0.999
        updated_info, evaluate = run(info_lcdm, force=True)
        info_lcdm["params"][bin_value1]["value"] = 1.
        info_lcdm["params"][bin_value2]["value"] = 1.


#for i in range(zbins - 1):
#    bin_name = "zbin" + str(i)
#    bin_value = "zvalue" + str(i)
#    info_lcdm['likelihood']['lsst_y1.lsst_cosmic_shear']['print_datavector_file'] = "./projects/lsst_y1/data/tenzData/1.001" + bin_name + ".modelvector"
#    info_lcdm["params"][bin_value]["value"] = 1.001
#    updated_info, evaluate = run(info_lcdm, force=True)
#    info_lcdm["params"][bin_value]["value"] = 1.

#for i in range(zbins - 1):
#    bin_name = "zbin" + str(i)
#    bin_value = "zvalue" + str(i)
#    info_lcdm['likelihood']['lsst_y1.lsst_cosmic_shear']['print_datavector_file'] = "./projects/lsst_y1/data/tenzData/0.999" + bin_name + ".modelvector"
#    info_lcdm["params"][bin_value]["value"] = 0.999
#    updated_info, evaluate = run(info_lcdm, force=True)
#    info_lcdm["params"][bin_value]["value"] = 1.

#for i in range(kbins - 1):
#    bin_name = "kbin" + str(i)
#    bin_value = "kvalue" + str(i)
#    info_lcdm['likelihood']['lsst_y1.lsst_cosmic_shear']['print_datavector_file'] = "./projects/lsst_y1/data/one8z7kData/1.002" + bin_name + ".modelvector"
#    info_lcdm["params"][bin_value]["value"] = 1.002
#    updated_info, evaluate = run(info_lcdm, force=True)
#    info_lcdm["params"][bin_value]["value"] = 1.

#for i in range(kbins - 1):
#    bin_name = "kbin" + str(i)
#    bin_value = "kvalue" + str(i)
#    info_lcdm['likelihood']['lsst_y1.lsst_cosmic_shear']['print_datavector_file'] = "./projects/lsst_y1/data/one8z7kData/0.998" + bin_name + ".modelvector"
#    info_lcdm["params"][bin_value]["value"] = 0.998
#    updated_info, evaluate = run(info_lcdm, force=True)
#    info_lcdm["params"][bin_value]["value"] = 1.
