import numpy as np
import skimage.util
from skvideo.utils.mscn import gen_gauss_window
from scipy.stats import kurtosis
from entropy.estimateggdparam import cal_shape_kurtosis, entropy_ggd

def est_params_ggd(y, blk, sigma_nsq):
    """ 'ss' and 'ent' refer to the local variance parameter and the
        entropy at different locations of the subband
        y is a subband of the decomposition, 'blk' is the block size, 'sigma_nsq' is
        the neural noise variance """
    
    sizeim = np.floor(np.array(y.shape)/blk) * blk
    sizeim = sizeim.astype(np.int)
    y = y[:sizeim[0],:sizeim[1]].T
    
    temp = skimage.util.view_as_blocks(np.ascontiguousarray(y), (blk,blk))\
    .reshape(-1,blk*blk).T
    
    #window
    window = np.array(gen_gauss_window((blk-1)/2,blk/6)).reshape(blk,1)
    window = (window@window.T).ravel()
    #window = np.ones(blk*blk)/(blk*blk)
    ss = np.sqrt(np.sum((temp**2)*window[:,None], axis=0).\
    reshape((int(sizeim[1]/blk), int(sizeim[0]/blk))).T)
    ss = ss + sigma_nsq
    
    sigma_sq = np.var(y.ravel())
    multiplier = (sigma_sq/(sigma_sq + sigma_nsq))**2
    
    kurt_obs = kurtosis(y.ravel())
    kurt_noisy = kurt_obs*multiplier + 3
    
    gam = cal_shape_kurtosis(kurt_noisy)
    #Compute entropy
    ent = entropy_ggd(gam,ss)
    return ss, ent

def est_params_ggd_temporal(y, blk, sigma_nsq):
    """ 'temporal_ss' and 'temporal_ent' refer to the temporal local variance 
        parameter and the entropy at different locations of the subband
        y is a subband of the decomposition, 'blk' is the block size, 'sigma' is
        the neural noise variance """
    height,width = int(np.floor(y.shape[0]/blk)),int(np.floor(y.shape[1]/blk))
    num_frames = y.shape[3]
    
    temporal_ss = []
    temporal_ent = []
    for freq in range(y.shape[2]):
        vol = y[:,:,freq,:]
        
        ss = np.zeros((height,width,num_frames),dtype=np.float64)
        ent = np.zeros((height,width,num_frames),dtype=np.float64)
        for time_idx in range((vol.shape[2])):
            ss[:,:,time_idx], ent[:,:,time_idx] = \
            est_params_ggd(vol[:,:,time_idx], blk, sigma_nsq)
        
        temporal_ss.append(ss)
        temporal_ent.append(ent)
    return temporal_ss, temporal_ent
