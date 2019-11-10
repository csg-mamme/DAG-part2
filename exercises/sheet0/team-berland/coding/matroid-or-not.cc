#include <cassert>
#include <chrono>
#include <cstring>
#include <fstream>
#include <iostream>
#include <set>
#include <sstream>

/**
 * Since all values in the input are integers between 0 and 19,
 * we can use masks to define the sets (aka matroids, in this case).
 * Masks work the following way: Each mask m represents a set. 
 * The i-th bit of the mask is 1 <==> i belongs to the set
 * We can check if take unions using the bitwise OR (|) operator,
 * intersections using the bitwise AND (&) operator, and complementaries
 * using the bitwise NOT (~) operator. We can also flip bits using the
 * bitwise XOR (^) operator. Finally, we can access the i-th bit by taking
 * a 1 and shifting it i positions to the left (1 << i)
 */
typedef unsigned int Mask;

// Reads the input, builds masks, and updates max_value
void read_masks(std::set<Mask>& masks, int& max_value, const std::string& file_path) {
  std::ifstream file_reader(file_path); 
  std::string line;
  // Read lines
  while (getline(file_reader, line)) {
    // Ignore commented lines
    if (line.front() == '#') 
      continue;
    std::stringstream ss(line);
    Mask mask = 0;
    int val;
    // Read values in the line, check that they are between 0 and 31,
    // update the maximum value, and build the mask,
    while (ss >> val) {
      assert(val >= 0 and val < 32);
      max_value = std::max(max_value, val);
      mask |= (1 << val);
    }
    // Insert the mask in the set of masks
    masks.insert(mask);
  }
}

// Checks if the set of masks corresponds to a matroid
bool is_matroid(const std::set<Mask>& masks, const int max_value) {
  for (Mask mask_base1 : masks)                                       // For each base B1
    for (Mask mask_base2 : masks)                                     // For each base B2
      for (int x = 0; x <= max_value; ++x)
        if ((mask_base1 & (1 << x)) and !(mask_base2 & (1 << x))) {   // If x \in B1 and x \notin B2
          Mask mask_base1_without_x = (mask_base1 ^ (1 << x));
          bool exists_exchangeable_base = false;                      // Checks if exists y
          for (int y = 0; y <= max_value and !exists_exchangeable_base; ++y)
            if (!(mask_base1 & (1 << y)) and (mask_base2 & (1 << y))) // If x \notin B1 and x \in B2
              if (masks.count(mask_base1_without_x ^ (1 << y)))       // If B1 \ {x} U {y} exists
                exists_exchangeable_base = true;                      // Then y exists
          if (!exists_exchangeable_base)                              // Not a matroid
            return false;
        }
  return true;
}

bool matroid_or_not(const std::string& file_path) {
  std::set<Mask> masks; // Set of masks
  int max_value = -1;   // Maximum value in the input
  read_masks(masks, max_value, file_path);
  return is_matroid(masks, max_value);
}

int main() {
  const std::string path = "../../matroid-or-not/";
  std::string file;
  while (std::cin >> file) {
    const std::string file_path = path + file;
    std::clog << "Opening file " << file << std::endl; 
    auto start = std::chrono::high_resolution_clock::now();

    std::cout << std::boolalpha << matroid_or_not(file_path) << std::endl;

    auto total_time = std::chrono::duration_cast<std::chrono::milliseconds>
      (std::chrono::high_resolution_clock::now() - start).count();
    std::clog << "Checked file " << file << " in " << double(total_time)/1000 << "s." << std::endl;
  }
}