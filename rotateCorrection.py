class Vector2D:
    def __init__(self,lon,lat,xDim,yDim):
        self.lon = lon / xDim
        self.lat = lat / yDim

    def goRight(self,xCoord):
        return (self.lon*xCoord, self.lat*xCoord)

    def goDown(self,yCoord):
        return (self.lon*yCoord, self.lat*yCoord)

def calculateGlobalCoord(self, meta_data, parent,rockCoord):
    dimensions = parent.shape
    x_len = dimensions[1]
    y_len = dimensions[0]

    vRight = Vector2D(meta_data.lr_lon - meta_data.ll_lon, meta_data.lr_lat - meta_data.ll_lat, x_len, y_len)
    vUp = Vector2D(meta_data.ul_lon - meta_data.ll_lon, meta_data.ul_lat - meta_data.ll_lat, x_len, y_len)

    goXDirection = (meta_data.ll_lon + vRight.goRight(rockCoord[0])[0], meta_data.ll_lat + vRight(rockCoord[0])[1])
    goYDirection = (goXDirection[0] + vUp.goUp(rockCoord[1])[0], goXDirection[1] + vUp.goUp(rockCoord[1])[1])

    return goYDirection

def vector_converter(pointpx, top_right, top_left, bottom_left, bottom_right, imagesize):
    vRight = Vector2D(top_right[0] - top_left[0],top_right[1] - top_left[1],imagesize[0],imagesize[1])
    vDown = Vector2D(bottom_left[0] - top_left[0],bottom_left[1] - top_left[1], imagesize[0],imagesize[1])

    goXDirection = (top_right[0] + vRight.goRight(pointpx[0]), top_right[1] + vRight.goRight(pointpx[0]))
    goYDirection = (goXDirection[0] + vDown.goDown(pointpx[1]), goXDirection[1] + vDown.goDown(pointpx[1]))

    return goYDirection[0], goYDirection[1]
