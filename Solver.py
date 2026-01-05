

class Solver(object):
    def solve(self,k):
        print("++solve")
        # Zeroeth: determine what are all the pieces of the game
        from Kanoodle import PIECE_STRING, EMPTY
        
        # First determine which game pieces are
        # off the board, in the player's hand.
        pieces_onboard = dict()
        pieces_inhand = dict()
        for row in k.field:
            for letter in row:
                if letter in PIECE_STRING:
                    pieces_onboard[letter] = True

        for P in PIECE_STRING:
            if not P in pieces_onboard:
                pieces_inhand[P] = True

        print(f'Solver: pieces_onboard=[{pieces_onboard}]')

        while True in pieces_inhand.values():
            # print(f'Solver: pieces_inhand=[{pieces_inhand}]')
            for piece in pieces_inhand:
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
                            offXY = k.pieces[piece].getLeftOffset()
                            dropX = localX + offXY[0]
                            dropY = localY # There's always a piece in the top row.