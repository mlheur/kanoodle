

class FirstSolver(object):

    def __init__(self):
        self.depth = 0

    def solve(self,k,k2):
        #print(f"++solve(k=[\n{k}\n])")
        
        from Piece import EMPTY
        
        # First determine which game pieces are
        # off the board, in the player's hand.
        pieces_onboard = dict()
        pieces_inhand = dict()
        for row in k.field:
            for letter in row:
                if letter in k.PIECE_STRING:
                    pieces_onboard[letter] = True

        for P in k.PIECE_STRING:
            if not P in pieces_onboard:
                pieces_inhand[P] = True

        # print(f'Solver: pieces_onboard=[{pieces_onboard}]')

        while True in pieces_inhand.values():
            # print(f'Solver: pieces_inhand=[{pieces_inhand}]')

            # Find the top-left-most free slot in the field.
            localY = 0
            for row in k.field:
                localX = 0
                localY += 1 
                for letter in row:
                    localX += 1
                    if letter == EMPTY:
                        print(f'found empty hole at {localX},{localY}')
                        for P in pieces_inhand:
                            # Normalize the desired X,Y drop coordinate.
                            k.pieces[P].reset()
                            while k.pieces[P].next():
                                print(f'Trying piece {P} in unique orientation {k.pieces[P].current_unique}')
                                #k.pieces[P].place(k2.field,0,0)
                                #k2.redraw()
                                #k.pieces[P].pickup(k2.field)
                                dropX = localX + k.pieces[P].getLeftOffset()
                                dropY = localY # There's always a piece in the top row.
                                #print(f'have offset at {dropX-1},{dropY-1}')
                                #if k.pieces[P].place(k2.field,dropX-1,dropY-1):
                                #    k2.redraw()
                                #    k.pieces[P].pickup(k2.field)
                                #input("press enter")
                                if k.pieces[P].place(k.field,dropX-1,dropY-1):
                                    print(f'depth={self.depth}')
                                    k.redraw()
                                    #input("IT FITS!")
                                    if len(pieces_inhand) > 1:
                                        self.depth += 1
                                        if not self.solve(k,k2):
                                            self.depth -= 1
                                            k.pieces[P].pickup(k.field)
                                        else:
                                            self.depth -= 1
                                            return True
                                    else:
                                        return True
                            print(f'Cannot fit piece {P} in this spot, backout one step for a previous piece\n')
                            return False
                        print(f'Cannot fit piece {P} in this spot, move to another spot\n')
                        return False


class Solver(object):
    def __init__(self,gamedata,puzzle):
        self.playboard = Kanoodle(gamedata)
        self.playboard.load(puzzle)
        self.showboard = Kanoodle(gamedata)
    
    def getHandPieces(self):
        hand = ""
        board = ""
        for row in k.field:
            for letter in row:
                if letter in k.PIECE_STRING and not letter in board:
                    board += letter
        for letter in k.PIECE_STRING:
            if not letter in board:
                hand += letter
        return hand

    def solve(self):
        hand = self.getHandPieces()
        while hand != "":
            P = hand[0]
            hand = hand[1:]
            if self.findSpotFor(P):
                continue
            hand += P



if __name__ == "__main__":
    from sys import argv
    DollarZero = argv.pop(0)

    from Kanoodle import Kanoodle

    gamedata = argv.pop(0)
    puzzle   = argv.pop(0)
    try: Solver(gamedata,puzzle).solve()
    except KeyboardInterrupt: pass