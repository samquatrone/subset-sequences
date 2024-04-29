from itertools import product, permutations
from math import comb
from sequence_verifier import verify_sequence_cyclic, check_unique_sequences

alphabet = [0, 1, 2, 3, 4]
alphabet_size = len(alphabet)
subset_size = 2

sequence_length = comb(alphabet_size, subset_size)

valid_sequences = set()

for sequence in permutations('0123401234'):
    sequence = ''.join(sequence)
    if verify_sequence_cyclic(sequence, alphabet_size, subset_size):
        valid_sequences.add(sequence)

# print(valid_sequences)
# print()
print(f"Valid sequences found: {len(valid_sequences)}. \nNow checking uniqueness...")

unique_sequences = check_unique_sequences(list(valid_sequences))

print(unique_sequences)
print()
print(f"Unique sequences found: {len(unique_sequences)}")
