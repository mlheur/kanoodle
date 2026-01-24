

class Solver(object):

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
                            k.pieces[P].reset()
                            # Normalize the desired X,Y drop coordinate.
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
                                    k.redraw()
                                    #input("IT FITS!")
                                    if len(pieces_inhand) > 1:
                                        if not self.solve(k,k2):
                                            k.pieces[P].pickup(k.field)
                                        else:
                                            return True
                                    else:
                                        return True
                            print(f'Cannot fit piece {P}, backout one step\n')
                            return False


if __name__ == "__main__":
    from sys import argv
    DollarZero = argv.pop(0)

    from Kanoodle import Kanoodle

    gamedata = argv.pop(0)
    k = Kanoodle(gamedata)
    k2 = Kanoodle(gamedata)
    k.load(argv.pop(0))
    s = Solver()
    try: s.solve(k,k2)
    except KeyboardInterrupt: pass