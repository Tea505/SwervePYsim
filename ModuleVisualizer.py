import math
from math import atan2, degrees, hypot, radians, cos, sin
import pygame
from kinematics import SwerveKinematics

# Initialize pygame
pygame.init()
pygame.joystick.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Swerve Module Visualizer")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    joystick = None
    print("No joystick detected.")
    
module_labels = {
    "leftFront": "LF",
    "rightFront": "RF",
    "leftRear": "LR",
    "rightRear": "RR"
}

# Robot dimensions (in inches)
TRACKWIDTH = 8
WHEELBASE = 8
ROBOT_WIDTH_PX = 200
ROBOT_CENTER = (400, 300)

# State
last_angles = {m: 0 for m in ["rightFront", "leftFront", "leftRear", "rightRear"]}
robot_heading = math.radians(90) # in radians
field_centric = False
robot_centric = True;

def draw_arrow(surface, x, y, angle_rad, length=40, color=(255, 255, 0)):
    end_x = x + length * cos(angle_rad)
    end_y = y + length * sin(angle_rad)
    pygame.draw.line(surface, color, (x, y), (end_x, end_y), 3)
    pygame.draw.circle(surface, color, (int(end_x), int(end_y)), 4)

def draw_compass(surface):
    compass_center = (700, 100)
    radius = 40
    pygame.draw.circle(surface, (255, 255, 255), compass_center, radius, 1)
    for angle_deg in [0, 90, 180, 270]:
        angle_rad = math.radians(-angle_deg)
        label = font.render(str(angle_deg), True, (255, 255, 255))
        label_pos = (
            compass_center[0] + (radius + 15) * cos(angle_rad) - label.get_width() // 2,
            compass_center[1] + (radius + 15) * sin(angle_rad) - label.get_height() // 2
        )
        surface.blit(label, label_pos)
        
    needle_len = 30
    needle_angle = -robot_heading
    end_x = compass_center[0] + needle_len * cos(needle_angle)
    end_y = compass_center[1] + needle_len * sin(needle_angle)
    pygame.draw.line(surface, (255, 0, 0), compass_center, (end_x, end_y), 3)

def draw_robot_markers(surface, center, size, angle_rad):
    half = size // 2
    front_x = center[0] + half * cos(angle_rad)
    front_y = center[1] + half * sin(angle_rad)
    back_x = center[0] - half * cos(angle_rad)
    back_y = center[1] - half * sin(angle_rad)
    pygame.draw.circle(surface, (0, 255, 0), (int(front_x), int(front_y)), 6)
    surface.blit(font.render("Front", True, (0, 255, 0)), (front_x + 10, front_y))
    pygame.draw.circle(surface, (255, 0, 0), (int(back_x), int(back_y)), 6)
    surface.blit(font.render("Back", True, (255, 0, 0)), (back_x + 10, back_y))

# Module positions (relative)
module_offsets = {
    "leftFront": (-ROBOT_WIDTH_PX // 2, -ROBOT_WIDTH_PX // 2),
    "rightFront": (ROBOT_WIDTH_PX // 2, -ROBOT_WIDTH_PX // 2),
    "leftRear": (-ROBOT_WIDTH_PX // 2, ROBOT_WIDTH_PX // 2),
    "rightRear": (ROBOT_WIDTH_PX // 2, ROBOT_WIDTH_PX // 2)
}

last_hat = (0, 0) 
rotation_enabled = True
last_button_a = False

# --- Main Loop ---
running = True
while running:
    screen.fill((0, 0, 0))
    vx = vy = rot = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if joystick:
        pygame.event.pump()
        vx = joystick.get_axis(0)
        vy = -joystick.get_axis(1)
        rot = joystick.get_axis(2)
        
        hat_x, hat_y = joystick.get_hat(0)
        
        if hat_y == 1 and last_hat[1] != 1:  # D-pad up just pressed
            field_centric = True
            robot_centric = False
        elif hat_y == -1 and last_hat[1] != -1:  # D-pad down just pressed
            field_centric = False
            robot_centric = True

        last_hat = (hat_x, hat_y)  # Update last hat state
        
        button_a = joystick.get_button(0)
        if button_a and not last_button_a:
            rotation_enabled = not rotation_enabled
        last_button_a = button_a
        
    if field_centric:
        # Always interpret joystick as if robot is facing up (90°)
        angle = math.radians(-90)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        temp_vx = vx * cos_a - vy * sin_a
        temp_vy = vx * sin_a + vy * cos_a
        vx, vy = temp_vx, temp_vy

    elif robot_centric:
        # Use current heading to rotate joystick input relative to robot
        angle = -robot_heading
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        temp_vx = vx * cos_a - vy * sin_a
        temp_vy = vx * sin_a + vy * cos_a
        vx, vy = temp_vx, temp_vy

    if abs(vx) > 0.05 or abs(vy) > 0.05 or abs(rot) > 0.05:
        angles = SwerveKinematics.SwerveKinematics.update(vx, vy, rot)
        for key in angles:
            last_angles[key] = SwerveKinematics.SwerveKinematics.normalize_angle(angles[key])
        if rotation_enabled:
            robot_heading += rot * 0.05

    # Draw rotated robot square
    half = ROBOT_WIDTH_PX // 2
    corners = [(-half, -half), (half, -half), (half, half), (-half, half)]
    rotated = [(ROBOT_CENTER[0] + x * cos(robot_heading) - y * sin(robot_heading),
                 ROBOT_CENTER[1] + x * sin(robot_heading) + y * cos(robot_heading)) for x, y in corners]
    pygame.draw.polygon(screen, (50, 150, 255), rotated, 3)

    draw_robot_markers(screen, ROBOT_CENTER, ROBOT_WIDTH_PX, robot_heading)

    for i, (key, (dx, dy)) in enumerate(module_offsets.items()):
        rotated_dx = dx * cos(robot_heading) - dy * sin(robot_heading)
        rotated_dy = dx * sin(robot_heading) + dy * cos(robot_heading)
        mx = ROBOT_CENTER[0] + rotated_dx
        my = ROBOT_CENTER[1] + rotated_dy
        pygame.draw.circle(screen, (200, 200, 200), (int(mx), int(my)), 20, 2)
        angle_rad = last_angles[key]
        if field_centric:
            draw_arrow(screen, mx, my, angle_rad, length=40)
        elif robot_centric:
            draw_arrow(screen, mx, my, angle_rad + robot_heading, length=40)
        label = font.render(f"{key}: {int(degrees(angle_rad))}°", True, (255, 255, 255))
        screen.blit(label, (20, 20 + i * 25))

    fps = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 0))
    screen.blit(fps, (10, 570))
    
    mode = "Field-Centric" if field_centric else "Robot-Centric" if robot_centric else "Unknown"
    mode_label = font.render(f"Mode: {mode}", True, (0, 255, 255))
    screen.blit(mode_label, (615, 570))
    rot_status = "Enabled" if rotation_enabled else "Disabled"
    screen.blit(font.render(f"Rotation: {rot_status}", True, (255, 255, 0)), (20, 155))
    
    draw_compass(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()