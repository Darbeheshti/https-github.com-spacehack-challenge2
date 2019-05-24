import numpy as np
import matplotlib.pyplot as plt


def scale(pointpx, corner1, corner2, corner4, imagesize):
    realsize = np.array([np.linalg.norm(corner1 - corner2), np.linalg.norm(corner1 - corner4)])
    scale = realsize / imagesize
    assert abs((scale[0] - scale[1]) / scale[1]) < 1.0, f"Scale is too different: x-scale={scale[0]} y-scale={scale[1]}"
    M_scale = np.array([[scale[0], 0], [0, scale[1]]])
    return M_scale @ pointpx


def rotate(points, corner1, corner2):
    v1 = corner2 - corner1
    v2 = np.array([1, 0])
    angle = np.arccos((v1 @ v2 / (np.linalg.norm(v1) * np.linalg.norm(v2))))
    M_rotation = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    return M_rotation @ points


def translate(points, corner):
    return points + corner


def transform(pointpx, corner1, corner2, corner3, corner4, imagesize):
    points = scale(pointpx, corner1, corner2, corner4, imagesize)
    points = rotate(points, corner1, corner2)
    points = translate(points, corner1)
    return points


def visualize():
    corner1 = np.array([26.49, 3.82])
    corner2 = np.array([25.54, 3.83])
    corner3 = np.array([25.54, 3.75])
    corner4 = np.array([26.49, 3.74])
    corners = np.column_stack((corner1, corner2, corner3, corner4))
    imagesize = np.array([52224, 5064]) // 10

    # --- plot corners --- #
    plt.scatter(corners[0], corners[1], s=np.linspace(30, 100, 4))
    plt.title("Corners")
    plt.xlabel("longitude")
    plt.ylabel("latitude")
    plt.show()

    nxs, nys = imagesize[0] + 1, imagesize[1] + 1
    xs, ys = np.mgrid[0:nxs:40 * 1j, 0:nys:40 * 1j]
    xs, ys = xs.flatten(), ys.flatten()
    v = np.random.random(xs.size) * 50

    # --- plot pixels --- #
    plt.scatter(xs, ys, s=v)
    plt.title("Pixels")
    plt.show()

    points = np.column_stack((xs, ys))

    # --- Calc scaled points --- #
    points_scaled = np.array([scale(p, corner1, corner2, corner4, imagesize) for p in points])
    plt.scatter(points_scaled[:, 0], points_scaled[:, 1], s=v)
    plt.scatter(corners[0], corners[1], s=np.linspace(30, 100, 4))
    plt.title("Scaled")
    plt.xlabel("longitude")
    plt.ylabel("latitude")
    plt.show()

    # --- Calc rotation --- #
    points_rotated = np.array([rotate(p, corner1, corner2) for p in points_scaled])
    plt.scatter(points_rotated[:, 0], points_rotated[:, 1], s=v)
    plt.scatter(corners[0], corners[1], s=np.linspace(30, 100, 4))
    plt.title("Scaled and rotated")
    plt.xlabel("longitude")
    plt.ylabel("latitude")
    plt.show()

    # --- Calc Translation --- #
    points_translated = np.array([translate(p, corner1) for p in points_rotated])
    plt.scatter(points_translated[:, 0], points_translated[:, 1], s=v)
    plt.scatter(corners[0], corners[1], s=np.linspace(30, 100, 4))
    plt.title("Complete transformation")
    plt.xlabel("longitude")
    plt.ylabel("latitude")
    plt.show()

    # --- Calc all together --- #
    points_transformed = np.array([transform(p, corner1, corner2, corner3, corner4, imagesize) for p in points])
    plt.scatter(points_translated[:, 0], points_translated[:, 1], s=v)
    plt.scatter(corners[0], corners[1], s=np.linspace(30, 100, 4))
    plt.title("Complete transformation -- all at once")
    plt.xlabel("longitude")
    plt.ylabel("latitude")
    plt.show()


