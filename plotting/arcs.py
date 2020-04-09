import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def arcToPoints(center, radius1, radius2, theta1, theta2, resolution=100):
    '''
    Given the starting point and 2 radia, create a polygon based on two arcs
    defined by starting theta and ending theta
    '''
    arc1 = np.linspace(np.radians(theta1), np.radians(theta2), resolution)
    arc1Points = np.array((radius1*np.cos(arc1) + center[0], radius1*np.sin(arc1) + center[1]))
    arc1StartingPoint = np.array([[arc1Points[0][0]], [arc1Points[1][0]]])

    arc2 = np.linspace(np.radians(theta2), np.radians(theta1), resolution)  # Reverse direction
    arc2Points = np.array((radius2*np.cos(arc2) + center[0], radius2*np.sin(arc2) + center[1]))

    closedPolygon = np.concatenate((arc1Points, arc2Points, arc1StartingPoint), axis=1)

    return closedPolygon

def arc_patch(center, radius1, radius2, theta1, theta2, ax=None, resolution=100, **kwargs):
    # make sure ax is not empty
    if ax is None:
        ax = plt.gca()
    # generate the points
    polygonPoints = arcToPoints(center, radius1, radius2, theta1, theta2, resolution)
    # build the polygon and add it to the axes
    poly = mpatches.Polygon(polygonPoints.T, closed=True, **kwargs)
    ax.add_patch(poly)
    return poly
