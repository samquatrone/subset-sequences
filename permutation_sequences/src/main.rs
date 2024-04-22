use std::collections::HashSet;
use num_integer::{self, binomial};
use std::fs::File;
use std::io::{self, Write};
use std::path::Path;


// Nodes should only be created if they are valid.
// Instead, children are checked for validity before instantiation.
struct Node {
    label: u32,
    sequence: Vec<u32>,
    seen_labels: HashSet<u32>, // Contains its own label
}
impl Node {

    fn new(parent_node: &Node, subset_size: usize, letter: u32) -> Option<Node> {
        let child_label = parent_node.get_child_label(subset_size, letter);
        if child_label.is_some() {
            let mut new_seen_labels: HashSet<u32> = parent_node.seen_labels.clone();
            new_seen_labels.insert(child_label.unwrap());
            let mut new_sequence = parent_node.sequence.clone();
            new_sequence.push(letter);
            let new_child = Node {
                label: child_label.unwrap(),
                sequence: new_sequence,
                seen_labels: new_seen_labels
            };
            
            Some(new_child)
        }
        else {
            None
        }
        
    }

    fn generate_children(&self, alphabet_size: usize, subset_size: usize, queue: &mut Vec<Node>) {
        let max_letter = *self.sequence.iter().max().unwrap();

        let used_letters = self.label;
        let all_letters = (max_letter << 1) - 1;
        let new_letters_label = all_letters & !used_letters;

        let mut new_letters: Vec<u32> = Vec::with_capacity(alphabet_size-subset_size-1);

        let mut i: u32 = 1;
        while i <= new_letters_label {
            if i & new_letters_label != 0 {
                new_letters.push(i)
            }
            i <<= 1
        }

        // println!("Max letter = {}", max_letter);
        // println!("Used letters: {}, All letters: {}, New letters label = {}", used_letters, all_letters, new_letters_label);

        if max_letter < (1 << alphabet_size - 1) {
            new_letters.push(max_letter << 1);
        }
        // println!("New letters for sequence {:?}: {:?}", &self.sequence, &new_letters);


        for letter in new_letters {
            let new_child = Node::new(&self, subset_size, letter);
            if new_child.is_some() {
                queue.push(new_child.unwrap());
                // println!("Oh yeah, {} is also okay", {})
            }
            else {
                // println!("Failure to add letter: {}", letter);
            }
        }

    }
    
    // fn _binary_decomp(num:u32) {
    //     let mut i: u32 = 1;
    //         while i <= num {
    //             if i & num != 0 {
    //             }
    //             i <<= 1
    //         }
    // }
    
    fn get_child_label(&self, subset_size: usize, new_element: u32) -> Option<u32> {
        let new_label = new_element + self.label - self.sequence[self.sequence.len()-subset_size];
        // Take parent's label, remove the oldest element from that label, add the new element to it.
        
        if self.seen_labels.contains(&new_label) {
            return None
        }
        else {
            return Some(new_label)
        }
    }
}

fn generate_tree(alphabet_size: usize, subset_size: usize) -> Vec<Vec<u32>> {
    let mut valid_sequences: Vec<Vec<u32>> = Vec::new();
    let mut queue: Vec<Node> = Vec::new();
    let max_depth = binomial(alphabet_size, subset_size) + subset_size-1;

    let root = generate_root(subset_size);

    queue.push(root);

    while !queue.is_empty() {
        let current_node = queue.pop().unwrap();
        let current_sequence = &current_node.sequence;

        if current_sequence.len() == max_depth {
            valid_sequences.push(current_sequence.clone());
            // println!("Found sequence: {:?}", current_sequence)
        }

        current_node.generate_children(alphabet_size, subset_size, &mut queue);
    }

    valid_sequences
}

fn generate_root(subset_size: usize) -> Node {
    let label = (1 << subset_size) - 1 << 1;
    let sequence: Vec<u32> = (0..subset_size+1).map(|i| 1 << i).collect();
    let seen_labels: HashSet<u32> = sequence[..]
                .windows(subset_size)
                .map(|w| w.iter().sum())
                .collect();

    Node {
        label,
        sequence,
        seen_labels
    }
}

fn format_sequences(sequences: &Vec<Vec<u32>>) -> Vec<String> {
    sequences
    .iter()
    .map(|sequence| {
        sequence
            .iter()
            .map(|&num| {
                let power = (num as f64).log2() as u32;
                power.to_string()
            })
            .collect::<Vec<String>>()
            .join(" ")
    })
    .collect()
}

fn save_sequences(sequences: &Vec<String>, filename: String) -> io::Result<()> {
    let folder_path = Path::new("./sequences/");
    if !folder_path.exists() {
        std::fs::create_dir(folder_path)?;
    }

    let file_path = folder_path.join(filename);
    let mut file = File::create(file_path)?;

    writeln!(file, "Number of sequences: {}\n", sequences.len())?;
    if sequences.is_empty() {
        return Ok(())
    }
    writeln!(file, "Sequences:")?;

    for sequence in sequences {
        writeln!(file, "{}", sequence)?;
    }

    Ok(())
}

fn main() -> io::Result<()> {
    let alphabet_size: usize = 7;
    let subset_size: usize = 3;

    let sequences = generate_tree(alphabet_size, subset_size);
    println!("Number of sequences: {}", sequences.len());
    println!("Printing sequences!");
    
    let formatted_sequences = format_sequences(&sequences);

    let filename = format!("sequence-{}-{}.txt", alphabet_size, subset_size);
    save_sequences(&formatted_sequences, filename)
}

