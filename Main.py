# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 21:41:16 2019

@author: Armi Tiihonen
"""
#from Color_plotting import plot_colors
from RGB_extractor import rgb_extractor
#from RGB_extractor_Xrite_CC import rgb_extractor_Xrite_CC
from Color_operations import color_calibration_results, color_conversion_results, plot_colors
from Video import save_as_video
import os
import pandas as pd
import numpy as np
#import functools as ft
#import numpy.matlib as matlib
#from matplotlib import pyplot as plt
#from colormath.color_objects import LabColor, sRGBColor
#from colormath.color_conversions import convert_color

# Purpose:
# Saves the extracted rgb or lab data.
# Input:
# results: a list that is either a direct output of rgb_extractor() or is
#          assembled as [sample, sample_percentiles_lo, sample_percentiles_hi,
#          CC, times, fig_CC, fig_samples]
# colorspace: input either 'RGB' or 'Lab'
# calibrated: input either 0 (raw data) or 1 (color calibrated data)
# sample_description: string descriptions of each sample
# results_folder: Folder to which the code saves the result files.
def save_results(results, colorspace, calibrated, sample_description, results_folder):

    sample = results[0]
    sample_percentiles_lo = results[1]
    sample_percentiles_hi = results[2]
    CC = results[3]
    times = results[4]
    fig_CC = results[5]
    fig_samples = results[6]

    folderpath = ''
    if colorspace == 'RGB':
        if calibrated == 0:
            folderpath = results_folder + '/RGB/Raw'
            filename_body = ['_r.csv', '_g.csv', '_b.csv']
        elif calibrated == 1:
            folderpath = results_folder + '/RGB/Calibrated'
            filename_body = ['_r_cal.csv', '_g_cal.csv', '_b_cal.csv']
    elif colorspace == 'Lab':
        if calibrated == 0:
            folderpath = results_folder + '/Lab/Raw'
            filename_body = ['_Ll.csv', '_La.csv', '_Lb.csv']
        elif calibrated == 1:
            folderpath = results_folder + '/Lab/Calibrated'
            filename_body = ['_Ll_cal.csv', '_La_cal.csv', '_Lb_cal.csv']
            
    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
            
    np.savetxt(folderpath+'/sample'+filename_body[0], sample[:,:,0], delimiter=",")
    np.savetxt(folderpath+'/sample'+filename_body[1], sample[:,:,1], delimiter=",")
    np.savetxt(folderpath+'/sample'+filename_body[2], sample[:,:,2], delimiter=",")
    np.savetxt(folderpath+'/CC'+filename_body[0], CC[:,:,0], delimiter=",")
    np.savetxt(folderpath+'/CC'+filename_body[1], CC[:,:,1], delimiter=",")
    np.savetxt(folderpath+'/CC'+filename_body[2], CC[:,:,2], delimiter=",")
    np.savetxt(folderpath+'/sample_percentiles_lo'+filename_body[0], sample_percentiles_lo[:,:,0], delimiter=",")
    np.savetxt(folderpath+'/sample_percentiles_lo'+filename_body[1], sample_percentiles_lo[:,:,1], delimiter=",")
    np.savetxt(folderpath+'/sample_percentiles_lo'+filename_body[2], sample_percentiles_lo[:,:,2], delimiter=",")
    np.savetxt(folderpath+'/sample_percentiles_hi'+filename_body[0], sample_percentiles_hi[:,:,0], delimiter=",")
    np.savetxt(folderpath+'/sample_percentiles_hi'+filename_body[1], sample_percentiles_hi[:,:,1], delimiter=",")
    np.savetxt(folderpath+'/sample_percentiles_hi'+filename_body[2], sample_percentiles_hi[:,:,2], delimiter=",")
    np.savetxt(folderpath+"/times.csv", times, delimiter=",")
        
    fig_samples.savefig(folderpath+'/Samples.pdf')
    fig_CC.savefig(folderpath+'/Small_CC.pdf')
    
    #Let's save the details of the samples in a format that is compatible with
    #GPyOpt_Campaign.
    sample_holder_locations = sample_description[0]
    sample_ids = sample_description[1]
    sample_compositions = sample_description[2]
    elements = sample_description[3]
    comments = sample_description[4]

    # Let's form the string that will be printed into the graphs.
    name_composition = {}
    t=''
    for i in range(0,len(sample_holder_locations)):
        t = '#' + str(i) + '-' + sample_holder_locations[i] + '-' + sample_ids[i]  + '-'
        for j in range(0, len(elements)):
            t = t + elements[j] + str(sample_compositions[i][j]) + ' '
            name_composition.update( {i : t} )
    #Compositions dataframe, manually created from array
    df_compositions = pd.DataFrame(np.array(sample_compositions), columns=elements)
    #Add sample name to dataframe of compositions
    df_compositions.insert(loc=0, column='Sample', value=pd.Series(name_composition))
    #Add comment field to dataframe of compositions
    df_compositions.insert(loc=0, column='Comments', value=pd.Series(comments))
    
    df_compositions.to_csv(folderpath+'/Samples.csv')
    
    return (None)

###############################################################################
# The locations at the sample holder are presented in this order in the code.
# The same order holds through all the code.
sample_holder_locations = ['D1', 'C1', 'B1', 'A1',
                           'D2', 'C2', 'B2', 'A2',
                           'D3', 'C3', 'B3', 'A3',
                           'D4', 'C4', 'B4', 'A4',
                           'D5', 'C5', 'B5', 'A5',
                           'D6', 'C6', 'B6', 'A6',
                           'D7', 'C7', 'B7', 'A7']
#######################################################################

# FILL IN THE DETAILS OF THE AGING TEST:

# Fill in the sample ids in string format in the same order than what
# is presented in the variable 'sample_holder_locations' (see above).
# If the position has been left empty, give '-'.
sample_ids = ['0', '0', '0', '0',
              '0', '0', '0', '0',
              '0', '0', '0', '0',
              '0', '0', '0', '0',
              '0', '0', '0', '0',
              '0', '0', '0', '0',
              '0', '0', '0', '0']

# From which elements the samples are composed of?
elements = ['MAPbI', 'FAPbI', 'CsPbI']

# Fill in sample compositions.
# Give all zero values if the position is empty.
# Otherwise the compositions should sum up till 1. E.g., 10% of Cs, 50% of MA,
# 40% FA would be written as [0.1, 0.5, 0.4].
sample_compositions = np.array(
        [[1.00,0.00,0.00], [1.00,0.00,0.00], [1.00,0.00,0.00], [1.00,0.00,0.00],
        [1.00,0.00,0.00], [1.00,0.00,0.00], [1.00,0.00,0.00], [1.00,0.00,0.00],
        [1.00,0.00,0.00], [1.00,0.00,0.00], [1.00,0.00,0.00], [1.00,0.00,0.00],
        [1.00,0.00,0.00], [1.00,0.00,0.00], [1.00,0.00,0.00], [1.00,0.00,0.00],
        [1.00,0.00,0.00], [1.00,0.00,0.00], [1.00,0.00,0.00], [1.00,0.00,0.00],
        [1.00,0.00,0.00], [1.00,0.00,0.00], [1.00,0.00,0.00], [1.00,0.00,0.00],
        [1.00,0.00,0.00], [1.00,0.00,0.00], [1.00,0.00,0.00], [1.00,0.00,0.00]])

# Do you have any other free-form comments about the samples? Give '-' if you
# don't have any.
comments = ['-', '-', '-', '-',
            '-', '-', '-', '-',
            '-', '-', '-', '-',
            '-', '-', '-', '-',
            '-', '-', '-', '-',
            '-', '-', '-', '-',
            '-', '-', '-', '-']

# Give the path to the folder that contains the pictures (without ending
# slash). Use '/' for linux and '\' for Windows.
# Note: The code assumes that the data folder contains only pictures from the
# aging test. See the assumptions on the filenames, sample alignment, and
# color chart alignment from the Github repository
# ( https://github.com/PV-Lab/RGBanalysis ).
# Note 2: The code assumes that the (alphabetically) first picture in the
# folder has been taken of Xrite color chart (i.e., this picture will not be
# analyzed) and all the other pictures are taken of sample holder (these
# pictures will be analyzed). 
pic_folder = './Data/Example_aging_test/BMP'
# Give the name of the picture that has been taken taken of Xrite color chart.
pic_name_Xrite = '20190723160422.bmp'

# Give the path to the folder where the code saves the results:
results_folder = './Results/Example_aging_test'

# Give the settings for finding the samples and color chart patches from the
# pics.
# Crop boxes are defined as (left, upper, right, lower) edge of the crop
# box in the picture (in pixels).
# Offset regions are dropped from around the edges of each sample or color
# patch (to cut out uneven edges of the sample). They are defined as
# [[left,right],[upper,lower]] offset (in pixels).
#
# Note: Optimize the values using Color_operations.py if necessary. Further
# explanations in the same file.
# 
crop_box_scc = (575,39,575+223,39+150) # Small color chart
offset_scc = [[8,8],[8,8]]
crop_box_samples = (358,270,358+570,270+505) # Films on sample holder
offset_samples = [[17,17],[14,14]]
crop_box_Xrite = (435,430,435+480,430+310) # Xrite passport
offset_Xrite = [[20,20],[20,20]]

# How often do you want to print out previews of the cropped images to the
# console (every nth picture)? For short aging tests, value 1 is okay. Code
# runs faster if the value is large (250 is sufficient for long aging tests).
print_out_interval = 5

###############################################################################
# COMPUTATION
# Extract color data, perform color calibration, and save the results.

# Rounding. Here, we assume that the sum of the compositional elements is
# exactly 1 (100%) with resolution of 0.01 (1%). This does not necessarily hold
# for other projects, in which case it should be commented out.
for i in range(0,len(sample_compositions)):
    if (np.sum(sample_compositions[i]) != 1) & (np.sum(sample_compositions[i]) != 0):
        sample_compositions[i] = np.round(sample_compositions[i]/np.sum(
                sample_compositions[i]),2)
        

sample_description = [sample_holder_locations, sample_ids, sample_compositions,
                      elements, comments]

# THE RESULTS in rgb color space (no color calibration)
results_rgb = rgb_extractor(pic_folder, crop_box_samples, offset_samples,
                            crop_box_scc, offset_scc, print_out_interval)
save_results(results_rgb, 'RGB', 0, sample_description, results_folder)
# Output explained: 
# results_rgb = [sample_rgb, sample_rgb_percentiles_lo,
# sample_rgb_percentiles_hi, CC_rgb, times, fig_CC_rgb, fig_samples_rgb]
# - sample_rgb[samples 0...27][times 0...][0:R/1:G/2:B]: rgb values of each
#   sample at each moment
# - sample_rgb_percentiles_lo: lower percentiles of each sample at each moment,
#   same format as above 
# - sample_rgb_percentiles_hi: higher percentiles of each sample at each moment,
#   same format as above 
# - CC_rgb[color patches 0...23][times 0...][0:R/1:G/2:B]: rgb values of each
#   color patch in the small reference color chart at each moment
# - times[times 0...]: each sampling moment (minutes after the beginning of the
#   aging test; that is the time defined in the filename of the first picture)
# - fig_CC_rgb: a plot about rgb values vs time in each color patch of the
#   small color chart
# - fig_samples_rgb: a plot about rgb values vs time in each sample
# - picfiles: filenames in the same order than the data is

# Let's convert these to Lab (no color calibration)
results_lab = color_conversion_results(results_rgb)
save_results(results_lab, 'Lab', 0, sample_description, results_folder)   

# Let's perform color calibration and save the data in both RGB and Lab
# formats.
[results_rgb_cal, results_lab_cal] = color_calibration_results(results_rgb,
    [pic_folder, pic_name_Xrite, crop_box_Xrite, offset_Xrite])    
save_results(results_rgb_cal, 'RGB', 1, sample_description, results_folder)   
save_results(results_lab_cal, 'Lab', 1, sample_description, results_folder)   


###############################################################################
# COMPLEMENTARY VIDEO AND VISUALIZATION
# Keep this section commented out if you use Windows.

# Let's produce a video about the unedited pictures (i.e. corresponds to raw
# RGB data). This should be commented unless you have the necessary software installed.
save_as_video(pic_folder, crop_box_samples, crop_box_scc, 1, 'bmp', results_folder)


# The following part has not been tested for Windows.
# 
# Let's plot ans save pictures illustrating the crop boxes and the mean color
# of each sample (in raw and calibrated colors).
# Note: These pictures are saved for later checking if the crop boxes have been
# correct and confirming how the color calibration affects the colors.
crop_box_ill = crop_box_samples
offset_ill = offset_samples
save_to_folder_raw = results_folder + '/RGB/Raw/Cropped pics'
save_to_folder_cal = results_folder + '/RGB/Calibrated/Cropped pics'
if not os.path.exists(save_to_folder_raw):
        os.makedirs(save_to_folder_raw)
if not os.path.exists(save_to_folder_cal):
        os.makedirs(save_to_folder_cal)
savefig = 1
print_out = 0
for i in range(0,len(results_rgb[-1])):
    if (print_out_interval > 0) & (i % print_out_interval == 0):
        print_out = 1
        pic_path = results_rgb[-1][i]
        color_array_raw = results_rgb[0][:,i,:]
        color_array_cal = results_rgb_cal[0][:,i,:]
        #print('i',i)
        plot_colors(pic_path, crop_box_ill, offset_ill,
                color_array_raw, save_to_folder_raw, savefig, '', print_out)
        plot_colors(pic_path, crop_box_ill, offset_ill,
                color_array_cal, save_to_folder_cal, savefig, '', print_out)
    else:
        print_out = 0
    
# Additionally, both series of pictures are saved in video format (only for
# Linux).
save_as_video(save_to_folder_raw, crop_box_samples, crop_box_scc, 0, 'jpg', results_folder + '/Raw_mean_colors')
save_as_video(save_to_folder_cal, crop_box_samples, crop_box_scc, 0, 'jpg', results_folder + '/Calibrated_mean_colors')


