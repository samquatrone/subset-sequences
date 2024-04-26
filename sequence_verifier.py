from math import comb
from collections import defaultdict
from itertools import permutations

def get_normal_form(s: str):
    seen_chars = set()
    current_id = 0
    # normal_form = [char for char in s]

    map = {
            0:"a", 
            1:"b", 
            2:"c", 
            3:"d", 
            4:"e",
            5:"f",
            6:"g",
            7:"h",
            8:"i",
            9:"j",           
        }
    
    for char in str(s):
        if char not in seen_chars:
            seen_chars.add(char)
            s = s.replace(char, map[current_id])
            current_id += 1
    
    return s

def count_unique_strings(strings):
    normal_forms = set()
    
    for s in strings:
        # normal_form = get_normal_form(s)
        # print(f'{s} -> {normal_form}')
        if s not in normal_forms:
            normal_forms.add(s)
        
    
    unique_count = len(normal_forms)
    
    return unique_count

def read_strings_from_file(filename):
    """
    Read strings from a file and return a list of strings.
    """
    with open(filename, 'r') as file:
        return [line.strip() for line in file]





def verify_sequence(sequence, alphabet_len, word_length):
    expected_length = comb(alphabet_len, word_length) + word_length-1
    if len(sequence) != expected_length:
        print(f'FAILURE: Sequence {sequence} is not the expected length.')
        return False
    
    word_set = set()
    
    for i in range(comb(alphabet_len, word_length)):
        word = tuple(sequence[i:i+word_length])
        if len(word) != len(set(word)):
            print(f'FAILURE: Sequence \'{sequence}\' has repeated characters in word: \'{word}\'.')
            return False

        if tuple(sorted(word)) in word_set:
            print(f'FAILURE: Sequence \'{sequence}\' has a repeated word: \'{word}\'')
            return False
        
        word_set.add(tuple(sorted(word)))

    # print(f'SUCCESS: Sequence \'{sequence}\'.')

    return True

def sanitize_sequences(sequences, alphabet_len, word_length):
    return [s for s in sequences if verify_sequence(s, alphabet_len, word_length)]



if __name__ == '__main__':
    alphabet_len = 7
    word_length = 2
    # verify_sequence('abcgfedgfbegcafecdgafdbgaedbceabfcdab', alphabet, word_length)

    # filename = 's7-2.txt'
    # unique_count = count_unique_strings(filename)
    # print(f'Number of unique strings: {unique_count}')

    # strings = ['abca', 'dbcd', 'abcd']

    # test = "0123452413026405163560"

    # print(get_normal_form(test))


    filename = 'strings.txt'  # Replace with your file name
    strings = [s.replace(" ", "") for s in read_strings_from_file(filename)]
    strings = sanitize_sequences(strings, alphabet_len, word_length)

    unique_count = count_unique_strings(strings)
    print(f'Number of unique strings: {unique_count}')


