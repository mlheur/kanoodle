from sys import argv
from Kanoodle import Kanoodle
from Piece import EMPTY

DollarZero = argv.pop(0)
gamedata = argv.pop(0)
puzzle   = argv.pop(0)

k = Kanoodle(gamedata)
k.load(puzzle)


def findSpotFor(P,k,hand,depth=None):
    if depth is None:
        depth = 1
    else:
        depth = depth + 1
    #print(f'findSpotFor(P={P},hand={hand},k=\n{k}\n) depth={depth}')

    FirstPiece = P

    while True:
        k.pieces[P].reset()
        while k.pieces[P].next():
            #print(f'checking unique rotation P={P} i={k.pieces[P].current_unique}')
            localY = 0
            for row in k.field:
                localX = 0
                localY += 1
                for letter in row:
                    localX += 1
                    #print(f'checking cell X,Y {localX},{localY} P={P}')
                    if k.pieces[P].place(k.field,localX-1,localY-1):
                        k.redraw()
                        #input(f'hit enter\n') #, hand={hand}')
                        if hand == "":
                            #print(f'The last piece was placed, everything is done')
                            return True
                        else:
                            #print(f'Go deeper')
                            bFound = findSpotFor(hand[0],k,hand[1:],depth=None)
                            if bFound:
                                return True
                            k.pieces[P].pickup(k.field)
                            #k.redraw()
        #print(f'exhausted all rotations with P=[{P}]')
        if len(hand) == 0:
            #print(f'failed after going all the way deep, back out one level and try something else.')
            return False
        #print(f'put that at the back of the hand, try with next piece first.')
        hand = hand + P
        P = hand[0]
        hand = hand[1:]
        #print(f'findSpotFor(P={P},hand={hand},k=\n{k}\n) depth={depth}')
        if P == FirstPiece:
            #print(f'tried all rotations of hand')
            return False

                


def __nothing__():
    for row in k.field:
        localX = 0
        localY += 1
        for letter in row:
            localX += 1
            print(f'checking cell X,Y {localX},{localY}')
            if letter == EMPTY:
                print(f'found empty hole at X,Y {localX},{localY}')
                k.pieces[P].reset()
                while k.pieces[P].next():
                    print(f'checking unique rotation P={P} i={k.pieces[P].current_unique}')
                    dropX = localX + k.pieces[P].getLeftOffset() - 1
                    dropY = localY - 1
                    print(f'computed zDrop X,Y {dropX},{dropY}')
                    if k.pieces[P].place(k.field,dropX,dropY):
                        k.redraw()
                        input(f'hit enter, hand={hand}')
                        if len(hand) > 0:
                            Q = hand[0]
                            hand = hand[1:]
                            print(f'since P={P} is down, try to place Q={Q},hand={hand}')
                            if findSpotFor(Q,k,hand,depth):
                                return True
                            else:
                                pass
                            k.pieces[P].pickup(k.field)
                            hand += P
                        else:
                            if getHand(k) == "":
                                print(f'That was the last piece, the puzzle is all done.')
                                return True
                            else:
                                
                                continue
                    else:
                        print(f'failed to place P={P} at X,Y hole {localX},{localY}; trying next rotation')
                        continue
                print(f'really failed to place P={P} at X,Y hole {localX},{localY}; searching for next hole')
                continue
    print(f'really really failed to place the piece on the board in any hole, returning piece P={P} to the hand, try another piece first.')
    return False

def getHand(k):
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

hand = getHand(k)
success = False
for i in range(len(hand)):
    P = hand[0]
    hand = hand[1:]
    #print(f'outer iterations: calling findSpotFor(P={P},hand={hand},k=\n{k}\n)')
    if findSpotFor(P,k,hand):
        #k.redraw()
        success = True
        break
    hand += P

if success:
    print(f'success')
else:
    print(f'failed')