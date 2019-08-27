# Merge sort algorithm, written by Jasper Law
# See line 70 for algorithm input

import random

def MergeLists(list1, list2):
    merged = []
    while len(list1) > 0 and len(list2) > 0:
        merged.append(min(list1[0], list2[0]))
        if list1[0] == min(list1[0], list2[0]):
            list1.pop(0)
        else:
            list2.pop(0)
    if len(list1) > len(list2):
        for i in list1:
            merged.append(i)
    elif len(list2) > len(list1):
        for i in list2:
            merged.append(i)
    return merged


def SplitList(inList):
    if len(inList) == 1:
        return inList
    if len(inList) % 2 == 1:
        mid = int((len(inList) + 1) / 2)
    else:
        mid = int(len(inList) / 2)
    return [inList[0:mid], inList[mid:len(inList)]]


def MergeSort(inList):
    midList = []
    if len(inList) <= 1:
        return inList
    else:
        for i in inList:
            midList.append([i])

        if len(midList) % 2 == 1:
            midList.append([min(midList[-2][0], midList[-1][0]), max(midList[-2][0], midList[-1][0])])
            midList.pop(-3)
            midList.pop(-2)

        count = 1
        while len(midList) > 1:
            print("Level",str(count) + ":", midList)
            outList = []
            if len(midList) % 2 == 1:
                times = (len(midList) - 1)/2
            else:
                times = len(midList)/2
            for i in range(int(times)):
                outList.append(MergeLists(midList[2*i], midList[2*i+1]))
            if len(midList) % 2 == 1:
                outList.append(midList[-1])
            midList = outList
            count += 1

        return midList[0]

def RandomList(sizeRange,numRange):
    outList = []
    listSize = random.randint(sizeRange[0], sizeRange[1])
    for i in range(listSize):
        outList.append(random.randint(numRange[0],numRange[1]))
    return outList

# This algorithm should theoretically work with any list size, containing any range of integer values, as long
# as your system memory is big enough.
# Here are a few input lists to try out. Simply uncomment one of them, and comment out line 80.
#inList = [1, 5, 7, 3, 4, 7, 1, 8, 3]
#inList = [4, 8, 3, 1, 6, 5, 7, 2, 9]
#inList = [55,2,74,1,15,37,7,45,9,65,456]

# The program can also generate a random list as input. The first argument is the size of the list, to be a
# random number between the first number in the list and the second. The second argument is range of possible
# values to fill the list with.
inList = RandomList([0,20],[0,200])

print("Input:",inList,'\n')
print("\nOutput:",MergeSort(inList))
