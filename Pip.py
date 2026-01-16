

class Pip(dict):

    def __init__(self, coords):
        if type(coords) == type(list()):
            for key in "XY":
                self[key] = coords.pop(0)
        else:
            for key in "XY":
                self[key] = coords[key]
        
        self.cache = dict()
        self.cache["str"] = f'{",".join(str(v) for v in self.values())}'
        self.cache["int"] = 10 * self["Y"] + self["X"]

    def __str__(self):
        return(self.cache["str"])

    def __int__(self):
        return(self.cache["int"])
    
    def rotate(self,sine_theta):
        Pip.__init__(
            self,
            [
                -1 * (self["Y"] * sine_theta),
                     (self["X"] * sine_theta)
            ]
        )
    def ror(self): self.rotate(1)
    def rol(self): self.rotate(-1)

    def slide(self,key,amt):
        self[key] += amt


if __name__ == "__main__":

    plist = [Pip([0,0]),Pip([1,0]),Pip([2,0]),Pip([0,1]),Pip([2,1])]
    for p in plist:
        print(f'PreRor: {str(p)}')
    for p in plist:
        p.ror()
        p.slide("X",1)
    for p in plist:
        print(f'PosRor: {p}')
    for p in plist:
        p.ror()
        p.slide("X",2)
    for p in plist:
        print(f'Further: {p}')
