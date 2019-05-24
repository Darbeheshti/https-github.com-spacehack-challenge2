import sys
sys.path.insert(0, '../')

from request import Request
import urllib.request
import os


class Download_Manager:
    def __init__(self, request, download_folder="./pictures"):
        self.request = request
        self.download_folder = download_folder
        self.downloaded = set()
        self.bad_pictures = set()

    def download_pictures(self):
        # to_download = self.__filter_overlap()
        to_download = self.request.picture_list
        import pdb
        pdb.set_trace()
        if not os.path.exists(self.download_folder):
            os.mkdir(self.download_folder)


        for pic in to_download: # TODO: Remove when downloaded in iteration before
            # if already downloaded
            if pic["product_id"] in self.downloaded:
                continue
            print("currently downloading {}.tif".format(pic["product_id"]))
            urllib.request.urlretrieve(pic["url"], "{}/{}.tif".format(self.download_folder, pic["product_id"]))
            self.downloaded.add(pic["picture_id"])


    def __filter_overlap(self):
        pass # Currently working on

    def is_bad_picture(self, id):
        self.bad_pictures.add(id)
        self.download_pictures()

if __name__ == '__main__':
    x = Download_Manager(Request(-147.23657, 40.34749, -147.11735, 40.40706, filter_anything=False))
    x.download_pictures()
