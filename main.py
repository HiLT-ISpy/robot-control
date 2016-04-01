import robot
from language import meaning

print "Hi, I'm Bobby. What would you like me to do?"
print "Examples: Is it pink? Point to the left. Look down."

words = ""
while meaning(words) != "quit":
    # get instructions
    text = raw_input("> ")
    text = text.lower()
    words = text.split()

    # looking
    if meaning(words) is "look":
        if meaning(words[1:]) is "right":
            # look right
            print "look r"
        elif meaning(words[1:]) is "left":
            # look left
            print "look l"
        elif meaning(words[1:]) is "up":
            print "look u"
        elif meaning(words[1:]) is "down":
            print "look d"

    # pointing
    elif meaning(words) is "point":
        if meaning(words[1:]) is "right":
            print "point r"
        elif meaning(words[1:]) is "left":
            print "point l"
        elif meaning(words[1:]) is "up":
            print "point u"
        elif meaning(words[1:]) is "down":
            print "point d"

    # speaking
    else:
        # account for "Ask if it's blue", "Say, "Is it blue?", "Ask him if it's blue"
        # speak text
        print text
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
