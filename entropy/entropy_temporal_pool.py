import numpy as np

def entropy_temporal_pool(ent,fps,ref_fps,end_lim):
    """finding subsampling indices to get temporal entropy 
    averaging based on ffmpeg convention"""
    
    mean_ent = np.zeros((ent.shape[0],ent.shape[1],ent.shape[2],end_lim),\
                        dtype=np.float32)
    
    ik = np.zeros((end_lim,2),dtype=np.uint16)
    if fps == 24:
        ind = np.arange(3,ent.shape[3],5)
    elif fps == 30:
        ind = np.arange(2,ent.shape[3],4)
    elif fps == 60:
        ind = np.arange(1,ent.shape[3],2)
    elif fps == 82:
        """ Following ffmpeg convention, find pattern for obtaining 82 fps from 120 fps,
        first find odd pattern, then even pattern an merge at the end. This code snippet
        was obtained by testing the index of the frames dropped by ffmpeg"""
        odd_id = np.arange(20, end_lim, fps // 2)
        odd_pl = [odd_id[0]-13,odd_id[0]]
        [odd_pl.extend([odd_id[x]+15,odd_id[x]+28,odd_id[x]+41]) \
         for x in range(len(odd_id)-1)]
        odd_pl = np.array(odd_pl)
        
        #Use the above indices along with even pattern
        diff = np.ones(end_lim,dtype=int)
        diff[odd_pl] = 0
        diff_fin = [0]
        [diff_fin.append(2 - diff_fin[a] - diff[a+1]) for a in range(len(diff)-1)]
        diff_fin = np.array(diff_fin)
        diff_fin[diff_fin==-1] = 1;diff_fin[diff_fin == 2] = 0
        
        #Calculate final indices
        ind = [1]
        [ind.append(ind[i-1]+1+diff_fin[i]) for i in range(1,end_lim)]
        ind = np.array(ind)
    elif fps == 98:
        """Following ffmpeg convention, find pattern for obtaining 98 fps from 120 fps.
        This code snippet was obtained by testing the index of the frames dropped by 
        ffmpeg"""
        num_drop_frames = ent.shape[3] - end_lim
        odd_id = np.arange(6,num_drop_frames,11)
        dk = np.ones(num_drop_frames)
        dk[odd_id] = 0
        
        #find patterns in differences
        diff_fin = [0]
        [diff_fin.append(2 - diff_fin[a] - dk[a+1]) for a in range(len(dk)-1)]
        diff_fin = np.array(diff_fin)
        diff_fin[diff_fin==0] = 5
        diff_fin[diff_fin==1] = 4
        drop_ind = [3]
        [drop_ind.append(drop_ind[i]+diff_fin[i]) for i in range(len(diff_fin))]
        drop_ind = np.array(drop_ind)
        drop_ind = drop_ind[drop_ind < end_lim]
        coord_diff = np.zeros(end_lim)
        coord_diff[drop_ind.astype(int) - 1] = 1
        
        #Calculate final indices
        ind = [1]
        [ind.append(ind[i-1]+1+coord_diff[i]) for i in range(1,end_lim)]
        ind = np.array(ind)
        
    ik[:,1] = ind[:end_lim]
    ik[1:,0] = ik[:-1,1]
    
    for i in range(end_lim):
        for j in range(ent.shape[0]):
            vol = ent[j,:,:,ik[i,0]:ik[i,1]]
            mean_ent[j,:,:,i] = np.mean(vol,axis=2)
    
    return mean_ent