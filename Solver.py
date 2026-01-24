

class Solver(object):

    def recount_hand(self):
        # First determine which game pieces are
        # off the board, in the player's hand.
        self.pieces_onboard = dict()
        self.pieces_inhand = dict()
        for row in k.field:
            for letter in row:
                if letter in k.PIECE_STRING:
                    self.pieces_onboard[letter] = True

        for P in k.PIECE_STRING:
            if not P in self.pieces_onboard:
                self.pieces_inhand[P] = True



    def solve(self,k,k2):
        print(f"++solve(k=[\n{k}\n])")
        
        from Piece import EMPTY
        
        self.recount_hand()
        print(f'Solver: self.pieces_onboard=[{self.pieces_onboard}]')

        while True in self.pieces_inhand.values():
            # print(f'Solver: self.pieces_inhand=[{self.pieces_inhand}]')
            for P in self.pieces_inhand:
                k.pieces[P].reset()

                # The top-left-most pip of any piece may be somewhere other than
                # 1,1.  Therefore, when we place that piece on the board we might
                # have to offset the field location where the piece will be place()d.

                # Said another way, finding a free hole in the field does not
                # necessarily mean that's the coordinate-point where we want
                # to place the piece.

                # Using piece "L" as example, assuming we want to place
                # below and right of piece 'K', when we try to place "L",
                # the field coordinate to the place() call is actually occupied
                # by piece "K"...

                # Now that theory's out of the way, do the logic.


                # Find the top-left-most free slot in the field.
                localX = 0
                localY = 0
                for row in k.field:
                    localY += 1 
                    for letter in row:
                        localX += 1
                        if letter == EMPTY:
                            # Normalize the desired X,Y drop coordinate.
                            print(f'found empty hole at {localX},{localY}')
                            while k.pieces[P].next():
                                print(f'Trying piece {P} in unique orientation {k.pieces[P].current_unique}')
                                k.pieces[P].place(k2.field,0,0)
                                k2.redraw()
                                k.pieces[P].pickup(k2.field)
                                dropX = localX + k.pieces[P].getLeftOffset()
                                dropY = localY # There's always a piece in the top row.
                                print(f'have offset empty hole at {dropX-1},{dropY-1}')
                                k.pieces[P].place(k2.field,dropX-1,dropY-1)
                                k2.redraw()
                                k.pieces[P].pickup(k2.field)
                                input("press enter")
                                if k.pieces[P].place(k.field,dropX-1,dropY-1):
                                    input("IT FITS!")
                                    self.recount_hand()
                                    break



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