# ___________ ____ ___ __ _ _ _
### MAIN
# ___________ ____ ___ __ _ _ _
# ______________________________________________________________________________
# %% imports

import glob
import os.path
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from osgeo import ogr
from metadata import MetaData
from boulder import Boulder

# keras tensorflow etc are missing

then = time.time()  # TIC
Image.MAX_IMAGE_PIXELS = None  # disarm PIL Decompression Bomb Error

# ___________________________________________________________________________________________________
# %% user_input
# MAX IS 5 by 5 degree bbox!
UL_LON = 40
UL_LAT = 40
LR_LON = 45
LR_LAT = 35
# ___________________________________________________________________________________________________
# %% clean_up previous_run_remnants

remove_tiles_path = glob.glob('./output/*.csv')
for i1 in remove_tiles_path:
    os.remove(i1)

# ___________________________________________________________________________________________________
# %% 0) get ptif and meta data from NASA

# use api to get data for bbox CHALLENGE #1

# ___________________________________________________________________________________________________
# %% 1) image selection algorithm

# use algorithm to select best NAC images for the CNN CHALLENGE #1

# ___________________________________________________________________________________________________
# %% 2) image ingestion algorithm

# use algorithm to download all NAC images + metadata from NASA and put everything in 'input' CHALLENGE #2
# USE FAKE LIST TO START

# ___________________________________________________________________________________________________
# %% 3) build_lists

# list of all NAC images in input folder
image_list = glob.glob('./input/*.tif')

# list of all metadata files in input folder
# [NAC resolution, upper right LAT, upper right LON, lower right LAT, lower right LON, lower left LAT, lower left LON, upper left LAT, upper left LON] --> order used by LROC page
meta_list = glob.glob('./input/*.txt')


def create_meta_obj(file_name):
    return MetaData(np.loadtxt(file_name))

#  image_coord = np.load(
#            './output/output_img_coord_02.npy')  # load results of RetinaNet, always the identical name
#        img_coord_split = np.hsplit(image_coord, 6)  # split loaded results for next steps

def create_boulder_obj(file_name):
    row_boulders = np.load('./output/output_img_coord_02.npy')
    row_boulders_split = np.vsplit(row_boulders, row_boulders.shape[0])
    boulders = []
    for rock in row_boulders_split:
        boulders.append(Boulder(rock))

    return boulders

def process_image(parent, meta_data):
    global remove_tiles_path
    # ______________________________________________________________________________
    # %% 4) nac_tiling
    print("Tiling NAC. . .")
    # NACs are tiled here - NOT INCLUDED HERE
    print("NAC Tiling COMPLETE!")
    # ______________________________________________________________________________
    # %% 5) cnn_loop
    print("Running RetinaNet. . .")
    # run CNN to predict on tiles - NOT INCLUDED HERE
    # USE FAKE .npy TO START
    print("RetinaNet COMPLETE!")
    # ______________________________________________________________________________
    # %% 6) coordinate_transform & final_output
    print("Running Coordinate Transformation. . .")
    # ___________________________________________________________________________________________________
    # %% 6a) image_metadata
    # CHALLENGE #2
    # USE FAKE .npy TO START
    # [NAC resolution, upper right LAT, upper right LON, lower right LAT, lower right LON, lower left LAT, lower left LON, upper left LAT, upper left LON] --> order used by LROC page
    image_id = str(image_list[0])  # NAC image ID
    image_id = image_id[8:]
    image_id = image_id[:-4]
    # ___________________________________________________________________________________________________
    # %% 6b) load_image_coordinates

    boulders = create_boulder_obj('./output/output_img_coord_02.npy')


    # ___________________________________________________________________________________________________
    # %% 6g) Calculations

    for rock in boulders:
        rock.calculateGlobalCoord(rock,meta_data,parent)
    # ___________________________________________________________________________________________________
    # %% 6h) Detected rectangle location correction according to Subject & Real world coordinate determination
    # -------> X
    # |
    # |
    # |
    # v
    # Y
    # ___________________________________________________________________________________________________
    # %% 6i) Additional calculations
    # bbox & boulder size estimation
        try:
            bbox_diameter = np.sqrt((rock.x_length_array ** 2) + (rock.y_length_array ** 2))
            boulder_diameter_pix = 0.059 * bbox_diameter + 0.9102  # based on Bickel et al., 2018, modified for gen4
            boulder_diameter_meter = boulder_diameter_pix * meta_data.pix
            x_length_array_meter = rock.x_length_array * meta_data.pix
            y_length_array_meter = rock.y_length_array * meta_data.pix
        except NameError:
            print("No detections for CT 0.2!")
    # NAC acquisition time reconstruction
    # under construction
    # ___________________________________________________________________________________________________
    # %% 6j) Detection extraction for re-training
        try:
            aa = 0
            bb = 0
            cc = 0
            dd = 0

            parent_width = 5064  # ALWAYS TRUE

            upper_left_y_int = rock.upper_left_y.astype(int)
            lower_right_y_int = rock.lower_right_y.astype(int)
            upper_left_x_int = rock.upper_left_x.astype(int)
            lower_right_x_int = rock.lower_right_x.astype(int)

            # Parent width filter & removal
            width_filter_array = np.column_stack(
            (upper_left_x_int, lower_right_x_int, upper_left_y_int, lower_right_y_int))
            width_filter_array[:, 0][width_filter_array[:, 0] > parent_width] = -1  # filter parent width
            width_filter_array[:, 1][width_filter_array[:, 1] > parent_width] = -1
            width_filter_array_T = width_filter_array.T
            width_filter_array_T_filtered = width_filter_array_T[:,
                                        width_filter_array_T[0] != -1]  # kick out > NAC parent width
            width_filter_array_T_filtered = width_filter_array_T_filtered[:, width_filter_array_T_filtered[1] != -1]
            width_filter_array = width_filter_array_T_filtered.T

            del upper_left_y_int, lower_right_y_int, upper_left_x_int, lower_right_x_int

            upper_left_y_int = width_filter_array[:, 2].astype(int)
            lower_right_y_int = width_filter_array[:, 3].astype(int)
            upper_left_x_int = width_filter_array[:, 0].astype(int)
            lower_right_x_int = width_filter_array[:, 1].astype(int)

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

        # print(lower_right_x_int) # width debugging

            if lower_right_x_int.size > 0:
                for i11 in range(length1):
                    uly = upper_left_y_int[aa, 0]
                    lry = lower_right_y_int[bb, 0]
                    ulx = upper_left_x_int[cc, 0]
                    lrx = lower_right_x_int[dd, 0]
                    detection_crop = parent[uly:lry, ulx:lrx]
                    current_time = str(int(time.time() * 10000))

                    image_save = Image.fromarray(detection_crop)
                    try:
                        image_save.save('./detections/0.2/' + image_id + '_crop_' + current_time + '_02.tif', 'TIFF')
                    except SystemError:
                        print("Patch touches parent edge - cutout not possible!")
                    aa = aa + 1
                    bb = bb + 1
                    cc = cc + 1
                    dd = dd + 1
        except NameError:
            print("No detections for CT 0.2!")
    # ___________________________________________________________________________________________________
    # %% 6k) output
    try:
        if lower_right_x_int.size > 0:
            length2 = len(boulder_diameter_meter)
            id_column = [image_id for x in range(length2)]
            pix_column = [meta_data.pix for x in range(length2)]
            path = os.path.join('.', 'output', 'output_nac_id_02.csv')
            # np.save(path, id_column)
            np.savetxt(path, id_column, delimiter=',', fmt="%s")
            del length2
        else:
            print("No detections - no id csv for CT 0.2!")

        if lower_right_x_int.size > 0:
            output = np.column_stack((lon_array_center, lat_array_center, lon_array, lat_array,
                                      boulder_diameter_meter, x_length_array, y_length_array, x_length_array_meter,
                                      y_length_array_meter, upper_left_x, upper_left_y, lower_right_x,
                                      lower_right_y, confidence, pix_column))
            # output: [center LON, center LAT, upper_left LON, upper_left LAT, boulder_diameter meter, x_length in pixel, y_length in pixel, x_length in meter, y_length in meter, upper_left_x_img, upper_left_y_img, lower_right_x_img, lower_right_y_img, confidence, NAC resolution]
            path = os.path.join('.', 'output', 'output_map_coord_02.csv')
            # np.save(path, output)
            np.savetxt(path, output, delimiter=',', fmt='%1.5f')
        else:
            print("No detections - no output csv for CT 0.2!")
    except NameError:
        print("No detections for CT 0.2!")
    # ArcGIS Export, not used
    # LON_list = np.vstack((meta_data.ul_lon, meta_data.ur_lon, meta_data.ll_lon, meta_data.lr_lon))
    # LAT_list = np.vstack((meta_data.ul_lat_orig, meta_data.ur_lat_orig, meta_data.ll_lat_orig, meta_data.lr_lat_orig))
    # LON_end_list = np.roll(LON_list,-1)
    # LAT_end_list = np.roll(LAT_list,-1)
    # parent_output = np.column_stack((LON_list, LAT_list, LON_list, LAT_list, LON_end_list, LAT_end_list))
    # NAC footprint output for ArcGIS: [LON of all points, LAT of all points, start LON, start LAT, end LON, end LAT]
    # path = os.path.join('.','output','output_NAC_footprint.csv')
    # np.save(path, parent_output)
    # np.savetxt(path, parent_output, delimiter=',', fmt='%1.5f')
    # QGIS Export, used
    # THIS NEEDS TO CONCATENATE EVERY LOOP!
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(meta_data.ll_lon, meta_data.ll_lat_orig)
    ring.AddPoint(meta_data.lr_lon, meta_data.lr_lat_orig)
    ring.AddPoint(meta_data.ur_lon, meta_data.ur_lat_orig)
    ring.AddPoint(meta_data.ul_lon, meta_data.ul_lat_orig)
    ring.AddPoint(meta_data.ll_lon, meta_data.ll_lat_orig)
    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(ring)
    polygon.FlattenTo2D()
    polygon.ExportToWkt()
    polygon_string = str(polygon)
    polygon_write = open('./output/output_NAC_footprint.csv', 'w')
    polygon_write.write(polygon_string)
    polygon_write.close()
    # THIS (below) NEEDS TO CONCATENATE EVERY LOOP!
    try:
        if lower_right_x_int.size > 0:
            csv1 = pd.read_csv('./output/output_nac_id_02.csv', header=None)
            csv2 = pd.read_csv('./output/output_map_coord_02.csv', header=None)
            merged = pd.concat([csv1, csv2], axis=1)
            # final output: [NAC ID, center LON, center LAT, upper_left LON, upper_left LAT, boulder_diameter meter, x_length in pixel, y_length in pixel, x_length in meter, y_length in meter, upper_left_x_img, upper_left_y_img, lower_right_x_img, lower_right_y_img, confidence, NAC resolution]
            path = os.path.join('.', 'output', 'output_merged_02.csv')
            merged.to_csv(path, sep=',', header=False, index=False)
        else:
            print("No detections - no output_merged csv for CT 0.2!")
    except NameError:
        print("No detections for CT 0.2!")
    print("Coordinate Transformation COMPLETE!")
    print("Final Output COMPLETE!")
    # ______________________________________________________________________________
    # %% 7) clean_up
    remove_tiles_path = glob.glob('./tiles/t_*.tif')
    for i0 in remove_tiles_path:
        os.remove(i0)
    # os.remove('./output/output_img_coord_02.npy') # commented because we don't actually loop
    # os.remove('./output/output_img_coord_03.npy')
    # os.remove('./output/output_img_coord_04.npy')
    # os.remove('./output/output_img_coord_05.npy')
    # os.remove('./output/output_img_coord_06.npy')
    # os.remove('./output/output_img_coord_07.npy')
    # os.remove('./output/output_img_coord_08.npy')
    if os.path.exists('./output/output_nac_id_02.csv'):
        os.remove('./output/output_nac_id_02.csv')
        os.remove('./output/output_map_coord_02.csv')
    else:
        print("Nothing to remove!")
    # if os.path.exists('./output/output_nac_id_03.csv'): # NOT INCLUDED HERE
    # os.remove('./output/output_nac_id_03.csv')
    # os.remove('./output/output_map_coord_03.csv')
    # else:
    # print("Nothing to remove!")
    # if os.path.exists('./output/output_nac_id_04.csv'): # NOT INCLUDED HERE
    # os.remove('./output/output_nac_id_04.csv')
    # os.remove('./output/output_map_coord_04.csv')
    # else:
    # print("Nothing to remove!")
    # if os.path.exists('./output/output_nac_id_05.csv'): # NOT INCLUDED HERE
    # os.remove('./output/output_nac_id_05.csv')
    # os.remove('./output/output_map_coord_05.csv')
    # else:
    # print("Nothing to remove!")
    # if os.path.exists('./output/output_nac_id_06.csv'): # NOT INCLUDED HERE
    # os.remove('./output/output_nac_id_06.csv')
    # os.remove('./output/output_map_coord_06.csv')
    # else:
    # print("Nothing to remove!")
    # if os.path.exists('./output/output_nac_id_07.csv'): # NOT INCLUDED HERE
    # os.remove('./output/output_nac_id_07.csv')
    # os.remove('./output/output_map_coord_07.csv')
    # else:
    # print("Nothing to remove!")
    # if os.path.exists('./output/output_nac_id_08.csv'): # NOT INCLUDED HERE
    # os.remove('./output/output_nac_id_08.csv')
    # os.remove('./output/output_map_coord_08.csv')
    # else:
    # print("Nothing to remove!")
    print("Clean up COMPLETE!")
    # loop over next NAC image in list


for i1 in image_list:
    i2 = '{}.txt'.format(i1[:-4])
    print("LOOPING!")
    parent = plt.imread(i1)
    meta_data = create_meta_obj(i2)

    process_image(parent, meta_data)

now = time.time()  # TOC
print("ELAPSED TIME: ", now - then, " seconds")
print("END OF SCRIPT")
