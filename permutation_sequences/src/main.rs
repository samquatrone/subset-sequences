fn main() {
    println!("Hello, world!");
}

struct Node {
    label: String
}
impl Node {
    fn new(self, label: String) -> Self {

        Self {
            label
        }
    }

    fn generate_children(self) {
        
    }

    fn is_valid(self) -> bool {

        false
    }
}

