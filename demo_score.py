import argparse
import os
from libsvm.svmutil import svm_predict, svm_load_model
import scipy.io
from GREED_feat import greed_feat

def main(args):
    ref_path = args.ref_path
    
    height = args.height
    width = args.width
    
    ref_fps = args.ref_fps
    bit_depth = args.bit_depth
    if bit_depth == 8:
        pix_format = 'yuv420p'
    else:
        pix_format = 'yuv420p10le'
    
    fps = args.dist_fps       #frame rate of distorted sequence
    
    #Obtain pseudo reference video by frame dropping using ffmpeg
    cmd = 'ffmpeg -r '+ str(ref_fps) +' -pix_fmt ' + pix_format + ' -s ' + str(width) +\
    'x' + str(height) + ' -i '+ ref_path + ' -filter:v fps=fps=' +\
    str(fps) + ' pseudo_reference.yuv'
    os.system(cmd)
    
    GREED_feat = greed_feat(args)
    
    #load svm model
    if args.height < 1080:
        #low resoltuion model
        model = svm_load_model('model_params/' + args.temp_filt + '_lowres.model')
    else:
        #high resolution model
        model = svm_load_model('model_params/' + args.temp_filt + '.model')
    
    #load parameter of trained features
    feat_param = scipy.io.loadmat('model_params/' + args.temp_filt + '_params.mat')
    low = feat_param['low'][0,:];high = feat_param['high'][0,:]
    GREED_feat = (GREED_feat - low)/(high - low)
    
    #Predict score
    score,_,_ = svm_predict([0.0], GREED_feat[None,:], model,'-q')
    print(score)

def parse_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--ref_path', type=str, default='data/books_crf_0_120fps.yuv', \
                        help='Path to reference video', metavar='')
    parser.add_argument('--dist_path', type=str, default='data/books_crf_28_30fps.yuv', \
                        help='Path to distorted video', metavar='')
    parser.add_argument('--ref_fps', type=int, default=120, \
                        help='frame rate of reference video', metavar='')
    parser.add_argument('--dist_fps', type=int, default=30, \
                        help='frame rate of distorted video', metavar='')
    parser.add_argument('--height', type=int, default=1080, \
                        help='spatial height of the frame', metavar='')
    parser.add_argument('--width', type=int, default=1920, \
                        help='spatial width of the frame', metavar='')
    parser.add_argument('--bit_depth', type=int, default=8, \
                        help='8 bit or 10 bit video', metavar='')
    parser.add_argument('--temp_filt', type=str, default='bior22', \
                        help='temporal filter', metavar='')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    main(args)