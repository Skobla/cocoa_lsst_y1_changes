import numpy as np
import os, sys, time
from io import StringIO
from cobaya.yaml import yaml_load_file
from cobaya.run import run
from cobaya.post import post
from getdist.mcsamples import MCSamplesFromCobaya

ggsplit_yaml_file   = "./projects/lsst_y1/EXAMPLE_EVALUATE1.yaml"

info_lcdm = yaml_load_file("./projects/lsst_y1/EXAMPLE_EVALUATE1.yaml")

kbins = 6
zbins = 6

for i in range(zbins - 1):
    bin_name = "zbin" + str(i)
    bin_value = "zvalue" + str(i)
    info_lcdm['likelihood']['lsst_y1.lsst_cosmic_shear']['print_datavector_file'] = "./projects/lsst_y1/data/Gdir/tmp_G1.01N" + bin_name + ".modelvector"
    info_lcdm["params"][bin_value]["value"] = 1.01
    updated_info, evaluate = run(info_lcdm, force=True)

for i in range(zbins - 1):
    bin_name = "zbin" + str(i)
    bin_value = "zvalue" + str(i)
    info_lcdm['likelihood']['lsst_y1.lsst_cosmic_shear']['print_datavector_file'] = "./projects/lsst_y1/data/Gdir/tmp_G0.99N" + bin_name + ".modelvector"
    info_lcdm["params"][bin_value]["value"] = 0.99
    updated_info, evaluate = run(info_lcdm, force=True)

for i in range(kbins - 1):
    bin_name = "kbin" + str(i)
    bin_value = "kvalue" + str(i)
    info_lcdm['likelihood']['lsst_y1.lsst_cosmic_shear']['print_datavector_file'] = "./projects/lsst_y1/data/Gdir/tmp_G1.01N" + bin_name + ".modelvector"
    info_lcdm["params"][bin_value]["value"] = 1.01
    updated_info, evaluate = run(info_lcdm, force=True)

for i in range(kbins - 1):
    bin_name = "kbin" + str(i)
    bin_value = "kvalue" + str(i)
    info_lcdm['likelihood']['lsst_y1.lsst_cosmic_shear']['print_datavector_file'] = "./projects/lsst_y1/data/Gdir/tmp_G0.99N" + bin_name + ".modelvector"
    info_lcdm["params"][bin_value]["value"] = 0.99
    updated_info, evaluate = run(info_lcdm, force=True)
