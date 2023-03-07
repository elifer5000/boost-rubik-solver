from pylgbst.hub import MoveHub, COLORS, COLOR_NONE, COLOR_RED
from pylgbst import get_connection_bleak
import time
import logging

QUARTER_TURN = 90

RTURN_OVERSHOOT = 24
LTURN_OVERSHOOT = -19

GRIP_TURN = 90
ROD_TURN = 80

class Boost():
    def __init__(self):
        self.grip = None
        self.hub = MoveHub(get_connection_bleak(hub_mac = "29D856D4-DE36-C0DC-D386-DADD8B1EA8AF"))
        
        
    def rotate(self, direction: int, overshoot: bool = False):
        overshoot_value = 0
        if overshoot:
            if direction > 0:
                overshoot_value = RTURN_OVERSHOOT
            else:
                overshoot_value = LTURN_OVERSHOOT

        print(direction*QUARTER_TURN + overshoot_value)
        self.hub.motor_external.angled(direction*QUARTER_TURN + overshoot_value, 0.3)
        if overshoot:
            self.hub.motor_external.angled(-overshoot_value, 2)
        
    def grip_up(self):
        if self.grip == True:
            return True
        self.hub.motor_B.angled(-GRIP_TURN, 0.2)
        self.grip = True
        
    def grip_down(self):
        if self.grip == False:
            return
        self.hub.motor_B.angled(GRIP_TURN, 0.2)
        self.grip = False
        
    
    def tilt(self):
        self.grip_down()
        self.hub.motor_A.angled(-ROD_TURN, 0.5)
        self.hub.motor_A.angled(ROD_TURN, 0.8)
        self.grip_up()

    def off(self):
        self.hub.switch_off()


