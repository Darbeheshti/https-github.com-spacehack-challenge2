from src.api import DBService


class Request:
    def __init__(self, ul_lon, ul_lat, lr_lon, lr_lat, filter_anything=True):
        """Initializes metadata, filters """
        if self.__pic_too_large(ul_lon, ul_lat, lr_lon, lr_lat):
            raise ValueError("Request too large")
        query = DBService()
        self.picture_list = query.query_by_bbox(ul_lon, ul_lat, lr_lon, lr_lat)
        self.filter_picture_list()

    def filter_picture_list(self):
        self.__filter_incidence_angle()
        self.__sort_by_res()

    def __filter_incidence_angle(self):
        self.picture_list = [x for x in self.picture_list if x["incidence_angle"] >= 10 and x["incidence_angle"] <= 80]

    def __sort_by_res(self):
        self.picture_list = sorted(self.picture_list, key=(lambda x : x["resolution"]))

    @staticmethod
    def __pic_too_large(ul_lon, ul_lat, lr_lon, lr_lat):
        '''Retuns True if the requested image field exceeds 5*5 degrees, due to Nasa API limitations'''
        size_to_big = False
        # just for understanding purpose
        thirdpoint = [ul_lon, lr_lat]

        if thirdpoint[1] - ul_lat > 5:
            size_to_big = True

        if thirdpoint[0] - lr_lon > 5:
            size_to_big = True

        return size_to_big


if __name__ == "__main__":
    x = Request(-147.23657, 40.34749, -147.11735, 40.40706)
    print(x.picture_list)

