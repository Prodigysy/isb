import json
import logging
import os
import mpmath

from math import erfc, fabs, pow, sqrt

logging.basicConfig(level=logging.INFO)

pi = [0.2148, 0.3672, 0.2305, 0.1875]
SEQUENCE_LENGTH = 128
BLOCK_SIZE = 6


def frequency_test(bitstring:str) -> float:
    """
    Calculates the p-value of the frequency (monobit) test for a given bit sequence.

    This test evaluates whether the number of ones and zeros in the sequence is approximately equal,
    indicating uniform distribution.

    Parameters:
    bitstring (str): The binary sequence to be tested.
    """
    try:
        N = len(bitstring)
        sum_values = fabs(sum(1 if bit == '1' else -1 for bit in bitstring))
        p_value = erfc((sum_values) / sqrt(2*N))
        return p_value
    except Exception as ex:
        logging.error(f"Error occurred during the test execution: {ex}\n")



def runs_test(sequence):
    """
    Performs the runs test for the given binary sequence.

    This test checks for the presence of runs in the sequence, where a run is defined as consecutive
    bits of the same value.

    Parameters:
    sequence (str): The binary sequence to be tested.

    Returns:
    float: The p-value indicating the randomness of the runs in the sequence.
    """
    try:
        n = len(sequence)
        runs = [sequence[0]]
        for bit in sequence:
            if bit != runs[-1]:
                runs.append(bit)
        k = len(runs)
        pi = sequence.count('1') / n
        tau = 2 / (pi * (1 - pi)) ** 0.5
        vobs = sum([1 for i in range(1, k - 1) if runs[i - 1] != runs[i + 1]]) + 1
        p_value = erfc(abs(vobs - 2 * n * pi * (1 - pi)) / (2 * pi * (1 - pi) * (2 * n) ** 0.5))
        return p_value
    except Exception as ex:
        logging.error(f"Error occurred during the test execution: {ex}\n")


def longest_run_test(bitstring:str) -> float:
    """
    Performs the longest run of ones test for the given bit sequence.
    Parameters:
    bitstring (str): The bit sequence to be tested.
    Returns:
    float: The p-value indicating the degree of randomness in the distribution of longest runs of ones.
    """
    try:
        N = len(bitstring)
        M = 8

        max_run_lengths = [max(len(run) for run in block.split('0')) for block in [bitstring[i:i+M] for i in range(0, N, M)]]

        v1 = sum(1 for length in max_run_lengths if length <= 1)
        v2 = sum(1 for length in max_run_lengths if length == 2)
        v3 = sum(1 for length in max_run_lengths if length == 3)
        v4 = sum(1 for length in max_run_lengths if length >= 4)
        V = [v1, v2, v3, v4]

        x_square = 0
        for i in range(4):
            x_square += pow(V[i] - 16 * pi[i], 2) / (16 * pi[i])
        p_value = mpmath.gammainc(3/2, x_square/2)

        return p_value
    except Exception as ex:
            logging.error(f"Error occurred during the test execution: {ex.message}\n{ex.args}\n")
            

def read_sequence_from_file(file_name):

    with open(file_name, 'r') as file:
        sequence = file.read().strip()
    return sequence

def save_results(results, output_path):
    with open(output_path, "w") as results_file:
        json.dump(results, results_file, indent=4)


if __name__ == "__main__":
    try:
        with open(os.path.join("lab_2", "settings.json"), "r") as paths_file:
            path = json.load(paths_file)
        path1 = path['path_input']
        path2 = path['path_output']

        with open(path1 , "r") as sequences:
            sequence = json.load(sequences)

        cpp_sequence = sequence['cpp']
        java_sequence = sequence['java']

        with open(path2, 'w') as sequences:
            sequences.write("Results(C++)\n")
            sequences.write(str(frequency_test(cpp_sequence)) + '\n')
            sequences.write(str(runs_test(cpp_sequence)) + '\n')
            sequences.write(str(longest_run_test(cpp_sequence)) + '\n')

            sequences.write("\nResults(Java)\n")
            sequences.write(str(frequency_test(java_sequence)) + '\n')
            sequences.write(str(runs_test(java_sequence)) + '\n')
            sequences.write(str(longest_run_test(java_sequence)) + '\n')
    except FileNotFoundError as e:
        logging.error(f"File not found: {e.filename}")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
    except KeyError as e:
        logging.error(f"KeyError: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
