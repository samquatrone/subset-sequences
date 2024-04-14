from math import comb
from collections import deque

class Node:
    def __init__(self, word, alphabet, seen_words, state):
        """
            - word is a tuple of elements from the alphabet
            - alphabet is a list/tuple of characters
            - seen words is a set of words (sorted tuples of characters). 
                This set contains every word of the ancestor nodes, not including the word of the current node.
            - state is the string representing the current game state
        """
        self.word = word
        self.alphabet = alphabet
        self.seen_words: list = seen_words
        self.state = state
        self.children = None

    def generate_children(self):
        children = []

        for letter in self.alphabet:
            if letter not in self.word:
                new_word = self.word[1:] + tuple(letter)
                children.append(
                    Node(
                        new_word, 
                        self.alphabet, 
                        self.seen_words + [tuple(sorted(self.word))], 
                        self.state + letter
                    )
                )

        self.children = children
        return children

    def is_valid(self):
        return tuple(sorted(self.word)) not in self.seen_words

    def has_children(self):
        return self.children is not None


def generate_tree(alphabet, start_word):
    root = Node(tuple(start_word), alphabet, [], start_word)
    max_words = comb(len(alphabet), len(start_word))
    data = {
        'alphabet': alphabet,
        'seed word': start_word,
        'node_count': {depth: 0 for depth in range(max_words+len(start_word)-1)},
        'failure_count': {},
        'depth_from_repeat_count': {
            depth: {
                distance: 0 for distance in range(len(start_word)+1, depth) 
            } for depth in range(max_words+len(start_word)-1)
        },
        'sequences': [],
    }

    queue: deque[Node] = deque([root])

    while queue:    
        current = queue.popleft()
        depth = len(current.seen_words) # depth starts at 0 with root.
        data['node_count'][depth] += 1

        if current.is_valid():
            children = current.generate_children()
            queue.extend(children)
        elif len(current.seen_words) == max_words:
            data['sequences'].append(current.state[:-1])
        else:
            if depth not in data['failure_count']:
                data['failure_count'][depth] = 0

            data['failure_count'][depth] += 1

            if depth not in data['depth_from_repeat']:
                data['depth_from_repeat'][depth] = {}
            failure_distance = depth - current.seen_words.index(tuple(sorted(current.word)))
            if failure_distance not in data['depth_from_repeat'][depth]:
                data['depth_from_repeat'][depth][failure_distance] = 0
            
            data['depth_from_repeat'][depth][failure_distance] += 1

        # print(f'Queue length: {len(queue)}')    # FIXME:
    return root, data

def print_tree_to_file(node: Node, filename: str, data: dict):
    with open(filename, 'w', encoding='utf-8') as f:
        for label, dataset in data.items():
            f.write(f'{label}:\n')

            if isinstance(dataset, (list,tuple)):
                for line in dataset:
                        f.write('  ' + str(line) + '\n')

            elif isinstance(dataset, dict):
                for key, value in dataset.items():
                    f.write(f'  {key}: {value}\n')
            else:
                f.write('  ' + str(dataset) + '\n')

        f.write('\n\nGame Tree:\n')

        print_tree(node, f)

def print_tree(node: Node, f, depth=0):
    if node.children is None:
        target_depth = comb(len(node.alphabet), len(node.word))
        if depth == target_depth:
            f.write('  ' * depth + ''.join(node.word) + ' - ✓\n')
        else:
            depth_from_failure = len(node.seen_words) - node.seen_words.index(tuple(sorted(node.word)))

            f.write('  ' * depth + ''.join(node.word) + f' - X{depth_from_failure}\n')
    else:
        f.write('  ' * depth + ''.join(node.word) + '\n')
        for child in node.children:
            print_tree(child, f, depth+1)

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



if __name__ == '__main__':
    alphabet = ('a','b','c','d', 'e', 'f')
    start_word = 'abc'

    root, data = generate_tree(alphabet, start_word)

    for sequence in data['sequences']:
        if not verify_sequence(sequence, alphabet, len(start_word)):
            data['sequences'].remove(sequence)

    data['sequence_count'] = len(data['sequences'])

    print_tree_to_file(root, 'game_tree.txt', data)




'''
Interesting analytics:
    - List valid sequences                                      ✓
    - How many are unique up to relabeling?                     x
        - How many including all relabelings?                   x
    - How many nodes at each depth?                             ✓
    - How many failures at each depth?                          ✓
        - How many layers up did the failure occur?             ✓
    - How many of these sequences can be written cyclically?    x
'''
