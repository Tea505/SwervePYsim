import math
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pygame
from kinematics import SwerveKinematics

pygame.init()
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick detected: {joystick.get_name()}")
else:
    print("No joystick detected. Try reconnecting it and restarting the script.")
    #sys.exit(1)

# Constants
FPS = 60        # Frames per second
Arrow_dt = 3    # Arrow Duration

x_min, x_max = -15, 15
y_min, y_max = -15, 15

robot_size = 8
half_size = robot_size / 2

corners = {
    "leftFront": (-half_size, half_size),
    "rightFront": (half_size, half_size),
    "rightRear": (half_size, -half_size),
    "leftRear": (-half_size, -half_size)
}

edges = [
    ("leftFront", "rightFront"),
    ("rightFront", "rightRear"),
    ("rightRear", "leftRear"),
    ("leftRear", "leftFront")
]

vectorX, vectorY, omega = 0, 0, 0  # initial values

fig, ax = plt.subplots()
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_xticks(np.arange(x_min, x_max + 1, 5))
ax.set_yticks(np.arange(y_min, y_max + 1, 5))
ax.grid(True, linestyle='--', alpha=0.6)
ax.set_aspect('equal')
    
angles = SwerveKinematics.SwerveKinematics.update(vectorX, vectorY, omega)
normalized_angles = {label: SwerveKinematics.SwerveKinematics.normalize_angle(angle) for label, angle in angles.items()}
square_heading = np.deg2rad(0)
 
# Plotting setup
for start, end in edges:
    x_values = [corners[start][0], corners[end][0]]
    y_values = [corners[start][1], corners[end][1]]
    ax.plot(x_values, y_values, 'k-', linewidth=2)
    
for label, (x, y) in corners.items():
    ax.scatter(x, y, color='red', s=50)  # Small circles at corners
    ax.text(x, y, label, fontsize=12, verticalalignment='bottom', horizontalalignment='right')
    
def draw_arrow(x, y, angle, length=1):
    return ax.annotate('', 
                       xy=(x + length * math.cos(angle), y + length * math.sin(angle)),
                       xytext=(x, y),
                       arrowprops=dict(facecolor='green', edgecolor='green', arrowstyle='->', lw=2))
    
def draw_corner_arrows():
    arrows = []
    for label, (x, y) in corners.items():
        # Draw arrow for each corner based on its angle
        arrow = ax.annotate('', 
                            xy=(x + 1 * math.cos(normalized_angles[label]), 
                                y + 1 * math.sin(normalized_angles[label])),
                            xytext=(x, y),
                            arrowprops=dict(facecolor='blue', edgecolor='blue', arrowstyle='->', lw=2))
        arrows.append(arrow)
    return arrows

# Set axis labels and title
ax.set_title('Swerve Module Simulation')
ax.set_xlabel('X')
ax.set_ylabel('Y')

def update(frame):
    global vectorX, vectorY, omega

    # Example inputs from joystick values (for now, these are placeholders)
    vectorX = np.sin(np.radians(frame))  # simulate joystick X input (left stick)
    vectorY = np.cos(np.radians(frame))  # simulate joystick Y input (left stick)
    omega = np.sin(np.radians(frame)) * 0.5  # simulate right joystick X input for omega (rotation)

    # Calculate angles using kinematics
    angles = SwerveKinematics.SwerveKinematics.update(vectorX, vectorY, omega)
    normalized_angles = {label: SwerveKinematics.SwerveKinematics.normalize_angle(angle) for label, angle in angles.items()}

    # Update the square's heading arrow
    ax.patches.clear()  # Clear old arrows
    draw_arrow(0, 0, math.atan2(vectorY, vectorX))  # Draw the central arrow pointing in the square's heading direction
    corner_arrows = draw_corner_arrows()  # Draw arrows for each corner

    return corner_arrows  # Return updated arrows for animation

# Animation loop
ani = animation.FuncAnimation(fig, update, interval=1000//FPS, blit=False)
plt.show()
    
pygame.quit()