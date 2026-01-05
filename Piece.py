EMPTY = "-"


from Pip import Pip


class GamePiece(object):

    def __init__(self, piece_line):
        
        self.pips = list()
        piece_gameentry = piece_line.split(":")
        self.name = piece_gameentry[0]
        all_points = piece_gameentry[1].split(";")
        self.maxX = 0
        self.maxY = 0
        for pt in all_points:
            aXY = pt.split(",")
            aXY[0] = int(aXY[0]) - 1
            aXY[1] = int(aXY[1]) - 1
            if aXY[0] > self.maxX: self.maxX = aXY[0]
            if aXY[1] > self.maxY: self.maxY = aXY[1]
            self.pips.append(Pip(aXY[0],aXY[1]))
        self.normalize()
        
    def __str__(self):
        outs = ""
        for pip in self.pips:
            if outs == "":
                outs = f'{pip}'
            else:
                outs = f'{outs}; {pip}'
        outs = f'{self.name} := {outs}'
        return outs
    
    def normalize(self):
        # The pips are stored in an ordered list.
        # The first orientation starts top,left; and proceeds
        # like english language: left to right, top to bottom.
        # After rotation/flip, the "first" pip is no longer
        # in the top left position.
        # Normalizing a piece means to re-order the list of rotated
        # points such that the "first" point is top-left again, and
        # proceeds in english language from there.
        # 
        # There are many ways to do this.  One of the most portable way to
        # place a 2D grid into a list is row by row, where value(0,0) is 1; and value(0,1) is MaxY + 1.
        # Since Kanoodle knows in advance there's at most 4 pips in any direction, it will
        # be much simpler to just set the value(X,Y) = X + 10 * Y.
        #
        # Once we can assign a linear value to every cell in the 2D grid,
        # we can feed the array into a general sort algorithm.
        self.pips.sort(key=lambda p: (p.X + 10*p.Y))

    def ror(self):
        temp = self.maxX
        self.maxX = self.maxY
        self.maxY = temp
        for pip in self.pips:
            pip.ror()
            pip.trxlate(self.maxX,0)
        self.normalize()

    def rol(self):
        temp = self.maxX
        self.maxX = self.maxY
        self.maxY = temp
        for pip in self.pips:
            pip.rol()
            pip.trxlate(0,self.maxY)
        self.normalize()
    
    def flip(self):
        for pip in self.pips:
            pip.Y = pip.Y * -1
            pip.Y = pip.Y + self.maxY
        self.normalize()
    
    def pickup(self,field):
        for Y in range(len(field)):
            for X in range(len(field[Y])):
                if field[Y][X] == self.name:
                    field[Y][X] = EMPTY
    
    def place(self,field,X,Y):
        for pip in self.pips:
            FieldX = pip.X + X
            FieldY = pip.Y + Y
            if field[FieldY][FieldX] == EMPTY:
                field[FieldY][FieldX] = self.name
            else:
                self.pickup(field)
                return False
        return True
    
    def getLeftOffset(self):
        offX = 0
        minX = 0
        for pip in self.pips:
            pass
        return(offX)


if __name__ == "__main__":
    gp = GamePiece("X:1,1;2,1;3,1;1,2;3,2")
    print(f'PreRor: {gp}')
    gp.ror()
    print(f'PosRor: {gp}')
    gp.ror()
    print(f'Furthr: {gp}')
    gp.ror()
    print(f'Fourth: {gp}')
    gp.ror()
    print("")
    print(f'PreRol: {gp}')
    gp.rol()
    print(f'PosRol: {gp}')
    gp.rol()
    print(f'Furthr: {gp}')
    gp.rol()
    print(f'Fourth: {gp}')
    gp.rol()
    print("")
    print(f'PreFlip: {gp}')
    gp.flip()
    print(f'PosFlip: {gp}')
    print("")
