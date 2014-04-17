# Given a sorted array with duplicates and a number, find the range in the
# form of (startIndex, endIndex) of that number. For example,

# find_range({0 2 3 3 3 10 10}, 3) should return (2,4).
# find_range({0 2 3 3 3 10 10}, 6) should return (-1,-1).
# The array and the number of duplicates can be large.

s_r = [0,0,1,1,1,2,3,4,5]

# identify the most important abstractions
# This iterate along and do stuff sort of a problem
# Problems requires a series of decisions at every element
# Identify the key set of decisions and the order in which they need to be made

# key decision
# 1. Check if the given number matches array element
# 2.    If so, check if a match has alredy happened

# The goal of these problems are -
# minimize the number of checks
# reuse existing variables as much as possible


start_index = end_index = -1

num = 2

for index, value in enumerate(s_r):
    if num == value:
        if start_index < 0:
            start_index = end_index = index
        else:
            end_index = index

print start_index, end_index

