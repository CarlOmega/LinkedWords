import time
import sys
import random
from collections import deque

# /////////////////////////////////////////////////////////////////////////////////////////////////
# Global Variables Start
# /////////////////////////////////////////////////////////////////////////////////////////////////
# Both ins/outs are used to compare what word should be next and what words should be start points.
ins = dict()  # Stores the number of words that can connect to a front pair  e"xa"mple.
outs = dict()  # Stores the number of words that can connect to a end pair  exam"pl"e.
# Two dictionarys with the same number of words just indexed by either front or end pair.
# The main reason of having two is so it is fast to look forward and backwards
words_start = dict()  # Allows fast lookup for words to go next in the sequence
words_end = dict()  # Allows fast lookup for words to go infront in the sequence
word_count = 0  # Keeps track of the number of words to escape when it can't beat a sequence length
# /////////////////////////////////////////////////////////////////////////////////////////////////
# Global Variables End
# /////////////////////////////////////////////////////////////////////////////////////////////////


# /////////////////////////////////////////////////////////////////////////////////////////////////
# add_word Function Start
# /////////////////////////////////////////////////////////////////////////////////////////////////
def add_word(word):
    """Adds the given word to both dictionarys and updates the ins/outs and word counts.

    Updates all 4 data structures (dictionarys) and increments the count
    uses a dictionary of buckets (dictionary of sets) to store the words and
    uses a dictionary of counts to keep track of the in and out connections.

    Args:
        word (string): A word to add to the data structures

    Examples:
        An Example showing for a board size N = 8 getting the cost.

        >>>
    """
    global word_count
    word_count += 1
    ins[word[-3:-1]] = ins[word[-3:-1]] + 1 if word[-3:-1] in ins else 1
    outs[word[1:3]] = outs[word[1:3]] + 1 if word[1:3] in outs else 1

    if word[1:3] in words_start:
        words_start[word[1:3]].add(word)
    else:
        words_start[word[1:3]] = set([word])

    if word[-3:-1] in words_end:
        words_end[word[-3:-1]].add(word)
    else:
        words_end[word[-3:-1]] = set([word])
# /////////////////////////////////////////////////////////////////////////////////////////////////
# add_word Function End
# /////////////////////////////////////////////////////////////////////////////////////////////////


# /////////////////////////////////////////////////////////////////////////////////////////////////
# pop_word Function Start
# /////////////////////////////////////////////////////////////////////////////////////////////////
def pop_word(word):
    global word_count
    word_count -= 1
    ins[word[-3:-1]] -= 1
    if ins[word[-3:-1]] == 0:
        del ins[word[-3:-1]]

    outs[word[1:3]] -= 1
    if outs[word[1:3]] == 0:
        del outs[word[1:3]]

    if word in words_start[word[1:3]]:
        words_start[word[1:3]].remove(word)
    if len(words_start[word[1:3]]) == 0:
        del words_start[word[1:3]]

    if word in words_end[word[-3:-1]]:
        words_end[word[-3:-1]].remove(word)
    if len(words_end[word[-3:-1]]) == 0:
        del words_end[word[-3:-1]]

    return word
# /////////////////////////////////////////////////////////////////////////////////////////////////
# pop_word Function End
# /////////////////////////////////////////////////////////////////////////////////////////////////

# /////////////////////////////////////////////////////////////////////////////////////////////////
# read_in_words Function Start
# /////////////////////////////////////////////////////////////////////////////////////////////////
def read_in_words(size):
    """Reads in words from dictionary.txt of the given length and adds them to the data structures.

    Opens the file dictionary.txt and reads every word only adding
    ones with size length to the data structures. Uses basic error
    handling incase the file isn't there aor there is another problem.

    Args:
        size (int): Length of the words to store.

    Returns:
        (bool): If there wasn't any errors when reading in.

    Examples:
        Reading in dictionary.txt with "example" in it.

        >>> read_in_words(7)
        >>>
        {'pl': 1} {'xa': 1} {'xa': {'example'}} {'pl': {'example'}} 1
    """
    try:
        with open("dictionary.txt", "r") as file:
            raw_words = file.read().splitlines()
            for word in raw_words:
                if len(word) == size:
                    add_word(word)
        file.close()
    except:
        print("Error: dictionary.txt File not found or Error reading.")
        return False
    return True
# /////////////////////////////////////////////////////////////////////////////////////////////////
# read_in_words Function End
# /////////////////////////////////////////////////////////////////////////////////////////////////

# /////////////////////////////////////////////////////////////////////////////////////////////////
# add_to_front Function Start
# /////////////////////////////////////////////////////////////////////////////////////////////////
def add_to_front(sequence):
    """Adds a valid word onto the front of the sequence.

    Take the first word of the sequence and see if it can add in front of it.
    If it can, check all the children (possible next words) and find the one
    with the most possible ways in (ins) and at least 1 way in. If it can't
    add an end cap (word with no where to go after). If no words were added
    return False otherwise return True.

    Returns:
        (bool): Returns Ture if it added anywords to the sequence.
    """
    first = sequence[0]  # Stores first word in variable for ease of use.
    flag = True  # Important to show if a word has children that have children. (Avoiding dead end)
    added = False  # For the return to show if a word was added at all.
    while first[1:3] in words_end and flag:
        flag = False  # If this doesn't change no children with children to add.
        best_child = ""
        max_ins = 0
        for sub in words_end[first[1:3]]:
            # Sets ins/outs to value in dictionary otherwise 0. (note outs was used in experiments)
            word_ins = ins[sub[1:3]] if sub[1:3] in ins else 0
            word_outs = outs[sub[-3:-1]] if sub[-3:-1] in outs else 0
            # Gets the word with the most ins (The Heuristic).
            if word_ins > max_ins:
                max_ins = ins[sub[1:3]]
                best_child = sub
                flag = True
        # If there was a child with a child add it to the sequence.
        if flag:
            sequence.appendleft(pop_word(best_child))
            print(sequence)
            added = True
        first = sequence[0]
    # Add the end cap. Child without any children.
    if first[1:3] in words_end:
        sequence.appendleft(pop_word(words_end[first[1:3]].pop()))
        added = True
    return added
# /////////////////////////////////////////////////////////////////////////////////////////////////
# add_to_front Function End
# /////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////////////
# get_starting_words Function Start
# /////////////////////////////////////////////////////////////////////////////////////////////////
def get_starting_words():
    """Goes through the data structures to get starting words with unique front pairs.

    Goes through all word pair and if a word has outs then takes it and
    moves to the next pair. So all starting words have unique starting points.

    Returns:
        (string)[]: List of chosen best staring words.

    Examples:
        Printing the amount of starting words for size of 4.

        >>> print(len(get_starting_words()))
        314
    """
    starting_words = []
    prefix = list(words_start.keys())  # All front pairs of words.
    for pre in prefix:
        for word in words_start[pre]:
            # Sets ins/outs to value in dictionary other 0.
            word_ins = ins[word[1:3]] if word[1:3] in ins else 0
            word_outs = outs[word[-3:-1]] if word[-3:-1] in outs else 0
            # Making sure there is more places into the word than out of the word.
            # This is due to the program first finds all words to put on the front.
            if word_outs <= word_ins:
                starting_words.append(word)
                break
    return starting_words
# /////////////////////////////////////////////////////////////////////////////////////////////////
# get_starting_words Function End
# /////////////////////////////////////////////////////////////////////////////////////////////////
read_in_words(5)
starting_words = get_starting_words()
print
add_to_front(starting_words[random.randint(0,len(starting_words))])
