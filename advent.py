# advent.py
#
# Score Advent Calendars by how pleasing they are (how far apart their
# numbers are) and generate pleasing calendars
#
# Copyright (c) 2018 John Graham-Cumming

import numpy as np
import time
import os

# The numbers that appear on the advent calendar (typically 1 to 24)

days = range(1,25)

# Real calendar from Paul in the UK

paul = np.matrix('14 7 10 11 4 17; 6 22 9 2 13 20; 15 8 16 19 24 21; 3 18 5 1 23 12')

# Real calendar from M&S in the UK

mands = np.matrix('1 7 5 9; 3 10 15 22; 18 16 6 20; 12 24 8 4; 14 21 2 17; 19 23 11 13')

# Boring calendars

boring1 = np.matrix('1 2 3 4 5 6; 7 8 9 10 11 12; 13 14 15 16 17 18; 19 20 21 22 23 24')
boring2 = np.matrix('1 2 3 4 5 6; 12 11 10 9 8 7; 13 14 15 16 17 18; 24 23 22 21 20 19')
boring3 = np.matrix('1 7 2 8 3 9; 4 10 5 11 6 12; 13 19 14 20 15 21; 16 22 17 23 18 24')

# Haribo calendar

haribo = np.matrix('2 15 1 13 20 18; 10 8 5 7 3 23; 4 22 14 19 6 11; 12 16 9 24 17 21')

# Found by searching 1,000,000 random calendars

million = np.matrix('9 4 18 10 15 20;16 21 12 1 22 7;2 6 24 5 17 13;14 8 19 11 23 3')

# coord finds the coordinates in cal of the number n and returns then
# as a tuple. ignore0 means that if it can't find the number searched
# for (because it may be 0 as it hasn't been added yet) then ignore
# that and return 0 (otherwise an error is raised)
def coord(cal, n, ignore0=False):
    (h, w) = cal.shape
    for y in range(h):
        for x in range(w):
            if cal[y,x] == n:
                return (x,y)

    if ignore0:
        return 0

    print("coord called with unexpected number: ", n)
    raise

# distance calculates the distance metric from the number n to every
# other number on the calendar. The distance is defined as the
# weighted sum of the inverted Euclidean distance in the cal calendar
# rectangle.  The weights are 1/(abs(n-p)) for each p in
# [1..24/n]. The idea is that numbers that are close to each other
# should be far apart and the goal will be to minimize the results of
# this function across all numbers.
def distance(cal, n, ignore0=False):
    (h, w) = cal.shape

    # The farthest apart two numbers can be in the advent calendar

    farthest = np.sqrt((w-1)*(w-1) + (h-1)*(h-1))

    npos = coord(cal, n, ignore0)
    if npos == 0:
        return 0

    d = 0
    for p in (x for x in days if x != n):
        ppos = coord(cal, p, ignore0)
        if ppos != 0:
            d0 = npos[0]-ppos[0]
            d1 = npos[1]-ppos[1]
            d += (farthest - np.sqrt(d0*d0 + d1*d1))/np.abs(n-p)
    return d

# score calculates the score for a single instance of an advent
# calendar
def score(cal, ignore0=False):
    score = 0
    for p in days:
        score += distance(cal, p, ignore0)
    return score

# animate outputs an advent calendar being opened by deleting each
# number from 1 to 24 and then outputting the matrix
def animate(cal):
    (h, w) = cal.shape

    for p in days:
        os.system('clear')
        for y in range(h):
            for x in range(w):
                if cal[y,x] == p:
                    cal[y,x] = 0
                if cal[y,x] == 0:
                    print '  ',
                else:
                    print '%2d' % cal[y,x],
            print
        time.sleep(1)

# randcal returns a random 6x4 calendar
def randcal():
    return np.random.choice(days, len(days), replace=False).reshape((4,6))

# generate creates a random calendar by putting 1 somewhere on the
# calendar (positing is controlled by the parameter n in range 0 to
# 23) and then finding the best place to put each number after that to
# minmize the distance metric
def generate(n):
    zerone = np.zeros(24, np.int8)
    zerone[n] = 1
    advent = zerone.reshape((4,6))

    # Now try adding each number to the advent calendar 

    for p in days[1:]:
        lowscore = 65536
        for i in range(24):
            if advent[i/6,i%6] == 0:
                attempt = np.copy(advent)
                attempt[i/6,i%6] = p
                ascore = score(attempt, True)
                if ascore < lowscore:
                    possible = np.copy(attempt)
                    lowscore = ascore
        advent = np.copy(possible)

    return (advent, score(advent))

# swap creates a random calendar and then starts swapping pairs
# of numbers to see if a better calendar can be found in n
# iterations
def swap(n):
    advent = randcal()
    lowscore = score(advent)

    for _ in range(n):
        i = np.random.randint(0,24)
        j = np.random.randint(0,24)
        advent[i/6,i%6], advent[j/6,j%6] = advent[j/6,j%6], advent[i/6,i%6]
        ascore = score(advent)
        if ascore < lowscore:
            lowscore = ascore
        else:
            advent[i/6,i%6], advent[j/6,j%6] = advent[j/6,j%6], advent[i/6,i%6]

    return (advent, lowscore)

# search generates random calendars and finds the one with the best
# score and returns it and its score by trying up to n times
def search(n):
    bestcal = randcal()
    bestscore = score(bestcal)
    
    for _ in range(n-1):
        acal = randcal()
        ascore = score(acal)
        if ascore < bestscore:
            bestscore = ascore
            bestcal = acal

    return (bestcal, bestscore)

#for cal in [paul, mands, boring1, boring2, boring3, million, haribo]:
#    print(cal)
#    print(score(cal))

(acal, ascore) = swap(1000)
print(acal)
print(ascore)
