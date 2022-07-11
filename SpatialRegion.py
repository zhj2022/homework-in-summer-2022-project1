from math import radians, sin, cos, asin, sqrt, ceil


def get_distance(lng1, lat1, lng2, lat2):
    lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)])
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
    distance = 2 * asin(sqrt(a)) * 6371 * 1000
    distance = round(distance / 1000, 3)
    return distance


class SpatialRegion:
    def __init__(self, minlat, minlng, maxlat, maxlng, xstep, ystep):
        assert minlat < maxlat, "minlat should be smaller than maxlat"
        assert minlng < maxlng, "minlng should be smaller than maxlng"
        self.minlat = minlat
        self.minlng = minlng
        self.maxlat = maxlat
        self.maxlng = maxlng

        self.xstep = xstep
        self.ystep = ystep

        self.num_x = ceil(get_distance(
            self.minlng, self.minlat, self.maxlng, self.minlat) / self.xstep)
        self.num_y = ceil(get_distance(
            self.minlng, self.minlat, self.minlng, self.maxlat) / self.ystep)

    def in_region(self, lat, lng):
        return self.minlat <= lat <= self.maxlat and self.minlng <= lng <= self.maxlng

    def offset(self, lat, lng):
        x_offset = get_distance(
            self.minlng, self.minlat, lng, self.minlat)
        y_offset = get_distance(
            self.minlng, self.minlat, self.minlng, lat)
        return x_offset, y_offset

    """返回输入点在网格地图中的编号"""
    def coord2cell(self, lat, lng):
        assert self.in_region(lat, lng), f"({lat}, {lng}) not in area"
        x_offset, y_offset = self.offset(lat, lng)
        x_offset = ceil(x_offset / self.xstep)
        y_offset = ceil(y_offset / self.ystep)
        return self.num_x * (y_offset - 1) + x_offset - 1
