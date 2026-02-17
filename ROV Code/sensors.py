flags = {
    "piConnect": False
}  # TODO: I also need to set up a flag to detect pi connection
data = {
    "intTemp": 0,
    "extTemp": 0,
    "pressure": 0,
    "depth": 0
}

def setPiConnection(c: bool):
    flags["piConnect"] = c