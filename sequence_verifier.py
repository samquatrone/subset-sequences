from math import comb
from collections import defaultdict
from itertools import permutations

def get_normal_form(s: str):
    seen_chars = set()
    current_id = 1
    normal_form = [char for char in s]
    
    for char in str(s):
        if char not in seen_chars:
            seen_chars.add(char)
            s = s.replace(char, str(current_id))
            current_id += 1
    
    return s

def count_unique_strings(strings):
    normal_forms = set()
    
    for s in strings:
        normal_form = get_normal_form(s)
        print(f'{s} -> {normal_form}')
        if normal_form not in normal_forms:
            
            normal_forms.add(normal_form)
        
        
    
    unique_count = len(normal_forms)
    
    return unique_count

def read_strings_from_file(filename):
    """
    Read strings from a file and return a list of strings.
    """
    with open(filename, 'r') as file:
        return [line.strip() for line in file]





def verify_sequence(sequence, alphabet, word_length):
    expected_length = comb(len(alphabet), word_length) + word_length-1
    if len(sequence) != expected_length:
        print(f'FAILURE: Sequence {sequence} is not the expected length.')
        return False
    
    word_set = set()
    
    for i in range(comb(len(alphabet), word_length)):
        word = tuple(sequence[i:i+word_length])
        if len(word) != len(set(word)):
            print(f'FAILURE: Sequence \'{sequence}\' has repeated characters in word: \'{word}\'.')
            return False

        if tuple(sorted(word)) in word_set:
            print(f'FAILURE: Sequence \'{sequence}\' has a repeated word: \'{word}\'')
            return False
        
        word_set.add(tuple(sorted(word)))

    print(f'SUCCESS: Sequence \'{sequence}\'.')

    return True

def sanitize_sequences(sequences, alphabet, word_length):
    return [s for s in sequences if verify_sequence(s, alphabet, word_length)]



if __name__ == '__main__':
    alphabet = ('a','b','c','d','e')
    word_length = 2
    # verify_sequence('abcgfedgfbegcafecdgafdbgaedbceabfcdab', alphabet, word_length)

    # filename = 's7-2.txt'
    # unique_count = count_unique_strings(filename)
    # print(f'Number of unique strings: {unique_count}')
    filename = 'strings.txt'  # Replace with your file name
    strings = sanitize_sequences(read_strings_from_file(filename), alphabet, word_length)

    # strings = ['abca', 'dbcd', 'abcd']
    unique_count = count_unique_strings(strings)
    print(f'Number of unique strings: {unique_count}')


