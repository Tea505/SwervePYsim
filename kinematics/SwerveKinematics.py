import math

TRACKWIDTH = 8  # in inches
WHEELBASE = 8   # in inches

class SwerveKinematics(): 
        
    @staticmethod
    def update(vectorX, vectorY, omega):
        R = math.hypot(TRACKWIDTH, WHEELBASE) # Diagnal distance between front n back wheels
    
        A = vectorX - omega * (TRACKWIDTH / R)
        B = vectorX + omega * (TRACKWIDTH / R)
        C = vectorY - omega * (WHEELBASE / R)
        D = vectorY + omega * (WHEELBASE / R)

        return {
            "rightFront": math.atan2(B, C),  # Right Front
            "leftFront": math.atan2(B, D),  # Left Front
            "leftRear": math.atan2(A, D),  # Left Rear
            "rightRear": math.atan2(A, C)   # Right Rear
        }
        
    @staticmethod
    def normalize_angle(angle):
        """ Normalize angle to be within the range -180 to 180 degrees """
        angle_deg = math.degrees(angle)
        angle_deg = (angle_deg + 180) % 360 - 180
        return math.radians(angle_deg)
    
    
