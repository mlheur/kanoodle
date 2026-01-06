from Pip import Pip


class Piece(object):
    EMPTY = "-"
    STRING = "ABCDEFGHIJKL"
    DATA = [
        "A:0,0;1,0;1,1;1,2",
        "B:0,0;0,1;1,0;1,1;1,2",
        "C:0,0;0,1;0,2;0,3;1,0",
        "D:0,0;0,1;0,2;0,3;1,2",
        "E:0,0;0,1;1,1;1,2;1,3",
        "F:0,0;0,1;1,1",
        "G:0,0;0,1;0,2;1,2;2,2",
        "H:0,0;0,1;1,1;1,2;2,2",
        "I:0,0;1,0;2,0;0,1;2,1",
        "J:0,0;0,1;0,2;0,3",
        "K:0,0;0,1;1,0;1,1",
        "L:0,1;1,0;1,1;1,2;2,1",
    ]

    def __init__(self, piece_line):
        piece_gameentry = piece_line.split(":")
        self.name = piece_gameentry[0]
        all_points = piece_gameentry[1].split(";")

        self.max = {"X":0,"Y":0}

        self.pips = list()
        for pt in all_points:
            aXY = {"X":pt[0],"Y":pt[2]}
            for a in aXY:
                aXY[a] = int(aXY[a])
                if aXY[a] > self.max[a]:
                    self.max[a] = aXY[a]
            self.pips.append(Pip(aXY))

        self.normalize()
        key = self._hash_orientation()
        self.cache["orients"] = dict()
        self.cache["orients"][key] = list(self.pips)

        self.cache = dict()

        outs = ""
        for pip in self.pips:
            if outs == "":
                outs = f'{pip}'
            else:
                outs = f'{outs}; {pip}'
        outs = f'{self.name} := {outs}'
        self.cache["str"] = outs

        
    def __str__(self):
        if "str" in self.cache: return self.cache["str"]

    def normalize(self):
        self.pips.sort(key=lambda p: int(p))
        OUTS = ""
        for pip in self.pips:
            for key in "XY":
                OUTS += pip[key]
        return(int(OUTS))

    def swapXY(self):
        self.max = {
            "X": self.max["Y"],
            "Y": self.max["X"],
        }

    def ror(self):
        self.swapXY()
        for pip in self.pips:
            pip.ror()
            key="X"
            pip.slide(key,self.max[key])
        self.normalize()

    def rol(self):
        self.swapXY()
        for pip in self.pips:
            pip.rol()
            key = "Y"
            pip.slide(key,self.max[key])
        self.normalize()
    
    def flip(self):
        for pip in self.pips:
            pip["Y"] *= -1
            key = "Y"
            pip.slide(key,self.max[key])
        self.normalize()
    
    def pickup(self,field):
        for Y in range(len(field)):
            for X in range(len(field[Y])):
                if field[Y][X] == self.name:
                    field[Y][X] = self.EMPTY
    
    def place(self,field,X,Y):
        for pip in self.pips:
            FieldX = pip["X"] + X
            FieldY = pip["Y"] + Y
            if field[FieldY][FieldX] == self.EMPTY:
                field[FieldY][FieldX] = self.name
            else:
                self.pickup(field)
                return False
        return True

if __name__ == "__main__":
    p = Piece("X:1,1;2,1;3,1;1,2;3,2")
    print(f'PreRor: {p}')
    p.ror()
    print(f'PosRor: {p}')
    p.ror()
    print(f'Furthr: {p}')
    p.ror()
    print(f'Fourth: {p}')
    p.ror()
    print("")
    print(f'PreRol: {p}')
    p.rol()
    print(f'PosRol: {p}')
    p.rol()
    print(f'Furthr: {p}')
    p.rol()
    print(f'Fourth: {p}')
    p.rol()
    print("")
    print(f'PreFlip: {p}')
    p.flip()
    print(f'PosFlip: {p}')
    print("")

    pieces = dict()
    DATA = list(Piece.DATA)
    for P in Piece.STRING:
        pieces[P] = Piece(DATA.pop(0))

    for P in Piece.STRING:
        print(str(pieces[P]))
        print(f'p.xoff=[{p.xoff}]')

    for line in Piece.DATA:
        OUT = ""
        for letter in line:
            try: OUT += str(int(letter)-1)
            except: OUT += letter
        print(OUT)