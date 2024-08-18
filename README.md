## Purpose/Theory
This repository is a collection of my research into a particular problem very related to [de Bruijn sequences](https://en.wikipedia.org/wiki/De_Bruijn_sequence) with a few restrictions.
For context, as described from wikipedia: a de Bruijn sequence of order *n* on a size-*k* alphabet *A* is a cyclic sequence in which every possible length-*n* string on *A* occurs exactly 
once as a substring.

My problem is an adaptation of this problem where similarly to the de Bruijn sequences, we are considering something like a sliding window problem and checking every length-*n* 
sliding window. The difference is that instead of considering every possible length-*n* string, we are considering every possible *n*-element subset of the alphabet. 
So in the original problem, the arrangement of elements within each sliding window was important, but now since we are only looking at the set of elements within the sliding window,
any arrangement of these elements is identical. The other distinction to note is that we are considering strictly sets rather than multisets. So the same element should not occur 
more than once within each sliding window.

My two guiding questions are:
1. For what *k* and *n* is there a valid sequence?
2. When there is a valid sequence, how many unique sequences are there total? (unique up to relettering)

## Usage
The majority of code currently in use is within the permutation_sequences rust folder, so make sure to change your directory before use. 
Running th rust program with `cargo run --release` will prompt you for a particular size of alphabet and 
subset size and by entering valid numbers, the program will either complete or update you with the number of sequences found every 10 million iterations.

## Data
All of the data from computations is stored into subset_sequences/sequence-data and the list of valid sequences is stored in subset_sequences/sequences with the
names data-k-n.txt and sequence-k-n.csv, respectively.
Due to the large sizes of these files, subset_sequence/sequences is not tracked, but all data can be accessed with the following link:
https://drive.google.com/drive/folders/1MmbN3PJwFkLt6ZNzSwF_0MmBVNdIH5s8?usp=sharing

For any inquiries or corrections feel free to contact me at samquatrone@gmail.com.
