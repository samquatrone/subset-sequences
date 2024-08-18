use std::collections::HashSet;
use num_integer::{self, binomial};
use std::fs::File;
use std::io::{self, Write};
use std::path::Path;
use std::time::Instant;

use rand::thread_rng;
use rand::seq::SliceRandom;


// Nodes should only be created if they are valid.
// Instead, children are checked for validity before instantiation.
struct Node {
    label: u16,
    sequence: Vec<u16>,
    seen_labels: HashSet<u16>, // Contains its own label
}
impl Node {
    fn new(parent_node: &Node, subset_size: usize, letter: u16) -> Option<Node> {
        let child_label = parent_node.get_child_label(subset_size, letter);
        if child_label.is_some() {
            let mut new_seen_labels: HashSet<u16> = parent_node.seen_labels.clone();
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

        // Find all letters from 1...max_letter which are not in self.sequence
        let used_letters = self.label;
        let all_letters = (max_letter << 1) - 1;
        let new_letters_label = all_letters & !used_letters;

        let mut new_letters: Vec<u16> = Vec::with_capacity(alphabet_size-subset_size-1);

        let mut i: u16 = 1;
        while i <= new_letters_label {
            if i & new_letters_label != 0 {
                new_letters.push(i)
            }
            i <<= 1
        }

        // If any letters from the alphabet have not been seen, add the next greatest letter to new_letters.
        if max_letter < (1 << alphabet_size - 1) {
            new_letters.push(max_letter << 1);
        }

        for letter in new_letters {
            // Try to create a new child from letter
            // If this child would contain a duplicate label, the node is not created
            let new_child = Node::new(&self, subset_size, letter);
            if new_child.is_some() {
                queue.push(new_child.unwrap());
            }
        }

    }
    
    
    fn get_child_label(&self, subset_size: usize, new_element: u16) -> Option<u16> {
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

fn generate_tree(root: Node, alphabet_size: usize, subset_size: usize) -> (Vec<Vec<u16>>, Vec<u128>, u128)  {
    let mut valid_sequences: Vec<Vec<u16>> = Vec::new();
    let mut queue: Vec<Node> = Vec::new();
    // let mut queue: VecDeque<Node> = VecDeque::new();

    // Potential optimization here
    // We don't need to check the very last few depths (assuming every sequence is cyclic)
    let max_depth = binomial(alphabet_size, subset_size)+ subset_size-1;   

    let mut num_iterations: u128 = 0;
    let mut depth_map: Vec<u128> = vec![0; max_depth];
    let mut num_sequences: u32 = 0;

    // let mut rand_num: u32 = 0;
    // let mut rng = thread_rng();
    let mut found_sequence = false;


    queue.push(root);
    let mut current_node: Node;

    while !queue.is_empty() {

        current_node = queue.pop().unwrap();

        
        let current_sequence = &current_node.sequence;

        let current_depth = current_sequence.len();


        if current_depth == max_depth {
            valid_sequences.push(current_sequence.clone());
            num_sequences += 1;
            println!("Found one! {}", format_sequence(current_sequence));
            found_sequence = true;
        }
        else {
            current_node.generate_children(alphabet_size, subset_size, &mut queue);
        }

        depth_map[current_depth-1] += 1;
        num_iterations += 1;
        // rand_num = rng.gen_range(0..=100);

        if num_iterations % 10000000 == 0 {
            println!("Sequence count: {}   Iteration count: {}   Queue length: {}", num_sequences, num_iterations, queue.len());
            if !found_sequence && queue.len() < 10000000 {
                // println!("Shuffling...");
                queue.shuffle(&mut thread_rng());
            }
            found_sequence = false;
        }
    }

    (valid_sequences, depth_map, num_iterations)
}


fn generate_root(subset_size: usize) -> Node {
    let label = (1 << subset_size) - 1 << 1;
    let sequence: Vec<u16> = (0..subset_size+1).map(|i| 1 << i).collect();
    let seen_labels: HashSet<u16> = sequence[..]
                .windows(subset_size)
                .map(|w| w.iter().sum())
                .collect();

    Node {
        label,
        sequence,
        seen_labels
    }
}

fn format_sequences(sequences: &Vec<Vec<u16>>) -> Vec<String> {
    sequences
    .iter()
    .map(|sequence| {
        sequence
            .iter()
            .map(|&num| {
                let power = (num as f64).log2() as u16;
                power.to_string()
            })
            .collect::<Vec<String>>()
            .join(",")
    })
    .collect()
}

fn format_sequence(sequence: &Vec<u16>) -> String {
    sequence
        .iter()
        .map(|&num| {
            let power = (num as f64).log2() as u16;
            power.to_string()
        })
        .collect::<Vec<String>>()
        .join(",")
}

fn _sequence_to_string(sequence: &Vec<u16>) -> String {
    sequence.into_iter().map(|x| x.to_string()).into_iter().collect::<Vec<String>>().join(",")
}


fn save_sequences(sequences: &Vec<String>, filename: String) -> io::Result<()> {
    let folder_path = Path::new("./sequences/");
    if !folder_path.exists() {
        std::fs::create_dir(folder_path)?;
    }

    let file_path = folder_path.join(filename);
    let mut file = File::create(file_path)?;

    for sequence in sequences {
        writeln!(file, "{}", sequence)?;
    }

    Ok(())
}

fn save_data(data: (&Vec<Vec<u16>>, &Vec<u128>, u128), filename: String ) -> io::Result<()> {
    let (sequences, depth_map, num_iterations) = data;
    let folder_path = Path::new("./sequence_data/");
    if !folder_path.exists() {
        std::fs::create_dir(folder_path)?;
    }

    let file_path = folder_path.join(filename);
    let mut file = File::create(file_path)?;

    writeln!(file, "Number of sequences: {}", sequences.len())?;
    writeln!(file, "Number of iterations: {}", num_iterations)?;

    writeln!(file, "Depth Map:")?;
    for depth in 0..depth_map.len() {
        writeln!(file, "   Depth: {}, Node count: {}", depth, depth_map[depth])?;
    }

    Ok(())
}

fn get_parameters() -> (usize, usize) {
    // Get user input for alphabet_size
    println!("Enter alphabet size:");
    let mut alphabet_size_input = String::new();
    io::stdin().read_line(&mut alphabet_size_input)
        .expect("Failed to read input");
    
    let alphabet_size: usize = alphabet_size_input.trim().parse()
        .expect("Please enter a valid number");

    // Get user input for subset_size
    println!("Enter subset size:");
    let mut subset_size_input = String::new();
    io::stdin().read_line(&mut subset_size_input)
        .expect("Failed to read input");
    
    let subset_size: usize = subset_size_input.trim().parse()
        .expect("Please enter a valid number");

    (alphabet_size, subset_size)
}


fn main() -> io::Result<()> {
    let (alphabet_size, subset_size) = get_parameters();
    let root = generate_root(subset_size);

    let now = Instant::now();

    let (sequences, depth_map, num_iterations) = generate_tree(root, alphabet_size, subset_size);
    let elapsed = now.elapsed();
    println!(
        "Sequence generation complete. Found {} sequences after {} iterations in {:.2?}.", 
        &sequences.len(), 
        num_iterations, 
        elapsed,
    );

    
    let formatted_sequences = format_sequences(&sequences);

    let sequence_filename = format!("sequence-{}-{}.csv", alphabet_size, subset_size);
    let data_filename = format!("data-{}-{}.txt", alphabet_size, subset_size);
    
    {
        save_data((&sequences, &depth_map, num_iterations), data_filename)?;
        save_sequences(&formatted_sequences, sequence_filename)?;
        Ok(())
    }
}

