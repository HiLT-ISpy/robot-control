vocab = {
    "and": ["+", "and"],
    "down": ["down", "downward", "floor", "ground", "low"],
    "forward": ["ahead", "forward", "forwards", "fwd", "straight"],
    "left": ["l", "left"],
    "look": ["look", "turn"],
    "point": ["motion", "point", "pointing", "signal"],
    "right": ["r", "right"],
    "stop": ["end", "exit", "close", "stop", "quit"],
    "up": ["high", "sky", "up", "upward"]
}

def introduce():
    print "Hi, I'm Bobby. What would you like me to do?"
    print "Examples: Is it pink? Point to the left. Look down."

def meaning(words):
    for word in words:
        for simple_word in vocab:
            if word in vocab[simple_word]:
                return simple_word
    return None
