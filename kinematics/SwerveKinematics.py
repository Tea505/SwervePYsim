import math

TRACKWIDTH = 8  # in inches
WHEELBASE = 8   # in inches

class SwerveKinematics(): 
        
    @staticmethod
    def update(vectorX, vectorY, omega):
        D = math.hypot(TRACKWIDTH, WHEELBASE) # Diagnal distance between front n back wheels
    
        A = vectorX - omega * (TRACKWIDTH / D)
        B = vectorX + omega * (TRACKWIDTH / D)
        C = vectorY - omega * (WHEELBASE / D)
        D = vectorY + omega * (WHEELBASE / D)

        return {
            "leftFront": math.atan2(B, C),  # Left Front
            "rightFront": math.atan2(B, D),  # Right Front
            "rightRear": math.atan2(A, D),  # Right Rear
            "leftRear": math.atan2(A, C)   # Left Rear
        }
        
    @staticmethod
    def normalize_angle(angle):
        """ Normalize angle to be within the range -180 to 180 degrees """
        angle_deg = math.degrees(angle)
        angle_deg = (angle_deg + 180) % 360 - 180
        return math.radians(angle_deg)
    
    
