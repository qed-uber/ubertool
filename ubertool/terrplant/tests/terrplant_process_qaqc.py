# needs to be run whenever the qaqc csv is updated

import os

csv_path = os.path.join(os.path.dirname(__file__),"terrplant_qaqc.csv")
csv_in = os.path.join(os.path.dirname(__file__),"terrplant_qaqc_in_transpose.csv")
csv_exp = os.path.join(os.path.dirname(__file__),"terrplant_qaqc_exp_transpose.csv")

import pandas as pd

pd_obj_inputs = pd.read_csv(csv_path, index_col=0, header=None, skiprows=1, skipfooter=66, engine='python')
pd_obj_inputs = pd_obj_inputs.drop(labels=pd_obj_inputs.columns[range(4)], axis=1)
pd_obj_inputs.index.name = None
pd_obj_inputs.columns -= 5
pd_obj_inputs_transposed = pd_obj_inputs.transpose()
pd_obj_inputs_transposed.to_csv(csv_in)

pd_obj_exp_out = pd.read_csv(csv_path, index_col=0, header=None, skiprows=53, engine='python')
pd_obj_exp_out = pd_obj_exp_out.drop(labels=pd_obj_exp_out.columns[range(4)], axis=1)
pd_obj_exp_out.index.name = None
pd_obj_exp_out.columns -= 5
pd_obj_exp_out_transposed = pd_obj_exp_out.transpose()
pd_obj_exp_out_transposed.to_csv(csv_exp)