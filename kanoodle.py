# List of Game Pieces.
#  Syntax: x,y values of any one rotation of all the pips on a piece.
# X :=> the column, the distance along the X axis, with 0 as leftmost and max_cols as rightmost.
# Y :=> the row, the distance down the Y axis, with 0 as the topmost and max_rows as bottommost.
# White       F:1,1;1,2;2,2
# Purple      J:1,1;1,2;1,4;1,4
# Orange      A:1,1;2,1;2,2;2,3
# BrightGreen K:1,1;1,2;2,1;2,2
# DarkGreen   E:1,1;1,2;2,2;2,3;2,4
# Red         B:1,1;1,2;2,1;2,2;2,3
# Azure       G:1,1;1,2,1,3;2,3;3,3
# Grey        L:1,2;2,1;2,2;2,3;3,2
# Blue        C:1,1;1,2;1,3;1,4;2,1
# Pink        D:1,1;1,2;1,3;1,4;2,3
# Magenta     H:1,1;1,2;2,2;2,3;3,3
# Yellow      I:1,1;2,1;3,1;1,2;3,2

DAT_FILENAME = "GamePieces.dat"


class Pip(object):

    def __init__(self,X,Y):
        self.X = X
        self.Y = Y

    def __str__(self):
        return(f'{self.X+1},{self.Y+1}')
    
    def rotate(self,sintheta):
        newX = -1 * (self.Y * sintheta)
        newY = (self.X * sintheta)
        self.X = newX
        self.Y = newY   
    def ror(self): self.rotate(1)
    def rol(self): self.rotate(-1)

    def trxlate(self,xoff,yoff):
        self.X = self.X + xoff
        self.Y = self.Y + yoff

#if __name__ == "__main__":
#    plist = {Pip(0,0),Pip(1,0),Pip(2,0),Pip(0,1),Pip(2,1)}
#    for p in plist:
#        print(f'PreRor: {p}')
#    for p in plist:
#        p.ror()
#        p.trxlate(1,0)
#    for p in plist:
#        print(f'PosRor: {p}')
#    for p in plist:
#        p.ror()
#        p.trxlate(2,0)
#    for p in plist:
#        print(f'Further: {p}')


class GamePiece(object):

    def __init__(self, piece_line):
        self.pips = list()
        piece_parts = piece_line.split(":")
        self.name = piece_parts[0]
        all_points = piece_parts[1].split(";")
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
        # map a 2D grid into a list is row by row, where value(0,0) is 1; and value(0,1) is MaxY + 1.
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
    
    def unmap(self,field):
        for Y in range(len(field)):
            for X in range(len(field[Y])):
                if field[Y][X] == self.name:
                    field[Y][X] = " "
    
    def map(self,field,X,Y):
        for pip in self.pips:
            FieldX = pip.X + X
            FieldY = pip.Y + Y
            if field[FieldY][FieldX] == " ":
                field[FieldY][FieldX] = self.name
            else:
                self.unmap(field)
                return False
        return True


#if __name__ == "__main__":
#    gp = GamePiece("X:1,1;2,1;3,1;1,2;3,2")
#    print(f'PreRor: {gp}')
#    gp.ror()
#    print(f'PosRor: {gp}')
#    gp.ror()
#    print(f'Furthr: {gp}')
#    gp.ror()
#    print(f'Fourth: {gp}')
#    gp.ror()
#    print("")
#    print(f'PreRol: {gp}')
#    gp.rol()
#    print(f'PosRol: {gp}')
#    gp.rol()
#    print(f'Furthr: {gp}')
#    gp.rol()
#    print(f'Fourth: {gp}')
#    gp.rol()
#    print("")
#    print(f'PreFlip: {gp}')
#    gp.flip()
#    print(f'PosFlip: {gp}')
#    print("")


class Kanoodle(object):

    def __init__(self, dat_filename, width, height):
        self.height = height
        self.width = width
        self.pieces = dict()
        try:
            with open(dat_filename, 'r', encoding='utf-8') as f:
                piece_line = f.readline().rstrip()
                while piece_line:
                    gp = GamePiece(piece_line)
                    self.pieces[gp.name] = gp
                    piece_line = f.readline().rstrip()
        except FileNotFoundError:
            print(f'Fata: Could not find [{dat_filename}]')
            return
        except Exception as e:
            print(f'Fatal error [{e}]')
            return
        
        self.field = list()
        for Y in range(self.height):
            self.field.append(list(" "*self.width))
        
    def __str__(self):
        outs = ""
#        for piece in self.pieces:
#            if outs == "":
#                outs = f'{piece}\n'
#            else:
#                outs = f'{outs}{piece}\n'

        for row in self.field:
            outs = f'{outs}{row}\n'

        return outs.rstrip()


if __name__ == "__main__":
    k = Kanoodle(DAT_FILENAME,11,5)
    for P in "ABCDEFGHI":
        for j in range(2):
            for i in range(4):
                k.pieces[P].map(k.field,0,0)
                print(f'{k}\n')
                k.pieces[P].unmap(k.field)
                k.pieces[P].ror()
            k.pieces[P].flip()
