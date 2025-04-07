import sys
import math
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from kinematics import SwerveKinematics as swervekinematics

"""
    This a 2D Graph simulator that allows the user to understand how a swerve drive works.
    Kind of like a mini game to drive around a Field Oriented swerve drive on a 2d plane, which in return
    displays the Pose, and current angle of your robot and modules.
"""
try:
    import pygame
except ImportError:
    print("pygame not found. Install it using: pip install pygame")
    sys.exit(1)

# Initialize pygame
pygame.init()
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick detected: {joystick.get_name()}")
else:
    print("No joystick detected. Try reconnecting it and restarting the script.")
    sys.exit(1)

# Constants
FPS = 60
TRAIL_DURATION = 5  # seconds
RESET_BUTTON = 6  # PS4 OPTIONS button
MOVE_SPEED = 0.09  # Adjusted for slower movement

# Robot state
robot_x, robot_y, robot_theta = 0, 0, 0
trail = []

# Setup plot
fig, ax = plt.subplots()
ax.set_xlim(-7, 7)
ax.set_ylim(-7, 7)
robot_shape, = ax.plot([], [], 'b-', linewidth=2)
corners, = ax.plot([], [], 'ro', markersize=5)
trail_dots, = ax.plot([], [], 'r.', markersize=2)
text_display = ax.text(-6, 6, "", fontsize=10, verticalalignment='top')
front_marker, = ax.plot([], [], 'go', markersize=6) 

def toDegrees(angle1, angle2, angle3, angle4):
    return [math.degrees(angle1), math.degrees(angle2), math.degrees(angle3), math.degrees(angle4)]

def update(frame):
    global robot_x, robot_y, robot_theta, trail
    pygame.event.pump()
    
    # Read joystick input
    if pygame.joystick.get_count() > 0:
        vectorX = joystick.get_axis(0)  # Left stick X
        vectorY = -joystick.get_axis(1)  # Left stick Y
        omega = -joystick.get_axis(2)  # Right stick X for rotation
        
        # Deadzone correction to prevent drifting
        if abs(vectorX) < 0.1:
            vectorX = 0
        if abs(vectorY) < 0.1:
            vectorY = 0
        if abs(omega) < 0.1:
            omega = 0
    else:
        return robot_shape, corners, trail_dots, text_display, front_marker
    
    if joystick.get_button(RESET_BUTTON):
        robot_x, robot_y, robot_theta = 0, 0, 0
        trail.clear()
    
    # Compute module angles
    angles = swervekinematics.SwerveKinematics.update(vectorX, vectorY, omega)
    
    lf = math.degrees(angles["leftFront"])
    rf = math.degrees(angles["rightFront"])
    rr = math.degrees(angles["rightRear"])
    lr = math.degrees(angles["leftRear"])
    
    # Update robot position
    robot_x += vectorX * MOVE_SPEED
    robot_y += vectorY * MOVE_SPEED
    robot_theta += omega * MOVE_SPEED
    
    # Normalize theta to be within -180 to 180
    robot_theta = swervekinematics.SwerveKinematics.normalize_angle(robot_theta)
    
    # Define square shape (robot body)
    half_size = 0.5  # Square side length / 2
    corners_x = [robot_x + half_size * math.cos(robot_theta) - half_size * math.sin(robot_theta),
                 robot_x - half_size * math.cos(robot_theta) - half_size * math.sin(robot_theta),
                 robot_x - half_size * math.cos(robot_theta) + half_size * math.sin(robot_theta),
                 robot_x + half_size * math.cos(robot_theta) + half_size * math.sin(robot_theta),
                 robot_x + half_size * math.cos(robot_theta) - half_size * math.sin(robot_theta)]
    
    corners_y = [robot_y + half_size * math.sin(robot_theta) + half_size * math.cos(robot_theta),
                 robot_y - half_size * math.sin(robot_theta) + half_size * math.cos(robot_theta),
                 robot_y - half_size * math.sin(robot_theta) - half_size * math.cos(robot_theta),
                 robot_y + half_size * math.sin(robot_theta) - half_size * math.cos(robot_theta),
                 robot_y + half_size * math.sin(robot_theta) + half_size * math.cos(robot_theta)]
    
    front_x = robot_x + (half_size + 0.2) * math.cos(robot_theta)
    front_y = robot_y + (half_size + 0.2) * math.sin(robot_theta)
    
    # Update trail
    trail.append((robot_x, robot_y, time.time()))
    trail = [(x, y, t) for x, y, t in trail if time.time() - t < TRAIL_DURATION]
    
    robot_shape.set_data(corners_x, corners_y)
    corners.set_data(corners_x[:-1], corners_y[:-1])
    trail_dots.set_data([x for x, y, _ in trail], [y for x, y, _ in trail])
    front_marker.set_data([front_x], [front_y])
    text_display.set_text(f"Current Pos: ({robot_x:.2f}, {robot_y:.2f})\n"
                          f"Current Robot Angle: {robot_theta:.2f} rad / {math.degrees(robot_theta):.2f}°\n"
                          f"Module Angles (Degrees): {lf:.2f}, {rf:.2f}, {rr:.2f}, {lr:.2f}")
    
    
    return robot_shape, corners, trail_dots, text_display, front_marker

ani = animation.FuncAnimation(fig, update, interval=1000//FPS, blit=False, cache_frame_data=False)
plt.show()

pygame.quit()
