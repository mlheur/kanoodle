#!/usr/bin/env python3

from sys import argv
from Kanoodle import Kanoodle
from Piece import EMPTY
from random import shuffle
from subprocess import run as shell

DollarZero = argv.pop(0)
gamedata = argv.pop(0)
puzzle   = argv.pop(0)


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
                        if k.hasSmallHoles():
                            k.pieces[P].pickup(k.field)
                        else:
                            #k.redraw()
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

def getHand(k,):
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


def try_hand(starterid):
    k = Kanoodle(gamedata)
    k.PIECE_STRING = starters[starterid]
    k.starterid = starterid
    k.load(puzzle)
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
        print(f'{starterid} success')
        k.redraw()
        # kill pool peers
    else:
        print(f'{starterid} failed')
        # die

def worker_found_solution(pool):
    for i in pool:
        pool[i].join(0.0)
        if not pool[i].is_alive():
            return True
    return False

k = Kanoodle(gamedata)
k.load(puzzle)
k.redraw(f"Loaded puzzle {puzzle}")

from multiprocessing import Process
from time import sleep
starters = dict()
pool = dict()
bKillAll = False
for i in range(48):
    start = list(Kanoodle.PIECE_STRING)
    shuffle(start)
    starters[i] = start
    print(f"creating solver [{i}] with seed [{start}]")
    pool[i] = Process(target=try_hand, args=(i,))
    pool[i].start()
    sleep(0.2)
    bKillAll = worker_found_solution(pool)
    if bKillAll:
        break

while not bKillAll:
    bKillAll = worker_found_solution(pool)

for i in pool:
    pool[i].terminate()
    pool[i].kill()

shell(["ksh","/home/marc/devel/kanoodle/do_kill.sh"])