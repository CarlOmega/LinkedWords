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
# Two dictionaries with the same number of words just indexed by either front or end pair.
# The main reason of having two is so it is fast to look forward and backwards
words_start = dict()  # Allows fast lookup for words to go next in the sequence
words_end = dict()  # Allows fast lookup for words to go in front in the sequence
word_count = 0  # Keeps track of the number of words to escape when it can't beat a sequence length
# /////////////////////////////////////////////////////////////////////////////////////////////////
# Global Variables End
# /////////////////////////////////////////////////////////////////////////////////////////////////

# /////////////////////////////////////////////////////////////////////////////////////////////////
# add_word Function Start
# /////////////////////////////////////////////////////////////////////////////////////////////////
def add_word(word):
    """Adds the given word to both dictionaries and updates the ins/outs and word counts.

    Updates all 4 data structures (dictionaries) and increments the word count
    uses dictionaries of buckets (dictionary of sets) to store the words and
    uses dictionaries of counts to keep track of the in and out connections.

    Args:
        word (string): A word to add to the data structures.

    Examples:
        An Example adding the word "example" to the data structures.

        >>> add_word("example")
        >>> print(ins, outs, words_start, words_end, word_count)
        {'pl': 1} {'xa': 1} {'xa': {'example'}} {'pl': {'example'}} 1
    """
    global word_count  # Make sure it edits the correct count in the global scope.
    word_count += 1

    # Increments if there is already a number otherwise sets to 1.
    ins[word[-3:-1]] = ins[word[-3:-1]] + 1 if word[-3:-1] in ins else 1
    outs[word[1:3]] = outs[word[1:3]] + 1 if word[1:3] in outs else 1

    # Adds the word to the set if it is there otherwise creates one.
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
    """Removes the given word from the dictionaries updates the ins/outs and word counts.

    Updates all 4 data structures (dictionaries) and decrements the word count
    uses dictionaries of buckets (dictionary of sets) to store the words and
    uses dictionaries of counts to keep track of the in and out connections.

    Args:
        word (string): A word to remove from the data structures.

    Returns:
        (string): The given word after the data structures have been updated.

    Examples:
        An Example popping "example" from the data structures assuming it is already added.

        >>> add_word("example")
        >>> print(ins, outs, words_start, words_end, word_count)
        {'pl': 1} {'xa': 1} {'xa': {'example'}} {'pl': {'example'}} 1
        >>> print(pop_word("example"))
        example
        >>> print(ins, outs, words_start, words_end, word_count)
        {} {} {} {} 0
    """
    global word_count  # Make sure it edits the correct count in the global scope.
    word_count -= 1

    # Decrements the ins/outs counts and deletes it if there is none there
    ins[word[-3:-1]] -= 1
    if ins[word[-3:-1]] == 0:
        del ins[word[-3:-1]]
    outs[word[1:3]] -= 1
    if outs[word[1:3]] == 0:
        del outs[word[1:3]]

    # Removes the word from the set. Then id there is no more words it deletes the set. (Start&End)
    if word in words_start[word[1:3]]:
        words_start[word[1:3]].remove(word)
    if len(words_start[word[1:3]]) == 0:
        del words_start[word[1:3]]
    if word in words_end[word[-3:-1]]:
        words_end[word[-3:-1]].remove(word)
    if len(words_end[word[-3:-1]]) == 0:
        del words_end[word[-3:-1]]

    # Returns the word for use inside of the code without using extra Variables.
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
        >>> print(ins, outs, words_start, words_end, word_count)
        {'pl': 1} {'xa': 1} {'xa': {'example'}} {'pl': {'example'}} 1
    """
    try:
        with open("dictionary.txt", "r") as file:
            raw_words = file.read().splitlines()
            for word in raw_words:
                if len(word) == size:
                    add_word(word)  # Adds the word to the data structures with add_word function.
        file.close()
    except:
        return False
    return True
# /////////////////////////////////////////////////////////////////////////////////////////////////
# read_in_words Function End
# /////////////////////////////////////////////////////////////////////////////////////////////////


# /////////////////////////////////////////////////////////////////////////////////////////////////
# save_results Function Start
# /////////////////////////////////////////////////////////////////////////////////////////////////
def save_results(sequence, time_found, time_finished, start_point, starting_count):
    """Constructs the results in a formatted way then saves to file.

    Opens the outfile "Results.txt" (Append mode) and constructs
    results based on; sequence length, starting word, time found,
    time to finish, validation and words tested.

    Args:
        sequence (string)[]: Best sequence of words.
        time_found (float): CPU time best sequence was found.
        time_finished (float): CPU time after full run through.
        start_point (string): word used as starting point.

    Examples:
        Output after a search on size = 4. Given program ran without error.

        >>>save_results(longest_sequence, time_found, time.process_time(), best_word)
        Saved:
        _____________________________________________________________________________________
        Starting word: carl
        Sequence length: 92
        Found at: 0000.16
        Is sequence valid?: True
        Words tested: 314
        Time taken (secs): 0.21875
    """
    out_file = open("Results.txt","a+")
    output = "_____________________________________________________________________________________"
    output += "\nStarting word: " + start_point
    output += "\nSequence length: " + str(len(sequence))
    output += "\nFound at: {:07.2f}".format(time_found)
    output += "\nIs sequence valid?: " + str(validate(longest_sequence))
    output += "\nWords tested: " + str(starting_count)
    output += "\nTime taken (secs): " + str(time_finished)
    print("Saving: \n", output, sep="")
    output += "\nSequence: " + str(longest_sequence) + "\n\n"
    out_file.write(output)
    out_file.close()
# /////////////////////////////////////////////////////////////////////////////////////////////////
# save_results Function End
# /////////////////////////////////////////////////////////////////////////////////////////////////


# /////////////////////////////////////////////////////////////////////////////////////////////////
# validate Function Start
# /////////////////////////////////////////////////////////////////////////////////////////////////
def validate(sequence):
    """Check the sequence follows sequence[i-1][-3:-1] == sequence[i][1:3] and no duplicate words.

    Runs two loops through the sequence first checks they follow
    sequence[i-1][-3:-1] == sequence[i][1:3] second checks if
    all words are unique. Used at the end to check if sequence is valid.

    Args:
        sequence (string)[]: A sequence of words.

    Returns:
        (bool): If the sequence is valid.
    """
    for i in range(1,len(sequence)):
        if sequence[i-1][-3:-1] != sequence[i][1:3]:
            return False
    return all([sequence.count(x) == 1 for x in sequence])
# /////////////////////////////////////////////////////////////////////////////////////////////////
# validate Function End
# /////////////////////////////////////////////////////////////////////////////////////////////////


# /////////////////////////////////////////////////////////////////////////////////////////////////
# get_starting_words Function Start
# /////////////////////////////////////////////////////////////////////////////////////////////////
def get_starting_words():
    """Goes through the data structures to get starting words with unique front pairs.

    Goes through all word pairs and if a word has more ins than outs
    then it takes it and moves to the next pair.
    So all starting words have unique starting points.

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


# /////////////////////////////////////////////////////////////////////////////////////////////////
# add_to_end Function Start
# /////////////////////////////////////////////////////////////////////////////////////////////////
def add_to_end(sequence):
    """Adds a valid word onto the end of the sequence.

    Take the last word of the sequence and see if it can add to it.
    If it can, check all the children (possible next words) and find the one
    with the most possible ways out (outs) and at least 1 way out. If it can't
    add an end cap (word with no where to go after). If no words were added
    return False otherwise return True.

    Returns:
        (bool): Returns True if it added anywords to the sequence.
    """
    last = sequence[-1]  # Stores last word in variable for ease of use.
    flag = True  # Important to show if a word has children that have children. (Avoiding dead end)
    added = False  # For the return to show if a word was added at all.
    while last[-3:-1] in words_start and flag:
        flag = False  # If this doesn't change no children with children to add.
        best_child = ""
        max_outs = 0
        for sub in words_start[last[-3:-1]]:
            # Sets ins/outs to value in dictionary otherwise 0. (note ins was used in experiments)
            word_ins = ins[sub[1:3]] if sub[1:3] in ins else 0
            word_outs = outs[sub[-3:-1]] if sub[-3:-1] in outs else 0
            # Gets the word with the most outs (The Heuristic).
            if word_outs > max_outs:
                max_outs = word_outs
                best_child = sub
                flag = True
        # If there was a child with a child add it to the sequence.
        if flag:
            sequence.append(pop_word(best_child))
            added = True
        last = sequence[-1]
    # Add the end cap. Child without any children.
    if last[-3:-1] in words_start:
        sequence.append(pop_word(words_start[last[-3:-1]].pop()))
        added = True
    return added
# /////////////////////////////////////////////////////////////////////////////////////////////////
# add_to_end Function End
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
                max_ins = word_ins
                best_child = sub
                flag = True
        # If there was a child with a child add it to the sequence.
        if flag:
            sequence.appendleft(pop_word(best_child))
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
# Main Start
# /////////////////////////////////////////////////////////////////////////////////////////////////
if __name__ == "__main__":
    # Error checking
    size = -1
    try:
        size = int(sys.argv[1])
    except:
        size = -1
    if size in range(4,16):
        if read_in_words(size):
            # Initialisation for variables to store longest sequence and keep track of things.
            best_word = ""
            time_found = 0.0  # How far into the runtime it found the best sequence.
            longest_sequence = []
            used_words = []  # Used to make sure a word isn't re tried.

            # Generate starting words and try them all.
            starting_words = get_starting_words()
            starting_count = len(starting_words)
            print(starting_count)
            for word in starting_words:
                # Start the sequence with the starting word
                sequence = deque([pop_word(word)])
                # Add as many as possible to the front first.
                add_to_front(sequence)
                # Checks if new sequence is best (odd cases it finds the best without altering n=4).
                if len(sequence) > len(longest_sequence):
                    longest_sequence = list(sequence)
                    best_word = word
                    time_found = time.process_time()
                # Add as many to the back as possible then start removing until it is possible.
                while add_to_end(sequence):
                    # Best sequence check and store.
                    if len(sequence) > len(longest_sequence):
                        longest_sequence = list(sequence)
                        best_word = word
                        time_found = time.process_time()
                    # Remove words off the end until words can be added. Also early escape cases;
                    # When there isn't enough possible words to beat current or back at the start word.
                    while sequence[-1][-3:-1] not in words_start and sequence[-1] != word and len(sequence) + word_count > len(longest_sequence):
                        used_words.append(sequence.pop())
                # Debug statement. (Uncomment to see progress)
                print("Starting word:", word, "Length of Best Sequence:", len(longest_sequence), "Time:", "{:07.2f}".format(time.process_time()), "Words to try:", starting_count)

                # Unwrapping the words from the sequence and used words.
                # Bit faster than copying all the dictionaries everytime.
                for i in range(len(sequence)):
                    add_word(sequence.pop())
                for i in range(len(used_words)):
                    add_word(used_words.pop())
            # Save the results once all the starting positions have been tried
            save_results(longest_sequence, time_found, time.process_time(), best_word, starting_count)
        else:
            print("Error: dictionary.txt File not found or Error reading.")  # Debug/Error message.
    else:
        print("Error: Please use range in argument $python", sys.argv[0], "<4-15>")  # Debug/Error message.

# /////////////////////////////////////////////////////////////////////////////////////////////////
# Main End
# /////////////////////////////////////////////////////////////////////////////////////////////////
