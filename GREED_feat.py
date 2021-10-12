import os
from entropy.entropy_cal import video_process
from entropy.entropy_temporal_pool import entropy_temporal_pool
import numpy as np

def greed_feat(args):
    dist_path = args.dist_path
    ref_path = args.ref_path
    
    filt = args.temp_filt
    num_levels = 3
    
    height = args.height
    width = args.width
    gray = True
    ref_fps = args.ref_fps
    bit_depth = args.bit_depth
    
    if bit_depth == 8:
        multiplier = 1.5    #8 bit yuv420 video
    else:
        multiplier = 3      #10 bit yuv420 video
    
    if height < 1080:
        scales = [3,4]      #for lower than 1080p resolution
    elif height < 2160:
        scales = [4,5]      #1080p resolution
    else:
        scales = [5,6]      #for 4K resolution
    
    #calculate number of frames in reference and distorted    
    ref_stream = open(ref_path,'r')
    ref_stream.seek(0, os.SEEK_END)
    ref_filesize = ref_stream.tell()
    ref_T = int(ref_filesize/(height*width*multiplier))
    
    dist_stream = open(dist_path,'r')
    dist_stream.seek(0, os.SEEK_END)
    dist_filesize = dist_stream.tell()
    dist_T = int(dist_filesize/(height*width*multiplier))
    
    fps = args.dist_fps       #frame rate of distorted sequence
    
    #calculate spatial entropy
    ref_entropy = video_process(ref_path, width, height, bit_depth, gray, \
                                   ref_T, filt, num_levels, scales)
    dist_entropy = video_process(dist_path, width, height, bit_depth, gray, \
                                   dist_T, filt, num_levels, scales)
    pr_entropy = video_process('pseudo_reference.yuv', width, height, bit_depth, gray, \
                                   dist_T, filt, num_levels, scales)
    
    #delete pseudo reference video
    os.remove('pseudo_reference.yuv')
    
    #number of valid frames
    end_lim = dist_entropy['spatial_scale' + str(scales[0])].shape[-1]
    
    greed_feat = np.zeros(16,dtype=np.float32)
    for idx,scale_factor in enumerate(scales):
        if int(fps) != ref_fps:
            #Temporal Pooling of reference entropies to match the number of frames
            ref_entropy['spatial_scale' + str(scale_factor)] = \
            entropy_temporal_pool(ref_entropy['spatial_scale' + str(scale_factor)][None,:,:,:],\
                                       int(fps),ref_fps,end_lim)
            ref_entropy['temporal_scale' + str(scale_factor)] = \
            entropy_temporal_pool(ref_entropy['temporal_scale' + str(scale_factor)],\
                                              int(fps),ref_fps,end_lim)
        
    #    spatial entropy difference
        ent_diff_sp = np.abs(ref_entropy['spatial_scale' + str(scale_factor)] - \
                             dist_entropy['spatial_scale' + str(scale_factor)])
        if len(ent_diff_sp.shape) < 4:
            ent_diff_sp = ent_diff_sp[None,:,:,:]
        spatial_ent = np.mean(np.mean(ent_diff_sp[0,:,:,:],axis=0),axis=0)
        greed_feat[idx] = np.mean(spatial_ent)
        
    #     temporal entropy difference
        for freq in range(dist_entropy['temporal_scale' + str(scale_factor)].shape[0]):
            a = dist_entropy['temporal_scale' + str(scale_factor)][freq,:,:,:]
            b = pr_entropy['temporal_scale' + str(scale_factor)][freq,:,:,:]
            c = ref_entropy['temporal_scale' + str(scale_factor)][freq,:,:,:]
            
            ent_diff_temporal = np.abs(((1+np.abs(a - b))*(1+c)/(1+b)) - 1)
            temp_ent_frame = np.mean(np.mean(ent_diff_temporal,axis=0),axis=0)
            
            greed_feat[2*(freq+1)+idx] = np.mean(temp_ent_frame)
    
    return greed_feat