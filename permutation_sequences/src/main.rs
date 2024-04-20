use std::collections::HashSet;

static PRIMES: [u32; 100] = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
    53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 
    127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 
    197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 
    277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 
    367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 
    449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541
];
static ASCII_LOWER: [char; 26] = [
    'a', 'b', 'c', 'd', 'e', 
    'f', 'g', 'h', 'i', 'j', 
    'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 
    'u', 'v', 'w', 'x', 'y', 
    'z',
];

struct Node {
    label: String,
    sequence: String,
    ancestor_set: HashSet<u32>,
}
impl Node {
    fn new(self, label: String, sequence: String, ancestor_set: HashSet<u32>) -> Self {

        Self {
            label,
            sequence,
            ancestor_set,
        }
    }

    fn generate_children(self) {

    }

    fn is_valid(self) -> bool {

        false
    }
}

fn generate_tree(alphabet_size: usize, subset_size: u32) -> Vec<String> {
    let mut valid_sequences: Vec<String> = Vec::new();

    let alphabet = vec![&ASCII_LOWER[0..alphabet_size]];
    let mut queue: Vec<Node> = Vec::new();

    valid_sequences
}


fn main() {
    println!("Hello, world!");
}