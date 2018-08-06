'''
Runs the entire workflow, taking motion capture data (a .csv) and radar data (a binary file), 
aligns data, calculates backprojected image, deconvolutes image, and plots.  

@author: Mason + David 
'''
#Import required modules
from pulson440_unpack import unpack 
from read_files import read_radar_data, read_motion_data
from rcs import rcs
from data_align import align_data
from GeneralAlignedRangeTimeGraph import AlignedGraph 
from FastLinInt import FastBackProjection
from LinInt import BackProjection
from Deconvolution import deconvolute
from plotRTI import plotRTI
from helper_functions import linear_interp_nan
import pickle

#Converts motion and RADAR data to the right data structures
unpack("../Raw_Data/uavsar1flight8")

#Loads data from the RADAR
motion_data = read_motion_data("../Raw_Data/UAVSAR1Flight8.csv","UAVSAR1")
motion_data = linear_interp_nan(motion_data[1],motion_data[0])
radar_data = read_radar_data("data.pkl", 580, 0.3) #580, 0.30 is probably good

#Performs RCS correction
radar_data = rcs(radar_data)

#Plot RTI for radar_data
plotRTI(radar_data)
'''
#Set parameters
#Take motion_start and  motion_end from .tak file video
#Estimate radar_start from the plotRTI above, initially comment out code below
radar_start = 300 #Initial 500 380 for flight 6 300 for flight 7
motion_start = 3850 #5200 flight 6 3900 flight 7 2411 flight 8 
motion_end = 34129 #16400 flight 6 34129 flight 7 29126 flight 8 

#Aligns data
aligned_data = align_data(radar_data,motion_data,radar_start,motion_start, motion_end, 200, 4600) #100, 3500

#Plots aligned graph with known data point
AlignedGraph(aligned_data,radar_data, [[-0.254065627,	0.252586546,	2.662674582], [-0.264097265,	0.237835515,	-3.115790777]] ) #[[.942713,.1,1.019]] Final: [[-0.254065627,	0.252586546,	2.662674582], [-0.264097265,	0.237835515,	-3.115790777]]


#Calculates and plots BackProjected Image
#IntensityList = BackProjection(aligned_data,radar_data,[-4,0],[4,4],0.1)
IntensityList2 = FastBackProjection(aligned_data, radar_data, [-2.5,0],[1.5,2], 0.005)

#Deconvolutes image and plots images
Image = deconvolute(IntensityList2, IterationNumber = 3, LeftInterval = [-4,0], RightInterval = [4,4], PercentageMin = 1/20)


FinalDict = {'orig_sar_img': IntensityList2, 'proc_sar_img': Image, 'x_axis': arange(-4, 4+0.01,0.01), 'y-axis': arange(0, 4+0.01, 0.01)}
with open('UAVSAR1.pickle', 'wb') as handle:
    pickle.dump(FinalDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
'''