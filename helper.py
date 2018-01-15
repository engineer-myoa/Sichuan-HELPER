# -*- coding: utf-8 -*-

from collections import deque, Counter
import Queue
import pprint
import numpy
import time

#pair = ((VERTEX-1)**2/2)
#print(pair)
#for i in xrange(10):
#    print(numpy.random.randint(1, pair+1)) # 1~pair까지



# ex) 5x5

#map = [ [0 for i in xrange(VERTEX+1) ] for i in xrange(VERTEX+1) ]
# +1은 path를 위한 상하좌우 여유 공백

# 추후 numpy로 배열을 수정하자. 속도를 위해서


startTime = time.time()

map = [[00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
       [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
       [00, 00, 00, 01, 02, 03, 04, 05, 06, 00, 00, 00],
       [00, 00, 07,  8, 00, 99, 99, 00,  9, 10, 00, 00],
       [00, 11, 12, 13, 14, 15, 16, 24, 13, 07, 11, 00],
       [00, 15, 16, 00, 17, 18, 19, 16, 00, 17, 12, 00],
       [00,  8, 20, 21, 22, 03, 23, 20, 21, 22, 25, 00],
       [00, 00, 14, 26, 25, 00, 00, 16, 26, 18, 00, 00],
       [00, 00, 00, 99, 10, 00, 00, 05, 99, 00, 00, 00],
       [00, 00, 00, 00,  9, 00, 00, 06, 00, 00, 00, 00],
       [00, 00, 00, 00, 00, 04, 02, 00, 00, 00, 00, 00],
       [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
       [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00]]
# ?? 는 추후에 클릭을해서 뒤집어주면 그값을 저장한다

# 카운터를 통해 각 숫자가 몇개씩 들어있는지, 그를 통해서 1개인곳을 정리

VERTEX = len(map)
NONE = -1
CHECK  = 1

#pprint.pprint(map)

map_anal = Counter()
for i in map:
    map_anal.update(i)
    map_anal

# 체크용
#for i in map_anal.iteritems():
#    print(i)

# 잘 나오넹
# print(map_anal)

for iKey in map:
    for jKey in iKey:
        if(jKey == 0): continue
        #print(jKey)


UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

def direction(intVal, i,j):
    if intVal == UP: return (i-1, j)
    if intVal == DOWN: return (i+1, j)
    if intVal == LEFT: return (i, j-1)
    if intVal == RIGHT: return (i, j+1)

def isStraight(prev, next):
    return abs(prev[0] - next[0]) >= 2 or abs(prev[1] - next[1]) >= 2

test = [[0,0,0,0,0,0],[0,1,2,3,4,0],[0,8,7,6,5,0],[0,4,3,2,1,0],[0,8,7,6,5,0],[0,0,0,0,0,0]]

def getPath(keyValue, i, j):

    VERTEX = len(map)

    open = Queue.Queue()
    openDirection = Queue.Queue()  # 방향성을 위해서 새로운 큐를 추가
    prevPos = Queue.Queue()  # 오버헤드방지. 되돌아가지않게 전진성.

    close = Queue.Queue()

    #put 은 한번에 하나밖에못넣음
    # i , j , 꺾인횟수.
    # 근데 이렇게 하면 꺾인횟수때문에 in연산자를 사용할 수 가 없음..

    # i, j 랑 꺾인횟수를 보관하는 queue를 따로 만든다.

    open.put(direction(UP, i,j))
    open.put(direction(DOWN, i, j))
    open.put(direction(LEFT, i, j))
    open.put(direction(RIGHT, i, j))

    openDirection.put(0)
    openDirection.put(0)
    openDirection.put(0)
    openDirection.put(0)

    prevPos.put((i, j))
    prevPos.put((i, j))
    prevPos.put((i, j))
    prevPos.put((i, j))

    while(not open.empty()):
        """
        print("-------------------------------")
        print("searching... " + str(open.queue))
        print("blocked ... " + str(close.queue))
        print("preved..." + str(prevPos.queue))
        """
        t = open.get()
        tD = openDirection.get()
        prev = prevPos.get()
        #print("curr: " + str(t) + ".. 꺾:" + str(tD) + " ..  이전:" + str(prev))


        if t[0] == i and t[1] == j:
            #print("자기 자신")
            close.put((t[0], t[1]))
            continue
        if t in close.queue:
            #print("낭비")
            continue

        if map[t[0]][t[1]] != 0: # -1도 포함 벽과 돌오브젝트
            if map[t[0]][t[1]] == keyValue:
                #print("찾음")
                return t

            # 그쪽 방향에 바리케이트가 있는거랑 같음.
            # open큐에 삽입은 없고, close에 put한다.

            #"""
            #print("바리케이트" + str(t))
            #"""
            close.put((t[0], t[1]))
            continue

        # 0이면. 길이면.. 다음 경로를 추가한다.
        # 가던방향이면 꺾임정보는 그대로, 방향이 꺾이면

        if t[1]-1 >= 0 and not (t[0] == prev[0] and t[1] -1 == prev[1]):
            next = direction(LEFT, t[0], t[1])

            if next not in close.queue:
                # 이전에 찾았던 바리케이트가 다음경로가 아니라면

                if isStraight(prev, next):
                    openDirection.put(tD)
                    open.put(next)  # 좌
                    prevPos.put((t[0], t[1]))
                else:
                    if (tD + 1 <= 2):
                        openDirection.put(tD + 1)
                        open.put(next)  # 좌
                        prevPos.put((t[0], t[1]))


        if t[1]+1 < VERTEX-1 and not (t[0] == prev[0] and t[1] +1 == prev[1]):
            next = direction(RIGHT, t[0], t[1])

            if next not in close.queue:

                if isStraight(prev, next):
                    openDirection.put(tD)
                    open.put(next)  # 우
                    prevPos.put((t[0], t[1]))
                else:
                    if (tD + 1 <= 2):
                        openDirection.put(tD + 1)
                        open.put(next)  # 우
                        prevPos.put((t[0], t[1]))



        if t[0]-1 >= 0  and not (t[0] - 1 == prev[0] and t[1] == prev[1]):
            next = direction(UP, t[0], t[1])

            if next not in close.queue:

                if isStraight(prev, next):
                    openDirection.put(tD)
                    open.put(next)  # 상
                    prevPos.put((t[0], t[1]))
                else:
                    if( tD + 1 <= 2):
                        openDirection.put(tD + 1)
                        open.put(next)  # 상
                        prevPos.put((t[0], t[1]))


        if t[0]+1 < VERTEX-1 and not (t[0] + 1 == prev[0] and t[1] == prev[1]):
            next = direction(DOWN, t[0], t[1])

            if next not in close.queue:


                if isStraight(prev, next):
                    openDirection.put(tD)
                    open.put(next)  # 하
                    prevPos.put((t[0], t[1]))
                else:
                    if (tD + 1 <= 2):
                        openDirection.put(tD + 1)
                        open.put(next)  # 하
                        prevPos.put((t[0], t[1]))

    return False

# 무조건 openDirection.put(tD+1을 하는건 문제가잇음..)



# 키에 대한 탐색 >>
alreadyFind = []

for i, iKey in enumerate(map):
    for j, jKey in enumerate(iKey):
    # 키에 대한 탐색 <<

        if jKey == 0 or jKey == 99 or jKey == -1: continue
        if ((i,j) in alreadyFind):
            continue

        """
        print("====================================")
        print(i,j)
        """

        result = getPath(jKey, i, j)
        if result:
            #alreadyFind.append(result)
            print("RESULT " + str((i,j)) + ", "+ str(result))

#print(alreadyFind)
print(str(time.time() - startTime) + "s")