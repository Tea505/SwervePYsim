import numpy as np
import matplotlib.pyplot as plt

""" 
A small graph that displays the Swerve Module angle 
from point A to point B using a range of (-1, 1)
"""
def plot_swerve_module(angle):
    plt.figure(figsize=(5, 5))
    x, y = [0, np.cos(angle)], [0, np.sin(angle)]
    plt.plot(x, y, marker="o", markersize=10)
    plt.xlim(-1.2, 1.2)
    plt.ylim(-1.2, 1.2)
    plt.grid()
    plt.title(f"Swerve Module Angle: {np.degrees(angle):.2f}°")
    plt.show()

# Example: Rotate module to 0 degrees
plot_swerve_module(np.radians(0))