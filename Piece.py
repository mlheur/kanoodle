EMPTY = "-"


from Pip import Pip


class Piece(object):

    def __computeLeftOffste(self):
        minX = 99
        for pip in self.pips:
            if pip.Y == 0 and minX > pip.X:
                minX = pip.X
        return(minX * -1)

    def __ror(self):
        temp = self.maxX
        self.maxX = self.maxY
        self.maxY = temp
        for pip in self.pips:
            pip.ror()
            pip.trxlate(self.maxX,0)
        self.__normalize()
    
    def __flip(self):
        for pip in self.pips:
            pip.Y = pip.Y * -1
            pip.Y = pip.Y + self.maxY
        self.__normalize()


    def __init__(self, piece_gameentry):
        self.current_orientation = None
        self.pips = list()
        self.name = piece_gameentry[0]
        all_points = piece_gameentry[1].split(";")
        self.maxX = 0
        self.maxY = 0
        for pt in all_points:
            #print(f'pt={pt}')
            aXY = pt.split(",")
            #print(f'aXY[0]={aXY[0]} aXY[1]={aXY[1]}')
            aXY[0] = int(aXY[0]) - 1
            aXY[1] = int(aXY[1]) - 1
            if aXY[0] > self.maxX: self.maxX = aXY[0]
            if aXY[1] > self.maxY: self.maxY = aXY[1]
            self.pips.append(Pip(aXY[0],aXY[1]))
        self.__normalize()

        self.offsets = dict()
        self.offsets["rotate"] = list()
        self.offsets["unique"] = list()

        self.orientations = list()
        self.unique_orientations = dict()
        self.unique_keys = list()
        self.qty_unique = 0
        for i in range(2):
            for j in range(4):
                new_pips = list()
                new_uniq = list()
                for pip in self.pips:
                    new_pips.append(Pip(pip.X,pip.Y))
                    new_uniq.append(Pip(pip.X,pip.Y))
                #print(f'Adding pip list [{new_pips}] to self.orientations')
                self.orientations.append(new_pips)
                leftoff = self.__computeLeftOffste()
                self.offsets["rotate"].append(leftoff)
                key = str(int(self))
                if key not in self.unique_orientations:
                    self.unique_orientations[key] = new_uniq
                    self.unique_keys.append(key)
                    self.offsets["unique"].append(leftoff)
                    self.qty_unique += 1
                self.__ror()
            self.__flip()
        self.mode = "rotate"
        self.current_orientation = 0
        self.current_unique = 0
        self.pips = None
        del self.pips

        #print(f'Piece [{self.name}] initialized with offset [{self.offsets}]')
        #print(f'Piece [{self.name}] initialized with orientations [{self.orientations}]')
        #print(f'Piece [{self.name}] initialized with self.unique_keys [{self.unique_keys}]')
        #print(f'Piece [{self.name}] initialized with self.unique_orientations [{self.unique_orientations}]')

    def __str__(self):
        outs = ""
        for pip in self.orientations[self.current_orientation]:
            if outs == "":
                outs = f'{pip}'
            else:
                outs = f'{outs}; {pip}'
        outs = f'{self.name} := {outs}'
        return outs

    def __int__(self):
        outs = ""
        if self.current_orientation is None:
            for pip in self.pips:
                outs += str(int(pip))
        else:
            for pip in self.orientations[self.current_orientation]:
                outs += str(int(pip))
        return(int(outs))

    def __normalize(self):
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
        self.current_orientation = self.current_orientation + 1
        if self.current_orientation == 4:
            self.current_orientation = 0
        elif self.current_orientation == 8:
            self.current_orientation = 4
    
    def rol(self):
        self.current_orientation = self.current_orientation - 1
        if self.current_orientation == 3:
            self.current_orientation = 7
        elif self.current_orientation == -1:
            self.current_orientation = 3
    
    def flip(self):
        if self.current_orientation < 4:
            self.current_orientation = self.current_orientation + 4
        else:
            self.current_orientation = self.current_orientation - 4
    
    def toggle(self):
        if self.mode == "rotate":
            self.mode == "unique"
        else:
            self.mode = "rotate"

    def next(self):
        if self.mode != "unique":
            self.mode = "unique"
        else:
            self.current_unique += 1
            if self.current_unique >= self.qty_unique:
                self.current_unique = 0
                return False
        return True
    
    def pickup(self,field):
        for Y in range(len(field)):
            for X in range(len(field[Y])):
                if field[Y][X] == self.name:
                    field[Y][X] = EMPTY
    
    def place(self,field,X,Y):

        def put(p):
            FieldX = p.X + X
            FieldY = p.Y + Y
            if field[FieldY][FieldX] == EMPTY:
                field[FieldY][FieldX] = self.name
            else:
                self.pickup(field)
                return False
            return True

        if self.mode == "rotate":
            for pip in self.orientations[self.current_orientation]:
                if not put(pip):
                    return False
        elif self.mode == "unique":
            key = self.unique_keys[self.current_unique]
            for pip in self.unique_orientations[key]:
                if not put(pip):
                    return False
        else:
            return False
        return True
    
    def getLeftOffset(self):
        if self.mode == "rotate":
            return self.offsets[self.mode][self.current_orientation]
        elif self.mode == "unique":
            return self.offsets[self.mode][self.current_unique]
    

if __name__ == "__main__":
    p = Piece(["0","1,1;2,1;3,1;1,2;3,2"])
    print(f'PreRor: int(p)=[{int(p)}] {p}')
    p.ror()
    print(f'PosRor: int(p)=[{int(p)}] {p}')
    p.ror()
    print(f'Furthr: int(p)=[{int(p)}] {p}')
    p.ror()
    print(f'Fourth: int(p)=[{int(p)}] {p}')
    p.ror()
    print("")
    print(f'PreRol: int(p)=[{int(p)}] {p}')
    p.rol()
    print(f'PosRol: int(p)=[{int(p)}] {p}')
    p.rol()
    print(f'Furthr: int(p)=[{int(p)}] {p}')
    p.rol()
    print(f'Fourth: int(p)=[{int(p)}] {p}')
    p.rol()
    print("")
    print(f'PreFlip: int(p)=[{int(p)}] {p}')
    p.flip()
    print(f'PosFlip: int(p)=[{int(p)}] {p}')
    print("")
