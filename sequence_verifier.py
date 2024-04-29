from math import comb
from collections import defaultdict
from itertools import permutations, product
import json
import pprint

def normalize_sequence(s: str):
    current_id = 0
    char_map = {}
    mapped_string = []
    
    for i, char in enumerate(s):
        if char not in char_map:
            char_map[char] = current_id
            current_id += 1
        mapped_string.append(str(char_map[char]))

    return ''.join(mapped_string)


def check_rotations(cyclic_sequences):
    unique_sequences = set()
    for sequence in cyclic_sequences:
        # Does there exist a rotation of this sequence which has already been seen?
        # If so, it is not unique and should not be added
        is_unique = True
        for i in range(len(sequence)):
            # Is rotation by i new too seen_sequences?
            if normalize_sequence(rotate_string(sequence, i)) in unique_sequences:
                is_unique = False
        if is_unique:
            unique_sequences.add(sequence)
            
    return unique_sequences
    

    

def find_symmetries(string1, string2):
    if len(string1) != len(string2): 
        raise ValueError('Cannot compare strings of unequal length.')
    
    # all rotations of string1 which result in string2
    symmetry1 = [i for i in range(len(string1)) if  normalize_sequence(rotate_string(string1, i)) == normalize_sequence(string2)]   
    # all rotations of string2 which result in string1
    symmetry2 = [i for i in range(len(string1)) if normalize_sequence(rotate_string(string2, i)) == normalize_sequence(string1)]   

    return symmetry1, symmetry2



def rotate_string(string, num_rotations):
    if num_rotations == 0:
        return string
    else:
        rotated_string = string[-1] + string[:-1]
        return rotate_string(rotated_string, num_rotations-1)


def check_unique_sequences(strings):
    normal_forms = set()

    for s in strings:
        normal_s = normalize_sequence(s)
        if normal_s not in normal_forms:
            normal_forms.add(normal_s)
    unique_sequences = check_rotations(normal_forms)
    
    return unique_sequences


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
            # print(f'FAILURE: Sequence \'{sequence}\' has repeated characters in word: \'{word}\'.')
            return False

        if tuple(sorted(word)) in word_set:
            # print(f'FAILURE: Sequence \'{sequence}\' has a repeated word: \'{word}\'')
            return False
        
        word_set.add(tuple(sorted(word)))

    # print(f'SUCCESS: Sequence \'{sequence}\'.')

    return True

def verify_sequence_cyclic(sequence, alphabet_length, subset_size):
    expected_length = comb(alphabet_length, subset_size)
    if len(sequence) != expected_length:
        # print(f'FAILURE: Sequence {sequence} is not the expected length.')
        return False
    
    sequence = sequence + sequence[:subset_size-1]
    return verify_sequence(sequence, alphabet_length, subset_size)


def sanitize_sequences_cyclic(sequences, alphabet_len, word_length):
    return [s for s in sequences if verify_sequence_cyclic(s, alphabet_len, word_length)]


def invert_dict(dict):
    return {v: k for k, v in dict.items()}


def cyclify(sequence, subset_size):
    return sequence[:-subset_size+1]

if __name__ == '__main__':
    alphabet_length = 8
    subset_size = 5

    filename = f'permutation_sequences\sequences\sequence-{alphabet_length}-{subset_size}.txt'
    strings = [s.replace(" ", "") for s in read_strings_from_file(filename)]
    # strings = [
    #     '0123420413',
    #     '0123420314',
    #     '0123413042',
    #     '0123413024',
    #     '0123403142',
    #     '0123402413',
    #     '0123143042',
    #     '0123143024',
    #     '0123142043',
    #     '0123142034',
    #     '0123140342',
    #     '0123140243',
    #     '0123043142',
    #     '0123041342',
    #     '0123024314',
    #     '0123024134',
    #     '0120342314',
    #     '0120341324',
    #     '0120324314',
    #     '0120324134',
    #     '0120314324',
    #     '0120314234',
    # ]


    # test = rotate_string(strings[2], 5)
    # print(test)
    # print(normalize_sequence(test))

    cyclic_sequences = [cyclify(s, subset_size) for s in strings]
    
    cyclic_sequences = sanitize_sequences_cyclic(cyclic_sequences, alphabet_length, subset_size)
    # unique_sequences = check_rotations(cyclic_sequences)
    unique_sequences = check_unique_sequences(cyclic_sequences)
    print(unique_sequences)
    print()
    print(len(unique_sequences))
    # test_sequence = strings[0]
    # cyclic = cyclify(test_sequence, subset_size)

    # print(f"Sequence: {test_sequence}  Cyclic representation: {cyclic}")

    # print (verify_sequence_cyclic(cyclic, alphabet_size, subset_size))






