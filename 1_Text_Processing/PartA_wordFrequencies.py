import re
from collections import defaultdict
import time
import sys


def frequency(file_path):
    '''
    This function takes the file path as parameter, and returns a dictionary which has
    word as the keys and their frequency as the values associated with each key.
    '''
    container = defaultdict(int)    # Using dictionary to store word and frequency, which is very efficient.
    file  = open(file_path, "r")
    for line in file:
        temp = re.split('[^a-zA-Z0-9]+', line)  # Using regular expression to remove all the non-alphanumeric token
        if len(temp) != 0:
            for i in temp:
                if i != '':
                    container[i.lower()] += 1   # Converting word to lower case and count their frequency in dictionary
    file.close()
    return container


def main():
    '''
    This is the main function to run partA. This function takes no parameter and will
    print words with their frequency to the screen by decreasing frequency and by
    alphabet if there is tie of frequency
    For time complexity, I ran two files with different sizes and compare their runtime.
    I found the file whose size is twice as another file took twice as long, so the time complexity is O(n).
    '''
    try:    # Using try except to handle bad input.
        start = time.time()
        result = frequency(sys.argv[1]) # Using sys to get input file as command line argument
        end = time.time()
        print("Here is word frequencies:")
        for k, v in sorted(result.items(), key=lambda x: (-x[1], x[0])):  # Sorting the word first according to frequency, then by alphabet.
            print("{} - {}".format(k, v))
        print("The program took", end - start, "seconds to excute.")
    except:
        print("Invalid file! Please re-enter.")


if __name__ == "__main__":
    main()