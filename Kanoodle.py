from Piece import Piece
from Solver import Solver


class Kanoodle(object):
    width = 11
    height = 5

    def __init__(self):
        self.colors = dict()
        self.colors[Piece.EMPTY] = '\x1B[38;5;234m'
        self.colors["A"] = '\x1B[38;5;208m'
        self.colors["B"] = '\x1B[38;5;196m'
        self.colors["C"] = '\x1B[38;5;20m'
        self.colors["D"] = '\x1B[38;5;222m'
        self.colors["E"] = '\x1B[38;5;34m'
        self.colors["F"] = '\x1B[38;5;15m'
        self.colors["G"] = '\x1B[38;5;14m'
        self.colors["H"] = '\x1B[38;5;163m'
        self.colors["I"] = '\x1B[38;5;226m'
        self.colors["J"] = '\x1B[38;5;165m'
        self.colors["K"] = '\x1B[38;5;82m'
        self.colors["L"] = '\x1B[38;5;245m'
        self.colors[0]   = '\x1B[0m'

        DATA = list(Piece.DATA)
        self.pieces = dict()
        for P in Piece.STRING:
            self.pieces[P] = Piece(DATA.pop(0))

        self.field = list()
        for Y in range(self.height):
            self.field.append(list(Piece.EMPTY*self.width))
        
    def __str__(self):
        outs = ""
#        for piece in self.pieces:
#            if outs == "": outs = f'{piece}\n'
#            else: outs = f'{outs}{piece}\n'
        for row in self.field:
            outs = f'{outs}{row}\n'
        return outs.rstrip()
    
    def redraw(self):
        for row in self.field:
            srow = ""
            for letter in row:
                srow += self.colors[letter] + letter + " "
            print(srow + self.colors[0])
        print("")

    def load(self,load_filename,gameid):
        try:
            with open(load_filename, 'r', encoding='utf-8') as f:
                gameline = f.readline().rstrip()
                gameentry = gameline.split(":")
                print(f'Starting to load game {gameid} from file {load_filename}')
                if gameentry[0] == str(gameid):
                    for pieceentry in gameentry[1].split(";"):
                        piecepos = pieceentry.split(",")
                        piece = piecepos[0]
                        X = int(piecepos[1]) - 1
                        Y = int(piecepos[2]) - 1
                        for n in range(len(piecepos)-3):
                            n += 3
                            if piecepos[n] == "rol":
                                self.pieces[piece].rol()
                            if piecepos[n] == "ror":
                                self.pieces[piece].ror()
                            if piecepos[n] == "flip":
                                self.pieces[piece].flip()
                        if not self.pieces[piece].place(self.field,X,Y):
                            raise(RuntimeError(f"Unable to place piece {piece} from gameid {gameid} from file {load_filename}"))
                        self.redraw()
                    print(f'Finished loading game {gameid} from file {load_filename}')
                    return
        except FileNotFoundError:
            print(f'Fata: Could not find [{load_filename}]')
            return
        except Exception as e:
            print(f'Fatal error [{e}]')
            return


def SyntaxError():
    print()

if __name__ == "__main__":
    
    k = Kanoodle()

    from sys import argv
    DollarZero = argv.pop(0)

    if "-layout" in argv:
        for piece in Piece.STRING:
            k.pieces[piece].place(0,0)
            k.redraw()
            k.pieces[piece].pickup()
    elif "-rotations" in argv:
        for P in Piece.STRING:
            for j in range(2):
                for i in range(4):
                    k.pieces[P].place(k.field,0,0)
                    k.redraw()
                    k.pieces[P].pickup(k.field)
                    k.pieces[P].ror()
                k.pieces[P].flip()
    else:
        k.load(argv.pop(0),argv.pop(0))
        try: Solver().solve(k)
        except KeyboardInterrupt: pass
