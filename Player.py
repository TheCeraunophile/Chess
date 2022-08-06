class Player:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.name == other.name
        return False
