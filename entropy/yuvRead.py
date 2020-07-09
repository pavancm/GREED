import numpy as np
import cv2

def yuvRead_frame(stream, width, height, iFrame, bit_depth, gray, sz):
    if bit_depth == 8:
        stream.seek(iFrame*1.5*width*height)
        y_plane = np.fromfile(stream, dtype=np.uint8, count=width*height).\
        reshape((height, width))
        
        y_plane = y_plane.astype(np.float)
        y_plane = cv2.resize(y_plane, (int(width*sz),int(height*sz)),\
                             interpolation = cv2.INTER_AREA)
        
        if not gray:
            u_plane = np.fromfile(stream, dtype=np.uint8, \
                                  count=(width//2)*(height//2)).\
                                  reshape((height//2, width//2)).\
                                  repeat(2, axis=0).repeat(2, axis=1)
            v_plane = np.fromfile(stream, dtype=np.uint8, \
                                  count=(width//2)*(height//2)).\
                                  reshape((height//2, width//2)).\
                                  repeat(2, axis=0).repeat(2, axis=1)
            u_plane = u_plane.astype(np.float)
            u_plane = cv2.resize(u_plane, (int(width*sz/2),int(height*sz/2)),\
                             interpolation = cv2.INTER_AREA)
            v_plane = v_plane.astype(np.float)
            v_plane = cv2.resize(v_plane, (int(width*sz/2),int(height*sz/2)),\
                             interpolation = cv2.INTER_AREA)
        else:
            u_plane = []
            v_plane = []
    else:
        stream.seek(iFrame*3*width*height)
        y_plane = np.fromfile(stream, dtype=np.uint16, count=width*height).\
        reshape((height, width))
        
        y_plane = y_plane.astype(np.float)
        y_plane = cv2.resize(y_plane, (int(width*sz),int(height*sz)),\
                             interpolation = cv2.INTER_AREA)
        
        if not gray:
            u_plane = np.fromfile(stream, dtype=np.uint16, \
                                  count=(width//2)*(height//2)).\
                                  reshape((height//2, width//2)).\
                                  repeat(2, axis=0).repeat(2, axis=1)
            v_plane = np.fromfile(stream, dtype=np.uint16, \
                                  count=(width//2)*(height//2)).\
                                  reshape((height//2, width//2)).\
                                  repeat(2, axis=0).repeat(2, axis=1)
            u_plane = u_plane.astype(np.float)
            u_plane = cv2.resize(u_plane, (int(width*sz/2),int(height*sz/2)),\
                             interpolation = cv2.INTER_AREA)
            v_plane = v_plane.astype(np.float)
            v_plane = cv2.resize(v_plane, (int(width*sz/2),int(height*sz/2)),\
                             interpolation = cv2.INTER_AREA)
        else:
            u_plane = []
            v_plane = []
    
    return y_plane,u_plane,v_plane