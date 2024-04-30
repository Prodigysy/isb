#include <iostream>
#include <random>
#include <string>

const int SEQUENCE_LENGTH = 128;

/**
 * Generates a pseudo-random binary sequence of the specified length.
 * 
 * @return The generated binary sequence as a string of binary digits ('0' and '1').
 */
std::string generateRandomSequence() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 1);

    std::string sequence;
    sequence.reserve(SEQUENCE_LENGTH);
    for (int i = 0; i < SEQUENCE_LENGTH; ++i) {
        int random_bit = dis(gen);
        sequence += std::to_string(random_bit);
    }
    return sequence;
}

int main() {
    std::string randomSequence = generateRandomSequence();
    std::cout << "Random sequence: " << randomSequence << std::endl;

    return 0;
}
