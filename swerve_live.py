import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
import math

"""
    A class that allows you to actively change the value of your
    cordinates and computes the angle based off the input.
    Can do the opposite and computes (x, y) based off angle 
"""
# Functions to compute values
def compute_angle_from_xy(x, y):
    """Compute the angle (in degrees) based on x and y coordinates."""
    return math.degrees(math.atan2(y, x))

def compute_xy_from_angle(angle):
    """Compute x and y coordinates given an angle (in degrees)."""
    radians = math.radians(angle)
    x = math.cos(radians)
    y = math.sin(radians)
    return x, y
\
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.4)

# Initial values
init_x, init_y = 1.0, 0.0
init_angle = compute_angle_from_xy(init_x, init_y)

ax_x = plt.axes([0.1, 0.25, 0.65, 0.03])
ax_y = plt.axes([0.1, 0.2, 0.65, 0.03])
ax_angle = plt.axes([0.1, 0.15, 0.65, 0.03])

slider_x = Slider(ax_x, 'X', -1.0, 1.0, valinit=init_x)
slider_y = Slider(ax_y, 'Y', -1.0, 1.0, valinit=init_y)
slider_angle = Slider(ax_angle, 'Angle', -180, 180, valinit=init_angle)

point, = ax.plot([init_x], [init_y], 'ro', label='Point')
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.legend()

# Flags to prevent recursive loops
updating_from_xy = False
updating_from_angle = False

def update_xy(val):
    global updating_from_xy, updating_from_angle
    if updating_from_xy:
        return
    updating_from_xy = True
    
    x = slider_x.val
    y = slider_y.val
    angle = compute_angle_from_xy(x, y)
    
    updating_from_angle = True
    slider_angle.set_val(angle)
    updating_from_angle = False
    
    point.set_xdata([x])
    point.set_ydata([y])
    ax.figure.canvas.draw_idle()
    
    updating_from_xy = False

def update_angle(val):
    global updating_from_xy, updating_from_angle
    if updating_from_angle:
        return
    updating_from_angle = True
    
    angle = slider_angle.val
    x, y = compute_xy_from_angle(angle)
    
    updating_from_xy = True
    slider_x.set_val(x)
    slider_y.set_val(y)
    updating_from_xy = False
    
    point.set_xdata([x])
    point.set_ydata([y])
    ax.figure.canvas.draw_idle()
    
    updating_from_angle = False

slider_x.on_changed(update_xy)
slider_y.on_changed(update_xy)
slider_angle.on_changed(update_angle)

plt.show()
