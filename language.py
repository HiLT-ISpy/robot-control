vocab = {
    "down": ["down", "downward", "floor", "ground", "low"],
    "left": ["l", "left"],
    "look": ["look", "turn"],
    "point": ["motion", "point", "signal"],
    "quit": ["end", "exit", "close", "stop", "quit"],
    "right": ["r", "right"],
    "up": ["high", "sky", "up", "upward"]
}

def meaning(words):
    for word in words:
        for simple_word in vocab:
            if word in vocab[simple_word]:
                return simple_word
    return None
