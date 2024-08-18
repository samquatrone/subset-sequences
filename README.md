# Subset Sequences
This repository is a collection of my research/tools for a sequence problem related to [de Bruijn sequences](https://en.wikipedia.org/wiki/De_Bruijn_sequence) with a few new restrictions. 

## Purpose/Theory
For context, as described from wikipedia: 
> a **de Bruijn sequence** of order *n* on a size-*k* alphabet *A* is a cyclic sequence in which every possible length-*n* string on *A* occurs exactly once as a contiguous subsequence.

My problem is much like this problem, except instead of considering every possible length-*n* ***string***, I am considering every length-*n* ***subset***.
So my inspired definition of a *subset sequence* is as follows:
> A **subset sequence** of order *n* on a size-*k* alphabet *A* is a cyclic sequence in which every possible *n*-subset of *A* occurs exactly once as a contiguous subsequence.

One other thing to note is that we are considering strictly *sets* rather than multisets. So the same element should not occur 
more than once within each sliding window.

Some of my guiding questions are:
1. For what *k* and *n* is there a valid sequence?
2. When there is a valid sequence, how many unique sequences are there total? (unique up to relettering)
3. Given valid *k* and *n*, is there a process which can non-exhaustively generate even a single valid sequence?


### Example
suppose our alphabet is `{a,b,c,d}` and consider the 3-subsets. A valid subset sequence is `abcd`, since
the substrings 'abc', 'bcd', 'cda', and 'dab' account for all 4 of the 3-subsets of the alphabet.
and in some sense this is actually the only valid subset sequence (up to relabelling).
An example of an invalid sequence is `abca...` which is immediately invalid since the substrings 'abc' and 'bca' are *identical* as sets, and so the 3-subset
`{a,b,c}` is repeated at least twice in this example.



## Usage
The majority of code currently in use is within the permutation_sequences rust folder, so make sure to change your directory before use. 
Running the rust program with `cargo run --release` will prompt you for a particular size of alphabet and 
subset size and by entering valid numbers, the program will either complete or update you with the number of sequences found every 10 million iterations.

## Data
All of the data from computations is stored into subset_sequences/sequence-data and the list of valid sequences is stored in subset_sequences/sequences with the
names data-k-n.txt and sequence-k-n.csv, respectively.
Due to the large sizes of these files, subset_sequence/sequences is not tracked, but all data can be accessed with the following link:
https://drive.google.com/drive/folders/1MmbN3PJwFkLt6ZNzSwF_0MmBVNdIH5s8?usp=sharing

For any inquiries or corrections feel free to contact me at samquatrone@gmail.com.
