from __future__ import divisionimport loggingimport numpy as npimport osimport pandas as pdimport scipy.interpolate as interpfrom scipy import integratefrom scipy.optimize import curve_fitimport sqlalchemy_utils as sqluimport sys#find parent directory and import modelparentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))sys.path.append(parentddir)from base.uber_model import UberModel, ModelSharedInputsfrom agdrift_functions import AgdriftFunctionsclass AgdriftInputs(ModelSharedInputs):    """    Input class for Agdrift.    """    def __init__(self):        """Class representing the inputs for TerrPlant"""        super(AgdriftInputs, self).__init__()        self.application_rate = pd.Series([], dtype="float")        self.application_method = pd.Series([], dtype="object")        self.drop_size = pd.Series([], dtype="object")        self.ecosystem_type = pd.Series([], dtype="object")        self.boom_height = pd.Series([], dtype="object")        self.airblast_type = pd.Series([], dtype="object")        self.aquatic_body_type = pd.Series([], dtype="object")        self.terrestrial_field_type = pd.Series([], dtype="object")        self.user_pond_width = pd.Series([], dtype="float")        self.user_pond_depth = pd.Series([], dtype="float")        self.user_wetland_width = pd.Series([], dtype="float")        self.user_wetland_depth = pd.Series([], dtype="float")        self.user_terrestrial_width = pd.Series([], dtype="float")        self.calculation_input = pd.Series([], dtype="object")        self.downwind_distance = pd.Series([], dtype="float")        self.user_frac_applied = pd.Series([], dtype="float")        self.user_avg_dep_gha = pd.Series([], dtype="float")        self.user_avg_dep_lbac = pd.Series([], dtype="float")        self.user_avg_conc_ngl = pd.Series([], dtype="float")        self.user_avg_dep_mgcm2 = pd.Series([], dtype="float")class AgdriftOutputs(object):    """    Output class for Agdrift.    """    def __init__(self):        """Class representing the outputs for Agdrift"""        super(AgdriftOutputs, self).__init__()        #self.out_nasae = pd.Series(name="out_nasae").astype("int")        self.out_sim_scenario_chk = pd.Series(name="out_sim_scenario_chk").astype("object")        self.out_sim_scenario_id = pd.Series(name="out_sim_scenario_id").astype("object")        self.out_interp_deposition = pd.Series(name="out_interp_deposition").astype("float")        #self.out_express_y = pd.Series(name="out_express_y").astype("object")        self.out_avg_dep_foa = pd.Series(name="out_avg_dep_foa").astype("float")        self.out_avg_dep_lbac = pd.Series(name="out_avg_dep_lbac").astype("float")        self.out_avg_dep_gha = pd.Series(name="out_avg_dep_gha").astype("float")        self.out_avg_waterconc_ngl = pd.Series(name="out_avg_waterconc_ngl").astype("float")        self.out_avg_field_dep_mgcm = pd.Series(name="out_avg_field_dep_mgcm").astype("float")        self.out_area_width = pd.Series(name="out_default_width").astype("float")        self.out_area_length = pd.Series(name="out_default_length").astype("float")        self.out_area_depth = pd.Series(name="out_default_pond_depth").astype("float")class Agdrift(UberModel, AgdriftInputs, AgdriftOutputs, AgdriftFunctions):    """    Agdrift class to implement tier 1 air drift screening models.    """    def __init__(self, pd_obj, pd_obj_exp):        """Class representing the Agdrift model and containing all its methods"""        super(Agdrift, self).__init__()        self.pd_obj = pd_obj        self.pd_obj_exp = pd_obj_exp        self.pd_obj_out = None    def execute_model(self):        """        Callable to execute the running of the model:            1) Populate input parameters            2) Create output DataFrame to hold the model outputs            3) Run the model's methods to generate outputs            4) Fill the output DataFrame with the generated model outputs        """        self.populate_inputs(self.pd_obj)        self.pd_obj_out = self.populate_outputs()        self.run_methods()        self.fill_output_dataframe()        logging.info(self.pd_obj_out)        logging.info('executed agdrift')    def run_methods(self):        """        Controller method that runs all subroutines in sequence.        :return:        """        try:            self.set_global_constants()            self.create_additional_io_parameters()            self.create_deposition_curve()            self.execute_interpolations_integrations()        except:            logging.info("Unexpected error:", sys.exc_info()[0])            raise    def execute_interpolations_integrations(self):        # loop through simulations calculating necessary interopolations/integrations and units conversions        for i in range(self.num_simulations):            if 'Invalid' not in self.out_sim_scenario_chk[i]:  # process only valid simulation scenarios                # locate index of scenario that applies to this simulation                for j in range(self.num_scenarios):                    if self.out_sim_scenario_id[i] == self.scenario_name[j]:                        scenario_index = j                #intialize internal variable datatypes and set as nan                interp_deposition = avg_dep_foa = avg_dep_lbac = avg_dep_gha = avg_waterconc_ngl = \                                    avg_field_dep_mgcm = float('nan')                # determine area/length/depth of area of concern                self.out_area_width[i], self.out_area_length[i], self.out_area_depth[i] = self.determine_area_dimensions(i)                # set distance from edge of application area to user specified initial point of interest                downwind_distance_short = self.downwind_distance[i]                # call interpolation function for downwind distance short                interp_deposition = self.scenario_interp_func[scenario_index](downwind_distance_short)                # perform integration across areas and calculate relevant average water concentrations and aerial deposition rates                if (self.ecosystem_type[i] == 'Aquatic Assessment' or                        (self.ecosystem_type[i] == 'Terrestrial Assessment' and                                 self.terrestrial_field_type[i] == 'User Defined Terrestrial')):                    # set distance value to downwind side of area for which  integration is needed                    downwind_distance_long = downwind_distance_short + self.out_area_width[i]                    # check if distance (from edge of application area) to upwind edge of waterbody is <= 997 and that                    # self.out_area_width[i] >= 6.56 & <= 997                    # if these conditions are not met then invalidate this simulation (997 is the furthest distance for which deposition data is available)                    if (downwind_distance_short <= self.max_distance and self.out_area_width[i] <= self.max_distance and                                self.out_area_width[i] >= self.min_area_width):                        # integrate over distance from nearest to furthest downwind points of pond/wetland/field                        integration_result = integrate.romberg(self.scenario_interp_func[scenario_index],                                                               downwind_distance_short, downwind_distance_long)                        # calculate output variables                        avg_dep_foa = self.calc_avg_dep_foa(integration_result, self.out_area_width[i])                        avg_dep_lbac = self.calc_avg_dep_lbac(avg_dep_foa, self.application_rate[i])                        avg_dep_gha = self.calc_avg_dep_gha(avg_dep_lbac)                        # calculate water concentration for waterbody or area avg deposition rate for terrestrial area                        if (self.ecosystem_type[i] == 'Aquatic Assessment'):                            avg_waterconc_ngl = self.calc_avg_waterconc_ngl(avg_dep_lbac,                                                self.out_area_width[i], self.out_area_length[i], self.out_area_depth[i])                        elif (self.ecosystem_type[i] == 'Terrestrial Assessment'):                            avg_field_dep_mgcm = self.calc_avg_fielddep_mgcm(avg_dep_lbac)                    else:                        # set simulation check variable to invalid                        self.out_sim_scenario_chk[i] = self.out_sim_scenario_chk[i].replace('Valid', 'Invalid') + \                                                       ' Due to Distance Violation'                elif (self.ecosystem_type[i] == 'Terrestrial Assessment' and                              self.terrestrial_field_type[i] == 'EPA Defined Terrestrial'):                    # just interested in point deposition (no integration)                    # calculate output variables                    avg_dep_foa = interp_deposition  # simply the fraction of applied deposition value at the point of intesest                    avg_dep_lbac = self.calc_avg_dep_lbac(avg_dep_foa, self.application_rate[i])                    avg_dep_gha = self.calc_avg_dep_gha(avg_dep_lbac)                    avg_field_dep_mgcm = self.calc_avg_fielddep_mgcm(avg_dep_lbac)                if self.round:                    # round output variable values (and place in output variable series) so that they can be directly                    # compared to expected results (which were limited in terms of their output format from the OPP AGDRIFT                    # model interface (we don't have the AGDRIFT code so we cannot change the output format to                    # agree with this model                    if (interp_deposition > 1e-4):                        self.out_interp_deposition[i] = round(interp_deposition, 4)                    else:                        self.out_interp_deposition[i] = interp_deposition                    if (avg_dep_foa > 1e-4):                        self.out_avg_dep_foa[i] = round(avg_dep_foa, 4)                    else:                        self.out_avg_dep_foa[i] = avg_dep_foa                    if (avg_dep_lbac > 1e-4):                        self.out_avg_dep_lbac[i] = round(avg_dep_lbac, 4)                    else:                        self.out_avg_dep_lbac[i] = avg_dep_lbac                    if (avg_dep_gha > 1e-4):                        self.out_avg_dep_gha[i] = round(avg_dep_gha, 4)                    else:                        self.out_avg_dep_gha[i] = avg_dep_gha                    if (avg_waterconc_ngl > 1e-4):                        self.out_avg_waterconc_ngl[i] = round(avg_waterconc_ngl, 4)                    else:                        self.out_avg_waterconc_ngl[i] = avg_waterconc_ngl                    if (avg_field_dep_mgcm > 1e-4):                        self.out_avg_field_dep_mgcm[i] = round(avg_field_dep_mgcm, 4)                    else:                        self.out_avg_field_dep_mgcm[i] = avg_field_dep_mgcm                else:                    self.out_interp_deposition[i] = interp_deposition                    self.out_avg_dep_foa[i] = avg_dep_foa                    self.out_avg_dep_lbac[i] = avg_dep_lbac                    self.out_avg_dep_gha[i] = avg_dep_gha                    self.out_avg_waterconc_ngl[i] = avg_waterconc_ngl                    self.out_avg_field_dep_mgcm[i] = avg_field_dep_mgcm            else:                pass        return    def create_deposition_curve(self):        # load, process/filter, and create interpolation function for deposition data        for i in range(self.num_scenarios):            if (self.num_scenario_sims[i] > 0):  # only get data if scenario is included in 1 or more simulations                self.scenario_raw_data[i] = self.get_scenario_deposition_data(self.scenario_name[i], self.num_db_values)                # process raw data to remove blank values from distance and deposition arrays                self.scenario_distance_data[i], self.scenario_deposition_data[i] = self.filter_arrays(                    self.distances_temp, self.scenario_raw_data[i])  # always send in the original distance_temp array                # extend distance vs deposition curve data (done for all curves)                self.extend_dist_dep_curve(i)                # establish functions for deposition curve to facilitate interpolation and integration                self.scenario_interp_func[i] = interp.interp1d(self.scenario_distance_data[i],                                                           self.scenario_deposition_data[i], kind=self.interpolator)        return    def create_additional_io_parameters(self):        # determine if scenario description data combine to form a valid scenario (i.e., one for which deposition data exists)        self.out_sim_scenario_chk = pd.Series([], dtype='object')        self.validate_sim_scenarios()        # pull column names from sql database ((these names reflect scenario types)        self.column_names = self.get_column_names()  # distance and scenario names as identified as database columns        # -1 is to avoid counting the distance column as a scenario type        self.num_scenarios = len(self.column_names) - 1        # assign column names to appropriate variables (i.e., the distance and scenario names)        self.assign_column_names()        # scan simulation input data and define scenario ids (to match column names from sql database)        self.set_sim_scenario_id()        # assign list of simulations per scenario        # this is so we can execute the interpolator function generator once per scenario type        self.num_scenario_sims, self.scenario_sim_indices = self.list_sims_per_scenario()        # pull distance array values from sql database (we assume array applies to all scenarios)        self.distances_temp = self.get_distances(self.num_db_values)        # populate output variable arrays with default values        self.out_area_width = pd.Series(self.num_simulations * ['nan'], dtype='float')        self.out_area_length = pd.Series(self.num_simulations * ['nan'], dtype='float')        self.out_area_depth = pd.Series(self.num_simulations * ['nan'], dtype='float')        self.out_interp_deposition = pd.Series(self.num_simulations * ['nan'], dtype='float')        self.out_avg_dep_foa = pd.Series(self.num_simulations * ['nan'], dtype='float')        self.out_avg_dep_lbac = pd.Series(self.num_simulations * ['nan'], dtype='float')        self.out_avg_dep_gha = pd.Series(self.num_simulations * ['nan'], dtype='float')        self.out_avg_waterconc_ngl = pd.Series(self.num_simulations * ['nan'], dtype='float')        self.out_avg_field_dep_mgcm = pd.Series(self.num_simulations * ['nan'], dtype='float')        # initialize internal variables        self.scenario_raw_data = pd.Series(self.num_scenarios * [[]], dtype='float')        self.scenario_distance_data = pd.Series(self.num_scenarios * [[]], dtype='float')        self.scenario_deposition_data = pd.Series(self.num_scenarios * [[]], dtype='float')        self.scenario_interp_func = pd.Series(self.num_scenarios * ['NoFunction'], dtype='object')        return    def set_global_constants(self):        #set scenario database name, table name, and number of data points (all scenarios have equal number of data points)        #we only want to set this if it hasn't been set from the outside (e.g., for integration tests)        if hasattr(self, 'db_name'):            pass        else:            dir_path = os.path.dirname(os.path.abspath(__file__))            logging.info('current directory path is:')            logging.info(dir_path)            #self.db_name = '/Users/puruckertom/git/qed_ubertool/ubertool_ecorest/ubertool/ubertool/agdrift/sqlite_agdrift_distance.db'            #self.db_name = 'sqlite:///sqlite_agdrift_distance.db'            #self.db_name = 'sqlite:///sqlite_agdrift_distance.db'            self.db_name = 'sqlite:///Users/puruckertom/git/qed_ubertool/ubertool_ecorest/ubertool/ubertool/agdrift/sqlite_agdrift_distance.db'        if sqlu.database_exists(self.db_name):            logging.info('found agdrift database')        else:            logging.info('cannot find agdrift database')            dir_path = os.path.dirname(os.path.abspath(__file__))            logging.info('current directory path is:')            logging.info(dir_path)        # set database table name, and number of data points/rows (all scenarios have equal number of data points)        self.db_table = 'output'        self.num_db_values = 161        #set interpolation method for runs        self.interpolator = 'linear'        #self.interpolator = 'quadratic'        #self.interpolator = 'cubic'        #set method for extending distance vs deposition curve (True: use ln ln transform; False: use relative ln ln transfrom)        self.extend_ln_ln = False        #set whether to round output values (rounding used when direct comparison with AGDRIFT model outputs as presented in user interface)        #self.round = False        self.round = True        #set rounding degree        self.round_to = 1e-4        #set number of model run simulations to be performed (equal to the number of entries in any one of the input variables)        #used throughout code to specify number of times a piece of code should be executed (e.g., for loops)        self.num_simulations = len(self.application_rate)        #set standard width and length for ponds/wetlands/terrestrial fields        self.default_width = pd.Series([208.7],dtype='float')  #feet of width of EPA Defined Pond or Wetland        self.default_length = pd.Series([515.8],dtype='float') #feet of length of EPA Defined Pond or Wetland        #set standard depth for ponds and wetlands        # 2.0 m = 6.56168 feet        self.default_pond_depth = pd.Series([6.56],dtype='float')       #feet        self.default_wetland_depth = pd.Series([0.4921],dtype='float')  #feet        self.max_distance = 997.   #feet (this applies to both area_width and downwind distance to leading edge of pond/wetland/terrestrial area        self.distance_inc = 6.56   #feet        self.min_area_width = 6.56  #feet : incremental distance between points in deposition data        self.sqft_per_hectare = 107636.  #size of all water (ponds and wetlands) and fields (terrestrial) in square feet (user can modify width only)        self.acres_per_hectare = 2.471        self.sqft_per_acre = 43560.        self.cm2_per_ft2 = 929.03        self.gms_per_lb = 453.592        self.mg_per_gram = 1.e3        self.ng_per_gram = 1.e9        self.liters_per_ft3 = 28.3168        return