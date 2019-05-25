from typing import NamedTuple

import numpy as np
import matplotlib.pyplot as plt
from numpy import array


def distance(a: np.ndarray, b: np.ndarray):
    """ Calculate the distance between `a` and `b`, correction for wraparound in the cordinates."""
    # x = longitude [0, 360]
    # y = latitude [-90, 90]
    a, b = np.array(a), np.array(b)
    if not -90 <= a[1] <= 90:
        print(f"[WARNING] latitude is not in [=90, 90] a={a}")
    if not -90 <= b[1] <= 90:
        print(f"[WARNING] latitude is not in [=90, 90] b={b}")
    if not 0 <= a[0] <= 360:
        print(f"[WARNING] longitude is not in [0, 360] a={a}")
    if not 0 <= b[0] <= 360:
        print(f"[WARNING] longitude is not in [0, 360] b={b}")

    diff_norm = np.abs(a - b)
    diff_wrapped = np.array([360, 180]) - diff_norm
    diff = np.minimum(diff_norm, diff_wrapped)
    return np.sqrt(np.sum(diff * diff))


def scale(pointpx: np.ndarray, corner_ur: np.ndarray, corner_ul: np.ndarray, corner_ll: np.ndarray,
          imagesize: np.ndarray):
    """
    Scale `pointpx` into the longitude/latitude coordinate space.

    Parameters
    ----------
    pointpx : np.ndarray
        X and Y value of the pixel to be scaled.
    corner_ur : np.ndarray
        The upper-right corner in (long, lat) space.
    corner_ul : np.ndarray
        The upper-left corner in (long, lat) space.
    corner_ll : np.ndarray
        The lower-right corner in (long, lat) space.
    imagesize : np.ndarray
        The X and Y size of the input-image in pixels.

    Returns
    -------
    point : np.ndarray
        The scaled point.
    """
    realsize = np.array([distance(corner_ur, corner_ul), distance(corner_ul, corner_ll)])
    scale = realsize / imagesize
    assert abs((scale[0] - scale[1]) / scale[1]) < 1.0, f"Scale is too different: x-scale={scale[0]} y-scale={scale[1]}"
    M_scale = np.array([[scale[0], 0], [0, scale[1]]])
    return M_scale @ pointpx


def calc_angle(v1, v2):
    """ Calcuate the signed angle. """
    return np.arctan2(v1[1], v1[0]) - np.arctan2(v2[1], v2[0])


def rotate(point: np.ndarray, corner_ur: np.ndarray, corner_ul: np.ndarray, corner_ll: np.ndarray) -> np.ndarray:
    """
    Rotate `point` to fit the rotation of the longitude/latitude coordinate-space.

    Parameters
    ----------
    point : np.ndarray
        X and Y value of the point.
    corner_ur : np.ndarray
        The upper-right corner in (long, lat) space.
    corner_ul : np.ndarray
        The upper-right corner in (long, lat) space.
    corner_ll : np.ndarray
        The lower-left corner in (long, lat) space.

    Returns
    -------
    point : np.ndarray
        The rotated point.
    """
    # find out what pair of corner to use to determine the roataion
    vec_top = corner_ul - corner_ur
    vec_left = corner_ll - corner_ul

    # keep in mind that the coordinates can wrap around.
    axis_top = np.array([-1, 0]) if vec_top[0] < 0 else np.array([1, 0])
    axis_left = np.array([0, -1]) if vec_left[1] < 0 else np.array([0, 1])

    # those angles should be similar.
    anglex = calc_angle(vec_top, axis_top)
    angley = calc_angle(vec_left, axis_left)
    angles = np.array([anglex, angley])
    print(angles)
    angle = angles[np.argmax(np.abs(angles))]
    M_rotation = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    return M_rotation @ point


def translate(point: np.ndarray, corner_ll: np.ndarray) -> np.ndarray:
    """
    Translate `point` to fit the 
    
    Parameters
    ----------
    point : np.ndarray
    corner_ll : np.ndarray

    Returns
    -------
    point : np.ndarray
        Translated point.
    """
    return point + corner_ll


def transform_old(pointpx, corner_ur, corner_ul, corner_ll, imagesize):
    x_deg_len = corner_ur[0] - corner_ul[0]
    y_deg_len = corner_ul[1] - corner_ll[1]
    deg_per_pix_xdir = x_deg_len / imagesize[0]
    deg_per_pix_ydir = y_deg_len / imagesize[1]

    x = pointpx[0]
    rec_ul_lon = (x * deg_per_pix_xdir) + corner_ul[0]
    lat = -1 * ((imagesize[1] - pointpx[1]) * deg_per_pix_ydir) + corner_ul[1]
    return np.array([rec_ul_lon, lat])


def transform(pointpx, corner_ur, corner_ul, corner_ll, imagesize):
    """
    Transform `pointpx` from pixel-coordinate-space into (long, lat)-coordinate-space.

    Parameters
    ----------
    pointpx : np.ndarray
        The image-point with x, y pixel coordinates.
    corner_ur : np.ndarray
        The upper-right corner in (long, lat) space.
    corner_ul : np.ndarray
        The upper-left corner in (long, lat) space.
    corner_ll : np.ndarray
        The lower-left corner in (long, lat) space.
    imagesize : np.ndarray
        The (x, y) size of the image in pixels.

    Returns
    -------
    point : np.ndarray
        The point in lat/long coordinate space.
    """
    pointpx = pointpx.copy()
    if not 0 <= pointpx[0] <= imagesize[0]:
        print(f"[WARNING] point x coordinate (={pointpx[0]}) not in image-width (={imagesize[0]})")
    if not 0 <= pointpx[1] <= imagesize[1]:
        print(f"[WARNING] point y coordinate (={pointpx[1]}) not in image-height (={imagesize[1]})")

    # pointpx[0] = imagesize[0] - pointpx[0]

    point = scale(pointpx,
                  corner_ur=corner_ur,
                  corner_ul=corner_ul,
                  corner_ll=corner_ll,
                  imagesize=imagesize)
    point = rotate(point, corner_ur, corner_ul, corner_ll)
    point = translate(point, corner_ll)
    if point[0] < 0:
        point[0] += 360
    return point


def make_points(imagesize):
    nxs, nys = imagesize[0] + 1, imagesize[1] + 1
    xs, ys = np.mgrid[0:nxs:40 * 1j, 0:nys:40 * 1j]
    xs, ys = xs.flatten(), ys.flatten()
    v = np.random.random(xs.size) * 50
    return np.column_stack((xs, ys)), v


def visualize():
    """ Visualize the transformation steps on example input. """
    inputb = eval("""(
        [array([ 1213.25018311, 50283.76699829]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 1069.20169067, 47749.85971069]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 5774.96826172, 44479.32678223]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 1445.67004395, 42035.75231934]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 2532.        , 41902.60980225]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 5623.76196289, 39992.25012207]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([  910.7706604 , 33793.68363953]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 2962.61135864, 30680.63146973]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 2440.19158936, 26486.56188965]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 3830.57794189, 24590.31072235]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 2597.1034317 , 23808.47906494]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 2532.        , 10459.66265869]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 4220.        , 10395.95028687]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([4807.8203125 , 7929.60699463]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([4726.63311768, 5713.96124268]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 844.        , 4983.78283691]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([3738.62582397, 2790.93508911]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])])""")

    inputa = eval("""([array([1090.2268219 , 4951.45690823]), array([  3.82, 116.49]), array([  3.74, 116.49]), array([  3.75, 115.54]), array([ 5064, 52224])]
    ,[array([ 4420.54425049, 13048.45074463]), array([  3.82, 116.49]), array([  3.74, 116.49]), array([  3.75, 115.54]), array([ 5064, 52224])]
    ,[array([ 4425.96748352, 14084.15847778]), array([  3.82, 116.49]), array([  3.74, 116.49]), array([  3.75, 115.54]), array([ 5064, 52224])]
    ,[array([ 4395.55039978, 14317.54650879]), array([  3.82, 116.49]), array([  3.74, 116.49]), array([  3.75, 115.54]), array([ 5064, 52224])]
    ,[array([ 4346.92008209, 47847.70596313]), array([  3.82, 116.49]), array([  3.74, 116.49]), array([  3.75, 115.54]), array([ 5064, 52224])]
    )""")
    points = np.array([x[0] for x in inputa])
    # offset = np.array([3.7, 116])
    offset = np.array([0, 0])
    corner_ur = [x[1] for x in inputa][0] - offset
    corner_ul = [x[2] for x in inputa][0] - offset
    corner_ll = [x[3] for x in inputa][0] - offset
    imagesize = [x[4] for x in inputa][0]
    if corner_ur[0] < 0:
        corner_ur[0] += 360
    elif corner_ur[0] > 360:
        corner_ur[0] -= 360
    if corner_ul[0] < 0:
        corner_ul[0] += 360
    elif corner_ul[0] > 360:
        corner_ul[0] -= 360
    if corner_ll[0] < 0:
        corner_ll[0] += 360
    elif corner_ll[0] > 360:
        corner_ll[0] -= 360

    corners = np.column_stack((corner_ur, corner_ul, corner_ll))

    # --- plot corners --- #
    plt.scatter(corners[0], corners[1], s=np.linspace(30, 100, 4))
    plt.title("Corners")
    plt.xlabel("longitude")
    plt.ylabel("latitude + 90")
    plt.show()

    pixelpoints, pixelv = make_points(imagesize)

    # --- plot pixels --- #
    plt.scatter(pixelpoints[:, 0], pixelpoints[:, 1], s=pixelv, label='pixelpoints')
    plt.title("Pixels (simulated image)")
    plt.show()
    v = np.random.random(len(points)) * 50
    plt.scatter(points[:, 0], points[:, 1], s=v)
    plt.title("Pixels")
    plt.show()

    # points = np.column_stack((xs, ys))

    # --- Calc scaled points --- #
    pixelpoints_scaled = np.array([scale(p,
                                         corner_ur=corner_ur,
                                         corner_ul=corner_ul,
                                         corner_ll=corner_ll,
                                         imagesize=imagesize) for p in pixelpoints])
    plt.scatter(pixelpoints_scaled[:, 0], pixelpoints_scaled[:, 1], s=pixelv)
    plt.xlim((0, 1.0))
    plt.ylim((0, 1.0))  #
    # plt.scatter(corners[0], corners[1], s=np.linspace(30, 100, 4))
    plt.title("Scaled pixelpoints")
    plt.xlabel("longitude")
    plt.ylabel("latitude + 90")
    plt.show()

    points_scaled = np.array([scale(p,
                                    corner_ur=corner_ur,
                                    corner_ul=corner_ul,
                                    corner_ll=corner_ll,
                                    imagesize=imagesize) for p in points])
    # xmin, xmax, ymin, ymax = points_scaled[:, 0].min(), points_scaled[:, 0].max(), points_scaled[:, 1].min(), points_scaled[:, 1].max()
    plt.scatter(points_scaled[:, 0], points_scaled[:, 1], s=v)
    plt.xlim((0, 1.0))
    plt.ylim((0, 1.0))  #
    # plt.scatter(corners[0], corners[1], s=np.linspace(30, 100, 4))
    plt.title("Scaled")
    plt.xlabel("longitude")
    plt.ylabel("latitude + 90")
    plt.show()

    # --- Calc rotation --- #

    pixelpoints_rotated = np.array([rotate(p,
                                           corner_ur=corner_ur,
                                           corner_ul=corner_ul,
                                           corner_ll=corner_ll) for p in pixelpoints_scaled])
    plt.scatter(pixelpoints_rotated[:, 0], pixelpoints_rotated[:, 1], s=v, label='rotated')
    plt.scatter(pixelpoints_scaled[:, 0], pixelpoints_scaled[:, 1], s=v, c='#FF0000AA', label='only scaled')
    plt.xlim((-0.5, 0.5))
    plt.ylim((0, 1.0))
    # plt.scatter(corners[0], corners[1], s=np.linspace(30, 100, 4))
    plt.title("Scaled and rotated")
    plt.xlabel("longitude")
    plt.ylabel("latitude + 90")
    plt.legend()
    plt.show()

    points_rotated = np.array([rotate(p,
                                      corner_ur=corner_ur,
                                      corner_ul=corner_ul,
                                      corner_ll=corner_ll) for p in points_scaled])
    plt.scatter(points_rotated[:, 0], points_rotated[:, 1], s=v, label='rotated')
    plt.scatter(points_scaled[:, 0], points_scaled[:, 1], s=v, c='#FF0000AA', label='only scaled')
    plt.xlim((0, 1.0))
    plt.ylim((0, 1.0))
    # plt.scatter(corners[0], corners[1], s=np.linspace(30, 100, 4))
    plt.title("Scaled and rotated")
    plt.xlabel("longitude")
    plt.ylabel("latitude + 90")
    plt.legend()
    plt.show()

    # --- Calc Translation --- #
    pixelpoints_translated = np.array([translate(p, corner_ll=corner_ll) for p in pixelpoints_rotated])
    pixelpoints_transformed_old = np.array(
        [transform_old(p, corner_ur, corner_ul, corner_ll, imagesize) for p in pixelpoints])
    xmin, xmax, ymin, ymax = (pixelpoints_translated[:, 0].min(), pixelpoints_translated[:, 0].max(),
                              pixelpoints_translated[:, 1].min(), pixelpoints_translated[:, 1].max())
    xmin, xmax = xmin - (xmax - xmin) * 0.1, xmax + (xmax - xmin) * 0.1
    ymin, ymax = ymin - (ymax - ymin) * 0.1, ymax + (ymax - ymin) * 0.1
    xmin2, xmax2, ymin2, ymax2 = (pixelpoints_translated[:, 0].min(), pixelpoints_translated[:, 0].max(),
                                  pixelpoints_translated[:, 1].min(), pixelpoints_translated[:, 1].max())
    xmin, xmax, ymin, ymax = min(xmin, xmin2), max(xmax, xmax2), min(ymin, ymin2), max(ymax, ymax2)
    xlength, ylength = xmax - xmin, ymax - ymin
    length = max(xlength, ylength)
    xmax, ymax = max(xmax, xmin + length), max(ymax, ymin + length)
    plt.scatter(pixelpoints_transformed_old[:, 0], pixelpoints_transformed_old[:, 1], s=v, label="Old algorithm")
    plt.scatter(pixelpoints_translated[:, 0], pixelpoints_translated[:, 1], s=v, label='translated')
    plt.scatter(corners[0], corners[1], s=np.linspace(30, 100, 4), label='corners')
    plt.title("Complete transformation pixelpoints")
    plt.xlim((xmin, xmax))
    plt.ylim((ymin, ymax))
    plt.xlabel("longitude")
    plt.ylabel("latitude + 90")
    plt.legend(loc="lower right")
    # plt.xlim((3.5-offset[0], 3.5 + 1.3-offset[0]))
    # plt.ylim((115.4-offset[1], 116.7-offset[1]))
    plt.show()

    points_translated = np.array([translate(p, corner_ll=corner_ll) for p in points_rotated])
    plt.scatter(points_translated[:, 0], points_translated[:, 1], s=v, label='translated')
    points_transformed_old = np.array([transform_old(p, corner_ur, corner_ul, corner_ll, imagesize) for p in points])
    plt.scatter(corners[0], corners[1], s=np.linspace(30, 100, 4), label='corners')
    plt.scatter(points_transformed_old[:, 0], points_transformed_old[:, 1], s=v, label="Old algorithm")
    plt.title("Complete transformation")
    plt.xlabel("longitude")
    plt.ylabel("latitude + 90")
    plt.xlim((xmin, xmax))
    plt.ylim((ymin, ymax))
    # plt.xlim((3.5-offset[0], 3.5 + 1.3-offset[0]))
    # plt.ylim((115.4-offset[1], 116.7-offset[1]))
    plt.legend()
    plt.show()

    # --- Calc all together --- #
    points_transformed = np.array([transform(p, corner_ur, corner_ul, corner_ll, imagesize) for p in points])
    points_transformed_old = np.array([transform_old(p, corner_ur, corner_ul, corner_ll, imagesize) for p in points])
    plt.scatter(corners[0], corners[1], s=np.linspace(30, 100, 4), label='Corners')
    plt.scatter(points_transformed[:, 0], points_transformed[:, 1], s=v, label="Our algorithm")
    plt.scatter(points_transformed_old[:, 0], points_transformed_old[:, 1], s=v, label="Old algorithm")
    # plt.xlim((3.5 - offset[0], 3.5 + 1.3 - offset[0]))
    # plt.ylim((115.4 - offset[1], 116.7 - offset[1]))
    plt.title("Complete transformation -- all at once")
    plt.xlabel("longitude")
    plt.ylabel("latitude + 90")
    plt.legend()
    plt.show()


class TestData(NamedTuple):
    corner1: np.ndarray
    corner2: np.ndarray
    corner3: np.ndarray
    corner4: np.ndarray
    imagesize: np.ndarray


def test_data_case_0():
    corner1 = np.array([26.49, 3.82])
    corner2 = np.array([25.54, 3.83])
    corner3 = np.array([25.54, 3.75])
    corner4 = np.array([26.49, 3.74])
    imagesize = np.array([52224, 5064]) // 10
    return TestData(corner1=corner1,
                    corner2=corner2,
                    corner3=corner3,
                    corner4=corner4,
                    imagesize=imagesize)


def test_data_case_1():
    """
    Product	M1282472090RE
    Pds dataset name	LRO-L-LROC-2-EDR-V1.0
    Pds volume name	LROLRC_0035
    Instrument host	LRO
    Instrument	LROC
    Original product	nacr001ddcd5
    Product version	v1.8
    Mission phase name	THIRD EXTENDED SCIENCE MISSION
    Rationale desc	TARGET OF OPPORTUNITY
    Data quality	0
    Nac preroll start time	(DOY:152) 2018-06-01T06:00:23
    Start time	(DOY:152) 2018-06-01T06:00:23
    Stop time	(DOY:152) 2018-06-01T06:00:52
    Spacecraft clock partition	1
    Nac spacecraft clock preroll count	549525622:64684
    Spacecraft clock start count	549525623:36862
    Spacecraft clock stop count	549525652:59738
    Target name	MOON
    Orbit number	40257
    Slew angle	0.00887697075602033
    Lro node crossing	A
    Lro flight direction	-X
    Nac line exposure duration	0.000559466666666667
    Nac frame	RIGHT
    Nac dac reset	190
    Nac channel a offset	12
    Nac channel b offset	74
    Instrument mode code	7
    Compand select code	3
    Mode compression	true
    Mode test	false
    Nac temperature scs	7.899
    Nac temperature fpa	19.374
    Nac temperature fpga	-8.109
    Nac temperature telescope	8.132
    Image lines	52224
    Line samples	5064
    Sample bits	8
    Scaled pixel width	0.84
    Scaled pixel height	0.88
    Resolution	0.856571977678108
    Emission angle	1.16
    Incidence angle	27.61
    Phase angle	26.45
    North azimuth	87.76
    Sub solar azimuth	179.78
    Sub solar latitude	-1.33
    Sub solar longitude	331.3
    Sub spacecraft latitude	0.14
    Sub spacecraft longitude	358.82
    Solar distance	152038784.5
    Solar longitude	306.07
    Center latitude	0.14
    Center longitude	358.87
    Upper right latitude	0.91
    Upper right longitude	358.9
    Lower right latitude	-0.61
    Lower right longitude	358.98
    Lower left latitude	-0.62
    Lower left longitude	358.84
    Upper left latitude	0.9
    Upper left longitude	358.76
    Spacecraft altitude	83.76
    Target center distance	1821.08
    """

    return TestData(corner1=np.array([0.91, 358.9]),
                    corner2=np.array([-0.61, 358.98]),
                    corner3=np.array([-0.62, 358.84]),
                    corner4=np.array([358.84, 358.76]),
                    imagesize=np.array([52224, 5064]))
