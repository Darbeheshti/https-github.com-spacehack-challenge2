class MetaData:
    def __init__(self, mata_data):
        self.ul_lon = mata_data[8]
        self.ul_lat_orig = mata_data[7]

        self.ur_lon = mata_data[2]
        self.ur_lat_orig = mata_data[1]

        self.ll_lon = mata_data[6]
        self.ll_lat_orig = mata_data[5]

        self.lr_lon = mata_data[4]
        self.lr_lat_orig = mata_data[3]

        self.pix = mata_data[0]  # NAC spatial resolution

        # ___________________________________________________________________________________________________
        # %% 6c) Latitude normalization
        # bring lat to 0-180 degree range to avoid edge effects
        if self.ul_lat_orig > 0:
            self.ul_lat = self.ul_lat_orig + 90
        if self.ur_lat_orig > 0:
            self.ur_lat = self.ur_lat_orig + 90
        if self.lr_lat_orig > 0:
            self.lr_lat = self.lr_lat_orig + 90
        if self.ll_lat_orig > 0:
            self.ll_lat = self.ll_lat_orig + 90
        if self.ul_lat_orig < 0:
            self.ul_lat = 90 - self.ul_lat_orig * (-1)
        if self.ur_lat_orig < 0:
            self.ur_lat = 90 - self.ur_lat_orig * (-1)
        if self.lr_lat_orig < 0:
            self.lr_lat = 90 - self.lr_lat_orig * (-1)
        if self.ll_lat_orig < 0:
            self.ll_lat = 90 - self.ll_lat_orig * (-1)

        # ___________________________________________________________________________________________________
        # %% 6d) Parent orientation
        # System determination, does NAC cross -180-180 cut?
        if self.ul_lon - self.ur_lon > 300:  # SPECIAL LON CASE
            system = 1
        if self.ul_lon - self.ur_lon < -300:  # SPECIAL LON CASE
            system = 1
        if self.ul_lon - self.ur_lon < 300:  # NORMAL LON CASE
            system = 2
        if self.ul_lon - self.ur_lon > -300:  # NORMAL LON CASE
            system = 2
        # ___________________________________________________________________________________________________
        # %% 6e) NAC ORIENTATION - NORMAL LONGITUDE CASE
        if system == 2:
            if self.ul_lon < self.ur_lon and self.ul_lat > self.ll_lat:
                self.subject = 1
                self.corner_ul_lon = self.ul_lon
                self.corner_ur_lon = self.ur_lon
                self.corner_ll_lon = self.ll_lon

                self.corner_ul_lat = self.ul_lat
                self.corner_ur_lat = self.ur_lat
                self.corner_ll_lat = self.ll_lat

            if self.ul_lon < self.ur_lon and self.ul_lat < self.ll_lat:
                self.subject = 3
                self.corner_ul_lon = self.ul_lon
                self.corner_ur_lon = self.ur_lon
                self.corner_ll_lon = self.ll_lon

                self.corner_ul_lat = self.ll_lat
                self.corner_ur_lat = self.lr_lat
                self.corner_ll_lat = self.ul_lat

            if self.ul_lon > self.ur_lon and self.ul_lat > self.ll_lat:
                self.subject = 2
                self.corner_ul_lon = self.ur_lon
                self.corner_ur_lon = self.ul_lon
                self.corner_ll_lon = self.lr_lon

                self.corner_ul_lat = self.ul_lat
                self.corner_ur_lat = self.ur_lat
                self.corner_ll_lat = self.ll_lat

            if self.ul_lon > self.ur_lon and self.ul_lat < self.ll_lat:
                self.subject = 4
                self.corner_ul_lon = self.ur_lon
                self.corner_ur_lon = self.ul_lon
                self.corner_ll_lon = self.lr_lon

                self.corner_ul_lat = self.ll_lat
                self.corner_ur_lat = self.lr_lat
                self.corner_ll_lat = self.ul_lat
        # ___________________________________________________________________________________________________
        # %% 6f) NAC ORIENTATION - SPECIAL LONGITUDE-BORDER CASE
        if system == 1:
            if self.ul_lon < self.ur_lon and self.ul_lat > self.ll_lat:
                self.subject = 2
                self.corner_ul_lon = self.ur_lon
                self.corner_ur_lon = self.ul_lon
                self.corner_ll_lon = self.lr_lon

                self.corner_ul_lat = self.ul_lat
                self.corner_ur_lat = self.ur_lat
                self.corner_ll_lat = self.ll_lat

            if self.ul_lon < self.ur_lon and self.ul_lat < self.ll_lat:
                self.subject = 4
                self.corner_ul_lon = self.ur_lon
                self.corner_ur_lon = self.ul_lon
                self.corner_ll_lon = self.lr_lon

                self.corner_ul_lat = self.ll_lat
                self.corner_ur_lat = self.lr_lat
                self.corner_ll_lat = self.ul_lat

            if self.ul_lon > self.ur_lon and self.ul_lat > self.ll_lat:
                self.subject = 1
                self.corner_ul_lon = self.ul_lon
                self.corner_ur_lon = self.ur_lon
                self.corner_ll_lon = self.ll_lon

                self.corner_ul_lat = self.ul_lat
                self.corner_ur_lat = self.ur_lat
                self.corner_ll_lat = self.ll_lat

            if self.ul_lon > self.ur_lon and self.ul_lat < self.ll_lat:
                self.subject = 3
                self.corner_ul_lon = self.ul_lon
                self.corner_ur_lon = self.ur_lon
                self.corner_ll_lon = self.ll_lon

                self.corner_ul_lat = self.ll_lat
                self.corner_ur_lat = self.lr_lat
                self.corner_ll_lat = self.ul_lat
