#include <iostream>
#include <random>
#include <string>

const int SEQUENCE_LENGTH = 128;

/**
 * Generates a pseudo-random binary sequence of the specified length.
 * 
 * @return The generated binary sequence as a string of hexadecimal digits.
 */
std::string generateRandomSequence() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 255);

    std::string sequence;
    sequence.reserve(SEQUENCE_LENGTH / 8 * 2); 
    for (int i = 0; i < SEQUENCE_LENGTH / 8; ++i) {
        int random_byte = dis(gen);
        sequence += std::to_string(random_byte);
    }
    return sequence;
}

int main() {
    std::string randomSequence = generateRandomSequence();

    std::cout << "Random sequence: " << randomSequence << std::endl;

    return 0;
}
