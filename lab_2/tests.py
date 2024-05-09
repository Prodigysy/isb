import json
import logging
import math
import os
from math import erfc, fabs, sqrt

logging.basicConfig(level=logging.INFO)

def serial_test(bitstring: str) -> float:
    """
    Performs the Serial Test for the given bit sequence.

    Parameters:
    bitstring (str): The bit sequence to be tested.

    Returns:
    float: The p-value indicating the degree of correlation in the sequence.
    """
    ones = bitstring.count('1')
    zeros = len(bitstring) - ones
    ones_sequence = zeros_sequence = 0

    for i in range(len(bitstring) - 1):
        if bitstring[i] == '1' and bitstring[i+1] == '1':
            ones_sequence += 1
        elif bitstring[i] == '0' and bitstring[i+1] == '0':
            zeros_sequence += 1

    p_value = erfc(fabs(ones_sequence - zeros_sequence) / sqrt(2 * ones * zeros))

    return p_value

def frequency_test_within_block(bitstring: str, M: int, Q: int) -> float:
    """
    Performs the Frequency Test within a Block for the given bit sequence.

    Parameters:
    bitstring (str): The bit sequence to be tested.
    M (int): The number of blocks.
    Q (int): The length of each block.

    Returns:
    float: The p-value indicating the degree of randomness in the bit sequence.
    """
    n = len(bitstring)
    if n < M * Q:
        logging.error("Error: M * Q should be less than or equal to the length of the bit sequence.")
        return None

    frequencies = []
    for i in range(0, n, Q):
        block = bitstring[i:i+Q]
        ones_count = block.count('1')
        frequencies.append(ones_count / Q)

    mean_frequency = sum(frequencies) / M
    chi_square = sum([(freq - mean_frequency) ** 2 for freq in frequencies]) * M
    p_value = erfc(chi_square / sqrt(2 * M))

    return p_value

def cumulative_sums_test(bitstring: str) -> float:
    """
    Performs the Cumulative Sums Test for the given bit sequence.

    Parameters:
    bitstring (str): The bit sequence to be tested.

    Returns:
    float: The p-value indicating the degree of randomness in the cumulative sums.
    """
    S = [0]
    for bit in bitstring:
        if bit == '1':
            S.append(S[-1] + 1)
        else:
            S.append(S[-1] - 1)

    max_S = max(S)
    min_S = min(S)
    z = max(fabs(max_S), fabs(min_S))
    N = len(bitstring)
    p_value = erfc(z / sqrt(N * (N + 1) * (2 * N + 1) / 6))

    return p_value

if __name__ == "__main__":
    try:
        with open(os.path.join("lab_2", "settings.json"), "r", encoding="utf-8") as paths_file:
            paths = json.load(paths_file)

        path1 = paths['path_input']
        path2 = paths['path_output']

        with open(path1, "r", encoding="utf-8") as sequences:
            sequence = json.load(sequences)

        M = paths.get('M')
        Q = paths.get('Q')
        cpp_sequence = sequence['cpp']
        java_sequence = sequence['java']

        with open(path2, 'w', encoding='utf-8') as out_file:
            out_file.write("Results (C++)\n")
            out_file.write("Serial Test: " + str(serial_test(cpp_sequence)) + '\n')
            out_file.write("Frequency Test within a Block: " + str(frequency_test_within_block(cpp_sequence, M, Q)) + '\n')
            out_file.write("Cumulative Sums Test: " + str(cumulative_sums_test(cpp_sequence)) + '\n\n')

            out_file.write("Results (Java)\n")
            out_file.write("Serial Test: " + str(serial_test(java_sequence)) + '\n')
            out_file.write("Frequency Test within a Block: " + str(frequency_test_within_block(java_sequence, M, Q)) + '\n')
            out_file.write("Cumulative Sums Test: " + str(cumulative_sums_test(java_sequence)) + '\n\n')

        logging.info("Tests completed successfully.")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e.filename}")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
    except KeyError as e:
        logging.error(f"KeyError: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
