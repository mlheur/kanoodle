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

## Design Choice:
# The math used to rotate pieces want a 0,0 coordinate system;
# Humans want a 1,1 coordinate system.
# Either:
# - Force one choice over the other.
#  - 1-based means having to inc/dec before AND after EVERY operation.
#  - 0-based means debugging, dat files and other programmer interactions have to
#    use a non-intuitive base.
# - Compromise:
#  - 1-based DAT files, decrement on load
#  - 0-based internally
#  - remember to increment on output


from Piece import Piece
from Solver import Solver


class Kanoodle(object):
    PIECE_STRING = "ABCDEFGHIJKL"

    def __init__(self, dat_filename):
        self.colors = dict()
        from Piece import EMPTY
        self.colors[EMPTY] = '\x1B[38;5;234m'
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

        self.pieces = dict()
        self.loads  = dict()
        try:
            with open(dat_filename, 'r', encoding='utf-8') as f:
                dimensions = f.readline().rstrip().split(",")
                self.width = int(dimensions[0])
                self.height = int(dimensions[1])

                nextline = f.readline().rstrip()
                while nextline:
                    parts = nextline.split(":")
                    if parts[0] in self.PIECE_STRING:
                        gp = Piece(parts)
                        self.pieces[gp.name] = gp
                    elif type(int(parts[0])) == type(int(0)):
                        self.loads[parts[0]] = parts[1]
                    else:
                        raise(RuntimeError(f'unexpected game data: nextline={nextline}'))
                    nextline = f.readline().rstrip()
        except FileNotFoundError:
            print(f'Fatal: Could not find [{dat_filename}]')
            return
        except Exception as e:
            print(f'Fatal error [{e}]')
            return
        
        self.field = list()
        for Y in range(self.height):
            self.field.append(list(EMPTY*self.width))
        
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

    def load(self,gameid):
        for pieceentry in self.loads[gameid].split(";"):
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
                raise(RuntimeError(f"Unable to place piece {piece} from gameid {gameid}"))
            self.redraw()
        print(f'Finished loading game {gameid}')

if __name__ == "__main__":
    from sys import argv

    DollarZero = argv.pop(0)
    k = Kanoodle(argv.pop(0))
    print(f'DollarZero={DollarZero}')
    k.redraw()

    if "-layout" in argv:
        for piece in PIECE_STRING:
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
        k.load(argv.pop(0))
        try: Solver().solve(k)
        except KeyboardInterrupt: pass
