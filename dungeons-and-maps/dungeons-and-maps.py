import sys
import math
import numpy as np

def path_length(map,start_row,start_col):
    row = start_row
    col = start_col

    visited = set()
    distance = 1
    while True: 
        if not(0<=row<map.shape[0] and 0<=col<map.shape[1]):
            return math.inf
        
        if (row,col) in visited:
            return math.inf

        dir = map[row][col]
        if dir == 'T':
            return distance
        if dir in ['.','#'] :
            return math.inf

        visited.add((row,col))
        if dir == '^':
            row -= 1
        elif dir == 'v':
            row += 1
        elif dir == '>':
            col += 1
        elif dir == '<':
            col -= 1
        distance += 1

TC = """19 19
0 9
6
#########v#########
##...............##
#........#........#
#....##..#..##....#
#....##..#..##....#
...####..#..####...
...####..#..####...
#........#........#
#.#............#..#
#.#..###.#.###.#..#
#.#............#..#
#.......###.......#
.......#####.......
..#...#######...#..
#..#...#####...#..#
##..#...###...#..##
###..#...#...#..###
####.....T.....####
###################
#########v#########
##.......>>v.....##
#........#.v......#
#....##..#.v##....#
#....##..#.v##....#
...####..#v<####...
...####..#>v####...
#........#.>>>>>>v#
#.#............#.v#
#.#..###.#.###.#.v#
#.#............#.v#
#.......###......v#
.......#####..v<<<.
..#...#######v<.#..
#..#...#####v<.#..#
##..#...###v<.#..##
###..#...#v<.#..###
####.....T<....####
###################
#########v#########
##......v>>>>>>>v##
#.......v#......>v#
#....##.v#..##...v#
#....##.v#..##...v#
...####.v#..####.>>
...####.v#..####...
#...v<<<v#........#
#.#.>^..v......#..#
#.#..###v#.###.#..#
#.#....v<......#..#
#.....v<###.......#
.....v<#####.......
..#..v#######...#..
#..#.>v#####...#..#
##..#.>v###...#..##
###..#.>v#...#..###
####....>T.....####
###################
#########v#########
##......v<>>>>>>v##
#.......v#......>v#
#....##.v#..##...v#
#....##.v#..##...v#
...####.v#..####.>>
...####.v#..####...
#...v<<<v#........#
#.#.>^..v......#..#
#.#..###v#.###.#..#
#.#....v<......#..#
#.....v<###.......#
.....v<#####.......
..#..v#######...#..
#..#.>v#####...#..#
##..#.>v###...#..##
###..#.>v#...#..###
####....>T.....####
###################
#########v#########
##.......>>>>>>>v##
#........#......>v#
#....##..#..##...v#
#....##..#..##...v#
...####..#..####.>v
...####..#..####.v<
#........#.......v#
#.#............#.v#
#.#..###v#.###.#.v#
#.#............#.v#
#.......###......v#
.......#####.....>v
..#...#######...#v<
#..#...#####...#v<#
##..#...###...#v<##
###..#...#...#v<###
####.....T<<<<<####
###################
#########v#########
##.......>>>>>>>v##
#........#......>v#
#....##..#..##...v#
#....##..#..##...v#
...####..#..####.>v
...####..#..####.v<
#........#.......v#
#.#............#.v#
#.#..###v#.###.#.v#
#.#....v<<<<...#.v#
#.....v<###^<....v#
.....v<#####^<...>v
..#..v#######^..#v<
#..#.>v#####>^.#v<#
##..#.>v###>^.#v<##
###..#.>v#>^.#v<###
####....>T^<<<<####
###################"""
input = iter(TC.splitlines())

w, h = [int(i) for i in next(input).split()]
start_row, start_col = [int(i) for i in next(input).split()]
n = int(next(input))
maps = [np.full((h,w),'.') for i in range(n)]
for i in range(n):
    for j in range(h):
        row_input = next(input)
        maps[i][j] = list(row_input)

distances = [math.inf]*n
for i in range(n):
    distances[i]  = path_length(maps[i],start_row,start_col)

min_distance = min(distances)
if min_distance == math.inf:
    print('TRAP')
else:
    print(distances.index(min_distance))
