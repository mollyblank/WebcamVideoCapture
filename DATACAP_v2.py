# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 12:47:51 2018
Latest revision 11/15/18

@author: Molly Blank

THIS VERSION: 
    Runs as all one chunk - which is not ideal but there ya go
    
Downsides: 
    Doesn't crop the images or preview before capture 
    
Next version: 
    Include a checker or some sort of confirmation of the camera number and framing before going forward 

# conda install --channel https://conda.anaconda.org/menpo opencv3
    
"""
#%%   ENVIRONMENT AND VARIABLES 


# --- IMOPRT everything 
import time
import cv2
import pandas as pd
from datetime import datetime
import os

# (Not currently used)
#import imutils
import numpy as np
#import matplotlib.pyplot as plt


# ----- TUNABLE VARIABLES  -- Make most adjustments here
DAcamNum = 2    # Set which camera is which
scaleCamNum = 1
waitTimer = 2   # this is how long the clock will sit between loops             # Adjust as needed for drip rate 


#%% OPTIONAL ---- Check video feed 


cap = cv2.VideoCapture(1)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

#%% DATA CAPTURE ----------


# ----- DIRECTORIES 
# creates high level folder by date/time and sub-directories with DA vs. scale

dateHeader = time.strftime("%m.%d_%H.%M")
new_directory = os.path.join('C:/Users/Molly Blank/Google Drive/DripRate_Characterization/DataLogs/'+ dateHeader)
try:
    if not os.path.exists(new_directory):                                       # Will only make a folder if it isn't a duplicate                                        
        os.makedirs(new_directory)
except OSError:
    print ('Error: Creating directory')                                         # Throws an error if it can't make a high-level folder
 
new_DA_directory = os.path.join(new_directory + '/DAlogs')                      
os.makedirs(new_DA_directory)
new_scale_directory = os.path.join(new_directory + '/ScaleLogs')                # Sub-folders for DA and Scale image separation 
os.makedirs(new_scale_directory)

#%%


# ---- DATAFRAME AND TIMER START 

start_time = datetime.now()     # start the timer 
df = pd.DataFrame(np.nan, index=[], columns = ['CurrentTime', 'DAFileName', 'DAValue', 'ScaleFileName', 'ScaleValue'])


# ---- RUN CAMERAS 
DAcam = cv2.VideoCapture(DAcamNum)
DAcam.set(3,320)
DAcam.set(4,240)

scaleCam = cv2.VideoCapture(scaleCamNum)
scaleCam.set(3,320)
scaleCam.set(4,240)




#%%
print('Interrupt with CTRL + C to complete data capture')



# ----- INFINITE LOOP - capturing and log images/data - interrupt when ready 
try:
    while True:
        elapsed_time = datetime.now() - start_time 
        DA_filename = ('%d_DA.jpg' % elapsed_time.seconds)                      # Assign file names that correspond with the timecode in seconds
        Scale_filename = ('%d_Scale.jpg' % elapsed_time.seconds)                    
        
        ret1, tempDA = DAcam.read()                                             # read an image from the VideoCapture object 
        ret2, tempScale = scaleCam.read()
        
        cv2.imwrite(os.path.join(new_DA_directory, DA_filename), tempDA)        # write jpgs to file of the camera frame 
        cv2.imwrite(os.path.join(new_scale_directory, Scale_filename), tempScale)
        
        df = df.append({'CurrentTime': datetime.now() - start_time,             # load time and corresponding file names into the dataframe
                    'DAFileName': DA_filename, 
                    'ScaleFileName': Scale_filename}, ignore_index=True)
                    
        time.sleep(waitTimer) 
        
except KeyboardInterrupt:                                                       # Use CTRL + C to exit the loop 
    pass
    
df.to_csv((new_directory + '/timecodeSummary' + dateHeader + '.csv'))  
#print(df)









