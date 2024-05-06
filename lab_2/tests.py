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

def maurers_universal_statistical_test(bitstring: str, L: int, Q: int) -> float:
    """
    Performs Maurer’s Universal Statistical Test for the given bit sequence.

    Parameters:
    bitstring (str): The bit sequence to be tested.
    L (int): The length of the substrings to be considered.
    Q (int): The number of substrings to be considered.

    Returns:
    float: The p-value indicating the degree of randomness in the bit sequence.
    """
    n = len(bitstring)
    K = n // Q

    if L * Q > n:
        logging.error("Error: L * Q should be less than or equal to the length of the bit sequence.")
        return None

    blocks = [bitstring[i:i+L] for i in range(0, L * Q, L)]
    T = [0] * Q

    for i in range(1, min(Q, len(blocks))):
        seen = set()
        for j in range(K):
            idx = i + j * Q
            if idx < len(blocks):
                if blocks[idx] not in seen:
                    T[i] += 1
                    seen.add(blocks[idx])

    v_obs = sum(T[1:]) / (Q - 1)
    lambda_val = (v_obs - 0.7) * math.sqrt(Q + 1.4)

    p_value = math.erfc(abs(lambda_val) / math.sqrt(2))

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
        L = paths.get('L')
        Q = paths.get('Q')

        with open(path1, "r", encoding="utf-8") as sequences:
            sequence = json.load(sequences)

        cpp_sequence = sequence['cpp']
        java_sequence = sequence['java']

        with open(path2, 'w', encoding='utf-8') as out_file:
            out_file.write("Results (C++)\n")
            out_file.write("Serial Test: " + str(serial_test(cpp_sequence)) + '\n')
            out_file.write("Maurer’s Universal Statistical Test: " + str(maurers_universal_statistical_test(cpp_sequence, L, Q)) + '\n')
            out_file.write("Cumulative Sums Test: " + str(cumulative_sums_test(cpp_sequence)) + '\n\n')

            out_file.write("Results (Java)\n")
            out_file.write("Serial Test: " + str(serial_test(java_sequence)) + '\n')
            out_file.write("Maurer’s Universal Statistical Test: " + str(maurers_universal_statistical_test(java_sequence, L, Q)) + '\n')
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
