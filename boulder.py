class Vector2D:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Boulder:
    def __init__(self, boulder_data):
        self.upper_left_x = boulder_data.upper_left_x  # img_coord_split[0]
        self.upper_left_y = boulder_data.upper_left_y  # img_coord_split[1]
        self.lower_right_x = boulder_data.lower_right_x  # img_coord_split[2]
        self.lower_right_y = boulder_data.lower_right_y  # img_coord_split[3]
        self.confidence = boulder_data.confidence  # img_coord_split[4]
        selfclass_type = boulder_data.selfclass_type  # img_coord_split[5]
        self.lon_coord = 0.0
        self.lat_coord = 0.0
        self.x_length_array = abs(self.lower_right_x - self.upper_left_x)
        self.y_length_array = abs(self.lower_right_y - self.upper_left_y)

    def calculateGlobalCoord_Org(self,meta_data, parent):
        dimensions = parent.shape
        x_len = dimensions[1]
        y_len = dimensions[0]
        x_deg_len = meta_data.corner_ur_lon - meta_data.corner_ul_lon
        y_deg_len = meta_data.corner_ul_lat - meta_data.corner_ll_lat
        deg_per_pix_xdir = x_deg_len / x_len
        deg_per_pix_ydir = y_deg_len / y_len

        # LON NAC rotation correction - appears not to help accuracy, subject to change!
        # re lon_alpha_rad = math.atan(x_deg_len/y_deg_len)
        # x_len_corr = x_len * math.cos(lon_alpha_rad)
        # LAT NAC rotation correction - appears not to help accuracy, subject to change!
        # lat_alpha_rad = math.atan(y_deg_len/x_deg_len)
        # y_len_corr = y_len * math.sin(lat_alpha_rad)
        # deg_per_pix_xdir = x_deg_len/x_len_corr
        # deg_per_pix_ydir = y_deg_len/y_len_corr

        if meta_data.subject == 1:  # NO CHANGE
            rec_ul_x_corr = self.upper_left_x
            rec_ul_y_corr = self.upper_left_y

        if meta_data.subject == 2:  # X FLIP
            rec_ul_x_corr = x_len - self.upper_left_x
            rec_ul_y_corr = self.upper_left_y

        if meta_data.subject == 3:  # Y FLIP
            rec_ul_x_corr = self.upper_left_x
            rec_ul_y_corr = y_len - self.upper_left_y

        if meta_data.subject == 4:  # XY FLIP
            rec_ul_x_corr = x_len - self.upper_left_x
            rec_ul_y_corr = y_len - self.upper_left_y

        rec_ul_lon = (rec_ul_x_corr * deg_per_pix_xdir) + meta_data.corner_ul_lon
        rec_ul_lat = -1 * (rec_ul_y_corr * deg_per_pix_ydir) + meta_data.corner_ul_lat - 90  # 90 degree correction lifted

        #lon_array = np.append(lon_array, rec_ul_lon)
        #lat_array = np.append(lat_array, rec_ul_lat)

        #center_x_shift = (x_length_array * deg_per_pix_xdir) / 2
        #center_y_shift = (y_length_array * deg_per_pix_ydir) / 2

        #lon_array_center = (lon_array.T + center_x_shift.T).T
        #lat_array_center = (lat_array.T + center_y_shift.T).T

        self.lon_coord = rec_ul_lon + (self.x_length_array * deg_per_pix_xdir) / 2
        self.lat_coord = rec_ul_lat + (self.y_length_array * deg_per_pix_ydir) / 2

    def calculateGlobalCoord(self,meta_data, parent):
        dimensions = parent.shape
        x_len = dimensions[1]
        y_len = dimensions[0]


        vRight = Vector2D()

        x_deg_len = meta_data.corner_ur_lon - meta_data.corner_ul_lon
        y_deg_len = meta_data.corner_ul_lat - meta_data.corner_ll_lat
        deg_to_centre_x = x_deg_len / x_len
        deg_to_centre_y = y_deg_len / y_len
