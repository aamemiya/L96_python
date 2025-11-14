# Python_LETKF

Simple python code of LETKF experiment with Lorenz96 model

## Contents 

```
### parameter list
param.py    

### exec scripts
spinup_nature.py
spinup_model.py
nature.py
obsmake.py
exp.py

### core functions
letkf.py
model.py

```

## The model equation 

Lorenz96 model is an autonomous dynamical system with 1-dimensional cyclic domain.  
```
dx_k/dt =  x_k-1 (x_k+1 - x_k-2) - x_k + F + A * sin(2 \pi * k / K)  (k=1,2,...,K)
```
The controling parameters of this system are the domain size K and the forcing intensity F.  
The system becomes spatiotemporal chaos when F is sufficiently large.   
The normal setting is K=40 and F=8.  
The last term is an optional additional term to induce the spatial inhomogeneity. Set A=0 to omit the term in standard experiments.   

## Getting started 

### Spinup and generate the nature run 

First, create a "nature run" by integrating Lorenz96 model for sufficient period of time.  
Important parameters in `param.py`   
```
param_model['dimension'] = 40         ### K
param_model['forcing'] = 8            ### F 
param_model['dt'] = 0.005             ### integration time interval
param_exp['spinup_length'] = 2000     ### time steps of spinup 
param_exp['exp_length'] = 30000       ### time steps of nature run
param_exp['dt_nature'] = 0.05         ### output interval of nature run (must be integer * dt)
param_exp['expdir'] = './DATA/test'   ### output directory
```

Run `spinup_nature.py` and create(overwrite) the initial state file 'init.nc' in the directory specified in `param_exp['expdir']`/spinup/.   
Then run `nature.py`, which creates the time series of x following the Lorenz96 equation as 'nature.nc' in `param_exp['expdir']`.   
Note that the time interval of nature run `param_exp['dt_nature']` can be larger than `param_model['dt'] `.   

### Create observation 

Next, create a synthetic observation time series from `nature.nc`.   
Important parameters in `param.py`  
```
param_exp['dt_obs'] = 0.05             ### output interval of observation (must be integer * dt_nature)
param_exp['obstype'] = 'obs_001'       ### output directory of observation 
param.param_letkf['obs_error'] = 1.0   ### observation error standard deviation 
param.param_letkf['obs_number'] = 40   ### number of observable variables at each observation step
```

Run `obsmake.py` and create `obs.nc` in the directory `param_exp['expdir']`/`param_exp['obstype']`/ .  
At each observation time step, the fixed number of variables `param.param_letkf['obs_number']` are randomly selected and 'observed', with the additional random noise with standard deviation `param.param_letkf['obs_error']`, while rest of them are filled with missing values.  
By adjusting `param_exp['dt_obs']` you can create sparse observation time series from the same nature run.  

### Run Data Assimilation 

Before performing data assimilation with LETKF, prepare first-guess initial conditions. They are picked up randomly from the same attractor of Lorenz96 model.    
Specify the number of ensembles in `param.py`.   
```
param_exp['ensembles'] = 20            ### number of ensemble members 
```
Run `spinup_model.py` to create a set of initial condition nc files in `param_exp['expdir']`/spinup/.   

Now you are ready to perform a data assimilation experiment.   
Important parameters regarding LETKF in `param.py` are as follows.     
```
param_letkf['obs_error'] = 1.0                  ### observation error standard deviation 
param_letkf['localization_length_scale'] = 3    ### localization gaussian length scale 
param_letkf['localization_length_cutoff'] = 5   ### localization cutoff length
param_letkf['inflation_factor'] = 1.05          ### multiplicative inflation factor 
param_exp['da_type'] = 'test'                   ### output directory of data assimilation result  
param_exp['dt_assim'] = 0.05                    ### time interval of data assimilation (must be integer * dt_obs)
```
Run `exp.py` to perform data assimilation with LETKF. The result is stored in 'assim.nc' in the directory `param_exp['expdir']`/`param_exp['obstype']`/`param_exp['da_type']`. Modify `param_exp['da_type']` when you perform multiple data assimilation experiments with different setting using the same observation data.  

The result 'assim.nc' contains the following variables.  
```
> ncdump -h assim.nc
netcdf assim {
dimensions:
        x = 40 ;
        e = 20 ;
        t = UNLIMITED ; // (999 currently)
variables:
        double x(x) ;          ### location 
        double e(e) ;          ### ensemble
        double t(t) ;          ### time
        double va(t, e, x) ;   ### analyis 
        double vf(t, e, x) ;   ### forecast (first guess)
        double vam(t, x) ;     ### analysis ensemble mean
        double vfm(t, x) ;     ### forecast ensemble mean
}
```

## References 
About the Lorenz96 model:  
[Lorenz, 1996](http://eaps4.mit.edu/research/Lorenz/Predicability_a_Problem_2006.pdf)  
[Lorenz and Emanuel, 2003](https://journals.ametsoc.org/doi/full/10.1175/1520-0469%281998%29055%3C0399%3AOSFSWO%3E2.0.CO%3B2)  
About LETKF:  
[Hunt et al. 2007](https://www.sciencedirect.com/science/article/pii/S0167278906004647)  

## Acknowledgement 
The main part of the Lorenz96 LETKF code is originally developed by Shigenori Otsuka ([https://github.com/otsuka-shigenori/da_demo](https://github.com/otsuka-shigenori/da_demo))


