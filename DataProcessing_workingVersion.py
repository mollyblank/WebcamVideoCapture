# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 15:41:53 2018

@author: Molly Blank
"""

#%% Annotation 

# load a csv of interest - pull from the csv file name the folder that we're itnerested in (maybe GUI?)
import time
import cv2
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt
import tkinter as tk


# ---- CHOOSE the date that you want to open 
dataDateHeader = '11.16_16.21' 

# open file
#dataDirectory = os.path.join('C:/Users/Molly Blank/Google Drive/DripRate_Characterization/DataLogs/'+ data_dateHeader)
dataDirectory = os.path.join('D:/New folder/DripRate_Characterization/DataLogs/'+ dataDateHeader)
loadedData = pd.read_csv((dataDirectory + '/timecodeSummary' + dataDateHeader + '.csv'))  

# Takes the input of the dataframe and the current index, returns two jpgs with DA and scale images for that row
def imagePull(dataFrameDuJour, indexNumber):
    
    findDAFile = (dataDirectory + '/DAlogs/' + dataFrameDuJour.DAFileName[indexNumber])
    currentDAImage = cv2.imread(findDAFile)

    findscaleFile = (dataDirectory + '/ScaleLogs/' + dataFrameDuJour.ScaleFileName[indexNumber])
    currentScaleImage = cv2.imread(findscaleFile)

    return(currentDAImage, currentScaleImage)
 
# Shows you the DA image and the Scale Image sequentially and stores the output 
def annotateImage(DAimage, ScaleImage):
    plt.figure(1)
    plt.imshow(DAIMG)
    plt.show()
    DAValue = input('What is the value? ---  ')
    
    plt.figure(2)
    plt.imshow(SCALEIMG)
    plt.show()
    scaleValue = input('what is the value? ---  ')

    return(DAValue, scaleValue)
    
#%% ---- Working draft - testing Tkinter
    
index = 1
    
[DAIMG, SCALEIMG] = imagePull(loadedData, index)
    
window = tk.Tk()

window.title("Join")
window.geometry("600x600")
window.configure(background='grey')   

window.create_image(20,20, image = DAIMG)

window.mainloop()
    


#%%  ------- MAIN LOOP -------------
 
startingIndex = 0
(totalRows, columns) = loadedData.shape


for index in range(startingIndex, 3, 1):
     
    [DAIMG, SCALEIMG] = imagePull(loadedData, index)
    [DAValue, ScaleValue] = annotateImage(DAIMG, SCALEIMG)

    loadedData.DAValue[index] = DAValue
    loadedData.ScaleValue[index] = ScaleValue



#%% 
loadedData.to_csv((dataDirectory + '/timecodeSummary' + dataDateHeader + 'annotated.csv'))  




