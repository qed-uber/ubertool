import datetime
import inspect
import numpy.testing as npt
import os.path
import pandas as pd
import pandas.util.testing as pdt
import sys
from tabulate import tabulate
import unittest

# #find parent directory and import model
# parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
# sys.path.append(parentddir)
from ..screenip_exe import Screenip

test = {}


class TestScreenip(unittest.TestCase):
    """
    Unit tests for screenip.
    """
    print("screenip unittests conducted at " + str(datetime.datetime.today()))

    def setUp(self):
        """
        Setup routine for screenip unittest.
        :return:
        """

        pass
        # screenip2 = screenip_model.screenip(0, pd_obj_inputs, pd_obj_exp_out)
        # setup the test as needed
        # e.g. pandas to open screenip qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def tearDown(self):
        """
        Teardown routine for screenip unittest.
        :return:
        """
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

    def create_screenip_object(self):
        # create empty pandas dataframes to create empty object for testing
        df_empty = pd.DataFrame()
        # create an empty screenip object
        screenip_empty = Screenip(df_empty, df_empty)
        return screenip_empty

    def test_screenip_unit_fw_bird(self):
        """
        unittest for function screenip.fw_bird:
        :return:
        """
        expected_results = pd.Series([0.0162, 0.0162, 0.0162], dtype='float')
        result = pd.Series([], dtype='float')

        # create empty pandas dataframes to create empty object for this unittest
        screenip_empty = self.create_screenip_object()

        try:
            # for i in range(0,3):
            #     result[i] = screenip_empty.fw_bird()
            screenip_empty.no_of_runs = len(expected_results)
            screenip_empty.fw_bird()
            result = screenip_empty.out_fw_bird
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_screenip_unit_fw_mamm(self):
        """
        unittest for function screenip.fw_mamm:
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        screenip_empty = self.create_screenip_object()

        expected_results = pd.Series([0.172, 0.172, 0.172], dtype='float')
        result = pd.Series([], dtype='float')

        try:
            screenip_empty.no_of_runs = len(expected_results)
            result = screenip_empty.fw_mamm()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_screenip_unit_dose_bird(self):
        """
        unittest for function screenip.dose_bird:
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        screenip_empty = self.create_screenip_object()

        expected_results = pd.Series([1000000., 4805.50175, 849727.21122], dtype='float')
        result = pd.Series([], dtype='float')

        try:
            #(self.out_fw_bird * self.solubility)/(self.bodyweight_assessed_bird / 1000.)
            screenip_empty.out_fw_bird = pd.Series([10., 0.329, 1.8349], dtype='float')
            screenip_empty.solubility = pd.Series([100., 34.9823, 453.83], dtype='float')
            screenip_empty.bodyweight_assessed_bird = pd.Series([1.0, 2.395, 0.98], dtype='float')
            result = screenip_empty.dose_bird()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_screenip_unit_dose_mamm(self):
        """
        unittest for function screenip.dose_mamm:
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        screenip_empty = self.create_screenip_object()

        expected_results = pd.Series([8000000., 48205.7595, 3808036.37889], dtype='float')
        result = pd.Series([], dtype='float')

        try:
            #(self.out_fw_mamm * self.solubility)/(self.bodyweight_assessed_mammal / 1000)
            screenip_empty.out_fw_mamm = pd.Series([20., 12.843, 6.998], dtype='float')
            screenip_empty.solubility = pd.Series([400., 34.9823, 453.83], dtype='float')
            screenip_empty.bodyweight_assessed_mammal = pd.Series([1., 9.32, 0.834], dtype='float')
            result = screenip_empty.dose_mamm()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_screenip_unit_at_bird(self):
        """
        unittest for function screenip.at_bird:
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        screenip_empty = self.create_screenip_object()

        expected_results = pd.Series([1000., 687.9231, 109.3361], dtype='float')
        result = pd.Series([], dtype='float')

        try:
            #(self.ld50_avian_water) * ((self.bodyweight_assessed_bird / self.bodyweight_tested_bird)**(self.mineau_scaling_factor - 1.))
            screenip_empty.ld50_avian_water = pd.Series([2000., 938.34, 345.83], dtype='float')
            screenip_empty.bodyweight_assessed_bird = pd.Series([100., 39.49, 183.54], dtype='float')
            screenip_empty.ld50_bodyweight_tested_bird = pd.Series([200., 73.473, 395.485], dtype='float')
            screenip_empty.mineau_scaling_factor = pd.Series([2., 1.5, 2.5], dtype='float')
            result = screenip_empty.at_bird()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_screenip_unit_at_mamm(self):
        """
        unittest for function screenip.at_mamm:
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        screenip_empty = self.create_screenip_object()

        expected_results = pd.Series([11.89207, 214.0572, 412.6864], dtype='float')
        result = pd.Series([], dtype='float')

        try:
            #(self.ld50_mammal_water) * ((self.bodyweight_tested_mammal / self.bodyweight_assessed_mammal)**0.25)
            screenip_empty.ld50_mammal_water = pd.Series([10., 250., 500.], dtype='float')
            screenip_empty.ld50_bodyweight_tested_mammal = pd.Series([200., 39.49, 183.54], dtype='float')
            screenip_empty.bodyweight_assessed_mammal = pd.Series([100., 73.473, 395.485], dtype='float')
            result = screenip_empty.at_mamm()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_screenip_unit_fi_bird(self):
        """
        unittest for function screenip.fi_bird:
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        screenip_empty = self.create_screenip_object()

        expected_results = pd.Series([0.012999, 0.026578, 0.020412], dtype='float')
        result = pd.Series([], dtype='float')

        try:
            #0.0582 * ((bw_grams / 1000.)**0.651)
            bw_grams = pd.Series([100., 300., 200.], dtype='float')
            result = screenip_empty.fi_bird(bw_grams)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_screenip_unit_act(self):
        """
        unittest for function screenip.test_act:
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        screenip_empty = self.create_screenip_object()

        expected_results = pd.Series([10.5737, 124.8032, 416.4873], dtype='float')
        result = pd.Series([], dtype='float')

        try:
            #(self.noael_mammal_water) * ((self.bodyweight_tested_mammal / self.bodyweight_assessed_mammal)**0.25)
            screenip_empty.noael_mammal_water = pd.Series([10., 120., 400.], dtype='float')
            screenip_empty.noael_bodyweight_tested_mammal = pd.Series([500., 385.45, 673.854], dtype='float')
            screenip_empty.bodyweight_assessed_mammal = pd.Series([400., 329.45, 573.322], dtype='float')
            result = screenip_empty.act()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_screenip_unit_det(self):
        """
        unittest for function screenip.det
        return:
        """
    #
    #     '''
    #     Dose Equiv. Toxicity:
    #
    #     The FI value (kg-diet) is multiplied by the reported NOAEC (mg/kg-diet) and then divided by
    #     the test animal's body weight to derive the dose-equivalent chronic toxicity value (mg/kg-bw):
    #
    #     Dose Equiv. Toxicity = (NOAEC * FI) / BW
    #
    #     NOTE: The user enters the lowest available NOAEC for the mallard duck, for the bobwhite quail,
    #     and for any other test species. The model calculates the dose equivalent toxicity values for
    #     all of the modeled values (Cells F20-24 and results worksheet) and then selects the lowest dose
    #     equivalent toxicity value to represent the chronic toxicity of the chemical to birds.
    #     '''
    #     try:
    #         # result =
    #         # self.assertEquals(result, )
    #         pass
    #     finally:
    #         pass
    #    return
    #
    #
    # def test_det_duck(self):
    #     """
    #     unittest for function screenip.det_duck:
    #     :return:
    #     """
    #     try:
    #         # det_duck = (self.noaec_duck * self.fi_bird(1580.)) / (1580. / 1000.)
    #         screenip_empty.noaec_duck = pd.Series([1.], dtype='int')
    #         screenip_empty.fi_bird = pd.Series([1.], dtype='int')
    #         result = screenip_empty.det_duck()
    #         npt.assert_array_almost_equal(result, 1000., 4, '', True)
    #     finally:
    #         pass
    #     return
    #
    # def test_det_quail(self):
    #     """
    #     unittest for function screenip.det_quail:
    #     :return:
    #     """
    #     try:
    #         # det_quail = (self.noaec_quail * self.fi_bird(178.)) / (178. / 1000.)
    #         screenip_empty.noaec_quail = pd.Series([1.], dtype='int')
    #         screenip_empty.fi_bird = pd.Series([1.], dtype='int')
    #         result = screenip_empty.det_quail()
    #         npt.assert_array_almost_equal(result, 1000., 4, '', True)
    #     finally:
    #         pass
    #     return
    #
    # def test_det_other_1(self):
    #     """
    #     unittest for function screenip.det_other_1:
    #     :return:
    #     """
    #     try:
    #         #det_other_1 = (self.noaec_bird_other_1 * self.fi_bird(self.bodyweight_bird_other_1)) / (self.bodyweight_bird_other_1 / 1000.)
    #         #det_other_2 = (self.noaec_bird_other_2 * self.fi_bird(self.bodyweight_bird_other_1)) / (self.bodyweight_bird_other_1 / 1000.)
    #         screenip_empty.noaec_bird_other_1 = pd.Series([400.]) # mg/kg-diet
    #         screenip_empty.bodyweight_bird_other_1 = pd.Series([100]) # grams
    #         result = screenip_empty.det_other_1()
    #         npt.assert_array_almost_equal(result, 4666, 4)
    #     finally:
    #         pass
    #     return
    #
    #   The following tests are configured such that:
        #   1. four values are provided for each needed input
        #   2. the four input values generate four values of out_det_* per bird type
        #   3. the inputs per bird type are set so that calculations of out_det_* will result in
        #      each bird type having one minimum among the bird types;
        #      thus all four calculations result in one minimum per bird type

        # create empty pandas dataframes to create empty object for this unittest
        screenip_empty = self.create_screenip_object()

        expected_results = pd.Series([4.2174, 4.96125, 7.97237, 10.664648], dtype='float')
        result = pd.Series([], dtype='float')

        try:
            screenip_empty.bodyweight_bobwhite_quail = 178.
            screenip_empty.bodyweight_mallard_duck = 1580.
            screenip_empty.noaec_quail = pd.Series([100., 300., 75., 150.], dtype='float')
            screenip_empty.noaec_duck = pd.Series([400., 100., 200., 350.], dtype='float')
            screenip_empty.noaec_bird_other_1 = pd.Series([50., 200., 300., 250.], dtype='float')
            screenip_empty.noaec_bird_other_2 = pd.Series([350., 400., 250., 100.], dtype='float')
            screenip_empty.noaec_bodyweight_bird_other_1 = pd.Series([345.34, 453.54, 649.29, 294.56], dtype='float')
            screenip_empty.noaec_bodyweight_bird_other_2 = pd.Series([123.84, 85.743, 127.884, 176.34], dtype='float')
            screenip_empty.no_of_runs = len(expected_results)
            result = screenip_empty.det()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_screenip_unit_acute_bird(self):
        """
        unittest for function screenip.acute_bird:
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        screenip_empty = self.create_screenip_object()

        expected_results = pd.Series([10., 5.22093, 0.479639], dtype='float')
        result = pd.Series([], dtype='float')

        try:
            # self.out_acute_bird = self.out_dose_bird / self.out_at_bird
            screenip_empty.out_dose_bird = pd.Series([100., 121.23, 43.994], dtype='float')
            screenip_empty.out_at_bird = pd.Series([10., 23.22, 91.723], dtype='float')
            result = screenip_empty.acute_bird()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_screenip_unit_acuconb(self):
        """
        unittest for function screenip.acuconb:
        Message stating whether or not a risk is present
        :return:
        """
        # if self.out_acuconb == -1:
        #     if self.out_acute_bird == None:
        #         raise ValueError\
        #         ('acute_bird variable equals None and therefor this function cannot be run.')
        # if self.out_acute_bird < 0.1:
        #     self.out_acuconb = ('Drinking water exposure alone is NOT a potential concern for birds')
        # else:
        #     self.out_acuconb = ('Exposure through drinking water alone is a potential concern for birds')

        # create empty pandas dataframes to create empty object for this unittest
        screenip_empty = self.create_screenip_object()

        expected_results = pd.Series(["Exposure through drinking water alone is a potential concern "
                            "for birds", "Drinking water exposure alone is NOT a potential "
                            "concern for birds", "Exposure through drinking water alone is a "
                            "potential concern for birds"], dtype='object')
        result = pd.Series([], dtype='object')

        try:
            screenip_empty.out_acute_bird = pd.Series([0.2, 0.09, 0.1], dtype='float')
            result = screenip_empty.acuconb()
            pdt.assert_series_equal(result, expected_results,  True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_screenip_unit_acute_mamm(self):
        """
        unittest for function screenip.acute_mamm:
        :return:
        """
        # self.out_acute_mamm = self.out_dose_mamm / self.out_at_mamm

        # create empty pandas dataframes to create empty object for this unittest
        screenip_empty = self.create_screenip_object()

        expected_results = pd.Series([10., 14.68657, 2.124852], dtype='float')
        result = pd.Series([], dtype='float')

        try:
            screenip_empty.out_dose_mamm = pd.Series([100., 34.44, 159.349], dtype='float')
            screenip_empty.out_at_mamm = pd.Series([10., 2.345, 74.993], dtype='float')
            result = screenip_empty.acute_mamm()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_screenip_unit_acuconm(self):
        """
        unittest for function screenip.acuconm:
        Message stating whether or not a risk is present
        :return:
        """
        # if self.out_acuconm == -1:
        #     if self.out_acute_mamm == None:
        #         raise ValueError\
        #         ('acute_mamm variable equals None and therefor this function cannot be run.')
        #     if self.out_acute_mamm < 0.1:
        #         self.out_acuconm = ('Drinking water exposure alone is NOT a potential concern for mammals')
        #     else:
        #         self.out_acuconm = ('Exposure through drinking water alone is a potential concern for mammals')
        #     return self.out_acuconm

        # create empty pandas dataframes to create empty object for this unittest
        screenip_empty = self.create_screenip_object()

        expected_results = pd.Series(["Drinking water exposure alone is NOT a potential concern "
                                      "for mammals", "Exposure through drinking water alone is a "
                                      "potential concern for mammals", "Drinking water exposure "
                                      "alone is NOT a potential concern for mammals"], dtype='object')
        result = pd.Series([], dtype='object')

        try:
            screenip_empty.out_acute_mamm = pd.Series([0.09, 0.2, 0.002], dtype='float')
            result = screenip_empty.acuconm()
            pdt.assert_series_equal(result, expected_results, True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_screenip_unit_chron_bird(self):
        """
        unittest for function screenip.chron_bird:
        :return:
        """
        #self.out_chron_bird = self.out_dose_bird / self.out_det

        # create empty pandas dataframes to create empty object for this unittest
        screenip_empty = self.create_screenip_object()

        expected_results = pd.Series([0.5, 0.10891, 2.39857], dtype='float')
        result = pd.Series([], dtype='float')

        try:
            screenip_empty.out_dose_bird = pd.Series([5., 1.32, 19.191], dtype='float')
            screenip_empty.out_det = pd.Series([10., 12.12, 8.001], dtype='float')
            result = screenip_empty.chron_bird()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_screenip_unit_chronconb(self):
        """
        unittest for function screenip.chronconb:
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        screenip_empty = self.create_screenip_object()

        expected_results = pd.Series(["Drinking water exposure alone is NOT "
                                      "a potential concern for birds", "Exposure through "
                                      "drinking water alone is a potential concern for "
                                      "birds", "Drinking water exposure alone is NOT a "
                                      "potential concern for birds"], dtype='object')
        result = pd.Series([], dtype='object')

        try:
            screenip_empty.out_chron_bird = pd.Series([0.12, 3., 0.97], dtype='float')
            result = screenip_empty.chronconb()
            pdt.assert_series_equal(result, expected_results, True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_screenip_unit_chron_mamm(self):
        """
        unittest for function screenip.chron_mamm:
        :return:
        """
        # self.out_chron_mamm = self.out_dose_mamm / self.out_act

        # create empty pandas dataframes to create empty object for this unittest
        screenip_empty = self.create_screenip_object()

        expected_results = pd.Series([2.0, 14.1333, 244.7245], dtype='float')
        result = pd.Series([], dtype='float')

        try:
            screenip_empty.out_dose_mamm = pd.Series([8., 34.344, 23.983], dtype='float')
            screenip_empty.out_act = pd.Series([4., 2.43, 0.098], dtype='float')
            result = screenip_empty.chron_mamm()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_screenip_unit_chronconm(self):
        """
        unittest for function screenip.chronconm:
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        screenip_empty = self.create_screenip_object()

        expected_results = pd.Series(["Drinking water exposure alone is NOT a potential "
                            "concern for mammals", "Exposure through drinking water alone "
                            "is a potential concern for mammals", "Drinking water exposure "
                            "alone is NOT a potential concern for mammals"], dtype='object')
        result = pd.Series([], dtype='object')

        try:
            screenip_empty.out_chron_mamm = pd.Series([0.5, 1.0, 0.09], dtype='float')
            result = screenip_empty.chronconm()
            pdt.assert_series_equal(result, expected_results, True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()
    #pass
