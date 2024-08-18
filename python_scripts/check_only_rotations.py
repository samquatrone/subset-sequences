import csv
from itertools import permutations

def convert_sequence_to_tuple(sequence):
    """Convert a string sequence to a tuple of integers based on character order."""
    char_to_int = {char: idx for idx, char in enumerate(sorted(set(sequence)))}
    return tuple(char_to_int[char] for char in sequence)

def generate_all_relabelings(sequence):
    """Generate all unique relabelings of a sequence."""
    unique_labels = sorted(set(sequence))
    label_permutations = permutations(unique_labels)
    
    relabelings = set()
    for perm in label_permutations:
        mapping = {old: new for old, new in zip(unique_labels, perm)}
        relabeled_sequence = tuple(mapping[x] for x in sequence)
        relabelings.add(relabeled_sequence)
        
    return relabelings

def generate_all_rotations(sequence):
    """Generate all rotations of a sequence."""
    rotations = set()
    n = len(sequence)
    for i in range(n):
        rotated_sequence = sequence[i:] + sequence[:i]
        rotations.add(rotated_sequence)
    return rotations

def canonical_form(sequence):
    """Return the canonical form of a sequence considering rotations."""
    rotations = generate_all_rotations(sequence)
    return min(rotations)

def unique_up_to_rotation(sequences):
    """Determine the number of unique sequences up to rotation."""
    unique_sequences = set()
    
    for sequence in sequences:
        relabelings = generate_all_relabelings(sequence)
        for relabeled_sequence in relabelings:
            canonical_sequence = canonical_form(relabeled_sequence)
            unique_sequences.add(canonical_sequence)
    
    return len(unique_sequences)

def read_sequences_from_csv(file_path):
    """Read sequences from a CSV file."""
    sequences = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        if ALPHABET_LENGTH == SUBSET_SIZE or SUBSET_SIZE == 1:
            for row in reader:
                sequence = tuple(map(int, row))
                sequences.append(sequence)
        else:
            for row in reader:
                sequence = cyclify(tuple(map(int, row)))
                sequences.append(sequence)
    return sequences

def cyclify(sequence):
    return tuple(sequence[:-SUBSET_SIZE+1])

ALPHABET_LENGTH = 7
SUBSET_SIZE = 4

if __name__ == '__main__':
    file_path = f'permutation_sequences\sequences\\sequence-{ALPHABET_LENGTH}-{SUBSET_SIZE}.csv'
    sequences = read_sequences_from_csv(file_path)
    # print(sequences)
    unique_count = unique_up_to_rotation(sequences)
    print("Number of unique sequences up to rotation:", unique_count)
