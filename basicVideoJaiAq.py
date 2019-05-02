# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 10:07:52 2019

@author: fc397
"""

# use this script to save a video using a JAI camera and the Harvester module


import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from harvesters.core import Harvester

# create harvester object
h = Harvester()
h.add_cti_file('C:/Program Files/JAI/SDK/bin/JaiUSB3vTL.cti')
h.update_device_info_list()
h.device_info_list[0]

# create image acquirer
ia = h.create_image_acquirer(0)
width = 2560
height = 1960
ia.device.node_map.Width.value, ia.device.node_map.Height.value = width, height
ia.device.node_map.PixelFormat.value = 'Mono8'

# create videowriter
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 25.0
out = cv2.VideoWriter('output.avi',fourcc, fps, (width,height))

# start image aq
ia.start_image_acquisition()
while(True):
    with ia.fetch_buffer() as buffer:
        # Let's create an alias of the 2D image component:
        component = buffer.payload.components[0]
    
        #     # Let's see the acquired data in 1D:
        #    _1d = component.data

        # Reshape the NumPy array into a 2D array:
        frame = component.data.reshape(component.height, component.width)
        
        # perform any operation on the image
        
        # convert to bgr for video saving
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR) 

        # save frames
        out.write(frame)
        
        # save snapshot
        #    cv2.imwrite('snap.jpg', frame)
        
        # show live acquisition
        cv2.imshow('frame',frame)
        
        # exit live aq with "q"-key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

out.release()
cv2.destroyAllWindows()
ia.stop_image_acquisition()
ia.destroy()
h.reset()
    
