from __future__ import division
import numpy as np


class Therps(object):
    """
    Estimate dietary exposure and risk to terrestrial-phase amphibians and reptiles from pesticide use.
    """

    def __init__(self, chem_name, use, formu_name, a_i, h_l, n_a, i_a, a_r, avian_ld50, avian_lc50, avian_noaec,
                 avian_noael,
                 species_of_the_tested_bird_avian_ld50, species_of_the_tested_bird_avian_lc50,
                 species_of_the_tested_bird_avian_noaec, species_of_the_tested_bird_avian_noael,
                 bw_avian_ld50, bw_avian_lc50, bw_avian_noaec, bw_avian_noael,
                 mineau_scaling_factor, bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg, wp_herp_a_sm, wp_herp_a_md,
                 wp_herp_a_lg, c_mamm_a, c_herp_a):
        """
        THerps constructor.
        :param chem_name:
        :param use:
        :param formu_name:
        :param a_i:
        :param h_l:
        :param n_a:
        :param i_a:
        :param a_r:
        :param avian_ld50:
        :param avian_lc50:
        :param avian_noaec:
        :param avian_noael:
        :param species_of_the_tested_bird_avian_ld50:
        :param species_of_the_tested_bird_avian_lc50:
        :param species_of_the_tested_bird_avian_noaec:
        :param species_of_the_tested_bird_avian_noael:
        :param bw_avian_ld50:
        :param bw_avian_lc50:
        :param bw_avian_noaec:
        :param bw_avian_noael:
        :param mineau_scaling_factor:
        :param bw_herp_a_sm:
        :param bw_herp_a_md:
        :param bw_herp_a_lg:
        :param wp_herp_a_sm:
        :param wp_herp_a_md:
        :param wp_herp_a_lg:
        :param c_mamm_a:
        :param c_herp_a:
        :return:
        """
        self.chem_name = chem_name
        self.use = use
        self.formu_name = formu_name
        self.a_i = a_i
        self.a_i_disp = 100 * a_i
        self.h_l = h_l
        self.n_a = n_a
        self.i_a = i_a
        self.a_r = a_r
        self.avian_ld50 = avian_ld50
        self.avian_lc50 = avian_lc50
        self.avian_noaec = avian_noaec
        self.avian_noael = avian_noael
        self.species_of_the_tested_bird_avian_ld50 = species_of_the_tested_bird_avian_ld50
        self.species_of_the_tested_bird_avian_lc50 = species_of_the_tested_bird_avian_lc50
        self.species_of_the_tested_bird_avian_noaec = species_of_the_tested_bird_avian_noaec
        self.species_of_the_tested_bird_avian_noael = species_of_the_tested_bird_avian_noael
        self.bw_avian_ld50 = bw_avian_ld50
        self.bw_avian_lc50 = bw_avian_lc50
        self.bw_avian_noaec = bw_avian_noaec
        self.bw_avian_noael = bw_avian_noael
        self.mineau_scaling_factor = mineau_scaling_factor
        self.bw_herp_a_sm = bw_herp_a_sm
        self.bw_herp_a_md = bw_herp_a_md
        self.bw_herp_a_lg = bw_herp_a_lg
        self.wp_herp_a_sm = wp_herp_a_sm
        self.wp_herp_a_md = wp_herp_a_md
        self.wp_herp_a_lg = wp_herp_a_lg
        self.c_mamm_a = c_mamm_a
        self.c_herp_a = c_herp_a

        # Result variables

        # Table 5
        self.ld50_ad_sm = self.at_bird(avian_ld50, bw_herp_a_sm, bw_avian_ld50, mineau_scaling_factor)
        self.ld50_ad_md = self.at_bird(avian_ld50, bw_herp_a_md, bw_avian_ld50, mineau_scaling_factor)
        self.ld50_ad_lg = self.at_bird(avian_ld50, bw_herp_a_lg, bw_avian_ld50, mineau_scaling_factor)

        self.eec_dose_bp_sm = self.eec_dose_herp(self.eec_diet, bw_herp_a_sm, wp_herp_a_sm, self.c_0,
                                                 self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.eec_dose_bp_md = self.eec_dose_herp(self.eec_diet, bw_herp_a_md, wp_herp_a_md, self.c_0,
                                                 self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.eec_dose_bp_lg = self.eec_dose_herp(self.eec_diet, bw_herp_a_lg, wp_herp_a_lg, self.c_0,
                                                 self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.arq_dose_bp_sm = self.arq_dose_herp(self.eec_dose_herp_sm, self.eec_diet, bw_herp_a_sm,
                                                 self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                 wp_herp_a_sm, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.arq_dose_bp_md = self.arq_dose_herp(self.eec_dose_herp_md, self.eec_diet, bw_herp_a_md,
                                                 self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                 wp_herp_a_md, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.arq_dose_bp_lg = self.arq_dose_herp(self.eec_dose_herp_lg, self.eec_diet, bw_herp_a_lg,
                                                 self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                 wp_herp_a_lg, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l)

        self.eec_dose_fr_sm = self.eec_dose_herp(self.eec_diet, bw_herp_a_sm, wp_herp_a_sm, self.c_0,
                                                 self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.eec_dose_fr_md = self.eec_dose_herp(self.eec_diet, bw_herp_a_md, wp_herp_a_md, self.c_0,
                                                 self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.eec_dose_fr_lg = self.eec_dose_herp(self.eec_diet, bw_herp_a_lg, wp_herp_a_lg, self.c_0,
                                                 self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.arq_dose_fr_sm = self.arq_dose_herp(self.eec_dose_herp_sm, self.eec_diet, bw_herp_a_sm,
                                                 self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                 wp_herp_a_sm, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.arq_dose_fr_md = self.arq_dose_herp(self.eec_dose_herp_md, self.eec_diet, bw_herp_a_md,
                                                 self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                 wp_herp_a_md, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.arq_dose_fr_lg = self.arq_dose_herp(self.eec_dose_herp_lg, self.eec_diet, bw_herp_a_lg,
                                                 self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                 wp_herp_a_lg, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l)

        self.eec_dose_hm_md = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r,
                                                 a_i, 240, h_l, self.fi_mamm, bw_herp_a_md, c_mamm_a, 0.8)
        self.eec_dose_hm_lg = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r,
                                                 a_i, 240, h_l, self.fi_mamm, bw_herp_a_lg, c_mamm_a, 0.8)
        self.arq_dose_hm_md = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet, bw_herp_a_md,
                                                 self.at_bird, avian_ld50, bw_avian_ld50,
                                                 mineau_scaling_factor, c_mamm_a, 0.8, self.c_0, self.c_t, n_a, i_a,
                                                 a_r, a_i, 240, h_l, self.fi_mamm)
        self.arq_dose_hm_lg = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet, bw_herp_a_lg,
                                                 self.at_bird, avian_ld50, bw_avian_ld50,
                                                 mineau_scaling_factor, c_mamm_a, 0.8, self.c_0, self.c_t, n_a, i_a,
                                                 a_r, a_i, 240, h_l, self.fi_mamm)

        self.eec_dose_im_md = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r,
                                                 a_i, 15, h_l, self.fi_mamm, bw_herp_a_md, c_mamm_a, 0.8)
        self.eec_dose_im_lg = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r,
                                                 a_i, 15, h_l, self.fi_mamm, bw_herp_a_lg, c_mamm_a, 0.8)
        self.arq_dose_im_md = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet, bw_herp_a_md,
                                                 self.at_bird, avian_ld50, bw_avian_ld50,
                                                 mineau_scaling_factor, c_mamm_a, 0.8, self.c_0, self.c_t, n_a, i_a,
                                                 a_r, a_i, 15, h_l, self.fi_mamm)
        self.arq_dose_im_lg = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet, bw_herp_a_lg,
                                                 self.at_bird, avian_ld50, bw_avian_ld50,
                                                 mineau_scaling_factor, c_mamm_a, 0.8, self.c_0, self.c_t, n_a, i_a,
                                                 a_r, a_i, 15, h_l, self.fi_mamm)

        self.eec_dose_tp_md = self.eec_dose_tp(self.eec_diet_tp, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i,
                                               135, h_l, self.fi_herp, bw_herp_a_md, c_herp_a, wp_herp_a_sm,
                                               wp_herp_a_md)
        self.eec_dose_tp_lg = self.eec_dose_tp(self.eec_diet_tp, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i,
                                               135, h_l, self.fi_herp, bw_herp_a_lg, c_herp_a, wp_herp_a_sm,
                                               wp_herp_a_md)
        self.arq_dose_tp_md = self.arq_dose_tp(self.eec_dose_tp, self.eec_diet_tp, self.eec_diet, self.c_0, self.c_t,
                                               n_a, i_a, a_r, a_i, 135, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm,
                                               wp_herp_a_md, self.at_bird, avian_ld50, bw_herp_a_md, bw_avian_ld50,
                                               mineau_scaling_factor)
        self.arq_dose_tp_lg = self.arq_dose_tp(self.eec_dose_tp, self.eec_diet_tp, self.eec_diet, self.c_0, self.c_t,
                                               n_a, i_a, a_r, a_i, 135, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm,
                                               wp_herp_a_md, self.at_bird, avian_ld50, bw_herp_a_lg, bw_avian_ld50,
                                               mineau_scaling_factor)

        # Table 6
        self.eec_diet_herp_bl = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.eec_arq_herp_bl = self.arq_diet_herp(self.eec_diet, avian_lc50, self.c_0, self.c_t, n_a, i_a, a_r, a_i,
                                                  135, h_l)
        self.eec_diet_herp_fr = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.eec_arq_herp_fr = self.arq_diet_herp(self.eec_diet, avian_lc50, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15,
                                                  h_l)
        self.eec_diet_herp_hm = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 240, h_l,
                                                   self.fi_mamm, c_mamm_a, 0.8)
        self.eec_arq_herp_hm = self.arq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_lc50, self.c_0, self.c_t,
                                                  n_a, i_a, a_r, a_i, 240, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.eec_diet_herp_im = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l,
                                                   self.fi_mamm, c_mamm_a, 0.8)
        self.eec_arq_herp_im = self.arq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_lc50, self.c_0, self.c_t,
                                                  n_a, i_a, a_r, a_i, 15, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.eec_diet_herp_tp = self.eec_diet_tp(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l,
                                                 self.fi_herp, c_herp_a, wp_herp_a_sm)
        self.eec_arq_herp_tp = self.arq_diet_tp(self.eec_diet_tp, self.eec_diet, avian_lc50, self.c_0, self.c_t, n_a,
                                                i_a, a_r, a_i, 135, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm)

        # Table 7
        self.eec_diet_herp_bl = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.eec_crq_herp_bl = self.crq_diet_herp(self.eec_diet, avian_noaec, self.c_0, self.c_t, n_a, i_a, a_r, a_i,
                                                  135, h_l)
        self.eec_diet_herp_fr = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.eec_crq_herp_fr = self.crq_diet_herp(self.eec_diet, avian_noaec, self.c_0, self.c_t, n_a, i_a, a_r, a_i,
                                                  15, h_l)
        self.eec_diet_herp_hm = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 240, h_l,
                                                   self.fi_mamm, c_mamm_a, 0.8)
        self.eec_crq_herp_hm = self.crq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_noaec, self.c_0, self.c_t,
                                                  n_a, i_a, a_r, a_i, 240, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.eec_diet_herp_im = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l,
                                                   self.fi_mamm, c_mamm_a, 0.8)
        self.eec_crq_herp_im = self.crq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_noaec, self.c_0, self.c_t,
                                                  n_a, i_a, a_r, a_i, 15, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.eec_diet_herp_tp = self.eec_diet_tp(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l,
                                                 self.fi_herp, c_herp_a, wp_herp_a_sm)
        self.eec_crq_herp_tp = self.crq_diet_tp(self.eec_diet_tp, self.eec_diet, avian_noaec, self.c_0, self.c_t, n_a,
                                                i_a, a_r, a_i, 135, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm)

        # Table 8
        self.eec_dose_bp_sm_mean = self.eec_dose_herp(self.eec_diet, bw_herp_a_sm, wp_herp_a_sm, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.eec_dose_bp_md_mean = self.eec_dose_herp(self.eec_diet, bw_herp_a_md, wp_herp_a_md, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.eec_dose_bp_lg_mean = self.eec_dose_herp(self.eec_diet, bw_herp_a_lg, wp_herp_a_lg, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.arq_dose_bp_sm_mean = self.arq_dose_herp(self.eec_dose_herp, self.eec_diet, bw_herp_a_sm,
                                                      self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                      wp_herp_a_sm, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.arq_dose_bp_md_mean = self.arq_dose_herp(self.eec_dose_herp, self.eec_diet, bw_herp_a_md,
                                                      self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                      wp_herp_a_md, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.arq_dose_bp_lg_mean = self.arq_dose_herp(self.eec_dose_herp, self.eec_diet, bw_herp_a_lg,
                                                      self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                      wp_herp_a_lg, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l)

        self.eec_dose_fr_sm_mean = self.eec_dose_herp(self.eec_diet, bw_herp_a_sm, wp_herp_a_sm, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.eec_dose_fr_md_mean = self.eec_dose_herp(self.eec_diet, bw_herp_a_md, wp_herp_a_md, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.eec_dose_fr_lg_mean = self.eec_dose_herp(self.eec_diet, bw_herp_a_lg, wp_herp_a_lg, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.arq_dose_fr_sm_mean = self.arq_dose_herp(self.eec_dose_herp, self.eec_diet, bw_herp_a_sm,
                                                      self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                      wp_herp_a_sm, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.arq_dose_fr_md_mean = self.arq_dose_herp(self.eec_dose_herp, self.eec_diet, bw_herp_a_md,
                                                      self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                      wp_herp_a_md, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.arq_dose_fr_lg_mean = self.arq_dose_herp(self.eec_dose_herp, self.eec_diet, bw_herp_a_lg,
                                                      self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                      wp_herp_a_lg, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l)

        self.eec_dose_hm_md_mean = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a,
                                                      a_r, a_i, 85, h_l, self.fi_mamm, bw_herp_a_md, c_mamm_a, 0.8)
        self.eec_dose_hm_lg_mean = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a,
                                                      a_r, a_i, 85, h_l, self.fi_mamm, bw_herp_a_lg, c_mamm_a, 0.8)
        self.arq_dose_hm_md_mean = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet,
                                                      bw_herp_a_md, self.at_bird, avian_ld50,
                                                      bw_avian_ld50, mineau_scaling_factor, c_mamm_a, 0.8, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 85, h_l, self.fi_mamm)
        self.arq_dose_hm_lg_mean = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet,
                                                      bw_herp_a_lg, self.at_bird, avian_ld50,
                                                      bw_avian_ld50, mineau_scaling_factor, c_mamm_a, 0.8, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 85, h_l, self.fi_mamm)

        self.eec_dose_im_md_mean = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a,
                                                      a_r, a_i, 7, h_l, self.fi_mamm, bw_herp_a_md, c_mamm_a, 0.8)
        self.eec_dose_im_lg_mean = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a,
                                                      a_r, a_i, 7, h_l, self.fi_mamm, bw_herp_a_lg, c_mamm_a, 0.8)
        self.arq_dose_im_md_mean = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet,
                                                      bw_herp_a_md, self.at_bird, avian_ld50,
                                                      bw_avian_ld50, mineau_scaling_factor, c_mamm_a, 0.8, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 7, h_l, self.fi_mamm)
        self.arq_dose_im_lg_mean = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet,
                                                      bw_herp_a_lg, self.at_bird, avian_ld50,
                                                      bw_avian_ld50, mineau_scaling_factor, c_mamm_a, 0.8, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 7, h_l, self.fi_mamm)

        self.eec_dose_tp_md_mean = self.eec_dose_tp(self.eec_diet_tp, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r,
                                                    a_i, 45, h_l, self.fi_herp, bw_herp_a_md, c_herp_a, wp_herp_a_sm,
                                                    wp_herp_a_md)
        self.eec_dose_tp_lg_mean = self.eec_dose_tp(self.eec_diet_tp, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r,
                                                    a_i, 45, h_l, self.fi_herp, bw_herp_a_lg, c_herp_a, wp_herp_a_sm,
                                                    wp_herp_a_md)
        self.arq_dose_tp_md_mean = self.arq_dose_tp(self.eec_dose_tp, self.eec_diet_tp, self.eec_diet, self.c_0,
                                                    self.c_t, n_a, i_a, a_r, a_i, 45, h_l, self.fi_herp, c_herp_a,
                                                    wp_herp_a_sm, wp_herp_a_md, self.at_bird, avian_ld50, bw_herp_a_md,
                                                    bw_avian_ld50, mineau_scaling_factor)
        self.arq_dose_tp_lg_mean = self.arq_dose_tp(self.eec_dose_tp, self.eec_diet_tp, self.eec_diet, self.c_0,
                                                    self.c_t, n_a, i_a, a_r, a_i, 45, h_l, self.fi_herp, c_herp_a,
                                                    wp_herp_a_sm, wp_herp_a_md, self.at_bird, avian_ld50, bw_herp_a_lg,
                                                    bw_avian_ld50, mineau_scaling_factor)

        # Table 9
        self.eec_diet_herp_bl_mean = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.eec_arq_herp_bl_mean = self.arq_diet_herp(self.eec_diet, avian_lc50, self.c_0, self.c_t, n_a, i_a, a_r,
                                                       a_i, 45, h_l)
        self.eec_diet_herp_fr_mean = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.eec_arq_herp_fr_mean = self.arq_diet_herp(self.eec_diet, avian_lc50, self.c_0, self.c_t, n_a, i_a, a_r,
                                                       a_i, 7, h_l)
        self.eec_diet_herp_hm_mean = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 85, h_l,
                                                        self.fi_mamm, c_mamm_a, 0.8)
        self.eec_arq_herp_hm_mean = self.arq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_lc50, self.c_0,
                                                       self.c_t, n_a, i_a, a_r, a_i, 85, h_l, self.fi_mamm, c_mamm_a,
                                                       0.8)
        self.eec_diet_herp_im_mean = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l,
                                                        self.fi_mamm, c_mamm_a, 0.8)
        self.eec_arq_herp_im_mean = self.arq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_lc50, self.c_0,
                                                       self.c_t, n_a, i_a, a_r, a_i, 7, h_l, self.fi_mamm, c_mamm_a,
                                                       0.8)
        self.eec_diet_herp_tp_mean = self.eec_diet_tp(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l,
                                                      self.fi_herp, c_herp_a, wp_herp_a_sm)
        self.eec_arq_herp_tp_mean = self.arq_diet_tp(self.eec_diet_tp, self.eec_diet, avian_lc50, self.c_0, self.c_t,
                                                     n_a, i_a, a_r, a_i, 45, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm)

        # Table 10
        self.eec_diet_herp_bl_mean = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.eec_crq_herp_bl_mean = self.crq_diet_herp(self.eec_diet, avian_noaec, self.c_0, self.c_t, n_a, i_a, a_r,
                                                       a_i, 45, h_l)
        self.eec_diet_herp_fr_mean = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.eec_crq_herp_fr_mean = self.crq_diet_herp(self.eec_diet, avian_noaec, self.c_0, self.c_t, n_a, i_a, a_r,
                                                       a_i, 7, h_l)
        self.eec_diet_herp_hm_mean = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 85, h_l,
                                                        self.fi_mamm, c_mamm_a, 0.8)
        self.eec_crq_herp_hm_mean = self.crq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_noaec, self.c_0,
                                                       self.c_t, n_a, i_a, a_r, a_i, 85, h_l, self.fi_mamm, c_mamm_a,
                                                       0.8)
        self.eec_diet_herp_im_mean = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l,
                                                        self.fi_mamm, c_mamm_a, 0.8)
        self.eec_crq_herp_im_mean = self.crq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_noaec, self.c_0,
                                                       self.c_t, n_a, i_a, a_r, a_i, 7, h_l, self.fi_mamm, c_mamm_a,
                                                       0.8)
        self.eec_diet_herp_tp_mean = self.eec_diet_tp(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l,
                                                      self.fi_herp, c_herp_a, wp_herp_a_sm)
        self.eec_crq_herp_tp_mean = self.crq_diet_tp(self.eec_diet_tp, self.eec_diet, avian_noaec, self.c_0, self.c_t,
                                                     n_a, i_a, a_r, a_i, 45, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm)

