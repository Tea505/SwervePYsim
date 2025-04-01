import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
"""
A Swerve kinematic calculator that converts x,y,z to module angle.
"""
# Function to compute angles
def compute_angles(vectorX, vectorY, omega):
    D = math.hypot(8, 8) # TRACKWIDTH n WHEELBASE = 8 (inches)
    A = vectorX - omega * (8 / D)
    B = vectorX + omega * (8 / D)
    C = vectorY - omega * (8 / D)
    D = vectorY + omega * (8 / D)
    
    angles_rad = [math.atan2(B, C), math.atan2(B, D), math.atan2(A, D), math.atan2(A, C)]
    angles_deg = [np.degrees(a) for a in angles_rad]
    
    return angles_rad, angles_deg

# Initial values
vectorX, vectorY, omega = 0, 0, 0
angles_rad, angles_deg = compute_angles(vectorX, vectorY, omega)

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.4)
text_display = ax.text(0.5, 0.5, '', ha='center', va='center', fontsize=12)
ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)

def update_display():
    angles_rad, angles_deg = compute_angles(vectorX, vectorY, omega)
    text_display.set_text(
        f"Left Front: {angles_rad[0]:.2f} rad | {angles_deg[0]:.2f}°\n"
        f"Right Front: {angles_rad[1]:.2f} rad | {angles_deg[1]:.2f}°\n"
        f"Right Rear: {angles_rad[2]:.2f} rad | {angles_deg[2]:.2f}°\n"
        f"Left Rear: {angles_rad[3]:.2f} rad | {angles_deg[3]:.2f}°"
    )
    fig.canvas.draw_idle()

ax_vx = plt.axes([0.1, 0.25, 0.65, 0.03])
ax_vy = plt.axes([0.1, 0.2, 0.65, 0.03])
ax_omega = plt.axes([0.1, 0.15, 0.65, 0.03])
ax_reset = plt.axes([0.8, 0.05, 0.1, 0.05])

slider_vx = Slider(ax_vx, 'Vector X', -1.0, 1.0, valinit=vectorX)
slider_vy = Slider(ax_vy, 'Vector Y', -1.0, 1.0, valinit=vectorY)
slider_omega = Slider(ax_omega, 'Omega', -1.0, 1.0, valinit=omega)
reset_button = Button(ax_reset, 'Reset')

def update_vx(val):
    global vectorX
    vectorX = slider_vx.val
    update_display()

def update_vy(val):
    global vectorY
    vectorY = slider_vy.val
    update_display()

def update_omega(val):
    global omega
    omega = slider_omega.val
    update_display()
    
def reset_values(event):
    global vectorX, vectorY, omega
    vectorX, vectorY, omega = 0, 0, 0
    slider_vx.set_val(0)
    slider_vy.set_val(0)
    slider_omega.set_val(0)
    update_display()

slider_vx.on_changed(update_vx)
slider_vy.on_changed(update_vy)
slider_omega.on_changed(update_omega)
reset_button.on_clicked(reset_values)

update_display()
plt.show()