class Tile:
    def __init__(self, piece=None):
        self.top = piece
        self.down = []

    def add(self, piece):
        self.down.append(self.top)
        self.top = piece

    def pick_up(self):
        self.down.append(self.top)
        tmp = self.top
        self.top = None
        return tmp

    def back(self):
        self.top = self.down.pop()

    def get_down(self):
        return self.down[len(self.down)-1]
