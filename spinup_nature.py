import os
import numpy as np
import model 
import param

### config
nx  = param.param_model['dimension'] 
f   = param.param_model['forcing']
dt  = param.param_model['dt']
amp = param.param_model['amp_const_nature']
length = param.param_exp['spinup_length']
expdir = param.param_exp['expdir']

### spin up of coupled Lorenz96 system (nature run)

def spinup(inum):
  np.random.seed(inum)
  x0  = np.array(np.random.randn(nx),  dtype=np.float64)
  l96 = model.Lorenz96(nx,f,dt, init_x = x0, amp_const = amp)
  for i in range(length):
    l96.runge_kutta()
  l96.save_snap(expdir + '/spinup/init.nc')

os.system('mkdir -p ' +  expdir + '/spinup')
spinup(0)
