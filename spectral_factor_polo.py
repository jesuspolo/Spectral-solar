# -*- coding: utf-8 -*-

import pvlib
import numpy as np


def spectral_factor_polo(precipitable_water, airmass_absolute, aod500, aoi, altitude,
                              module_type=None, coefficients=None, albedo=0.2):
    """
    Estimation of spectral mismatch for BIPV application in vertical facades.
    
    SMM=
    

    Parameters
    ----------
    precipitable_water : numeric
        atmospheric precipitable water. [cm]

    airmass_absolute : numeric
        absolute (pressure-adjusted) airmass. [unitless]

    aod500 : numeric
        atmospheric aerosol optical depth at 500 nm. [unitless]
    
    aoi : numeric
        angle of incidence. [degrees]
    
    altitude: numeric
        altitude over sea level. [m]    
        
    module_type : str, optional
        One of the following PV technology strings from [1]_:

        * ``'cdte'`` - anonymous CdTe module.
        * ``'monosi'`` - anonymous sc-si module.
        * ``'cigs'`` - anonymous copper indium gallium selenide module.
        * ``'asi'`` - anonymous amorphous silicon module.
    albedo
        Ground albedo (default value if 0.2). [unitless]    

    coefficients : array-like, optional
        user-defined coefficients, if not using one of the default coefficient
        sets via the ``module_type`` parameter.

    Returns
    -------
    modifier: numeric
        spectral mismatch factor (unitless) which is multiplied
        with broadband irradiance reaching a module's cells to estimate
        effective irradiance, i.e., the irradiance that is converted to
        electrical current.

    References
    ----------
    Polo, J., Sanz-saiz, C., 2025. Development of spectral mismatch models
    for BIPV applications in building façades Abbreviations : Renew. Energy 245, 122820.
    https://doi.org/10.1016/j.renene.2025.122820
    
    """
    if module_type is None and coefficients is None:
        raise ValueError('Must provide either `module_type` or `coefficients`')
    if module_type is not None and coefficients is not None:
        raise ValueError('Only one of `module_type` and `coefficients` should '
                         'be provided')
    
    am_aoi=pvlib.atmosphere.get_relative_airmass(aoi)
    pressure=pvlib.atmosphere.alt2pres(altitude)
    am90=pvlib.atmosphere.get_absolute_airmass(am_aoi,pressure)
    Ram=am90/airmass_absolute
    
    _coefficients={}
    _coefficients['cdte']=(
        -0.0009,46.80,49.20,-0.87, 0.00041,0.053 )
    _coefficients['monosi']=(
        0.0027,10.34,9.48,0.307,0.00077,0.006 )
    _coefficients['cigs']=(
        0.0017,2.33,1.30,0.11,0.00098,-0.0177 )
    _coefficients['asi']=(
        0.0024,7.32,7.09,-0.72,-0.0013,0.089 )
    
    c={}
    c['asi']=(0.0056,-0.020,1.014)
    c['cigs']=(-0.0009,-0.0003,1)
    c['cdte']=(0.0021,-0.01,1.01)
    c['monosi']=(0,-0.003,1.0)
    
    
    if module_type is not None:
        coeff = _coefficients[module_type]
        c_albedo=c[module_type]
    else:
        coeff = coefficients
        c_albedo=(0.0,0.0,1.0) # 0.2 albedo assumed
        albedo=0.2
    
    
    smm=coeff[0]*Ram+coeff[1]/(coeff[2]+Ram**coeff[3])+coeff[4]/aod500+coeff[5]*np.sqrt(precipitable_water)
    # Ground albedo correction
      
    g=c_albedo[0]*(albedo/0.2)**2+c_albedo[1]*(albedo/0.2)+c_albedo[2]
    
        
    return g*smm
    
    
    
    
    