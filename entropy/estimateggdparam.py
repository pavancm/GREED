import numpy as np
import scipy.special

gam = np.arange(0.2, 10, 0.001)

def ggd_features(vec):
    r_gam = (scipy.special.gamma(1/gam)*scipy.special.gamma(3/gam))\
    /((scipy.special.gamma(2/gam))**2)
    
    sigma_sq = np.mean(vec**2)
    sigma = np.sqrt(sigma_sq)
    E = np.mean(np.abs(vec))
    rho = sigma_sq/E**2
    pos = np.argmin(np.abs(rho - r_gam))
    gamparam = gam[pos]
    return gamparam,sigma

def cal_shape_kurtosis(kurt):
    gam = np.arange(0.2, 10, 0.001)
    r_gam = (scipy.special.gamma(5/gam)*scipy.special.gamma(1/gam))\
    /((scipy.special.gamma(3/gam))**2)
    pos = np.argmin(np.abs(kurt - r_gam))
    gamparam = gam[pos]
    return gamparam

def entropy_ggd(gam, sig):
    beta = sig*np.sqrt(scipy.special.gamma(1/gam)/scipy.special.gamma(3/gam))
    ent = (1/gam) - np.log(gam/(2*beta*scipy.special.gamma(1/gam)))
    return ent
