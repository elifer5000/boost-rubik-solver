from video import Webcam
from boost import Boost
from solver import Solver
import threading

boost = Boost()
webcam = Webcam()
solver = Solver(boost, webcam)

print("Available commands:")
print("s   - solve the cube")
print("r   - rotate bed clockwise")
print("l   - rotate bed counter-clockwise")
print("tr   - rotate bed clockwise, gripped")
print("tl   - rotate bed counter-clockwise, gripped")
print("t   - tilt")
print("gu  - grip up")
print("gd  - grip down")
print("q   - exit")

def runloop():
    while True:
        cmd = input("Enter your command: ")
        if cmd == "r":
            boost.grip_down()
            boost.rotate(1)
        elif cmd == "l":
            boost.grip_down()
            boost.rotate(-1)
        elif cmd == "tr":
            boost.grip_up()
            boost.rotate(1, overshoot=True)
        elif cmd == "tl":   
            boost.grip_up()
            boost.rotate(-1, overshoot=True)
        elif cmd == "gu":
            boost.grip_up()
        elif cmd == "gd":
            boost.grip_down()
        elif cmd == "t":
            boost.tilt()
        elif cmd == "s":
            solver.solve()
        elif cmd == "q":
            boost.off()
            webcam.stop_video()
            break
        else:
            print("Unknown command")
            

runloop = threading.Thread(target=runloop, daemon=True)
runloop.start()
webcam.start_video()

