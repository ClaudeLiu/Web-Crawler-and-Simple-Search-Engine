from PartA_wordFrequencies import frequency
import time
import sys

def intersection_count():
    '''
    This function reads the content of two text files and outputs the number
    of tokens they have in common.
    For time complexity, I used two pairs of files with the size of one pair is much great
    than another pair's. And I found that the runtime just increased a little bit compared to
    the difference of size. So, I conclude that the time complexity is O(log n).
    '''
    try:    # Using try except to handle bad input.
        start = time.time()
        container1 = frequency(sys.argv[1]).keys()
        container2 = frequency(sys.argv[2]).keys()
        temp = container1 & container2  # Using intersection of two sets to extract common tokens.
        end = time.time()
        print("The program took", end - start, "seconds to excute.")
    except:
        print("Invalid file(s)! Please re-enter.")
        return
    print("Number of words in common:", len(temp))    # Printing the number of tokens they have in common to screen.
    return


if __name__ == "__main__":
    intersection_count()
