#___________ ____ ___ __ _ _ _
### MAIN
#___________ ____ ___ __ _ _ _
#______________________________________________________________________________
# %% imports

import os
import os.path
import glob
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from PIL import Image
from osgeo import ogr
# keras tensorflow etc are missing

then = time.time() # TIC
Image.MAX_IMAGE_PIXELS = None # disarm PIL Decompression Bomb Error

#___________________________________________________________________________________________________
# %% user_input
# MAX IS 5 by 5 degree bbox!
UL_LON = 40
UL_LAT = 40
LR_LON = 45
LR_LAT = 35
#___________________________________________________________________________________________________
# %% clean_up previous_run_remnants

remove_tiles_path = glob.glob('./output/*.csv')
for i1 in remove_tiles_path:
    os.remove(i1)

#___________________________________________________________________________________________________
# %% 0) get ptif and meta data from NASA
    
# use api to get data for bbox CHALLENGE #1
    
#___________________________________________________________________________________________________
# %% 1) image selection algorithm
    
# use algorithm to select best NAC images for the CNN CHALLENGE #1
 
#___________________________________________________________________________________________________
# %% 2) image ingestion algorithm
    
# use algorithm to download all NAC images + metadata from NASA and put everything in 'input' CHALLENGE #2
# USE FAKE LIST TO START
   
#___________________________________________________________________________________________________
# %% 3) build_lists
    
# list of all NAC images in input folder
image_list = glob.glob('./input/*.tif')

# list of all metadata files in input folder
# [NAC resolution, upper right LAT, upper right LON, lower right LAT, lower right LON, lower left LAT, lower left LON, upper left LAT, upper left LON] --> order used by LROC page
meta_list = glob.glob('./input/*.txt')

# sort both lists the same way = all elements are in the identical order (verify)

# loop through both lists - NOT YET IMPLEMENTED
for i1 in image_list:
for i2 in meta_list:
    print("LOOPING!")
    parent = plt.imread(i1)
    input = np.loadtxt(i2)

#______________________________________________________________________________
# %% 4) nac_tiling
    
    print("Tiling NAC. . .")
    # NACs are tiled here - NOT INCLUDED HERE
    print("NAC Tiling COMPLETE!")

#______________________________________________________________________________    
# %% 5) cnn_loop

    print("Running RetinaNet. . .")
    # run CNN to predict on tiles - NOT INCLUDED HERE
    # USE FAKE .npy TO START
    print("RetinaNet COMPLETE!")

#______________________________________________________________________________
# %% 6) coordinate_transform & final_output

    print("Running Coordinate Transformation. . .")
#___________________________________________________________________________________________________
# %% 6a) image_metadata
# CHALLENGE #2
# USE FAKE .npy TO START
# [NAC resolution, upper right LAT, upper right LON, lower right LAT, lower right LON, lower left LAT, lower left LON, upper left LAT, upper left LON] --> order used by LROC page

    parent_ul_lon = input[8]
    parent_ul_lat_orig = input[7]

    parent_ur_lon = input[2]
    parent_ur_lat_orig = input[1]

    parent_ll_lon = input[6]
    parent_ll_lat_orig = input[5]

    parent_lr_lon = input[4]
    parent_lr_lat_orig = input[3]

    pix = input[0] # NAC spatial resolution

    id = str(image_list[0]) # NAC image ID
    id = id[8:]
    id = id[:-4]

#___________________________________________________________________________________________________
# %% 6b) load_image_coordinates

    image_coord = np.load('./output/output_img_coord_02.npy') # load results of RetinaNet, always the identical name

    img_coord_split =np.hsplit(image_coord,6) # split loaded results for next steps
    for i7 in img_coord_split[0]:
        upper_left_x = img_coord_split[0]
    for i7 in img_coord_split[1]:
        upper_left_y = img_coord_split[1]
    for i7 in img_coord_split[2]:
        lower_right_x = img_coord_split[2]
    for i7 in img_coord_split[3]:
        lower_right_y = img_coord_split[3]
    for i7 in img_coord_split[4]:
        confidence = img_coord_split[4]
    for i7 in img_coord_split[5]:
        class_type = img_coord_split[5]
#___________________________________________________________________________________________________
# %% 6c) Latitude normalization
# bring lat to 0-180° range to avoid edge effects
    
    if parent_ul_lat_orig > 0:
        parent_ul_lat = parent_ul_lat_orig+90
    if parent_ur_lat_orig > 0:
        parent_ur_lat = parent_ur_lat_orig+90
    if parent_lr_lat_orig > 0:
        parent_lr_lat = parent_lr_lat_orig+90
    if parent_ll_lat_orig > 0:
        parent_ll_lat = parent_ll_lat_orig+90

    if parent_ul_lat_orig < 0:
        parent_ul_lat = 90-parent_ul_lat_orig*(-1)
    if parent_ur_lat_orig < 0:
        parent_ur_lat = 90-parent_ur_lat_orig*(-1)
    if parent_lr_lat_orig < 0:
        parent_lr_lat = 90-parent_lr_lat_orig*(-1)
    if parent_ll_lat_orig < 0:
        parent_ll_lat = 90-parent_ll_lat_orig*(-1)

#___________________________________________________________________________________________________
# %% 6d) Parent orientation
# System determination, does NAC cross -180-180 cut?
    
    if parent_ul_lon-parent_ur_lon > 300: # SPECIAL LON CASE
        system = 1;
    if parent_ul_lon-parent_ur_lon < -300: # SPECIAL LON CASE
        system = 1;
    
    if parent_ul_lon-parent_ur_lon < 300: # NORMAL LON CASE
        system = 2;
    if parent_ul_lon-parent_ur_lon > -300: # NORMAL LON CASE
        system = 2;

#___________________________________________________________________________________________________
# %% 6e) NAC ORIENTATION - NORMAL LONGITUDE CASE
    
    if system == 2:
        if parent_ul_lon < parent_ur_lon and parent_ul_lat > parent_ll_lat:
            subject = 1
            corner_ul_lon = parent_ul_lon
            corner_ur_lon = parent_ur_lon
            corner_ll_lon = parent_ll_lon
    
            corner_ul_lat = parent_ul_lat
            corner_ur_lat = parent_ur_lat
            corner_ll_lat = parent_ll_lat
        
        if parent_ul_lon < parent_ur_lon and parent_ul_lat < parent_ll_lat:
            subject = 3
            corner_ul_lon = parent_ul_lon
            corner_ur_lon = parent_ur_lon
            corner_ll_lon = parent_ll_lon
    
            corner_ul_lat = parent_ll_lat
            corner_ur_lat = parent_lr_lat
            corner_ll_lat = parent_ul_lat 

        if parent_ul_lon > parent_ur_lon and parent_ul_lat > parent_ll_lat:
            subject = 2
            corner_ul_lon = parent_ur_lon
            corner_ur_lon = parent_ul_lon
            corner_ll_lon = parent_lr_lon
    
            corner_ul_lat = parent_ul_lat
            corner_ur_lat = parent_ur_lat
            corner_ll_lat = parent_ll_lat

        if parent_ul_lon > parent_ur_lon and parent_ul_lat < parent_ll_lat:
            subject = 4
            corner_ul_lon = parent_ur_lon
            corner_ur_lon = parent_ul_lon
            corner_ll_lon = parent_lr_lon
    
            corner_ul_lat = parent_ll_lat
            corner_ur_lat = parent_lr_lat
            corner_ll_lat = parent_ul_lat

#___________________________________________________________________________________________________
# %% 6f) NAC ORIENTATION - SPECIAL LONGITUDE-BORDER CASE
        
    if system == 1:
        if parent_ul_lon < parent_ur_lon and parent_ul_lat > parent_ll_lat:
            subject = 2
            corner_ul_lon = parent_ur_lon
            corner_ur_lon = parent_ul_lon
            corner_ll_lon = parent_lr_lon
    
            corner_ul_lat = parent_ul_lat
            corner_ur_lat = parent_ur_lat
            corner_ll_lat = parent_ll_lat

        if parent_ul_lon < parent_ur_lon and parent_ul_lat < parent_ll_lat:
            subject = 4
            corner_ul_lon = parent_ur_lon
            corner_ur_lon = parent_ul_lon
            corner_ll_lon = parent_lr_lon
    
            corner_ul_lat = parent_ll_lat
            corner_ur_lat = parent_lr_lat
            corner_ll_lat = parent_ul_lat 

        if parent_ul_lon > parent_ur_lon and parent_ul_lat > parent_ll_lat:
            subject = 1
            corner_ul_lon = parent_ul_lon
            corner_ur_lon = parent_ur_lon
            corner_ll_lon = parent_ll_lon
    
            corner_ul_lat = parent_ul_lat
            corner_ur_lat = parent_ur_lat
            corner_ll_lat = parent_ll_lat

        if parent_ul_lon > parent_ur_lon and parent_ul_lat < parent_ll_lat:
            subject = 3
            corner_ul_lon = parent_ul_lon
            corner_ur_lon = parent_ur_lon
            corner_ll_lon = parent_ll_lon
    
            corner_ul_lat = parent_ll_lat
            corner_ur_lat = parent_lr_lat
            corner_ll_lat = parent_ul_lat

#___________________________________________________________________________________________________
# %% 6g) Calculations
  
    dimensions = parent.shape      
    x_len = dimensions[1]
    y_len = dimensions[0]

    x_deg_len = corner_ur_lon-corner_ul_lon
    y_deg_len = corner_ul_lat-corner_ll_lat

    deg_per_pix_xdir = x_deg_len/x_len
    deg_per_pix_ydir = y_deg_len/y_len

# LON NAC rotation correction - appears not to help accuracy, subject to change!
    #lon_alpha_rad = math.atan(x_deg_len/y_deg_len)
    #x_len_corr = x_len * math.cos(lon_alpha_rad)

# LAT NAC rotation correction - appears not to help accuracy, subject to change!
    #lat_alpha_rad = math.atan(y_deg_len/x_deg_len)
    #y_len_corr = y_len * math.sin(lat_alpha_rad)

    #deg_per_pix_xdir = x_deg_len/x_len_corr
    #deg_per_pix_ydir = y_deg_len/y_len_corr

#___________________________________________________________________________________________________
# %% 6h) Detected rectangle location correction according to Subject & Real world coordinate determination
# -------> X
# |
# |
# |
# v
# Y

    lon_array = []
    lat_array = []

    try:
        for rec_ul_x, rec_ul_y in zip(upper_left_x, upper_left_y):
            #print(rec_ul_x, rec_ul_y)
    
            if subject == 1: # NO CHANGE
                rec_ul_x_corr = rec_ul_x
                rec_ul_y_corr = rec_ul_y

            if subject == 2: # X FLIP
                rec_ul_x_corr = x_len-rec_ul_x
                rec_ul_y_corr = rec_ul_y 

            if subject == 3: # Y FLIP
                rec_ul_x_corr = rec_ul_x
                rec_ul_y_corr = y_len-rec_ul_y   

            if subject == 4: # XY FLIP
                rec_ul_x_corr = x_len-rec_ul_x
                rec_ul_y_corr = y_len-rec_ul_y    

            rec_ul_lon = (rec_ul_x_corr*deg_per_pix_xdir)+corner_ul_lon
            rec_ul_lat = -1*(rec_ul_y_corr*deg_per_pix_ydir)+corner_ul_lat-90 # 90° correction lifted
    
            x_length_array = abs(lower_right_x - upper_left_x) # bbox x dimension
            y_length_array = abs(lower_right_y - upper_left_y) # bbox y dimension
    
            lon_array = np.append(lon_array, rec_ul_lon)
            lat_array = np.append(lat_array, rec_ul_lat)
    
        center_x_shift = (x_length_array * deg_per_pix_xdir)/2
        center_y_shift = (y_length_array * deg_per_pix_ydir)/2
    
        lon_array_center = (lon_array.T + center_x_shift.T).T
        lat_array_center = (lat_array.T + center_y_shift.T).T

    except NameError:
        print("No detections for CT 0.2!")

#___________________________________________________________________________________________________
# %% 6i) Additional calculations   
 
# bbox & boulder size estimation
    try:
        bbox_diameter = np.sqrt((x_length_array**2)+(y_length_array**2))
        boulder_diameter_pix = 0.059*bbox_diameter + 0.9102 # based on Bickel et al., 2018, modified for gen4
        boulder_diameter_meter = boulder_diameter_pix*pix
        x_length_array_meter = x_length_array * pix
        y_length_array_meter = y_length_array * pix
    except NameError:
        print("No detections for CT 0.2!")
        
# NAC acquisition time reconstruction
    # under construction

#___________________________________________________________________________________________________
# %% 6j) Detection extraction for re-training

    try: 
        aa = 0
        bb = 0
        cc = 0
        dd = 0

        parent_width = 5064 # ALWAYS TRUE

        upper_left_y_int = upper_left_y.astype(int)
        lower_right_y_int = lower_right_y.astype(int)
        upper_left_x_int = upper_left_x.astype(int)
        lower_right_x_int = lower_right_x.astype(int)

        # Parent width filter & removal
        width_filter_array = np.column_stack((upper_left_x_int, lower_right_x_int, upper_left_y_int, lower_right_y_int))
        width_filter_array[:,0][width_filter_array[:,0] > parent_width] = -1 # filter parent width
        width_filter_array[:,1][width_filter_array[:,1] > parent_width] = -1
        width_filter_array_T = width_filter_array.T
        width_filter_array_T_filtered = width_filter_array_T[:,width_filter_array_T[0]!=-1] # kick out > NAC parent width
        width_filter_array_T_filtered = width_filter_array_T_filtered[:,width_filter_array_T_filtered[1]!=-1]
        width_filter_array = width_filter_array_T_filtered.T

        del upper_left_y_int, lower_right_y_int, upper_left_x_int, lower_right_x_int

        upper_left_y_int = width_filter_array[:,2].astype(int)
        lower_right_y_int = width_filter_array[:,3].astype(int)
        upper_left_x_int = width_filter_array[:,0].astype(int)
        lower_right_x_int = width_filter_array[:,1].astype(int)

        upper_left_y_integer = np.array(upper_left_y_int)
        lower_right_y_integer = np.array(lower_right_y_int)
        upper_left_x_integer = np.array(upper_left_x_int)
        lower_right_x_integer = np.array(lower_right_x_int)

        upper_left_y_int = upper_left_y_integer.astype(int)
        lower_right_y_int = lower_right_y_integer.astype(int)
        upper_left_x_int = upper_left_x_integer.astype(int)
        lower_right_x_int = lower_right_x_integer.astype(int)

        if upper_left_y_int.size > 0:
            upper_left_y_int = np.column_stack(upper_left_y_int)
        else:
            upper_left_y_int = upper_left_y_int 
        upper_left_y_int = upper_left_y_int.T

        if lower_right_y_int.size > 0:
            lower_right_y_int = np.column_stack(lower_right_y_int)
        else:
            lower_right_y_int = lower_right_y_int
        lower_right_y_int = lower_right_y_int.T

        if upper_left_x_int.size > 0:
            upper_left_x_int = np.column_stack(upper_left_x_int)
        else:
            upper_left_x_int = upper_left_x_int 
        upper_left_x_int = upper_left_x_int.T

        if lower_right_x_int.size > 0:
            lower_right_x_int = np.column_stack(lower_right_x_int)
        else:
            lower_right_x_int = lower_right_x_int 
        lower_right_x_int = lower_right_x_int.T

        length1 = len(lower_right_x_int)

        #print(lower_right_x_int) # width debugging

        if lower_right_x_int.size > 0:
            for i11 in range(length1) :
                uly = upper_left_y_int[aa,0]
                lry = lower_right_y_int[bb,0]
                ulx = upper_left_x_int[cc,0]
                lrx = lower_right_x_int[dd,0]
                detection_crop = parent[uly:lry, ulx:lrx]
                current_time = str(int(time.time() * 10000))
        
                image_save = Image.fromarray(detection_crop)
                try:
                    image_save.save('./detections/0.2/' + id + '_crop_' + current_time + '_02.tif', 'TIFF')
                except SystemError:
                    print("Patch touches parent edge - cutout not possible!")
                aa = aa+1
                bb = bb+1
                cc = cc+1
                dd = dd+1 
    except NameError:
        print("No detections for CT 0.2!")
    
#___________________________________________________________________________________________________
# %% 6k) output
    try: 
        if lower_right_x_int.size > 0:
            length2 = len(boulder_diameter_meter)
            id_column = [id for x in range(length2)]
            pix_column = [pix for x in range(length2)]
            path = os.path.join('.','output','output_nac_id_02.csv')
            #np.save(path, id_column)
            np.savetxt(path, id_column, delimiter=',', fmt="%s")
            del length2
        else:
            print("No detections - no id csv for CT 0.2!")

        if lower_right_x_int.size > 0:
            output = np.column_stack((lon_array_center, lat_array_center, lon_array, lat_array, boulder_diameter_meter, x_length_array, y_length_array, x_length_array_meter, y_length_array_meter, upper_left_x, upper_left_y, lower_right_x, lower_right_y, confidence, pix_column))
            # output: [center LON, center LAT, upper_left LON, upper_left LAT, boulder_diameter meter, x_length in pixel, y_length in pixel, x_length in meter, y_length in meter, upper_left_x_img, upper_left_y_img, lower_right_x_img, lower_right_y_img, confidence, NAC resolution]
            path = os.path.join('.','output','output_map_coord_02.csv')
            #np.save(path, output)
            np.savetxt(path, output, delimiter=',', fmt='%1.5f')
        else:
            print("No detections - no output csv for CT 0.2!")
    except NameError:
        print("No detections for CT 0.2!")

    # ArcGIS Export, not used
    #LON_list = np.vstack((parent_ul_lon, parent_ur_lon, parent_ll_lon, parent_lr_lon))
    #LAT_list = np.vstack((parent_ul_lat_orig, parent_ur_lat_orig, parent_ll_lat_orig, parent_lr_lat_orig))
    #LON_end_list = np.roll(LON_list,-1)
    #LAT_end_list = np.roll(LAT_list,-1)
    #parent_output = np.column_stack((LON_list, LAT_list, LON_list, LAT_list, LON_end_list, LAT_end_list))
    # NAC footprint output for ArcGIS: [LON of all points, LAT of all points, start LON, start LAT, end LON, end LAT]
    #path = os.path.join('.','output','output_NAC_footprint.csv')
    #np.save(path, parent_output) 
    #np.savetxt(path, parent_output, delimiter=',', fmt='%1.5f')
    
    # QGIS Export, used
    # THIS NEEDS TO CONCATENATE EVERY LOOP!
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(parent_ll_lon, parent_ll_lat_orig)
    ring.AddPoint(parent_lr_lon, parent_lr_lat_orig)
    ring.AddPoint(parent_ur_lon, parent_ur_lat_orig)
    ring.AddPoint(parent_ul_lon, parent_ul_lat_orig)
    ring.AddPoint(parent_ll_lon, parent_ll_lat_orig)
    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(ring)
    polygon.FlattenTo2D()
    polygon.ExportToWkt()
    polygon_string = str(polygon)
    polygon_write = open('./output/output_NAC_footprint.csv','w')
    polygon_write.write(polygon_string)
    polygon_write.close()

    # THIS (below) NEEDS TO CONCATENATE EVERY LOOP!
    try:
        if lower_right_x_int.size > 0:
            csv1 = pd.read_csv('./output/output_nac_id_02.csv', header=None)
            csv2 = pd.read_csv('./output/output_map_coord_02.csv', header=None)
            merged = pd.concat([csv1, csv2], axis=1)
            # final output: [NAC ID, center LON, center LAT, upper_left LON, upper_left LAT, boulder_diameter meter, x_length in pixel, y_length in pixel, x_length in meter, y_length in meter, upper_left_x_img, upper_left_y_img, lower_right_x_img, lower_right_y_img, confidence, NAC resolution]
            path = os.path.join('.','output','output_merged_02.csv')
            merged.to_csv(path, sep=',', header=False, index=False)
        else:
            print("No detections - no output_merged csv for CT 0.2!")
    except NameError:
        print("No detections for CT 0.2!")

    print("Coordinate Transformation COMPLETE!")
    print("Final Output COMPLETE!")

#______________________________________________________________________________	
# %% 7) clean_up

    remove_tiles_path = glob.glob('./tiles/t_*.tif')
    for i0 in remove_tiles_path:
        os.remove(i0)

    #os.remove('./output/output_img_coord_02.npy') # commented because we don't actually loop
    #os.remove('./output/output_img_coord_03.npy')
    #os.remove('./output/output_img_coord_04.npy')
    #os.remove('./output/output_img_coord_05.npy')
    #os.remove('./output/output_img_coord_06.npy')
    #os.remove('./output/output_img_coord_07.npy')
    #os.remove('./output/output_img_coord_08.npy')

    if os.path.exists('./output/output_nac_id_02.csv'):
      os.remove('./output/output_nac_id_02.csv')
      os.remove('./output/output_map_coord_02.csv')
    else:
      print("Nothing to remove!")

    #if os.path.exists('./output/output_nac_id_03.csv'): # NOT INCLUDED HERE
      #os.remove('./output/output_nac_id_03.csv')
      #os.remove('./output/output_map_coord_03.csv')
    #else:
      #print("Nothing to remove!")
  
    #if os.path.exists('./output/output_nac_id_04.csv'): # NOT INCLUDED HERE
      #os.remove('./output/output_nac_id_04.csv')
      #os.remove('./output/output_map_coord_04.csv')
    #else:
      #print("Nothing to remove!")
  
    #if os.path.exists('./output/output_nac_id_05.csv'): # NOT INCLUDED HERE
      #os.remove('./output/output_nac_id_05.csv')
      #os.remove('./output/output_map_coord_05.csv')
    #else:
      #print("Nothing to remove!")
  
    #if os.path.exists('./output/output_nac_id_06.csv'): # NOT INCLUDED HERE
      #os.remove('./output/output_nac_id_06.csv')
      #os.remove('./output/output_map_coord_06.csv')
    #else:
      #print("Nothing to remove!")
  
    #if os.path.exists('./output/output_nac_id_07.csv'): # NOT INCLUDED HERE
      #os.remove('./output/output_nac_id_07.csv')
      #os.remove('./output/output_map_coord_07.csv')
    #else:
      #print("Nothing to remove!")
  
    #if os.path.exists('./output/output_nac_id_08.csv'): # NOT INCLUDED HERE
      #os.remove('./output/output_nac_id_08.csv')
      #os.remove('./output/output_map_coord_08.csv')
    #else:
      #print("Nothing to remove!")

    print("Clean up COMPLETE!")
    # loop over next NAC image in list
    
now = time.time() # TOC
print("ELAPSED TIME: ", now-then, " seconds")
print("END OF SCRIPT")