class Piso:
    def __init__(self, r, g, b):
        self.red = r
        self.green = g
        self.blue = b
    def pantano(self):
        return abs(self.red - 169) < 15 \
            and abs(self.green - 135) < 15 \
            and abs(self.blue - 75) < 15
    def blackHole(self):
        return abs(self.red) < 30 \
            and abs(self.green) < 30 \
            and abs(self.blue) < 30
    def verde(self):
        return abs(self.red - 25) < 15 \
            and abs(self.green - 227) < 15 \
            and abs(self.blue - 25) < 15
    def amarillo(self):
        return abs(self.red - 234) < 15 \
            and abs(self.green - 234) < 15 \
            and abs(self.blue - 47) < 15
    def rojo(self):
        return abs(self.red - 234) < 15 \
            and abs(self.green - 47) < 15 \
            and abs(self.blue - 47) < 15

    def azul(self):
        return abs(self.red - 47) <10 \
            and abs(self.green - 47) < 10 \
            and abs(self.blue - 234) < 10

    def violeta(self):
        return abs(self.red - 109) < 15 \
            and abs(self.green - 47) < 15 \
            and abs(self.blue - 188) < 15

    def del_suelo(self):
        return abs(self.red - 195) < 2 \
            and abs(self.green - 195) < 2 \
            and abs(self.blue - 195) < 2

    def checkpoint(self):
        return abs(self.red - 70) < 15 \
            and abs(self.green - 75) < 15 \
            and abs(self.blue - 90) < 15
    def orange(self):
        return abs(self.red - 234) < 15 \
            and abs(self.green - 188) < 15 \
            and abs(self.blue - 47) < 15