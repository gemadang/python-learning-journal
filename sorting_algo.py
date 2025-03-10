'''
Objective:
- pick a sorting algorithm
- implement it in Python
- analyze its performance by measuring the time taken to sort arrays of various sizes under worst-case conditions

Instructions:
Pick a Sorting Algorithm: Choose one of the following sorting algorithms to implement:

Merge Sort
Quick Sort
Implement the Algorithm: Write a Python function that implements the sorting algorithm you have chosen. The function should take an array as input and return the sorted array.

Test for Worst-Case Performance:

Generate arrays of various sizes.
Modify these arrays to create worst-case conditions for your chosen algorithm.
If you are implementing Quick Sort, construct an array where all elements are the same or an array where the pivot selection consistently results in unbalanced partitions (e.g., sorted or reverse-sorted arrays).
Measure the Time Complexity:

Use Python's time module to measure the time it takes for your algorithm to sort arrays of increasing size under the worst-case condition.
Report Your Findings:

Include the code for your sorting algorithm in your report.
Create a graph of the array sizes and the time it took to sort each array in the worst case.
'''


def quicksort_helper(arr, low, high):
    pivot_val = arr[high]
    i = low
    while i <= high:
        val = arr[i]
        if val <= pivot_val: # if high <= pivot
            if high == i:
                arr[low], arr[i] = arr[i], arr[low]
            if val < arr[low]:
                arr[low], arr[i] = arr[i], arr[low]
            low += 1

        # if val > pivot, we continue on high pointer will increase with low pointer
        i += 1

    return low - 1 #return where pivot came in

def quicksort(unsorted, low, high):
    if low < high:
        pivot = quicksort_helper(unsorted, low, high)
        quicksort(unsorted, low, pivot-1)
        quicksort(unsorted, pivot+1, high)

unsorted = [3,2,0,1]
unsorted = [8,7,6,9,5]
unsorted = [3,2]

unsorted = [3,2,5,0,1,8,7,6,9,4]
quicksort(unsorted,0,len(unsorted)-1)
print(unsorted)