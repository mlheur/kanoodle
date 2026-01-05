

class Solver(object):
    def solve(self,k):
        # Zeroeth: determine what are all the pieces of the game
        from Kanoodle import PIECE_STRING
        
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

        # print(f'Solver: pieces_onboard=[{pieces_onboard}] pieces_inhand=[{pieces_inhand}]')

        for piece in pieces_inhand:
            # The top-left-most pip may be somewhere other than 1,1
            # Therefore, when we place that piece on the board we might
            # have to offset the field location where the piece will be place()d.

            # Said another way, finding a free hole in the field does not
            # necessarily mean that's the coordinate point where we want
            # to place the piece.

            # Using piece "L" as example, assuming we want to place
            # below and left of piece 'K', when we try to place "L",
            # the field coordinate to place on is actually occupied
            # by piece "K"...

            # Find the top-left-most free slot in the field.
