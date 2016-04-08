import math
from language import meaning, introduce
import robot

robot_ip = "bobby.local"
robot.connect(robot_ip)
robot.robot().wake()
robot.robot().stand()
robot.robot().trackFace()
introduce()

words = ""
while not (len(words) == 1 and meaning(words) == "stop"):
    # get instructions
    text = raw_input("> ")
    text = text.lower()
    words = text.split()

    # looking
    if meaning(words) is "look":
        if meaning(words[1:]) is "forward":
            robot.robot().turnHead(yaw = 0, pitch = -5)
        elif meaning(words[1:]) is "right":
            robot.robot().turnHead(yaw = -60, pitch = -5)
        elif meaning(words[1:]) is "left":
            robot.robot().turnHead(yaw = 60, pitch = -5)
        elif meaning(words[1:]) is "up":
            robot.robot().turnHead(pitch = -25)
        elif meaning(words[1:]) is "down":
            robot.robot().turnHead(pitch = 30)

    # pointing
    elif meaning(words) is "point":
        if meaning(words[1:]) is "right":
            robot.robot().moveRightArm(10)
        elif meaning(words[1:]) is "left":
            robot.robot().moveLeftArm(10)

    # speaking
    elif meaning(words) != "stop":
        robot.robot().say(text, block = False)
        # account for "Ask if it's blue", "Say, "Is it blue?", "Ask him if it's blue"

    # stopping actions
    if meaning(words) is "stop":
        if meaning(words[1:]) is "point":
            robot.robot().moveRightArm(80)
            robot.robot().moveLeftArm(80)

robot.robot().rest()

# rest arm angles [L, R]: [[1.389762043952942, 0.1548919677734375, -0.7992560863494873, -1.0553500652313232, 0.18557214736938477, 0.014799952507019043], [1.4235939979553223, -0.16264605522155762, 0.7899680137634277, 1.0462298393249512, -0.1825878620147705, 0.014799952507019043]]
# r-arm pointing arm angles: [[1.3805580139160156, 0.11807608604431152, -0.8069260120391846, -1.084496021270752, 0.1840381622314453, 0.014799952507019043], [0.3804740905761719, 0.21318411827087402, 0.6825881004333496, 0.05066394805908203, -0.14270401000976562, 0.014799952507019043]]

"""
speaking
    is it pink
    does it have designs on it
    is it the green ball

pointing
    point right
    point left

looking
    look down
    look right
    look left
    look up
"""
