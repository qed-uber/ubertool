from __future__ import division  #brings in Python 3.0 mixed type calculation rules
import datetime
import inspect
import numpy as np
import numpy.testing as npt
import os.path
import pandas as pd
import pandas.util.testing as pdt
import sys
from tabulate import tabulate
import unittest

print("Python version: " + sys.version)
print("Numpy version: " + np.__version__)

#find parent directory and import model
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parent_dir)
from therps_exe import THerps



class Testtherps(unittest.TestCase):
    """
    Unit tests for T-Rex model.
    """
    print("THerps unittests conducted at " + str(datetime.datetime.today()))

    def setUp(self):
        """
        Setup routine for therps unit tests.
        :return:
        """
        self.therps_empty = object
        # create empty pandas dataframes to create empty object for testing
        df_empty = pd.DataFrame()
        # create an empty therps object
        self.therps_empty = THerps(df_empty, df_empty)

        test = {}
        # setup the test as needed
        # e.g. pandas to open therps qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def tearDown(self):
        """
        Teardown routine for therps unit tests.
        :return:
        """
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

    def test_convert_app_intervals(self):
        """
        unit test for function convert_app_intervals
        the method converts number of applications and application interval into application rates and day of year number
        this is so that the same concentration timeseries method from trex_functions can be reused here
        :return:
        """
        result_day_out = pd.Series([], dtype="object")
        result_app_rates = pd.Series([], dtype="object")

        expected_result_day_out = pd.Series([[0,6,13], [0], [0,20,41,62], [0,6,13]], dtype = 'object')
        expected_result_app_rates = pd.Series([[1.2,1.2,1.2], [2.3], [2.5,2.5,2.5,2.5], [5.1,5.1,5.1]], dtype = 'object')
        try:
            self.therps_empty.num_apps = [3,1,4,3]
            self.therps_empty.app_interval = [7,1,21,7]
            self.therps_empty.application_rate = [1.2, 2.3, 2.5,5.1]
            result_day_out, result_app_rates = self.therps_empty.convert_app_intervals()
                #using pdt.assert_series_equal assertion instead of npt.assert_allclose
                #because npt.assert_allclose does not handle uneven object/series lists
                #Note that pdt.assert_series_equal requires object/series to be exactly equal
                #this is ok in this instance because we are not "calculating" real numbers
                #but rather simply distributing them from an input value into a new object/series
            pdt.assert_series_equal(result_app_rates,expected_result_app_rates)
            pdt.assert_series_equal(result_day_out,expected_result_day_out)
        finally:
            tab1 = [result_app_rates, expected_result_app_rates]
            tab2 = [result_day_out, expected_result_day_out]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab1, headers='keys', tablefmt='rst'))
            print(tabulate(tab2, headers='keys', tablefmt='rst'))
        return

    def test_conc_initial(self):
        """
        unittest for function conc_initial:
        conc_0 = (app_rate * self.frac_act_ing * food_multiplier)
        """
        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([12.7160, 9.8280, 11.2320], dtype = 'float')
        try:
                # specify an app_rates Series (that is a series of lists, each list representing
                # a set of application rates for 'a' model simulation)
            self.therps_empty.app_rates = pd.Series([[0.34, 1.384, 13.54], [0.78, 11.34, 3.54],
                                              [2.34, 1.384, 3.4]], dtype='float')
            self.therps_empty.food_multiplier_init_sg = pd.Series([110., 15., 240.], dtype='float')
            self.therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype='float')
            for i in range(len(self.therps_empty.frac_act_ing)):
                result[i] = self.therps_empty.conc_initial(i, self.therps_empty.app_rates[i][0], self.therps_empty.food_multiplier_init_sg[i])
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_conc_timestep(self):
        """
        unittest for function conc_timestep:
        """
        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([6.25e-5, 0.039685, 7.8886e-30], dtype = 'float')
        try:
            self.therps_empty.foliar_diss_hlife = pd.Series([.25, 0.75, 0.01], dtype='float')
            conc_0 = pd.Series([0.001, 0.1, 10.0])
            for i in range(len(conc_0)):
                result[i] = self.therps_empty.conc_timestep(i, conc_0[i])
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_percent_to_frac(self):
        """
        unittest for function percent_to_frac:
        """
        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([.04556, .1034, .9389], dtype = 'float')
        try:
            self.therps_empty.percent_incorp = pd.Series([4.556, 10.34, 93.89], dtype='float')
            result = self.therps_empty.percent_to_frac(self.therps_empty.percent_incorp)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_at_bird(self):
        """
        unittest for function at_bird1; alternative approach using more vectorization:
        adjusted_toxicity = self.ld50_bird * (aw_bird / self.tw_bird_ld50) ** (self.mineau_sca_fact - 1)
        """
        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([48.97314, 180.76569, 31.49672], dtype = 'float')
        try:
            self.therps_empty.ld50_bird = pd.Series([100., 125., 90.], dtype='float')
            self.therps_empty.tw_bird_ld50 = pd.Series([175., 100., 200.], dtype='float')
            self.therps_empty.mineau_sca_fact = pd.Series([1.15, 0.9, 1.25], dtype='float')
            self.therps_empty.aw_herp_sm = pd.Series([1.5, 2.5, 3.0], dtype = 'float')

            result = self.therps_empty.at_bird(self.therps_empty.aw_herp_sm)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_fi_mamm(self):
        """
        unittest for function fi_mamm:
        food_intake = (0.621 * (aw_mamm ** 0.564)) / (1 - mf_w_mamm)
        """
        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([3.17807, 16.8206, 42.28516], dtype = 'float')
        try:
            self.therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')
            self.therps_empty.aw_mamm_sm = pd.Series([15., 20., 30.], dtype='float')

            result = self.therps_empty.fi_mamm(self.therps_empty.aw_mamm_sm, self.therps_empty.mf_w_mamm_2)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_fi_herp(self):
        """
        unittest for function fi_herp: Food intake for herps.
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.1171708, 0.6585815, 1.802014], dtype = 'float')

        try:
            self.therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')
            self.therps_empty.aw_herp_sm = pd.Series([15., 20., 30.], dtype='float')

            result = self.therps_empty.fi_herp(self.therps_empty.aw_herp_sm, self.therps_empty.mf_w_mamm_2)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_eec_diet_timeseries(self):
        """
        combined unit test for methods eec_diet_timeseries;

        * this test calls eec_diet_timeseries, which in turn calls conc_initial and conc_timestep

        * this unittest executes the timeseries method for three sets of inputs (i.e., model simulations)
        * each timeseries is the target of an assertion test
        * the complete timeseries is not compared between actual and expected results
        * rather selected values from each series are extracted and placed into a list for comparison
        * the values extracted include the first and last entry in the timeseries (first and last day of simulated year)
        * additional values are extracted on each day of the year for which there is a pesticide application
        * the code here is not elegant (each simulation timeseries is checked within it own code segment; as opposed to
        * getting the indexing squared away so that a single piece of code would loop through all simulations
        * (perhaps at a later time this can be revisited and made more elegant)
        """

        conc_timeseries = pd.Series([], dtype = 'object')
        result1 = pd.Series([], dtype = 'float')
        result2 = pd.Series([], dtype = 'float')
        result3 = pd.Series([], dtype = 'float')
        expected_results1 = [0.0, 1.734, 6.791566e-5]
        expected_results2 = [9.828, 145.341, 80.93925, 20.6686758, 1.120451e-18]
        expected_results3 = [0.0, 0.702, 0.5656463, 0.087722]
        num_app_days = pd.Series([], dtype='int')

        try:
            #define needed inputs for method
            self.therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            self.therps_empty.food_multiplier_init_sg = 15.
            self.therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios (i.e., model simulations) of 1, 4, and 2 applications
            self.therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            self.therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            #self.therps_empty.num_apps = [0] * len(self.therps_empty.app_rates) #set length of num_apps list (no longer needed)
            for i in range(len(self.therps_empty.app_rates)):
                self.therps_empty.num_apps[i] = len(self.therps_empty.app_rates[i])
                num_app_days[i] = len(self.therps_empty.day_out[i])
                assert (self.therps_empty.num_apps[i] == num_app_days[i]), 'series of app-rates and app_days do not match'

            #run method and get timeseries (all simulations will be executed here)
            conc_timeseries = self.therps_empty.eec_diet_timeseries(self.therps_empty.food_multiplier_init_sg)

            #let's extract from each timeseries values on the first day, each day of an application, and the last day
            #these will be placed into the 'result#' and used for the allclose assertion
            #need to execute this extraction for each simulation timeseries because 'allclose' will not handle uneven series lists

            #first simulation result
            num_values_to_check = len(self.therps_empty.app_rates[0]) + 2 #number of applications plus first and last timeseries elements
            if (self.therps_empty.day_out[0][0] == 1):  #if first app day is first day of year
                num_values_to_check = num_values_to_check - 1
            result1 = [0.] * num_values_to_check
            result1[0] = float(conc_timeseries[0][0])  #first day of timeseries
            result1[-1] = float(conc_timeseries[0][370])  #last day of timeseries
            num_values_to_check = len(self.therps_empty.app_rates[0])
            if ((num_values_to_check) >= 1):
                result_index = 1
                for i in range(0 ,num_values_to_check):
                    if(self.therps_empty.day_out[0][i] != 1):
                        series_index = self.therps_empty.day_out[0][i] - 1
                        result1[result_index] = float(conc_timeseries[0][series_index])
                        result_index = result_index + 1
            npt.assert_allclose(result1,expected_results1,rtol=1e-4, atol=0, err_msg='', verbose=True)

            #second simulation result
            num_values_to_check = len(self.therps_empty.app_rates[1]) + 2
            if (self.therps_empty.day_out[1][0] == 1):  #if first app day is first day of year
                num_values_to_check = num_values_to_check - 1
            result2 = [0.] * num_values_to_check
            result2[0] = float(conc_timeseries[1][0])  #first day of timeseries
            result2[-1] = float(conc_timeseries[1][370])  #last day of timeseries
            num_values_to_check = len(self.therps_empty.app_rates[1])
            if ((num_values_to_check) >= 1):
                result_index = 1
                for i in range(0 ,num_values_to_check):
                    if(self.therps_empty.day_out[1][i] != 1):
                        series_index = self.therps_empty.day_out[1][i] - 1
                        result2[result_index] = float(conc_timeseries[1][series_index])
                        result_index = result_index + 1
            npt.assert_allclose(result2,expected_results2,rtol=1e-4, atol=0, err_msg='', verbose=True)

            #3rd simulation result
            num_values_to_check = len(self.therps_empty.app_rates[2]) + 2
            if (self.therps_empty.day_out[2][0] == 1):  #if first app day is first day of year
                num_values_to_check = num_values_to_check - 1
            result3 = [0.] * num_values_to_check
            result3[0] = float(conc_timeseries[2][0])  #first day of timeseries
            result3[-1] = float(conc_timeseries[2][370])  #last day of timeseries
            num_values_to_check = len(self.therps_empty.app_rates[2])
            if ((num_values_to_check) >= 1):
                result_index = 1
                for i in range(0 ,num_values_to_check):
                    if(self.therps_empty.day_out[2][i] != 1):
                        series_index = self.therps_empty.day_out[2][i] - 1
                        result3[result_index] = float(conc_timeseries[2][series_index])
                        result_index = result_index + 1
            npt.assert_allclose(result3,expected_results3,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab1 = [result1, expected_results1]
            tab2 = [result2, expected_results2]
            tab3 = [result3, expected_results3]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab1, headers='keys', tablefmt='rst'))
            print(tabulate(tab2, headers='keys', tablefmt='rst'))
            print(tabulate(tab3, headers='keys', tablefmt='rst'))
        return

    def test_eec_diet_timeseriesA(self):
        """
        combined unit test for methods eec_diet_timeseries;

        * this test calls eec_diet_timeseries, which in turn calls conc_initial and conc_timestep

        * this unittest executes the timeseries method for three sets of inputs (i.e., model simulations)
        * each timeseries (i.e., simulation result) is the target of an assertion test
        * the complete timeseries is not compared between actual and expected results
        * rather selected values from each series are extracted and placed into a list for comparison
        * the values extracted include the first and last entry in the timeseries (first and last day of simulated year)
        * additional values are extracted on each day of the year for which there is a pesticide application
        """

        conc_timeseries = pd.Series([], dtype = 'object')
        result = pd.Series([], dtype = 'object')
        expected_results = pd.Series([[0.0, 1.734, 6.791566e-5], [9.828, 145.341, 80.93925, 20.6686758, 1.120451e-18],
                                      [0.0, 0.702, 0.5656463, 0.087722]], dtype = 'object')
        num_app_days = pd.Series([], dtype='int')

        try:
            #define needed inputs for method
            self.therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            self.therps_empty.food_multiplier_init_sg = 15.
            self.therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios (i.e., model simulations) of 1, 4, and 2 applications
            self.therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            self.therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            #self.therps_empty.num_apps = [0] * len(self.therps_empty.app_rates) #set length of num_apps list (no longer needed)
            for i in range(len(self.therps_empty.app_rates)):
                self.therps_empty.num_apps[i] = len(self.therps_empty.app_rates[i])
                num_app_days[i] = len(self.therps_empty.day_out[i])
                assert (self.therps_empty.num_apps[i] == num_app_days[i]), 'series of app-rates and app_days do not match'

            #run method and get timeseries (all simulations will be executed here)
            conc_timeseries = self.therps_empty.eec_diet_timeseries(self.therps_empty.food_multiplier_init_sg)

            #let's extract from each timeseries values on the first day, each day of an application, and the last day
            #these will be placed into 'result' and used for the allclose assertion

            #loop through simulation results extracting values of interest per timeseries
            for isim in range(len(self.therps_empty.app_rates)):
                num_values_to_check = len(self.therps_empty.app_rates[isim]) + 2 #number of applications plus first and last timeseries elements
                if (self.therps_empty.day_out[isim][0] == 1):  #if first app day is first day of year
                    num_values_to_check = num_values_to_check - 1
                result[isim] = [0.] * num_values_to_check
                result[isim][0] = float(conc_timeseries[isim][0])  #first day of timeseries
                result[isim][-1] = float(conc_timeseries[isim][370])  #last day of timeseries
                num_values_to_check = len(self.therps_empty.app_rates[isim])
                if ((num_values_to_check) >= 1):
                    result_index = 1
                    for i in range(0 ,num_values_to_check):
                        if(self.therps_empty.day_out[isim][i] != 1):
                            series_index = self.therps_empty.day_out[isim][i] - 1
                            result[isim][result_index] = float(conc_timeseries[isim][series_index])
                            result_index = result_index + 1
                npt.assert_allclose(result[isim][:],expected_results[isim][:],rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            for isim in range(len(self.therps_empty.app_rates)):
                tab1 = [result[isim], expected_results[isim]]
                print(tabulate(tab1, headers='keys', tablefmt='rst'))
        return


    def test_eec_diet_max(self):
        """
        combined unit test for methods eec_diet_max & eec_diet_timeseries;

        * this test calls eec_diet_max, which in turn calls eec_diet_timeseries (which produces
          concentration timeseries), which in turn calls conc_initial and conc_timestep
        * eec_diet_max processes the timeseries and extracts the maximum values

        * this test tests both eec_diet_max & eec_diet_timeseries together (ok, so this violates the exact definition
        * of 'unittest', get over it)
        * the assertion check is that the maximum values from the timeseries match expectations
        * this assumes that for the maximums to be 'as expected' then the timeseries are as well
        * note: the 1st application day ('day_out') for the 2nd model simulation run is set to 0 here
        * to make sure the timeseries processing works when an application occurs on 1st day of year
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([1.734, 145.3409, 0.702], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            self.therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            self.therps_empty.food_multiplier_init_sg = 15.
            self.therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            self.therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            self.therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            #self.therps_empty.num_apps = [0] * len(self.therps_empty.app_rates) #set length of num_apps list (no longer needed)
            for i in range(len(self.therps_empty.app_rates)):
                self.therps_empty.num_apps[i] = len(self.therps_empty.app_rates[i])
                num_app_days[i] = len(self.therps_empty.day_out[i])
                assert (self.therps_empty.num_apps[i] == num_app_days[i]), 'series of app-rates and app_days do not match'

            result = self.therps_empty.eec_diet_max(self.therps_empty.food_multiplier_init_sg)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_eec_dose_mamm(self):
        """
        unit test for function eec_dose_mamm;
        internal calls to 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'eec_dose_mamm' are correctly implemented
        * methods called inside of 'eec_dose_mamm' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
       """
        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.36738, 124.3028, 0.989473], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')
        try:
            self.therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            self.therps_empty.food_multiplier_init_sg = 15.
            self.therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            self.therps_empty.aw_herp_sm = pd.Series([1.5, 2.5, 3.0], dtype = 'float')
            self.therps_empty.bw_frog_prey_mamm = pd.Series([15., 35., 45.], dtype='float')
            self.therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')

             #specifying 3 different application scenarios of 1, 4, and 2 applications
            self.therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            self.therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            for i in range(len(self.therps_empty.app_rates)):
                self.therps_empty.num_apps[i] = len(self.therps_empty.app_rates[i])
                num_app_days[i] = len(self.therps_empty.day_out[i])
                assert (self.therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = self.therps_empty.eec_dose_mamm(self.therps_empty.food_multiplier_init_sg, self.therps_empty.aw_herp_sm,
                                                self.therps_empty.bw_frog_prey_mamm, self.therps_empty.mf_w_mamm_2)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_arq_dose_mamm(self):
        """
        unit test for function arq_dose_mamm;
        internal calls to 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'arq_dose_mamm' are correctly implemented
        * methods called inside of 'arq_dose_mamm' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.0083319, 3.755716, 0.01906], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')
        try:
            self.therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            self.therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')
            self.therps_empty.ld50_bird = pd.Series([2000., 5., 45.], dtype = 'float')
            self.therps_empty.tw_bird_ld50 = pd.Series([180., 5., 45.], dtype = 'float')
            self.therps_empty.mineau_sca_fact = pd.Series([1.15, 1., 1.5], dtype = 'float')

            self.therps_empty.food_multiplier_init_sg = 240.
            self.therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')
            self.therps_empty.aw_herp_sm = pd.Series([1.5, 2.5, 3.0], dtype = 'float')
            self.therps_empty.bw_frog_prey_mamm = pd.Series([15., 35., 45.], dtype='float')

             #specifying 3 different application scenarios of 1, 4, and 2 applications
            self.therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            self.therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            for i in range(len(self.therps_empty.app_rates)):
                self.therps_empty.num_apps[i] = len(self.therps_empty.app_rates[i])
                num_app_days[i] = len(self.therps_empty.day_out[i])
                assert (self.therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = self.therps_empty.arq_dose_mamm(self.therps_empty.food_multiplier_init_sg, self.therps_empty.aw_herp_sm,
                                                self.therps_empty.bw_frog_prey_mamm, self.therps_empty.mf_w_mamm_2)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_arq_diet_mamm(self):
        """
        unit test for function arq_diet_mamm;
        internal calls to 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'arq_diet_mamm' are correctly implemented
        * methods called inside of 'arq_diet_mamm' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)

        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.0266769, 20.81662, 0.0068823], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')
        try:
            self.therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            self.therps_empty.food_multiplier_init_sg = 15.
            self.therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')
            self.therps_empty.lc50_bird = pd.Series([125., 2500., 500.], dtype = 'float')
            self.therps_empty.bw_frog_prey_mamm = pd.Series([15., 35., 45.], dtype='float')
            self.therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')

             #specifying 3 different application scenarios of 1, 4, and 2 applications
            self.therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            self.therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            for i in range(len(self.therps_empty.app_rates)):
                self.therps_empty.num_apps[i] = len(self.therps_empty.app_rates[i])
                num_app_days[i] = len(self.therps_empty.day_out[i])
                assert (self.therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = self.therps_empty.arq_diet_mamm(self.therps_empty.food_multiplier_init_sg,
                                                self.therps_empty.bw_frog_prey_mamm, self.therps_empty.mf_w_mamm_2)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_crq_diet_mamm(self):
        """
        unit test for function crq_diet_mamm;
        internal calls to 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_diet_mamm' are correctly implemented
        * methods called inside of 'crq_diet_mamm' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')
        try:
            self.therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            self.therps_empty.food_multiplier_init_sg = 240.
            self.therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')
            self.therps_empty.noaec_bird = pd.Series([25., 100., 55.], dtype = 'float')
            self.therps_empty.bw_frog_prey_mamm = pd.Series([15., 35., 45.], dtype='float')
            self.therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')

             #specifying 3 different application scenarios of 1, 4, and 2 applications
            self.therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            self.therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            for i in range(len(self.therps_empty.app_rates)):
                self.therps_empty.num_apps[i] = len(self.therps_empty.app_rates[i])
                num_app_days[i] = len(self.therps_empty.day_out[i])
                assert (self.therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = self.therps_empty.crq_diet_mamm(self.therps_empty.food_multiplier_init_sg,
                                                self.therps_empty.bw_frog_prey_mamm, self.therps_empty.mf_w_mamm_2 )
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_crq_diet_tp(self):
        """
        unit test for function crq_diet_tp;  amphibian chronic dietary-based risk quotients for tp
        internal calls to : 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
        * methods called inside of 'crq_diet_tp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            self.therps_empty.food_multiplier_init_blp = 135.
            self.therps_empty.bw_frog_prey_herp = pd.Series([2.5, 15., 25.], dtype = 'float')
            self.therps_empty.awc_herp_sm = pd.Series([70., 85., 105.], dtype = 'float')
            self.therps_empty.noaec_bird = pd.Series([25., 100., 55.], dtype = 'float')
            self.therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            self.therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            self.therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            self.therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            for i in range(len(self.therps_empty.app_rates)):
                self.therps_empty.num_apps[i] = len(self.therps_empty.app_rates[i])
                num_app_days[i] = len(self.therps_empty.day_out[i])
                assert (self.therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = self.therps_empty.crq_diet_tp(self.therps_empty.food_multiplier_init_blp,
                                              self.therps_empty.bw_frog_prey_herp, self.therps_empty.awc_herp_sm)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_crq_diet_herp(self):
        """
        amphibian chronic dietary-based risk quotients


        unit test for function crq_diet_herp;  amphibian acute dietary-based risk quotients for tp
        internal calls to : 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
        * methods called inside of 'crq_diet_herp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            self.therps_empty.food_multiplier_init_blp = 135.
            self.therps_empty.noaec_bird = pd.Series([25., 100., 55.], dtype = 'float')
            self.therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            self.therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            self.therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            self.therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            for i in range(len(self.therps_empty.app_rates)):
                self.therps_empty.num_apps[i] = len(self.therps_empty.app_rates[i])
                num_app_days[i] = len(self.therps_empty.day_out[i])
                assert (self.therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = self.therps_empty.crq_diet_herp(self.therps_empty.food_multiplier_init_blp)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_arq_diet_tp(self):
        """
        unit test for function arq_diet_tp;  amphibian acute dietary-based risk quotients for tp
        internal calls to : 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included
                            'fi_herp'
        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
        * methods called inside of 'arq_diet_tp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            self.therps_empty.lc50_bird = pd.Series([125., 2500., 500.], dtype = 'float')
            self.therps_empty.food_multiplier_init_blp = 135.
            self.therps_empty.bw_frog_prey_herp = pd.Series([2.5, 15., 25.], dtype = 'float')
            self.therps_empty.awc_herp_sm = pd.Series([70., 85., 105.], dtype = 'float')
            self.therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            self.therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            self.therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            self.therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            for i in range(len(self.therps_empty.app_rates)):
                self.therps_empty.num_apps[i] = len(self.therps_empty.app_rates[i])
                num_app_days[i] = len(self.therps_empty.day_out[i])
                assert (self.therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = self.therps_empty.arq_diet_tp(self.therps_empty.food_multiplier_init_blp,
                                              self.therps_empty.bw_frog_prey_herp, self.therps_empty.awc_herp_sm)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_arq_diet_herp(self):
        """
        unit test for function arq_diet_herp;  amphibian acute dietary-based risk quotients
        internal calls to : 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
        * methods called inside of 'arq_diet_herp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            self.therps_empty.food_multiplier_mean_fp = 15.
            self.therps_empty.lc50_bird = pd.Series([125., 2500., 500.], dtype = 'float')
            self.therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            self.therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            self.therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            self.therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            for i in range(len(self.therps_empty.app_rates)):
                self.therps_empty.num_apps[i] = len(self.therps_empty.app_rates[i])
                num_app_days[i] = len(self.therps_empty.day_out[i])
                assert (self.therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = self.therps_empty.arq_diet_herp(self.therps_empty.food_multiplier_mean_fp)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_arq_dose_tp(self):
        """
        unit test for function arq_dose_tp; amphibian acute dose-based risk quotients for tp
        internal calls to : 'eec_dose_herp' --> 'fi_herp'  --> ;
                            'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included
                            'at_bird'
        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
        * methods called inside of 'arq_dose_tp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            self.therps_empty.food_multiplier_init_blp = 135.
            self.therps_empty.aw_herp_lg = pd.Series([200., 250., 300.], dtype = 'float')
            self.therps_empty.bw_frog_prey_herp = pd.Series([2.5, 15., 25.], dtype = 'float')
            self.therps_empty.awc_herp_sm = pd.Series([70., 85., 105.], dtype = 'float')
            self.therps_empty.awc_herp_md = pd.Series([105., 125., 145.], dtype = 'float')
            self.therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            self.therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            self.therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            self.therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            for i in range(len(self.therps_empty.app_rates)):
                self.therps_empty.num_apps[i] = len(self.therps_empty.app_rates[i])
                num_app_days[i] = len(self.therps_empty.day_out[i])
                assert (self.therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = self.therps_empty.arq_dose_tp(self.therps_empty.food_multiplier_init_blp,
                                              self.therps_empty.aw_herp_lg, self.therps_empty.bw_frog_prey_herp,
                                              self.therps_empty.awc_herp_sm, self.therps_empty.awc_herp_md)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_arq_dose_herp(self):
        """
        unit test for function arq_dose_herp; amphibian acute dose-based risk quotients
        internal calls to : 'eec_dose_herp' --> 'fi_herp'  --> ;
                            'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included
                            'at_bird'
        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
        * methods called inside of 'arq_dose_herp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            self.therps_empty.aw_herp_sm = pd.Series([1.5, 2.5, 3.0], dtype = 'float')
            self.therps_empty.awc_herp_sm = pd.Series([70., 85., 105.], dtype = 'float')
            self.therps_empty.food_multiplier_mean_blp = 45.
            self.therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            self.therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            self.therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            self.therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            for i in range(len(self.therps_empty.app_rates)):
                self.therps_empty.num_apps[i] = len(self.therps_empty.app_rates[i])
                num_app_days[i] = len(self.therps_empty.day_out[i])
                assert (self.therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = self.therps_empty.arq_dose_herp(self.therps_empty.aw_herp_sm, self.therps_empty.awc_herp_sm,
                                                self.therps_empty.food_multiplier_mean_blp)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_eec_dose_tp(self):
        """
        unit test for function eec_dose_tp; amphibian Dose based eecs for terrestrial
        internal calls to : "fi_herp";
                            'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
        * methods called inside of 'eec_dose_tp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            self.therps_empty.food_multiplier_mean_blp = 45.
            self.therps_empty.aw_herp_md = pd.Series([20., 40., 60.], dtype = 'float')
            self.therps_empty.bw_frog_prey_herp = pd.Series([2.5, 15., 25.], dtype = 'float')
            self.therps_empty.awc_herp_sm = pd.Series([70., 85., 105.], dtype = 'float')
            self.therps_empty.awc_herp_md = pd.Series([105., 125., 145.], dtype = 'float')
            self.therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            self.therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            self.therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            self.therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            for i in range(len(self.therps_empty.app_rates)):
                self.therps_empty.num_apps[i] = len(self.therps_empty.app_rates[i])
                num_app_days[i] = len(self.therps_empty.day_out[i])
                assert (self.therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = self.therps_empty.eec_dose_tp(self.therps_empty.food_multiplier_mean_blp,
                                              self.therps_empty.aw_herp_md, self.therps_empty.bw_frog_prey_herp,
                                              self.therps_empty.awc_herp_sm, self.therps_empty.awc_herp_md)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_eec_dose_herp(self):
        """
        unit test for function eec_dose_herp; amphibian Dose based eecs
        internal calls to : "fi_herp";
                            'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
        * methods called inside of 'eec_dose_herp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            self.therps_empty.aw_herp_sm = pd.Series([1.5, 2.5, 3.0], dtype = 'float')
            self.therps_empty.awc_herp_sm = pd.Series([70., 85., 105.], dtype = 'float')
            self.therps_empty.food_multiplier_init_blp = 135.
            self.therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            self.therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            self.therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            self.therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            for i in range(len(self.therps_empty.app_rates)):
                self.therps_empty.num_apps[i] = len(self.therps_empty.app_rates[i])
                num_app_days[i] = len(self.therps_empty.day_out[i])
                assert (self.therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = self.therps_empty.eec_dose_herp(self.therps_empty.aw_herp_sm, self.therps_empty.awc_herp_sm,
                                                self.therps_empty.food_multiplier_init_blp)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_eec_diet_tp(self):
        """

        unit test for function eec_diet_tp; Dietary terrestrial phase based eecs
        internal calls to : "fi_herp";
                            'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
        * methods called inside of 'eec_diet_tp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            self.therps_empty.food_multiplier_mean_sg = 240.
            self.therps_empty.bw_frog_prey_herp = pd.Series([2.5, 15., 25.], dtype = 'float')
            self.therps_empty.awc_herp_sm = pd.Series([70., 85., 105.], dtype = 'float')
            self.therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            self.therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            self.therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            self.therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            for i in range(len(self.therps_empty.app_rates)):
                self.therps_empty.num_apps[i] = len(self.therps_empty.app_rates[i])
                num_app_days[i] = len(self.therps_empty.day_out[i])
                assert (self.therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = self.therps_empty.eec_diet_tp(self.therps_empty.food_multiplier_mean_sg,
                                              self.therps_empty.bw_frog_prey_herp, self.therps_empty.awc_herp_sm)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_eec_diet_mamm(self):
        """
        unit test for function eec_diet_mamm; Dietary_mammal based eecs
        internal calls to : "fi_mamm";
                            'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
        * methods called inside of 'eec_diet_mamm' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """
        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            self.therps_empty.food_multiplier_mean_sg = 240.
            self.therps_empty.bw_frog_prey_mamm = pd.Series([15., 35., 45.], dtype='float')
            self.therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')
            self.therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            self.therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            self.therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            self.therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            for i in range(len(self.therps_empty.app_rates)):
                self.therps_empty.num_apps[i] = len(self.therps_empty.app_rates[i])
                num_app_days[i] = len(self.therps_empty.day_out[i])
                assert (self.therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = self.therps_empty.eec_diet_mamm(self.therps_empty.food_multiplier_mean_sg,
                                                self.therps_empty.bw_frog_prey_mamm, self.therps_empty.mf_w_mamm_2)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
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