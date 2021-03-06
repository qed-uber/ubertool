from __future__ import division
from functools import wraps
import pandas as pd
from base.uber_model import UberModel, ModelSharedInputs
from .trex_functions import TrexFunctions
import time


def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print("trex_model_rest.py@timefn: " + fn.func_name + " took " + "{:.6f}".format(t2 - t1) + " seconds")
        return result
    return measure_time


class TrexInputs(ModelSharedInputs):
    """
    Required inputs class for Trex.
    """

    def __init__(self):
        """Class representing the inputs for Trex"""
        super(TrexInputs, self).__init__()
        # Inputs: Assign object attribute variables from the input Pandas DataFrame
        self.use = pd.Series([], dtype="object")
        self.formu_name = pd.Series([], dtype="object")
        self.percent_act_ing = pd.Series([], dtype="float")
        self.application_type = pd.Series([], dtype="object")
        self.seed_treatment_formulation_name = pd.Series([], dtype="object")
        self.seed_crop = pd.Series([], dtype="object")
        self.max_seed_rate = pd.Series([], dtype="float") # maximum seeding rate per use
        # ??what is the seed_crop_v,
        # not listed in the crosswalk table, not referenced in code
        #self.seed_crop_v = pd.Series([], dtype="float")
        self.row_spacing = pd.Series([], dtype="float")
        self.bandwidth = pd.Series([], dtype="float")
        self.percent_incorp = pd.Series([], dtype="float")
        self.density = pd.Series([], dtype="float")
        self.foliar_diss_hlife = pd.Series([], dtype="float")
        self.num_apps = pd.Series([], dtype="int") # number of applications per model simulation run
                # could calculate self.num_apps = len(self.app_rates) # should at least check if user supplied value is consistent
        self.app_rates = pd.Series([], dtype="object") #Series of lists, each list contains app_rates of a model simulation run
        self.day_out = pd.Series([], dtype="object") #Series of lists, each list contains day #'s of applications within a model simulaiton run
        self.mineau_sca_fact = pd.Series([], dtype="float")

        self.ld50_bird = pd.Series([], dtype="float")
        self.lc50_bird = pd.Series([], dtype="float")
        self.noaec_bird = pd.Series([], dtype="float")
        self.noael_bird = pd.Series([], dtype="float")
        self.aw_bird_sm = pd.Series([], dtype="float")  # body weight of assessed bird (small)
        self.aw_bird_md = pd.Series([], dtype="float")  # body weight of assessed bird (medium)
        self.aw_bird_lg = pd.Series([], dtype="float")  # body weight of assessed bird (large)
        self.tw_bird_ld50 = pd.Series([], dtype="float")
        self.tw_bird_lc50 = pd.Series([], dtype="float")
        self.tw_bird_noaec = pd.Series([], dtype="float")
        self.tw_bird_noael = pd.Series([], dtype="float")

        self.species_of_the_tested_bird_avian_ld50 = pd.Series([], dtype="object")
        self.species_of_the_tested_bird_avian_lc50 = pd.Series([], dtype="object")
        self.species_of_the_tested_bird_avian_noaec = pd.Series([], dtype="object")
        self.species_of_the_tested_bird_avian_noael = pd.Series([], dtype="object")

        self.ld50_mamm = pd.Series([], dtype="float")
        self.lc50_mamm = pd.Series([], dtype="float")
        self.noaec_mamm = pd.Series([], dtype="float")
        self.noael_mamm = pd.Series([], dtype="float")
        self.aw_mamm_sm = pd.Series([], dtype="float")  # body weight of assessed mammal (small)
        self.aw_mamm_md = pd.Series([], dtype="float")  # body weight of assessed mammal (medium)
        self.aw_mamm_lg = pd.Series([], dtype="float")  # body weight of assessed mammal (large)
        self.tw_mamm = pd.Series([], dtype="float")     # body weight of tested mammal


class TrexOutputs(object):
    """
    Output class for Trex.
    """

    def __init__(self):
        """Class representing the outputs for Trex"""
        super(TrexOutputs, self).__init__()

        # ??do the following 15 variables need to be included in the crosswalk table
        # initial concentrations for different food types
        self.out_c_0_sg = pd.Series([], dtype='float', name="out_c_0_sg")  # short grass
        self.out_c_0_tg = pd.Series([], dtype='float', name="out_c_0_tg")  # tall grass
        self.out_c_0_blp = pd.Series([], dtype='float', name="out_c_0_blp")  # broad-leafed plants
        self.out_c_0_fp = pd.Series([], dtype='float', name="out_c_0_fp")  # fruits/pods
        self.out_c_0_arthro = pd.Series([], dtype='float', name="out_c_0_arthro")  # arthropods

        # mean concentration estimate based on first application rate
        self.out_c_mean_sg = pd.Series([], dtype='float', name="out_c_mean_sg")  # short grass
        self.out_c_mean_tg = pd.Series([], dtype='float', name="out_c_mean_tg")  # tall grass
        self.out_c_mean_blp = pd.Series([], dtype='float', name="out_c_mean_blp")  # broad-leafed plants
        self.out_c_mean_fp = pd.Series([], dtype='float', name="out_c_mean_fp")  # fruits/pods
        self.out_c_mean_arthro = pd.Series([], dtype='float', name="out_c_mean_arthro")  # arthropods

        # TODO: Add these back in after deciding how to handle the numpy arrays
        # time series of concentrations per food source
        # self.out_c_ts_sg = pd.Series([], dtype='float', name="out_c_ts_sg")  # short grass
        # self.out_c_ts_tg = pd.Series([], dtype='float', name="out_c_ts_tg")  # tall grass
        # self.out_c_ts_blp = pd.Series([], dtype='float', name="out_c_ts_blp")  # broad-leafed plants
        # self.out_c_ts_fp = pd.Series([], dtype='float', name="out_c_ts_fp")  # fruits/pods
        # self.out_c_ts_arthro = pd.Series([], dtype='float', name="out_c_ts_arthro")  # arthropods

        # Table5
        self.out_sa_bird_1_s = pd.Series([], dtype='float', name="out_sa_bird_1_s")
        self.out_sa_bird_2_s = pd.Series([], dtype='float', name="out_sa_bird_2_s")
        self.out_sc_bird_s = pd.Series([], dtype='float', name="out_sc_bird_s")
        self.out_sa_mamm_1_s = pd.Series([], dtype='float', name="out_sa_mamm_1_s")
        self.out_sa_mamm_2_s = pd.Series([], dtype='float', name="out_sa_mamm_2_s")
        self.out_sc_mamm_s = pd.Series([], dtype='float', name="out_sc_mamm_s")

        self.out_sa_bird_1_m = pd.Series([], dtype='float', name="out_sa_bird_1_m")
        self.out_sa_bird_2_m = pd.Series([], dtype='float', name="out_sa_bird_2_m")
        self.out_sc_bird_m = pd.Series([], dtype='float', name="out_sc_bird_m")
        self.out_sa_mamm_1_m = pd.Series([], dtype='float', name="out_sa_mamm_1_m")
        self.out_sa_mamm_2_m = pd.Series([], dtype='float', name="out_sa_mamm_2_m")
        self.out_sc_mamm_m = pd.Series([], dtype='float', name="out_sc_mamm_m")

        self.out_sa_bird_1_l = pd.Series([], dtype='float', name="out_sa_bird_1_l")
        self.out_sa_bird_2_l = pd.Series([], dtype='float', name="out_sa_bird_2_l")
        self.out_sc_bird_l = pd.Series([], dtype='float', name="out_sc_bird_l")
        self.out_sa_mamm_1_l = pd.Series([], dtype='float', name="out_sa_mamm_1_l")
        self.out_sa_mamm_2_l = pd.Series([], dtype='float', name="out_sa_mamm_2_l")
        self.out_sc_mamm_l = pd.Series([], dtype='float', name="out_sc_mamm_l")

        # Table 6
        self.out_eec_diet_sg = pd.Series([], dtype='float', name="out_eec_diet_sg")
        self.out_eec_diet_tg = pd.Series([], dtype='float', name="out_eec_diet_tg")
        self.out_eec_diet_bp = pd.Series([], dtype='float', name="out_eec_diet_bp")
        self.out_eec_diet_fr = pd.Series([], dtype='float', name="out_eec_diet_fr")
        self.out_eec_diet_ar = pd.Series([], dtype='float', name="out_eec_diet_ar")

        # Table 7
        self.out_eec_dose_bird_sg_sm = pd.Series([], dtype='float', name="out_eec_dose_bird_sg_sm")
        self.out_eec_dose_bird_sg_md = pd.Series([], dtype='float', name="out_eec_dose_bird_sg_md")
        self.out_eec_dose_bird_sg_lg = pd.Series([], dtype='float', name="out_eec_dose_bird_sg_lg")
        self.out_eec_dose_bird_tg_sm = pd.Series([], dtype='float', name="out_eec_dose_bird_tg_sm")
        self.out_eec_dose_bird_tg_md = pd.Series([], dtype='float', name="out_eec_dose_bird_tg_md")
        self.out_eec_dose_bird_tg_lg = pd.Series([], dtype='float', name="out_eec_dose_bird_tg_lg")
        self.out_eec_dose_bird_bp_sm = pd.Series([], dtype='float', name="out_eec_dose_bird_bp_sm")
        self.out_eec_dose_bird_bp_md = pd.Series([], dtype='float', name="out_eec_dose_bird_bp_md")
        self.out_eec_dose_bird_bp_lg = pd.Series([], dtype='float', name="out_eec_dose_bird_bp_lg")
        self.out_eec_dose_bird_fp_sm = pd.Series([], dtype='float', name="out_eec_dose_bird_fp_sm")
        self.out_eec_dose_bird_fp_md = pd.Series([], dtype='float', name="out_eec_dose_bird_fp_md")
        self.out_eec_dose_bird_fp_lg = pd.Series([], dtype='float', name="out_eec_dose_bird_fp_lg")
        self.out_eec_dose_bird_ar_sm = pd.Series([], dtype='float', name="out_eec_dose_bird_ar_sm")
        self.out_eec_dose_bird_ar_md = pd.Series([], dtype='float', name="out_eec_dose_bird_ar_md")
        self.out_eec_dose_bird_ar_lg = pd.Series([], dtype='float', name="out_eec_dose_bird_ar_lg")
        self.out_eec_dose_bird_se_sm = pd.Series([], dtype='float', name="out_eec_dose_bird_se_sm")
        self.out_eec_dose_bird_se_md = pd.Series([], dtype='float', name="out_eec_dose_bird_se_md")
        self.out_eec_dose_bird_se_lg = pd.Series([], dtype='float', name="out_eec_dose_bird_se_lg")

        # Table 7_add
        self.out_arq_bird_sg_sm = pd.Series([], dtype='float', name="out_arq_bird_sg_sm")
        self.out_arq_bird_sg_md = pd.Series([], dtype='float', name="out_arq_bird_sg_md")
        self.out_arq_bird_sg_lg = pd.Series([], dtype='float', name="out_arq_bird_sg_lg")
        self.out_arq_bird_tg_sm = pd.Series([], dtype='float', name="out_arq_bird_tg_sm")
        self.out_arq_bird_tg_md = pd.Series([], dtype='float', name="out_arq_bird_tg_md")
        self.out_arq_bird_tg_lg = pd.Series([], dtype='float', name="out_arq_bird_tg_lg")
        self.out_arq_bird_bp_sm = pd.Series([], dtype='float', name="out_arq_bird_bp_sm")
        self.out_arq_bird_bp_md = pd.Series([], dtype='float', name="out_arq_bird_bp_md")
        self.out_arq_bird_bp_lg = pd.Series([], dtype='float', name="out_arq_bird_bp_lg")
        self.out_arq_bird_fp_sm = pd.Series([], dtype='float', name="out_arq_bird_fp_sm")
        self.out_arq_bird_fp_md = pd.Series([], dtype='float', name="out_arq_bird_fp_md")
        self.out_arq_bird_fp_lg = pd.Series([], dtype='float', name="out_arq_bird_fp_lg")
        self.out_arq_bird_ar_sm = pd.Series([], dtype='float', name="out_arq_bird_ar_sm")
        self.out_arq_bird_ar_md = pd.Series([], dtype='float', name="out_arq_bird_ar_md")
        self.out_arq_bird_ar_lg = pd.Series([], dtype='float', name="out_arq_bird_ar_lg")
        self.out_arq_bird_se_sm = pd.Series([], dtype='float', name="out_arq_bird_se_sm")
        self.out_arq_bird_se_md = pd.Series([], dtype='float', name="out_arq_bird_se_md")
        self.out_arq_bird_se_lg = pd.Series([], dtype='float', name="out_arq_bird_se_lg")

        # Table 8
        self.out_arq_diet_bird_sg_a = pd.Series([], dtype='float', name="out_arq_diet_bird_sg_a")
        self.out_arq_diet_bird_sg_c = pd.Series([], dtype='float', name="out_arq_diet_bird_sg_c")
        self.out_arq_diet_bird_tg_a = pd.Series([], dtype='float', name="out_arq_diet_bird_tg_a")
        self.out_arq_diet_bird_tg_c = pd.Series([], dtype='float', name="out_arq_diet_bird_tg_c")
        self.out_arq_diet_bird_bp_a = pd.Series([], dtype='float', name="out_arq_diet_bird_bp_a")
        self.out_arq_diet_bird_bp_c = pd.Series([], dtype='float', name="out_arq_diet_bird_bp_c")
        self.out_arq_diet_bird_fp_a = pd.Series([], dtype='float', name="out_arq_diet_bird_fp_a")
        self.out_arq_diet_bird_fp_c = pd.Series([], dtype='float', name="out_arq_diet_bird_fp_c")
        self.out_arq_diet_bird_ar_a = pd.Series([], dtype='float', name="out_arq_diet_bird_ar_a")
        self.out_arq_diet_bird_ar_c = pd.Series([], dtype='float', name="out_arq_diet_bird_ar_c")

        # Table 9
        self.out_eec_dose_mamm_sg_sm = pd.Series([], dtype='float', name="out_eec_dose_mamm_sg_sm")
        self.out_eec_dose_mamm_sg_md = pd.Series([], dtype='float', name="out_eec_dose_mamm_sg_md")
        self.out_eec_dose_mamm_sg_lg = pd.Series([], dtype='float', name="out_eec_dose_mamm_sg_lg")
        self.out_eec_dose_mamm_tg_sm = pd.Series([], dtype='float', name="out_eec_dose_mamm_tg_sm")
        self.out_eec_dose_mamm_tg_md = pd.Series([], dtype='float', name="out_eec_dose_mamm_tg_md")
        self.out_eec_dose_mamm_tg_lg = pd.Series([], dtype='float', name="out_eec_dose_mamm_tg_lg")
        self.out_eec_dose_mamm_bp_sm = pd.Series([], dtype='float', name="out_eec_dose_mamm_bp_sm")
        self.out_eec_dose_mamm_bp_md = pd.Series([], dtype='float', name="out_eec_dose_mamm_bp_md")
        self.out_eec_dose_mamm_bp_lg = pd.Series([], dtype='float', name="out_eec_dose_mamm_bp_lg")
        self.out_eec_dose_mamm_fp_sm = pd.Series([], dtype='float', name="out_eec_dose_mamm_fp_sm")
        self.out_eec_dose_mamm_fp_md = pd.Series([], dtype='float', name="out_eec_dose_mamm_fp_md")
        self.out_eec_dose_mamm_fp_lg = pd.Series([], dtype='float', name="out_eec_dose_mamm_fp_lg")
        self.out_eec_dose_mamm_ar_sm = pd.Series([], dtype='float', name="out_eec_dose_mamm_ar_sm")
        self.out_eec_dose_mamm_ar_md = pd.Series([], dtype='float', name="out_eec_dose_mamm_ar_md")
        self.out_eec_dose_mamm_ar_lg = pd.Series([], dtype='float', name="out_eec_dose_mamm_ar_lg")
        self.out_eec_dose_mamm_se_sm = pd.Series([], dtype='float', name="out_eec_dose_mamm_se_sm")
        self.out_eec_dose_mamm_se_md = pd.Series([], dtype='float', name="out_eec_dose_mamm_se_md")
        self.out_eec_dose_mamm_se_lg = pd.Series([], dtype='float', name="out_eec_dose_mamm_se_lg")

        # Table 10out_
        self.out_arq_dose_mamm_sg_sm = pd.Series([], dtype='float', name="out_arq_dose_mamm_sg_sm")
        self.out_crq_dose_mamm_sg_sm = pd.Series([], dtype='float', name="out_crq_dose_mamm_sg_sm")
        self.out_arq_dose_mamm_sg_md = pd.Series([], dtype='float', name="out_arq_dose_mamm_sg_md")
        self.out_crq_dose_mamm_sg_md = pd.Series([], dtype='float', name="out_crq_dose_mamm_sg_md")
        self.out_arq_dose_mamm_sg_lg = pd.Series([], dtype='float', name="out_arq_dose_mamm_sg_lg")
        self.out_crq_dose_mamm_sg_lg = pd.Series([], dtype='float', name="out_crq_dose_mamm_sg_lg")

        self.out_arq_dose_mamm_tg_sm = pd.Series([], dtype='float', name="out_arq_dose_mamm_tg_sm")
        self.out_crq_dose_mamm_tg_sm = pd.Series([], dtype='float', name="out_crq_dose_mamm_tg_sm")
        self.out_arq_dose_mamm_tg_md = pd.Series([], dtype='float', name="out_arq_dose_mamm_tg_md")
        self.out_crq_dose_mamm_tg_md = pd.Series([], dtype='float', name="out_crq_dose_mamm_tg_md")
        self.out_arq_dose_mamm_tg_lg = pd.Series([], dtype='float', name="out_arq_dose_mamm_tg_lg")
        self.out_crq_dose_mamm_tg_lg = pd.Series([], dtype='float', name="out_crq_dose_mamm_tg_lg")
        self.out_arq_dose_mamm_bp_sm = pd.Series([], dtype='float', name="out_arq_dose_mamm_bp_sm")
        self.out_crq_dose_mamm_bp_sm = pd.Series([], dtype='float', name="out_crq_dose_mamm_bp_sm")
        self.out_arq_dose_mamm_bp_md = pd.Series([], dtype='float', name="out_arq_dose_mamm_bp_md")
        self.out_crq_dose_mamm_bp_md = pd.Series([], dtype='float', name="out_crq_dose_mamm_bp_md")
        self.out_arq_dose_mamm_bp_lg = pd.Series([], dtype='float', name="out_arq_dose_mamm_bp_lg")
        self.out_crq_dose_mamm_bp_lg = pd.Series([], dtype='float', name="out_crq_dose_mamm_bp_lg")

        self.out_arq_dose_mamm_fp_sm = pd.Series([], dtype='float', name="out_arq_dose_mamm_fp_sm")
        self.out_crq_dose_mamm_fp_sm = pd.Series([], dtype='float', name="out_crq_dose_mamm_fp_sm")
        self.out_arq_dose_mamm_fp_md = pd.Series([], dtype='float', name="out_arq_dose_mamm_fp_md")
        self.out_crq_dose_mamm_fp_md = pd.Series([], dtype='float', name="out_crq_dose_mamm_fp_md")
        self.out_arq_dose_mamm_fp_lg = pd.Series([], dtype='float', name="out_arq_dose_mamm_fp_lg")
        self.out_crq_dose_mamm_fp_lg = pd.Series([], dtype='float', name="out_crq_dose_mamm_fp_lg")

        self.out_arq_dose_mamm_ar_sm = pd.Series([], dtype='float', name="out_arq_dose_mamm_ar_sm")
        self.out_crq_dose_mamm_ar_sm = pd.Series([], dtype='float', name="out_crq_dose_mamm_ar_sm")
        self.out_arq_dose_mamm_ar_md = pd.Series([], dtype='float', name="out_arq_dose_mamm_ar_md")
        self.out_crq_dose_mamm_ar_md = pd.Series([], dtype='float', name="out_crq_dose_mamm_ar_md")
        self.out_arq_dose_mamm_ar_lg = pd.Series([], dtype='float', name="out_arq_dose_mamm_ar_lg")
        self.out_crq_dose_mamm_ar_lg = pd.Series([], dtype='float', name="out_crq_dose_mamm_ar_lg")

        self.out_arq_dose_mamm_se_sm = pd.Series([], dtype='float', name="out_arq_dose_mamm_se_sm")
        self.out_crq_dose_mamm_se_sm = pd.Series([], dtype='float', name="out_crq_dose_mamm_se_sm")
        self.out_arq_dose_mamm_se_md = pd.Series([], dtype='float', name="out_arq_dose_mamm_se_md")
        self.out_crq_dose_mamm_se_md = pd.Series([], dtype='float', name="out_crq_dose_mamm_se_md")
        self.out_arq_dose_mamm_se_lg = pd.Series([], dtype='float', name="out_arq_dose_mamm_se_lg")
        self.out_crq_dose_mamm_se_lg = pd.Series([], dtype='float', name="out_crq_dose_mamm_se_lg")

        # Table 11
        self.out_arq_diet_mamm_sg = pd.Series([], dtype='float', name="out_arq_diet_mamm_sg")
        self.out_arq_diet_mamm_tg = pd.Series([], dtype='float', name="out_arq_diet_mamm_tg")
        self.out_arq_diet_mamm_bp = pd.Series([], dtype='float', name="out_arq_diet_mamm_bp")
        self.out_arq_diet_mamm_fp = pd.Series([], dtype='float', name="out_arq_diet_mamm_fp")
        self.out_arq_diet_mamm_ar = pd.Series([], dtype='float', name="out_arq_diet_mamm_ar")

        self.out_crq_diet_mamm_sg = pd.Series([], dtype='float', name="out_crq_diet_mamm_sg")
        self.out_crq_diet_mamm_tg = pd.Series([], dtype='float', name="out_crq_diet_mamm_tg")
        self.out_crq_diet_mamm_bp = pd.Series([], dtype='float', name="out_crq_diet_mamm_bp")
        self.out_crq_diet_mamm_fp = pd.Series([], dtype='float', name="out_crq_diet_mamm_fp")
        self.out_crq_diet_mamm_ar = pd.Series([], dtype='float', name="out_crq_diet_mamm_ar")

        # Table12
        self.out_ld50_rg_bird_sm = pd.Series([], dtype='float', name="out_ld50_rg_bird_sm")
        self.out_ld50_rg_mamm_sm = pd.Series([], dtype='float', name="out_ld50_rg_mamm_sm")
        self.out_ld50_rg_bird_md = pd.Series([], dtype='float', name="out_ld50_rg_bird_md")
        self.out_ld50_rg_mamm_md = pd.Series([], dtype='float', name="out_ld50_rg_mamm_md")
        self.out_ld50_rg_bird_lg = pd.Series([], dtype='float', name="out_ld50_rg_bird_lg")
        self.out_ld50_rg_mamm_lg = pd.Series([], dtype='float', name="out_ld50_rg_mamm_lg")

        # Table13
        self.out_ld50_rl_bird_sm = pd.Series([], dtype='float', name="out_ld50_rl_bird_sm")
        self.out_ld50_rl_mamm_sm = pd.Series([], dtype='float', name="out_ld50_rl_mamm_sm")
        self.out_ld50_rl_bird_md = pd.Series([], dtype='float', name="out_ld50_rl_bird_md")
        self.out_ld50_rl_mamm_md = pd.Series([], dtype='float', name="out_ld50_rl_mamm_md")
        self.out_ld50_rl_bird_lg = pd.Series([], dtype='float', name="out_ld50_rl_bird_lg")
        self.out_ld50_rl_mamm_lg = pd.Series([], dtype='float', name="out_ld50_rl_mamm_lg")

        # Table14
        self.out_ld50_bg_bird_sm = pd.Series([], dtype='float', name="out_ld50_bg_bird_sm")
        self.out_ld50_bg_mamm_sm = pd.Series([], dtype='float', name="out_ld50_bg_mamm_sm")
        self.out_ld50_bg_bird_md = pd.Series([], dtype='float', name="out_ld50_bg_bird_md")
        self.out_ld50_bg_mamm_md = pd.Series([], dtype='float', name="out_ld50_bg_mamm_md")
        self.out_ld50_bg_bird_lg = pd.Series([], dtype='float', name="out_ld50_bg_bird_lg")
        self.out_ld50_bg_mamm_lg = pd.Series([], dtype='float', name="out_ld50_bg_mamm_lg")

        # Table15
        self.out_ld50_bl_bird_sm = pd.Series([], dtype='float', name="out_ld50_bl_bird_sm")
        self.out_ld50_bl_mamm_sm = pd.Series([], dtype='float', name="out_ld50_bl_mamm_sm")
        self.out_ld50_bl_bird_md = pd.Series([], dtype='float', name="out_ld50_bl_bird_md")
        self.out_ld50_bl_mamm_md = pd.Series([], dtype='float', name="out_ld50_bl_mamm_md")
        self.out_ld50_bl_bird_lg = pd.Series([], dtype='float', name="out_ld50_bl_bird_lg")
        self.out_ld50_bl_mamm_lg = pd.Series([], dtype='float', name="out_ld50_bl_mamm_lg")


class Trex(UberModel, TrexInputs, TrexOutputs, TrexFunctions):
    """
    Estimate exposure concentrations and risk quotients for birds and mammals.
    """

    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the Trex model and containing all its methods"""
        super(Trex, self).__init__()
        self.pd_obj = pd_obj
        self.pd_obj_exp = pd_obj_exp
        self.pd_obj_out = None

    def execute_model(self):
        """
        Callable to execute the running of the model:
            1) Populate input parameters
            2) Create output DataFrame to hold the model outputs
            3) Run the model's methods to generate outputs
            4) Fill the output DataFrame with the generated model outputs
        """
        self.populate_inputs(self.pd_obj)
        self.pd_obj_out = self.populate_outputs()
        self.run_methods()
        self.fill_output_dataframe()

    # Begin model methods
#    @timefn
    def run_methods(self):

        # convert user supplied app_rates/day_out from series of lists as
        # strings to series of lists as floats/integers
        self.app_rates = self.convert_strlist_float(self.app_rates)
        print(self.app_rates)
        self.day_out = self.convert_strlist_int(self.day_out)
        print(self.day_out)

        # Define constants and perform units conversions on necessary raw inputs
        self.set_global_constants()
        self.frac_incorp = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.frac_act_ing = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.frac_act_ing = self.percent_to_frac(self.percent_act_ing)
        self.frac_incorp = self.percent_to_frac(self.percent_incorp)
        self.bandwidth = self.inches_to_feet(self.bandwidth)
        self.row_spacing = self.inches_to_feet(self.row_spacing)

        # extract first day and maximum application rates from each model simulation run
        self.app_rate_parsing()

        # initial concentrations for different food types
        # need to pass in first_app_rate[] because other functions calculate c_initial per timestep application rate
        for i in range(len(self.first_app_rate)):
            self.out_c_0_sg[i] = self.conc_initial(i, self.first_app_rate[i], self.food_multiplier_init_sg)
            self.out_c_0_tg[i] = self.conc_initial(i, self.first_app_rate[i], self.food_multiplier_init_tg)
            self.out_c_0_blp[i] = self.conc_initial(i, self.first_app_rate[i], self.food_multiplier_init_blp)
            self.out_c_0_fp[i] = self.conc_initial(i, self.first_app_rate[i], self.food_multiplier_init_fp)
            self.out_c_0_arthro[i] = self.conc_initial(i, self.first_app_rate[i], self.food_multiplier_init_arthro)

            # mean concentration estimates based on first application rate (per type of foodsource)
            self.out_c_mean_sg[i] = self.conc_initial(i, self.first_app_rate[i], self.food_multiplier_mean_sg)
            self.out_c_mean_tg[i] = self.conc_initial(i, self.first_app_rate[i], self.food_multiplier_mean_tg)
            self.out_c_mean_blp[i] = self.conc_initial(i, self.first_app_rate[i], self.food_multiplier_mean_blp)
            self.out_c_mean_fp[i] = self.conc_initial(i, self.first_app_rate[i], self.food_multiplier_mean_fp)
            self.out_c_mean_arthro[i] = self.conc_initial(i, self.first_app_rate[i], self.food_multiplier_mean_arthro)

        # time series of daily concentrations (one year + one week) related to each food source
        self.out_c_ts_sg = self.eec_diet_timeseries(self.food_multiplier_init_sg)  # short grass
        self.out_c_ts_tg = self.eec_diet_timeseries(self.food_multiplier_init_tg)  # tall grass
        self.out_c_ts_blp = self.eec_diet_timeseries(self.food_multiplier_init_blp)  # broad-leafed plants
        self.out_c_ts_fp = self.eec_diet_timeseries(self.food_multiplier_init_fp)  # fruits/pods
        self.out_c_ts_arthro = self.eec_diet_timeseries(self.food_multiplier_init_arthro)  # arthropods

        # Table5
        self.out_sa_bird_1_s = self.sa_bird_1("small") # Seed treatment acute RQ for small birds method 1
        self.out_sa_bird_2_s = self.sa_bird_2("small") # Seed treatment acute RQ for small birds method 2
        self.out_sc_bird_s = self.sc_bird()            # Seed treatment chronic RQ for small birds
        self.out_sa_mamm_1_s = self.sa_mamm_1("small") # Seed treatment acute RQ for small mammals method 1
        self.out_sa_mamm_2_s = self.sa_mamm_2("small") # Seed treatment acute RQ for small mammals method 2
        self.out_sc_mamm_s = self.sc_mamm("small")     # Seed treatment chronic RQ for small mammals

        self.out_sa_bird_1_m = self.sa_bird_1("medium") # Seed treatment acute RQ for medium birds method 1
        self.out_sa_bird_2_m = self.sa_bird_2("medium") # Seed treatment acute RQ for medium birds method 2
        self.out_sc_bird_m = self.sc_bird()             # Seed treatment chronic RQ for medium birds
        self.out_sa_mamm_1_m = self.sa_mamm_1("medium") # Seed treatment acute RQ for medium mammals method 1
        self.out_sa_mamm_2_m = self.sa_mamm_2("medium") # Seed treatment acute RQ for medium mammals method 2
        self.out_sc_mamm_m = self.sc_mamm("medium")     # Seed treatment chronic RQ for mammals mammals

        self.out_sa_bird_1_l = self.sa_bird_1("large") # Seed treatment acute RQ for large birds method 1
        self.out_sa_bird_2_l = self.sa_bird_2("large") # Seed treatment acute RQ for large birds method 2
        self.out_sc_bird_l = self.sc_bird()            # Seed treatment chronic RQ for large birds
        self.out_sa_mamm_1_l = self.sa_mamm_1("large") # Seed treatment acute RQ for large mammals method 1
        self.out_sa_mamm_2_l = self.sa_mamm_2("large") # Seed treatment acute RQ for large mammals method 2
        self.out_sc_mamm_l = self.sc_mamm("large")     # Seed treatment chronic RQ for large mammals

        # Table 6 (maximum daily concentrations occurring during year of applications per food source)
        self.out_eec_diet_sg = self.eec_diet_max(self.food_multiplier_init_sg)
        self.out_eec_diet_tg = self.eec_diet_max(self.food_multiplier_init_tg)
        self.out_eec_diet_bp = self.eec_diet_max(self.food_multiplier_init_blp)
        self.out_eec_diet_fr = self.eec_diet_max(self.food_multiplier_init_fp)
        self.out_eec_diet_ar = self.eec_diet_max(self.food_multiplier_init_arthro)

        # Table 7 (Dose based EECs for birds per food source and size of bird)
        self.out_eec_dose_bird_sg_sm = self.eec_dose_bird(self.aw_bird_sm, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_eec_dose_bird_sg_md = self.eec_dose_bird(self.aw_bird_md, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_eec_dose_bird_sg_lg = self.eec_dose_bird(self.aw_bird_lg, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_eec_dose_bird_tg_sm = self.eec_dose_bird(self.aw_bird_sm, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_eec_dose_bird_tg_md = self.eec_dose_bird(self.aw_bird_md, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_eec_dose_bird_tg_lg = self.eec_dose_bird(self.aw_bird_lg, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_eec_dose_bird_bp_sm = self.eec_dose_bird(self.aw_bird_sm, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_eec_dose_bird_bp_md = self.eec_dose_bird(self.aw_bird_md, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_eec_dose_bird_bp_lg = self.eec_dose_bird(self.aw_bird_lg, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_eec_dose_bird_fp_sm = self.eec_dose_bird(self.aw_bird_sm, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_eec_dose_bird_fp_md = self.eec_dose_bird(self.aw_bird_md, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_eec_dose_bird_fp_lg = self.eec_dose_bird(self.aw_bird_lg, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_eec_dose_bird_ar_sm = self.eec_dose_bird(self.aw_bird_sm, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_eec_dose_bird_ar_md = self.eec_dose_bird(self.aw_bird_md, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_eec_dose_bird_ar_lg = self.eec_dose_bird(self.aw_bird_lg, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_eec_dose_bird_se_sm = self.eec_dose_bird(self.aw_bird_sm, self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_eec_dose_bird_se_md = self.eec_dose_bird(self.aw_bird_md, self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_eec_dose_bird_se_lg = self.eec_dose_bird(self.aw_bird_lg, self.mf_w_bird_1, self.food_multiplier_init_fp)

        # Table 7_add (Acute dose-based risk quotients for birds per food source and size of bird)
        self.out_arq_bird_sg_sm = self.arq_dose_bird(self.aw_bird_sm, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_arq_bird_sg_md = self.arq_dose_bird(self.aw_bird_md, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_arq_bird_sg_lg = self.arq_dose_bird(self.aw_bird_lg, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_arq_bird_tg_sm = self.arq_dose_bird(self.aw_bird_sm, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_arq_bird_tg_md = self.arq_dose_bird(self.aw_bird_md, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_arq_bird_tg_lg = self.arq_dose_bird(self.aw_bird_lg, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_arq_bird_bp_sm = self.arq_dose_bird(self.aw_bird_sm, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_arq_bird_bp_md = self.arq_dose_bird(self.aw_bird_md, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_arq_bird_bp_lg = self.arq_dose_bird(self.aw_bird_lg, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_arq_bird_fp_sm = self.arq_dose_bird(self.aw_bird_sm, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_arq_bird_fp_md = self.arq_dose_bird(self.aw_bird_md, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_arq_bird_fp_lg = self.arq_dose_bird(self.aw_bird_lg, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_arq_bird_ar_sm = self.arq_dose_bird(self.aw_bird_sm, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_arq_bird_ar_md = self.arq_dose_bird(self.aw_bird_md, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_arq_bird_ar_lg = self.arq_dose_bird(self.aw_bird_lg, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_arq_bird_se_sm = self.arq_dose_bird(self.aw_bird_sm, self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_arq_bird_se_md = self.arq_dose_bird(self.aw_bird_md, self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_arq_bird_se_lg = self.arq_dose_bird(self.aw_bird_lg, self.mf_w_bird_1, self.food_multiplier_init_fp)

        # Table 8 (Acute dietary-based risk quotients for birds per food source and size of bird)
        self.out_arq_diet_bird_sg_a = self.arq_diet_bird(self.food_multiplier_init_sg)
        self.out_arq_diet_bird_sg_c = self.crq_diet_bird(self.food_multiplier_init_sg)
        self.out_arq_diet_bird_tg_a = self.arq_diet_bird(self.food_multiplier_init_tg)
        self.out_arq_diet_bird_tg_c = self.crq_diet_bird(self.food_multiplier_init_tg)
        self.out_arq_diet_bird_bp_a = self.arq_diet_bird(self.food_multiplier_init_blp)
        self.out_arq_diet_bird_bp_c = self.crq_diet_bird(self.food_multiplier_init_blp)
        self.out_arq_diet_bird_fp_a = self.arq_diet_bird(self.food_multiplier_init_fp)
        self.out_arq_diet_bird_fp_c = self.crq_diet_bird(self.food_multiplier_init_fp)
        self.out_arq_diet_bird_ar_a = self.arq_diet_bird(self.food_multiplier_init_arthro)
        self.out_arq_diet_bird_ar_c = self.crq_diet_bird(self.food_multiplier_init_arthro)

        # Table 9 (Chronic dose-based risk quotients for mammals per food source and size of mammal)
        self.out_eec_dose_mamm_sg_sm = self.eec_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_eec_dose_mamm_sg_md = self.eec_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_eec_dose_mamm_sg_lg = self.eec_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_eec_dose_mamm_tg_sm = self.eec_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_eec_dose_mamm_tg_md = self.eec_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_eec_dose_mamm_tg_lg = self.eec_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_eec_dose_mamm_bp_sm = self.eec_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_eec_dose_mamm_bp_md = self.eec_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_eec_dose_mamm_bp_lg = self.eec_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_eec_dose_mamm_fp_sm = self.eec_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_eec_dose_mamm_fp_md = self.eec_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_eec_dose_mamm_fp_lg = self.eec_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_eec_dose_mamm_ar_sm = self.eec_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_eec_dose_mamm_ar_md = self.eec_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_eec_dose_mamm_ar_lg = self.eec_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_eec_dose_mamm_se_sm = self.eec_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_eec_dose_mamm_se_md = self.eec_dose_mamm(self.aw_mamm_md, self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_eec_dose_mamm_se_lg = self.eec_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_1, self.food_multiplier_init_fp)

        # Table 10 (Acute -arq- and chronic =crq- dose-based risk quotients for mammals per food source and size of mammal)
        self.out_arq_dose_mamm_sg_sm = self.arq_dose_mamm(self.aw_mamm_sm,self.mf_w_bird_2,self.food_multiplier_init_sg)
        self.out_crq_dose_mamm_sg_sm = self.crq_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2,self.food_multiplier_init_sg)
        self.out_arq_dose_mamm_sg_md = self.arq_dose_mamm(self.aw_mamm_md,self.mf_w_bird_2,self.food_multiplier_init_sg)
        self.out_crq_dose_mamm_sg_md = self.crq_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2,self.food_multiplier_init_sg)
        self.out_arq_dose_mamm_sg_lg = self.arq_dose_mamm(self.aw_mamm_lg,self.mf_w_bird_2,self.food_multiplier_init_sg)
        self.out_crq_dose_mamm_sg_lg = self.crq_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2,self.food_multiplier_init_sg)

        self.out_arq_dose_mamm_tg_sm = self.arq_dose_mamm(self.aw_mamm_sm,self.mf_w_bird_2,self.food_multiplier_init_tg)
        self.out_crq_dose_mamm_tg_sm = self.crq_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2,self.food_multiplier_init_tg)
        self.out_arq_dose_mamm_tg_md = self.arq_dose_mamm(self.aw_mamm_md,self.mf_w_bird_2,self.food_multiplier_init_tg)
        self.out_crq_dose_mamm_tg_md = self.crq_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2,self.food_multiplier_init_tg)
        self.out_arq_dose_mamm_tg_lg = self.arq_dose_mamm(self.aw_mamm_lg,self.mf_w_bird_2,self.food_multiplier_init_tg)
        self.out_crq_dose_mamm_tg_lg = self.crq_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2,self.food_multiplier_init_tg)

        self.out_arq_dose_mamm_bp_sm = self.arq_dose_mamm(self.aw_mamm_sm,self.mf_w_bird_2,self.food_multiplier_init_blp)
        self.out_crq_dose_mamm_bp_sm = self.crq_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2,self.food_multiplier_init_blp)
        self.out_arq_dose_mamm_bp_md = self.arq_dose_mamm(self.aw_mamm_md,self.mf_w_bird_2,self.food_multiplier_init_blp)
        self.out_crq_dose_mamm_bp_md = self.crq_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2,self.food_multiplier_init_blp)
        self.out_arq_dose_mamm_bp_lg = self.arq_dose_mamm(self.aw_mamm_lg,self.mf_w_bird_2,self.food_multiplier_init_blp)
        self.out_crq_dose_mamm_bp_lg = self.crq_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2,self.food_multiplier_init_blp)

        self.out_arq_dose_mamm_fp_sm = self.arq_dose_mamm(self.aw_mamm_sm,self.mf_w_bird_2,self.food_multiplier_init_fp)
        self.out_crq_dose_mamm_fp_sm = self.crq_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2,self.food_multiplier_init_fp)
        self.out_arq_dose_mamm_fp_md = self.arq_dose_mamm(self.aw_mamm_md,self.mf_w_bird_2,self.food_multiplier_init_fp)
        self.out_crq_dose_mamm_fp_md = self.crq_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2,self.food_multiplier_init_fp)
        self.out_arq_dose_mamm_fp_lg = self.arq_dose_mamm(self.aw_mamm_lg,self.mf_w_bird_2,self.food_multiplier_init_fp)
        self.out_crq_dose_mamm_fp_lg = self.crq_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2,self.food_multiplier_init_fp)

        self.out_arq_dose_mamm_ar_sm = self.arq_dose_mamm(self.aw_mamm_sm,self.mf_w_bird_2,self.food_multiplier_init_arthro)
        self.out_crq_dose_mamm_ar_sm = self.crq_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2,self.food_multiplier_init_arthro)
        self.out_arq_dose_mamm_ar_md = self.arq_dose_mamm(self.aw_mamm_md,self.mf_w_bird_2,self.food_multiplier_init_arthro)
        self.out_crq_dose_mamm_ar_md = self.crq_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2,self.food_multiplier_init_arthro)
        self.out_arq_dose_mamm_ar_lg = self.arq_dose_mamm(self.aw_mamm_lg,self.mf_w_bird_2,self.food_multiplier_init_arthro)
        self.out_crq_dose_mamm_ar_lg = self.crq_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2,self.food_multiplier_init_arthro)

        self.out_arq_dose_mamm_se_sm = self.arq_dose_mamm(self.aw_mamm_sm,self.mf_w_bird_1,self.food_multiplier_init_fp)
        self.out_crq_dose_mamm_se_sm = self.crq_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_1,self.food_multiplier_init_fp)
        self.out_arq_dose_mamm_se_md = self.arq_dose_mamm(self.aw_mamm_md,self.mf_w_bird_1,self.food_multiplier_init_fp)
        self.out_crq_dose_mamm_se_md = self.crq_dose_mamm(self.aw_mamm_md, self.mf_w_bird_1,self.food_multiplier_init_fp)
        self.out_arq_dose_mamm_se_lg = self.arq_dose_mamm(self.aw_mamm_lg,self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_crq_dose_mamm_se_lg = self.crq_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_1, self.food_multiplier_init_fp)

        # table 11 (Acute dietary-based risk quotients for mammals per food source)
        self.out_arq_diet_mamm_sg = self.arq_diet_mamm(self.food_multiplier_init_sg)
        self.out_arq_diet_mamm_tg = self.arq_diet_mamm(self.food_multiplier_init_tg)
        self.out_arq_diet_mamm_bp = self.arq_diet_mamm(self.food_multiplier_init_blp)
        self.out_arq_diet_mamm_fp = self.arq_diet_mamm(self.food_multiplier_init_fp)
        self.out_arq_diet_mamm_ar = self.arq_diet_mamm(self.food_multiplier_init_arthro)

        # (Chronic dietary-based risk quotients for mammals per food source)
        self.out_crq_diet_mamm_sg = self.crq_diet_mamm(self.food_multiplier_init_sg)
        self.out_crq_diet_mamm_tg = self.crq_diet_mamm(self.food_multiplier_init_tg)
        self.out_crq_diet_mamm_bp = self.crq_diet_mamm(self.food_multiplier_init_blp)
        self.out_crq_diet_mamm_fp = self.crq_diet_mamm(self.food_multiplier_init_fp)
        self.out_crq_diet_mamm_ar = self.crq_diet_mamm(self.food_multiplier_init_arthro)

        # Table12 (LD50ft-2 for row/band/in-furrow granular for birds and mammals per size)
        self.out_ld50_rg_bird_sm = self.ld50_rg_bird(self.aw_bird_sm)
        self.out_ld50_rg_mamm_sm = self.ld50_rg_mamm(self.aw_mamm_sm)
        self.out_ld50_rg_bird_md = self.ld50_rg_bird(self.aw_bird_md)
        self.out_ld50_rg_mamm_md = self.ld50_rg_mamm(self.aw_mamm_md)
        self.out_ld50_rg_bird_lg = self.ld50_rg_bird(self.aw_bird_lg)
        self.out_ld50_rg_mamm_lg = self.ld50_rg_mamm(self.aw_mamm_lg)

        # Table13 (LD50ft-2 for row/band/in-furrow liquid for birds and mammals per size)
        self.out_ld50_rl_bird_sm = self.ld50_rl_bird(self.aw_bird_sm)
        self.out_ld50_rl_mamm_sm = self.ld50_rl_mamm(self.aw_mamm_sm)
        self.out_ld50_rl_bird_md = self.ld50_rl_bird(self.aw_bird_md)
        self.out_ld50_rl_mamm_md = self.ld50_rl_mamm(self.aw_mamm_md)
        self.out_ld50_rl_bird_lg = self.ld50_rl_bird(self.aw_bird_lg)
        self.out_ld50_rl_mamm_lg = self.ld50_rl_mamm(self.aw_mamm_lg)

        # Table14 (LD50ft-2 for broadcast granular birds and mammals per size)
        self.out_ld50_bg_bird_sm = self.ld50_bg_bird(self.aw_bird_sm)
        self.out_ld50_bg_mamm_sm = self.ld50_bg_mamm(self.aw_mamm_sm)
        self.out_ld50_bg_bird_md = self.ld50_bg_bird(self.aw_bird_md)
        self.out_ld50_bg_mamm_md = self.ld50_bg_mamm(self.aw_mamm_md)
        self.out_ld50_bg_bird_lg = self.ld50_bg_bird(self.aw_bird_lg)
        self.out_ld50_bg_mamm_lg = self.ld50_bg_mamm(self.aw_mamm_lg)

        # Table15 (LD50ft-2 for broadcast liquid birds and mammals per size)
        self.out_ld50_bl_bird_sm = self.ld50_bl_bird(self.aw_bird_sm)
        self.out_ld50_bl_mamm_sm = self.ld50_bl_mamm(self.aw_mamm_sm)
        self.out_ld50_bl_bird_md = self.ld50_bl_bird(self.aw_bird_md)
        self.out_ld50_bl_mamm_md = self.ld50_bl_mamm(self.aw_mamm_md)
        self.out_ld50_bl_bird_lg = self.ld50_bl_bird(self.aw_bird_lg)
        self.out_ld50_bl_mamm_lg = self.ld50_bl_mamm(self.aw_mamm_lg)

    def set_global_constants(self):
        # Assigned constants

        #initial residue concentration multiplier
        self.food_multiplier_init_sg = 240.  # short grass
        self.food_multiplier_init_tg = 110.  # tall grass
        self.food_multiplier_init_blp = 135.  # broad-leafed plants
        self.food_multiplier_init_fp = 15.  # fruits/pods
        self.food_multiplier_init_arthro = 94.  # arthropods

        #mean residue concentration multiplier
        self.food_multiplier_mean_sg = 85.  # short grass
        self.food_multiplier_mean_tg = 36.  # tall grass
        self.food_multiplier_mean_blp = 45.  # broad-leafed plants
        self.food_multiplier_mean_fp = 7.  # fruits/pods
        self.food_multiplier_mean_arthro = 65.  # arthropods

        # mass fraction of water in food source (higher values for herbivores and lower for granivores)
        # (EFED value = 0.8 for herbivores and insectivores, 0.1 for granivores)
        self.mf_w_bird_1 = 0.1
        self.mf_w_bird_2 = 0.8
        #self.mf_w_bird_3 = 0.9
        self.mf_w_mamm_1 = 0.1
        self.mf_w_mamm_2 = 0.8
        #self.mf_w_mamm_3 = 0.9

        self.nagy_bird_coef_sm = 0.02
        self.nagy_bird_coef_md = 0.1
        self.nagy_bird_coef_lg = 1.0
        self.nagy_mamm_coef_sm = 0.015
        self.nagy_mamm_coef_md = 0.035
        self.nagy_mamm_coef_lg = 1.0
