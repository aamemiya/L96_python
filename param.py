###
### Common experiment parameter
###

param_model = {}
param_model['dimension'] = 40
param_model['forcing'] = 8
param_model['dt'] = 0.005
param_model['amp_const_nature'] = 0
param_model['amp_const_model'] = 0

param_letkf = {}
param_letkf['obs_error'] = 1.0
param_letkf['obs_number'] = 40
param_letkf['localization_length_scale'] = 3
param_letkf['localization_length_cutoff'] = 5
param_letkf['inflation_factor'] = 1.05
param_letkf['missing_value'] = -9.99e8

param_exp = {}
param_exp['exp_length'] = 1000  ### test
#param_exp['exp_length'] = 30000 
param_exp['ensembles'] = 20
param_exp['expdir'] = './DATA/test'
param_exp['obs_type'] = 'obs_001'
param_exp['da_type'] = 'test'
param_exp['dt_nature'] = 0.05
param_exp['dt_obs'] = 0.05
param_exp['dt_assim'] = 0.05
param_exp['spinup_length'] = 2000
