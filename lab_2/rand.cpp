#include <iostream>
#include <cstdlib>
#include <ctime>

/**
 * @brief Generates a pseudo-random 128-bit binary sequence and prints it to the standard output.
 *
 * This function initializes the random number generator using the current time and generates
 * a 128-bit binary sequence, printing it to the standard output.
 */
void generateRandomBinarySequence() {
    std::srand(static_cast<unsigned>(std::time(0)));

    for (int i = 0; i < 128; ++i) {
        int random_bit = std::rand() % 2;
        std::cout << random_bit;
    }
}

int main() {
    generateRandomBinarySequence();

    return 0;
}